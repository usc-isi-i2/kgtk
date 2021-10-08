"""
Connect to a graph cache using the Kypher API.
"""

import attr
from pathlib import Path
import sqlite3
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader
import kgtk.kypher.api as kapi

@attr.s(slots=True, frozen=False)
class GraphCacheAdaptor:
    from kgtk.io.kgtkreader import KgtkReaderOptions

    graph_cache_path: Path = attr.ib(validator=attr.validators.instance_of(Path)) # for feedback
    api: kapi.KypherApi = attr.ib(validator=attr.validators.instance_of(kapi.KypherApi))
    sql_store = attr.ib() # Problems defining this type.
    table_name: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib()

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    is_open: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)


    @classmethod
    def open(cls,
             graph_cache_path: Path,
             file_path: Path,
             log_level: int = 1,
             index_mode: str = 'none',
             max_results: int = 10000,
             max_cache_size: int = 1000,
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
                print("Graph cache %s: file %s not found." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
            return None
        if verbose:
            print("Graph cache %s: file %s found." % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
                          
        if "graph" not in file_info or file_info["graph"] is None:
            api.close()
            if verbose:
                print("Graph cache %s: table name not found for file %s" % (repr(str(graph_cache_path)), repr(str(file_path))), file=error_file, flush=True)
            return None
        table_name: str = file_info["graph"]

        if verbose:
            print("The table name is %s" % repr(table_name), file=error_file, flush=True)
            
        column_names: typing.List[str] = sql_store.get_table_header(table_name)

        # api.add_input(table_name, name="table", handle=True)

        return cls(graph_cache_path=graph_cache_path,
                   api=api,
                   sql_store=sql_store,
                   table_name=table_name,
                   column_names=column_names,
                   error_file=error_file,
                   verbose=verbose,
                   very_verbose=very_verbose,
                   )

    def close(self):
        if self.is_open:
            self.api.close()
            self.is_open = False

    def reader(self,
               fetch_size: int = 0,
               filter_batch_size: int = 0,
               options: typing.Optional[KgtkReaderOptions] = None,
               ):
        """Based on the parameters passed in, select one of the Graph Cache reader
        implementations.  In the future, we might always use the Graph Cache
        filter batch reader or the slow reader; the other two are just simpler
        fallbacks.

        """
        if options is not None and \
           (options.repair_and_validate_values or \
            options.repair_and_validate_lines or \
            options.implied_label is not None):
            if self.verbose:
                print("Using the Graph Cache slow reader.", file=self.error_file, flush=True)
            return self.slow_reader(fetch_size, filter_batch_size, options)
            
        if fetch_size > 0:
            if filter_batch_size > 0:
                if self.verbose:
                    print("Using the Graph Cache filter batch reader.", file=self.error_file, flush=True)
                return self.filter_batch_reader(fetch_size, filter_batch_size)
            else:
                if self.verbose:
                    print("Using the Graph Cache fetchmany reader.", file=self.error_file, flush=True)
                return self.fetchmany_reader(fetch_size)
        else:
            if self.verbose:
                print("Using the Graph Cache simple reader.", file=self.error_file, flush=True)
            return self.simple_reader()

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
                return row

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
                        row = reader_self.buffer[reader_self.buffer_idx]
                        reader_self.buffer_idx += 1
                        return row

                    reader_self.buffer = reader_self.cursor.fetchmany(fetch_size)
                    reader_self.buffer_idx = 0

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
                                            verbose=adapter_self.verbose,
                                            very_verbose=adapter_self.very_verbose,
                                            )

                while True:
                    if reader_self.need_query:
                        if not reader_self.advance_state():
                            adapter_self.close()
                            raise StopIteration
                        reader_self.start_query()
                            
                    while True:
                        if reader_self.buffer is not None and reader_self.buffer_idx < len(reader_self.buffer):
                            row = reader_self.buffer[reader_self.buffer_idx]
                            reader_self.buffer_idx += 1
                            return row

                        reader_self.buffer = reader_self.cursor.fetchmany(fetch_size)
                        reader_self.buffer_idx = 0
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
                                            verbose=adapter_self.verbose,
                                            very_verbose=adapter_self.very_verbose,
                                            )

                while True:
                    if reader_self.need_query:
                        if not reader_self.advance_state():
                            adapter_self.close()
                            raise StopIteration
                        reader_self.start_query()
                            
                    while True:
                        if reader_self.buffer is not None and reader_self.buffer_idx < len(reader_self.buffer):
                            row = reader_self.buffer[reader_self.buffer_idx]
                            reader_self.buffer_idx += 1

                            if options.repair_and_validate_lines:
                                line: str = options.column_separator.join(row)

                                # TODO: Use a separate option to control this.
                                if adapter_self.very_verbose:
                                    print("'%s'" % line, file=self.error_file, flush=True)

                                # Ignore empty lines.
                                if options.empty_line_action != ValidationAction.PASS and all([len(e) == 0 for e in row]):
                                    if reader_self.exclude_line(self.options.empty_line_action, "saw an empty line", line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_ignored += 1
                                        continue

                                # Ignore comment lines:
                                if options.comment_line_action != ValidationAction.PASS  and len(row[0]) > 0 and row[0][0] == reader_self.COMMENT_INDICATOR:
                                    if reader_self.exclude_line(self.options.comment_line_action, "saw a comment line", line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_ignored += 1
                                        continue

                                # Ignore whitespace lines
                                if options.whitespace_line_action != ValidationAction.PASS and all([e.isspace() for e in row]):
                                    if reader_self.exclude_line(self.options.whitespace_line_action, "saw a whitespace line", line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_ignored += 1
                                        continue

                                if reader_self._ignore_if_blank_required_fields(row, line):
                                    reader_self.reject(line)
                                    reader_self.data_lines_excluded_blank_fields += 1
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
                                        continue

                                if options.prohibited_list_action != ValidationAction.PASS:
                                    if reader_self._ignore_prohibited_lists(row, line):
                                        reader_self.reject(line)
                                        reader_self.data_lines_excluded_prohibited_lists += 1
                                        continue

                            if options.implied_label is not None:
                                row.append(options.implied_label)
                                
                            return row

                        reader_self.buffer = reader_self.cursor.fetchmany(fetch_size)
                        reader_self.buffer_idx = 0
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
            print("Query: %s" % repr(query), file=adapter_self.error_file, flush=True)
            print("Parameters: [%s]" % ", ".join([repr(x) for x in parameters]), file=adapter_self.error_file, flush=True)

        return query, parameters

    def get_cursor(self, sql_store)->sqlite3.Cursor:
        return sql_store.get_conn().cursor()

    def start_query(self,
                    table_name: str,
                    column_names: typing.List[str],
                    verbose: bool = False,
                    very_verbose: bool = False,
                    ):
        query: str
        parameters: typing.List[str]
        query, parameters = self.build_query(table_name, column_names, verbose=verbose, very_verbose=very_verbose)
        self.cursor.execute(query, parameters)
        self.need_query = False

    def advance_state(self)->bool:
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

    from kgtk.exceptions import KGTKException

    parser = ArgumentParser()
    parser.add_argument("--graph-cache", dest="graph_cache", type=str,
                        help="The graph cache file.", required=True)
    parser.add_argument("--input-file", dest="input_file", type=str,
                        help="The input file to find in the graph cache.", required=True)

    args: Namespace = parser.parse_args()

    print("The graph cache is %s" % repr(args.graph_cache), flush=True)
    print("The input file is %s" % repr(args.input_file), flush=True)

    try:
        gca: GraphCacheAdaptor = GraphCacheAdaptor.open(graph_cache_path=Path(args.graph_cache),
                                                        file_path=Path(args.input_file),
                                                        )
    except KGTKException as e:
        print("KGTKException: %s" % str(e), file=sys.stderr, flush=True)
        return

    if gca is None:
        print("%s not found in %s" % (repr(args.input_file), repr(args.graph_cache)), file=sys.stderr, flush=True)
        return

    print("The columns are: [%s]" % ", ".join(gca.column_names))
    print("", flush=True)

    gca.close()

if __name__ == "__main__":
    main()
