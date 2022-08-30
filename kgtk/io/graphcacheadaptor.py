"""
Connect to a graph cache using the Kypher API.

Note: Sqlite3 may return tuples.  KTK code tends to assume that
rows are lists (for example, to use `.copy()`). We will proactively
conver the rows we're read into lists.
"""

import attr
from pathlib import Path
import sqlite3
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader
from kgtk.utils.closableiter import ClosableIter, ClosableIterTextIOWrapper
import kgtk.kypher.api as kapi

@attr.s(slots=True, frozen=False)
class GraphCacheAdaptor:
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    graph_cache_path: Path = attr.ib(validator=attr.validators.instance_of(Path)) # for feedback
    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    who: str = attr.ib(validator=attr.validators.instance_of(str))

    # TODO: Fix this validator:
    # options: KgtkReaderOptions = attr.ib(validator=attr.validators.instance_of(KgtkReaderOptions))
    options: KgtkReaderOptions = attr.ib()
    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions))


    api: kapi.KypherApi = attr.ib(validator=attr.validators.instance_of(kapi.KypherApi))
    sql_store = attr.ib() # Problems defining this type.
    table_name: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib()
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    header: str = attr.ib(validator=attr.validators.instance_of(str))
    source: ClosableIter[str] = attr.ib() # Todo: validate
    input_format: str = attr.ib(validator=attr.validators.instance_of(str))
 
    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The following fields may change during the lifetime of this object.

    # is_open is used to prevent sending duplicate close calls to the
    # KypherApi.
    is_open: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    # reader_method contains the name of the reader class.  It is set when a
    # reader is opened. This should simplify unit tests.
    reader_method: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    @classmethod
    def open(cls,
             graph_cache_path: Path,
             file_path: Path,
             who: str,
             options: KgtkReaderOptions,
             value_options: KgtkValueOptions,
             log_level: int = 1,
             index_mode: str = 'none',
             max_results: int = 10000,
             max_cache_size: int = 1000,
             ignore_stale_graph_cache: bool = True,
             error_file: typing.TextIO = sys.stderr,
             verbose: bool = False,
             very_verbose: bool = False,
             )->typing.Optional['GraphCacheAdaptor']:

        api: kapi.KypherApi = kapi.KypherApi(graphcache=str(graph_cache_path),
                                             loglevel=log_level,
                                             index=index_mode,
                                             maxresults=max_results,
                                             maxcache=max_cache_size,
                                             )

        # Open the connection to the sqlite3 database file. This will
        # throw a KGTKException if the database file does not exist
        # or cannot be opened.
        sql_store = api.get_sql_store()

        # Check to see if the specified file exists in the database.
        # The result will be None or a dictionary.
        file_info = sql_store.get_file_info(str(file_path))
        if file_info is None:
            api.close()
            if verbose:
                print("Graph cache %s: file %s not found in the cache." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
            return None
        if verbose:
            print("Graph cache %s: file %s found in the cache." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
                          
        if ignore_stale_graph_cache:
            if verbose:
                print("Graph cache %s: file %s will be checked for stale data." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
            if file_path.is_file():
                is_stale: bool = False

                cached_file_size = file_info.get("size", None)
                if cached_file_size is None:
                    is_stale = True
                    if verbose:
                        print("Graph cache %s: file %s is missing a cached file size." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)

                cached_file_modtime = file_info.get("modtime", None)
                if cached_file_modtime is None:
                    is_stale = True
                    if verbose:
                        print("Graph cache %s: file %s is missing a cached modification time." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)

                if cached_file_size is not None and cached_file_modtime is not None:
                    if cached_file_size != file_path.stat().st_size:
                        is_stale = True
                        if verbose:
                            print("Graph cache %s: file %s: cached file size is stale." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
                    if cached_file_modtime != file_path.stat().st_mtime:
                        is_stale = True
                        if verbose:
                            print("Graph cache %s: file %s: cached file modification time is stale." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
                    if is_stale:
                        api.close()
                        if verbose:
                            print("Graph cache %s: file %s: ignoring stale contents." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
                        return None
            else:
                if verbose:
                    print("Graph cache %s: file %s was not found outside the cache." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)

        if "graph" not in file_info or file_info["graph"] is None:
            api.close()
            if verbose:
                print("Graph cache %s: table name not found for file %s" % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
            return None
        table_name: str = file_info["graph"]

        if verbose:
            print("The table name is %s" % repr(table_name), file=error_file, flush=True)
            
        column_names: typing.List[str] = sql_store.get_table_header(table_name)
        header: str = KgtkFormat.COLUMN_SEPARATOR.join(column_names)
        source: ClosableIter[str] = ClosableIterTextIOWrapper(sys.stdin), # This is a dummy definition.
        column_name_map: typing.Mapping[str, int] = KgtkReader.build_column_name_map(column_names,
                                                                                     header_line=header,
                                                                                     who=who,
                                                                                     error_action=options.header_error_action,
                                                                                     error_file=error_file)

        # api.add_input(table_name, name="table", handle=True)

        return cls(graph_cache_path=graph_cache_path,
                   file_path=file_path,
                   who=who,
                   options=options,
                   value_options=value_options,
                   api=api,
                   sql_store=sql_store,
                   table_name=table_name,
                   column_names=column_names,
                   column_count=len(column_names),
                   column_name_map=column_name_map,
                   header=header,
                   source=source,
                   input_format="gca",
                   error_file=error_file,
                   verbose=verbose,
                   very_verbose=very_verbose,
                   )

    def close(self):
        if self.is_open:
            self.api.close()
            self.is_open = False

    def reader(self):
        """Based on the parameters passed in, select one of the Graph Cache
        reader implementations and return the class of the implementation.  In
        the future, we might always use the Graph Cache filter batch reader or
        the slow reader; the other two are just simpler fallbacks.

        """
        fetch_size: int = self.options.graph_cache_fetchmany_size
        filter_batch_size: int = self.options.graph_cache_filter_batch_size

        if self.options.repair_and_validate_values or \
           self.options.repair_and_validate_lines or \
           self.options.implied_label is not None:
            self.reader_method = "slow_reader"
            if self.verbose:
                print("Using the Graph Cache slow reader.", file=self.error_file, flush=True)
            return self.slow_reader(fetch_size, filter_batch_size, self.options)
            
        if fetch_size > 0:
            if filter_batch_size > 0:
                self.reader_method = "filter_batch_reader"
                if self.verbose:
                    print("Using the Graph Cache filter batch reader.", file=self.error_file, flush=True)
                return self.filter_batch_reader(fetch_size, filter_batch_size)
            else:
                self.reader_method = "fetchmany_reader"
                if self.verbose:
                    print("Using the Graph Cache fetchmany reader.", file=self.error_file, flush=True)
                return self.fetchmany_reader(fetch_size)
        else:
            self.reader_method = "simple_reader"
            if self.verbose:
                print("Using the Graph Cache simple reader.", file=self.error_file, flush=True)
            return self.simple_reader()

    def reader_instance(self):
        """For debugging, return an instantiated reader using the parameters sent to the adapter."""
        return self.reader()(file_path=self.file_path,
                             source=self.source,
                             options=self.options,
                             value_options=self.value_options,
                             column_names=self.column_names.copy(),
                             column_count=self.column_count,
                             column_name_map=self.column_name_map,
                             header=self.header,
                             input_format=self.input_format,
                             )

    def simple_reader(adapter_self):
        """This is the simple Graph Cache reader.

        If there is a filter, then all of the filter parameters are passed to
        sqlite3 in a single SELECT statement.  This may lead to poor
        performance if the filter parameters includes a very large value set.

        The results of the database query are retrieved one at a time.  This
        may lead to suboptimal performance if the result set is very large,
        and might lead to memory exhaustion.

        """
        @attr.s(slots=True, frozen=False)
        class SimpleGraphCacheReader(KgtkReader):
            
            cursor: sqlite3.Cursor = attr.ib(default=None)
            
            def build_query(reader_self)->typing.Tuple[str, typing.List[str]]:
                query_list: typing.List[str] = list()
                parameters: typing.List[str] = list()

                query_list.append("SELECT ")

                idx: int
                col_name: str
                for idx, col_name in enumerate(adapter_self.column_names):
                    if idx == 0:
                        query_list.append(" ")
                    else:
                        query_list.append(", ")
                    query_list.append('"' + col_name + '"')

                query_list.append(" FROM " )
                query_list.append(adapter_self.table_name)

                if reader_self.input_filter is not None and len(reader_self.input_filter) > 0:
                    query_list.append(" WHERE ")
                    col_idx: int
                    col_values: typing.Set[str]
                    first: bool = True
                    for col_idx, col_values in reader_self.input_filter.items():
                        if len(col_values) == 0:
                            continue;
                        if first:
                            first = False
                        else:
                            query_list.append(" AND ")
                        query_list.append('"' + adapter_self.column_names[col_idx] + '"')
                        if len(col_values) == 1:
                            query_list.append(" = ?")
                            parameters.append(list(col_values)[0])
                        else:
                            query_list.append(" IN (")
                            col_value: str
                            for idx, col_value in enumerate(sorted(list(col_values))):
                                if idx > 0:
                                    query_list.append(", ")
                                query_list.append("?")
                                parameters.append(col_value)
                            query_list.append(")")

                query: str = "".join(query_list)

                if adapter_self.very_verbose:
                    print("Query: %s" % repr(query), file=adapter_self.error_file, flush=True)
                    print("Parameters: [%s]" % ", ".join([repr(x) for x in parameters]), file=adapter_self.error_file, flush=True)
                
                return query, parameters

            def get_cursor(reader_self):
                cursor = adapter_self.sql_store.get_conn().cursor()
                query: str
                parameters: typing.List[str]
                query, parameters = reader_self.build_query()
                cursor.execute(query, parameters)
                return cursor


            def nextrow(reader_self)->typing.List[str]:
                if reader_self.cursor is None:
                    reader_self.cursor = reader_self.get_cursor()
                row = reader_self.cursor.fetchone()
                if row is None:
                    adapter_self.close()
                    raise StopIteration
                return list(row)

        return SimpleGraphCacheReader

    def fetchmany_reader(adapter_self, fetch_size: int):
        """This is the fetchmany Graph Cache reader.

        If there is a filter, then all of the filter parameters are passed to
        sqlite3 in a single SELECT statement.  This may lead to poor
        performance if the filter parameters includes a very large value set.

        The results of the database query are retrieved in batches.  The
        maximum size of a batch is specified with `--graph-cache-fetchmany-size`.

        """
        @attr.s(slots=True, frozen=False)
        class FetchManyGraphCacheReader(KgtkReader):
            
            cursor = attr.ib(default=None)
            buffer = attr.ib(default=None)
            buffer_idx: int = attr.ib(default=0)

            def build_query(reader_self)->typing.Tuple[str, typing.List[str]]:
                query_list: typing.List[str] = list()
                parameters: typing.List[str] = list()

                query_list.append("SELECT ")

                idx: int
                col_name: str
                for idx, col_name in enumerate(adapter_self.column_names):
                    if idx == 0:
                        query_list.append(" ")
                    else:
                        query_list.append(", ")
                    query_list.append('"' + col_name + '"')

                query_list.append(" FROM " )
                query_list.append(adapter_self.table_name)

                if reader_self.input_filter is not None and len(reader_self.input_filter) > 0:
                    query_list.append(" WHERE ")
                    col_idx: int
                    col_values: typing.Set[str]
                    first: bool = True
                    for col_idx, col_values in reader_self.input_filter.items():
                        if len(col_values) == 0:
                            continue;
                        if first:
                            first = False
                        else:
                            query_list.append(" AND ")
                        query_list.append('"' + adapter_self.column_names[col_idx] + '"')
                        if len(col_values) == 1:
                            query_list.append(" = ?")
                            parameters.append(list(col_values)[0])
                        else:
                            query_list.append(" IN (")
                            col_value: str
                            for idx, col_value in enumerate(sorted(list(col_values))):
                                if idx > 0:
                                    query_list.append(", ")
                                query_list.append("?")
                                parameters.append(col_value)
                            query_list.append(")")

                query: str = "".join(query_list)

                if adapter_self.very_verbose:
                    print("Query: %s" % repr(query), file=adapter_self.error_file, flush=True)
                    print("Parameters: [%s]" % ", ".join([repr(x) for x in parameters]), file=adapter_self.error_file, flush=True)
                
                return query, parameters

            def get_cursor(reader_self):
                cursor: sqlite3.Cursor = adapter_self.sql_store.get_conn().cursor()
                query: str
                parameters: typing.List[str]
                query, parameters = reader_self.build_query()
                cursor.execute(query, parameters)
                return cursor


            def nextrow(reader_self)->typing.List[str]:
                if reader_self.cursor is None:
                    reader_self.cursor = reader_self.get_cursor()

                while True:
                    if reader_self.buffer is not None and reader_self.buffer_idx < len(reader_self.buffer):
                        if adapter_self.very_verbose:
                            print("Returning buffer index %d" % reader_self.buffer_idx, file=adapter_self.error_file, flush=True)
                        row = list(reader_self.buffer[reader_self.buffer_idx])
                        reader_self.buffer_idx += 1
                        return row

                    if adapter_self.very_verbose:
                        print("Fetching a buffer of maximum size %d" % fetch_size, file=adapter_self.error_file, flush=True)
                    reader_self.buffer = reader_self.cursor.fetchmany(fetch_size)
                    reader_self.buffer_idx = 0
                    if adapter_self.very_verbose:
                        print("Fetched %d records" % len(reader_self.buffer), file=adapter_self.error_file, flush=True)

                    if len(reader_self.buffer) == 0:
                        adapter_self.close()
                        raise StopIteration

        return FetchManyGraphCacheReader
        
    def filter_batch_reader(adapter_self, fetch_size: int, filter_batch_size: int):
        """This is the filter batch Graph Cache reader.

        If there is a filter, then all of the filter parameters are passed to
        sqlite3 in multiple SELECT statements.  The database will scanned multiple
        times, but if the indexing works properly, performance should be adequate.
        The maximum number of filter values in a SELECT statement for a single column
        is specified with `--graph-cache-filter-batch-size`.

        The results of each database query are retrieved in batches.  The
        maximum size of a batch is specified with `--graph-cache-fetchmany-size`.

        """
        @attr.s(slots=True, frozen=False)
        class FilterBatchGraphCacheReader(GraphCacheReaderBase):
            def nextrow(reader_self)->typing.List[str]:
                if reader_self.first_time:
                    reader_self.first_time = False
                    reader_self.convert_input_filter()
                    reader_self.cursor = reader_self.get_cursor(adapter_self.sql_store)
                    reader_self.start_query(adapter_self.table_name,
                                            adapter_self.column_names,
                                            filter_batch_size,
                                            verbose=adapter_self.verbose,
                                            very_verbose=adapter_self.very_verbose,
                                            )

                while True:
                    if reader_self.need_query:
                        if not reader_self.advance_state(filter_batch_size):
                            adapter_self.close()
                            raise StopIteration
                        reader_self.start_query(adapter_self.table_name,
                                                adapter_self.column_names,
                                                filter_batch_size,
                                                verbose=adapter_self.verbose,
                                                very_verbose=adapter_self.very_verbose,
                                                )
                            
                    while True:
                        if reader_self.buffer is not None and reader_self.buffer_idx < len(reader_self.buffer):
                            if adapter_self.very_verbose:
                                print("Returning buffer index %d" % reader_self.buffer_idx, file=adapter_self.error_file, flush=True)
                            row = list(reader_self.buffer[reader_self.buffer_idx])
                            reader_self.buffer_idx += 1
                            return row

                        if adapter_self.very_verbose:
                            print("Fetching a buffer of maximum size %d" % fetch_size, file=adapter_self.error_file, flush=True)
                        reader_self.buffer = reader_self.cursor.fetchmany(fetch_size)
                        reader_self.buffer_idx = 0
                        if adapter_self.very_verbose:
                            print("Fetched %d records" % len(reader_self.buffer), file=adapter_self.error_file, flush=True)

                        if len(reader_self.buffer) == 0:
                            reader_self.need_query = True
                            break
                            

        return FilterBatchGraphCacheReader

    def slow_reader(adapter_self,
                    fetch_size: int,
                    filter_batch_size: int,
                    options: KgtkReaderOptions,
                    ):
        """This is the filter batch Graph Cache reader.

        If there is a filter, then all of the filter parameters are passed to
        sqlite3 in multiple SELECT statements.  The database will scanned multiple
        times, but if the indexing works properly, performance should be adequate.
        The maximum number of filter values in a SELECT statement for a single column
        is specified with `--graph-cache-filter-batch-size`.

        The results of each database query are retrieved in batches.  The
        maximum size of a batch is specified with `--graph-cache-fetchmany-size`.

        """
        @attr.s(slots=True, frozen=False)
        class SlowGraphCacheReader(GraphCacheReaderBase):
            def nextrow(reader_self)->typing.List[str]:
                from kgtk.utils.validationaction import ValidationAction
                if reader_self.first_time:
                    reader_self.first_time = False
                    reader_self.convert_input_filter()
                    reader_self.cursor = reader_self.get_cursor(adapter_self.sql_store)
                    reader_self.start_query(adapter_self.table_name,
                                            adapter_self.column_names,
                                            filter_batch_size,
                                            verbose=adapter_self.verbose,
                                            very_verbose=adapter_self.very_verbose,
                                            )

                while True:
                    if reader_self.need_query:
                        if not reader_self.advance_state(filter_batch_size):
                            adapter_self.close()
                            raise StopIteration
                        reader_self.start_query(adapter_self.table_name,
                                                adapter_self.column_names,
                                                filter_batch_size,
                                                verbose=adapter_self.verbose,
                                                very_verbose=adapter_self.very_verbose,
                                                )
                            
                    while True:
                        if reader_self.buffer is not None and reader_self.buffer_idx < len(reader_self.buffer):
                            if adapter_self.very_verbose:
                                print("Returning buffer index %d" % reader_self.buffer_idx, file=adapter_self.error_file, flush=True)
                            row = list(reader_self.buffer[reader_self.buffer_idx])
                            reader_self.buffer_idx += 1

                            if options.repair_and_validate_lines:
                                line: str = options.column_separator.join(row)

                                # TODO: Use a separate option to control this.
                                if adapter_self.very_verbose:
                                    print("row: '%s'" % line, file=adapter_self.error_file, flush=True)

                                # Ignore empty lines.
                                if options.empty_line_action != ValidationAction.PASS and all([len(e) == 0 for e in row]):
                                    if reader_self.exclude_line(self.options.empty_line_action, "saw an empty line", line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_ignored += 1
                                        if adapter_self.very_verbose:
                                            print("Ignoring empty row.", file=adapter_self.error_file, flush=True)
                                        continue

                                # Ignore comment lines:
                                if options.comment_line_action != ValidationAction.PASS  and len(row[0]) > 0 and row[0][0] == reader_self.COMMENT_INDICATOR:
                                    if reader_self.exclude_line(self.options.comment_line_action, "saw a comment line", line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_ignored += 1
                                        if adapter_self.very_verbose:
                                            print("Ignoring comment row.", file=adapter_self.error_file, flush=True)
                                        continue

                                # Ignore whitespace lines
                                if options.whitespace_line_action != ValidationAction.PASS and all([e.isspace() for e in row]):
                                    if reader_self.exclude_line(self.options.whitespace_line_action, "saw a whitespace line", line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_ignored += 1
                                        if adapter_self.very_verbose:
                                            print("Ignoring whitespace row.", file=adapter_self.error_file, flush=True)
                                        continue

                                if reader_self._ignore_if_blank_required_fields(row, line):
                                    reader_self.reject(line)
                                    reader_self.data_lines_excluded_blank_fields += 1
                                    if adapter_self.very_verbose:
                                        print("Ignoring row due to blank required fields.", file=adapter_self.error_file, flush=True)
                                    continue

                            if options.repair_and_validate_values:
                                line: str = options.column_separator.join(row)
                                if options.invalid_value_action != ValidationAction.PASS:
                                    # TODO: find a way to optionally cache the KgtkValue objects
                                    # so we don't have to create them a second time in the conversion
                                    # and iterator methods below.
                                    if reader_self._ignore_invalid_values(row, line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_excluded_invalid_values += 1
                                        if adapter_self.very_verbose:
                                            print("Ignoring row due to invalid values.", file=adapter_self.error_file, flush=True)
                                        continue

                                if options.prohibited_list_action != ValidationAction.PASS:
                                    if reader_self._ignore_prohibited_lists(row, line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_excluded_prohibited_lists += 1
                                        if adapter_self.very_verbose:
                                            print("Ignoring row due to prohibited lists.", file=adapter_self.error_file, flush=True)
                                        continue

                            if options.implied_label is not None:
                                row.append(options.implied_label)
                                
                            return row

                        if adapter_self.very_verbose:
                            print("Fetching a buffer of maximum size %d" % fetch_size, file=adapter_self.error_file, flush=True)
                        reader_self.buffer = reader_self.cursor.fetchmany(fetch_size)
                        reader_self.buffer_idx = 0
                        if adapter_self.very_verbose:
                            print("Fetched %d records" % len(reader_self.buffer), file=adapter_self.error_file, flush=True)

                        if len(reader_self.buffer) == 0:
                            reader_self.need_query = True
                            break
                            

        return SlowGraphCacheReader

@attr.s(slots=True, frozen=False)
class GraphCacheReaderBase(KgtkReader):
           
    first_time: bool = attr.ib(default=True)
    need_query: bool = attr.ib(default=True)
    cursor = attr.ib(default=None)
    buffer = attr.ib(default=None)
    buffer_idx: int = attr.ib(default=0)

    batch_state: typing.List[int] = attr.ib(default=attr.Factory(list))
    input_filter_idxs: typing.List[int] = attr.ib(default=attr.Factory(list))
    input_filter_lists: typing.List[typing.List[str]] = attr.ib(default=attr.Factory(list))

    def convert_input_filter(self):
        if self.input_filter is None:
            return
        if len(self.input_filter) == 0:
            return


        col_idx: int
        col_values: typing.Set[str]
        for col_idx, col_values in self.input_filter.items():
            if len(col_values) == 0:
                continue;
            self.batch_state.append(0)
            self.input_filter_idxs.append(col_idx)
            self.input_filter_lists.append(sorted(list(col_values)))


    def build_query(self,
                    table_name: str,
                    column_names: typing.List[str],
                    filter_batch_size: int,
                    verbose: bool = False,
                    very_verbose: bool = False,
                    )->typing.Tuple[str, typing.List[str]]:
        query_list: typing.List[str] = list()
        parameters: typing.List[str] = list()

        query_list.append("SELECT ")

        idx: int
        col_name: str
        for idx, col_name in enumerate(column_names):
            if idx == 0:
                query_list.append(" ")
            else:
                query_list.append(", ")
            query_list.append('"' + col_name + '"')

        query_list.append(" FROM " )
        query_list.append(table_name)

        if len(self.input_filter_idxs) > 0:
            query_list.append(" WHERE ")
            first_constrained_column: bool = True

            for idx in range(len(self.input_filter_lists)):
                col_state: int = self.batch_state[idx]
                col_idx: int = self.input_filter_idxs[idx]
                col_values: typing.List[str] = self.input_filter_lists[idx][col_state:(col_state+filter_batch_size)]

                if first_constrained_column:
                    first_constrained_column = False
                else:
                    query_list.append(" AND ")

                query_list.append('"' + column_names[col_idx] + '"')

                if len(col_values) == 0:
                    raise ValueError("GraphCacheAdaptor internal error: len(col_values) == 0")

                elif len(col_values) == 1:
                    query_list.append(" = ?")
                    parameters.append(list(col_values)[0])

                else:
                    query_list.append(" IN (")
                    col_value: str
                    for idx, col_value in enumerate(col_values):
                        if idx > 0:
                            query_list.append(", ")
                        query_list.append("?")
                        parameters.append(col_value)
                    query_list.append(")")

        query: str = "".join(query_list)

        if very_verbose:
            print("Query: %s" % repr(query), file=self.error_file, flush=True)
            print("Parameters: [%s]" % ", ".join([repr(x) for x in parameters]), file=self.error_file, flush=True)

        return query, parameters

    def get_cursor(self, sql_store)->sqlite3.Cursor:
        return sql_store.get_conn().cursor()

    def start_query(self,
                    table_name: str,
                    column_names: typing.List[str],
                    filter_batch_size: int,
                    verbose: bool = False,
                    very_verbose: bool = False,
                    ):
        query: str
        parameters: typing.List[str]
        query, parameters = self.build_query(table_name, column_names, filter_batch_size, verbose=verbose, very_verbose=very_verbose)
        self.cursor.execute(query, parameters)
        self.need_query = False

    def advance_state(self, filter_batch_size: int)->bool:
        idx: int
        for idx in range(len(self.batch_state)):
            self.batch_state[idx] += filter_batch_size
            if self.batch_state[idx] < len(self.input_filter_lists[idx]):
                return True
            self.batch_state[idx] = 0
        return False

def main():
    """Test the graph cache adaptor.
    """
    from argparse import ArgumentParser, Namespace
    import sys

    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.exceptions import KGTKException

    parser = ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", type=str,
                        help="The input file to find in the graph cache.", required=True)

    parser.add_argument("--index-mode", dest="index_mode", type=str,
                        help="The index mode to pass to the Kypher API.", default='none')

    parser.add_argument("--max-results", dest="max_results", type=int,
                        help="The maximum results to pass to the Kypher API.", default=10000)

    parser.add_argument("--max-cache-size", dest="max_cache_size", type=int,
                        help="The maximum cache size to pass to the Kypher API.", default=1000)

    parser.add_argument("--filter-index", dest="filter_index", type=int,
                        help="The index of the column on which to filter.")

    parser.add_argument("--filter-values", dest="filter_values", type=str, nargs='*',
                        help="The values to include in the filter.")

    parser.add_argument("--verbose", dest="verbose", type=optional_bool, metavar="optional True|False",
                        help="Print verbose progress messages.", nargs="?", const=True, default=False)

    parser.add_argument("--very-verbose", dest="very_verbose", type=optional_bool, metavar="optional True|False",
                        help="Print very verbose progress messages.", nargs="?", const=True, default=False)

    KgtkReaderOptions.add_arguments(parser)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    if reader_options.graph_cache is not None:
        print("The graph cache is %s" % repr(reader_options.graph_cache), flush=True)
    else:
        print("The graph cache must be supplied.", flush=True)
        return
              
    print("The input file is %s" % repr(args.input_file), flush=True)
    print("The index mode is %s" % repr(args.index_mode), flush=True)
    print("The maximum number of results is %d" % args.max_results, flush=True)
    print("The maximum cache size is %d" % args.max_cache_size, flush=True)
    print("The maximum fetch size is %d" % reader_options.graph_cache_fetchmany_size, flush=True)
    print("The filter batch size is %d" % reader_options.graph_cache_filter_batch_size, flush=True)
    print("Verbose = %s" % repr(args.verbose), flush=True)
    print("Very verbose = %s" % repr(args.very_verbose), flush=True)

    try:
        gca: GraphCacheAdaptor = GraphCacheAdaptor.open(graph_cache_path=Path(args.graph_cache),
                                                        file_path=Path(args.input_file),
                                                        who="gca",
                                                        options=reader_options,
                                                        value_options=value_options,
                                                        index_mode=args.index_mode,
                                                        max_results=args.max_results,
                                                        max_cache_size=args.max_cache_size,
                                                        verbose=args.verbose,
                                                        very_verbose=args.very_verbose,
                                                        )
    except KGTKException as e:
        print("KGTKException: %s" % str(e), file=sys.stderr, flush=True)
        return

    if gca is None:
        print("%s not found in %s" % (repr(args.input_file), repr(args.graph_cache)), file=sys.stderr, flush=True)
        return

    print("The columns are: [%s]" % ", ".join(gca.column_names), flush=True)

    reader = gca.reader_instance()
    if gca.reader_method is not None:
        print("Using reader method %s" % gca.reader_method, flush=True)

    if args.filter_index is not None and args.filter_values is not None and len(args.filter_values) > 0:
        print("Building an input filter. index=%d, values=%s" % (args.filter_index, repr(args.filter_values)), flush=True)
        input_filter = {
            args.filter_index: set(args.filter_values)
        }
        reader.add_input_filter(input_filter=input_filter)

    record_count: int = 0
    record: typing.List[str]
    for record in reader:
        record_count += 1
        if args.very_verbose:
            print("record %d: %s" % (record_count, repr(record)), flush=True)

    print("%d records read" % record_count, flush=True)

    gca.close()

if __name__ == "__main__":
    main()
