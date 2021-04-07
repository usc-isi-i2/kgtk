"""
Import an wikidata file into KGTK file

TODO: references

TODO: qualifiers-order

TODO: incorporate calendar into the KGTK data model.

TODO: Incorporate geographic precision into the KGTK data model.

TODO: Incorporate URLs into the KGTK data model.

TODO: Node type needs to be optional in the edge file.

See:
https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
https://www.wikidata.org/wiki/Special:ListDatatypes
https://www.wikidata.org/wiki/Help:Data_type

"""

from argparse import Namespace
import typing
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import an wikidata file into KGTK file'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    
    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True, who='input path file (may be .bz2)')

    parser.add_argument(
        '--procs',
        action="store",
        type=int,
        dest="procs",
        default=2,
        help='number of processes to run in parallel, default %(default)d')

    parser.add_argument(
        '--max-size-per-mapper-queue',
        action="store",
        type=int,
        dest="max_size_per_mapper_queue",
        default=4,
        help='max depth of server queues, default %(default)d')

    parser.add_argument(
        '--mapper-batch-size',
        action="store",
        type=int,
        dest="mapper_batch_size",
        default=5,
        help='How many statements to queue in a batch to a worker. (default=%(default)d)')

    parser.add_argument(
        "--single-mapper-queue",
        nargs='?',
        type=optional_bool,
        dest="single_mapper_queue",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use a single queue for worker tasks.  If false, each worker has its own task queue. (default=%(default)s).",
    )

    parser.add_argument(
        "--collect-results",
        nargs='?',
        type=optional_bool,
        dest="collect_results",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, collect the results before writing to disk.  If false, write results to disk, then concatenate. (default=%(default)s).",
    )

    parser.add_argument(
        "--collect-seperately",
        nargs='?',
        type=optional_bool,
        dest="collect_seperately",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, collect the node, edge, and qualifier results using seperate processes.  If false, collect the results with a single process. (default=%(default)s).",
    )

    parser.add_argument(
        '--collector-batch-size',
        action="store",
        type=int,
        dest="collector_batch_size",
        default=5,
        help='How many statements to queue in a batch to the collector. (default=%(default)d)')

    parser.add_argument(
        "--use-shm",
        nargs='?',
        type=optional_bool,
        dest="use_shm",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use ShmQueue. (default=%(default)s).")

    parser.add_argument(
        '--collector-queue-per-proc-size',
        action="store",
        type=int,
        dest="collector_queue_per_proc_size",
        default=2,
        help='collector queue depth per proc, default %(default)d')

    parser.add_argument(
        "--node", '--node-file',
        action="store",
        type=str,
        dest="node_file",
        default=None,
        help='path to output node file')

    parser.add_argument(
        "--edge", '--edge-file', '--detailed-edge-file',
        action="store",
        type=str,
        dest="detailed_edge_file",
        default=None,
        help='path to output edge file with detailed data')

    parser.add_argument(
        '--minimal-edge-file',
        action="store",
        type=str,
        dest="minimal_edge_file",
        default=None,
        help='path to output edge file with minimal data')

    parser.add_argument(
        "--qual", '--qual-file', '--detailed-qual-file',
        action="store",
        type=str,
        dest="detailed_qual_file",
        default=None,
        help='path to output qualifier file with full data')

    parser.add_argument(
        '--minimal-qual-file',
        action="store",
        type=str,
        dest="minimal_qual_file",
        default=None,
        help='path to output qualifier file with minimal data')

    # Optionally write only the ID column to the node file.
    parser.add_argument(
        '--node-file-id-only',
        nargs='?',
        type=optional_bool,
        dest="node_id_only",
        const=True,
        default=False,
        metavar="True/False",
        help='Option to write only the node ID in the node file. (default=%(default)s)')

    # The remaining files are KGTK edge files that split out
    # special properties, removing them from the edge file.
    parser.add_argument(
        '--split-alias-file',
        action="store",
        type=str,
        dest="split_alias_file",
        default=None,
        help='path to output split alias file')
    parser.add_argument(
        '--split-en-alias-file',
        action="store",
        type=str,
        dest="split_en_alias_file",
        default=None,
        help='path to output split English alias file')
    parser.add_argument(
        '--split-datatype-file',
        action="store",
        type=str,
        dest="split_datatype_file",
        default=None,
        help='path to output split datatype file')
    parser.add_argument(
        '--split-description-file',
        action="store",
        type=str,
        dest="split_description_file",
        default=None,
        help='path to output splitdescription file')
    parser.add_argument(
        '--split-en-description-file',
        action="store",
        type=str,
        dest="split_en_description_file",
        default=None,
        help='path to output split English description file')
    parser.add_argument(
        '--split-label-file',
        action="store",
        type=str,
        dest="split_label_file",
        default=None,
        help='path to output split label file')
    parser.add_argument(
        '--split-en-label-file',
        action="store",
        type=str,
        dest="split_en_label_file",
        default=None,
        help='path to output split English label file')
    parser.add_argument(
        '--split-sitelink-file',
        action="store",
        type=str,
        dest="split_sitelink_file",
        default=None,
        help='path to output split sitelink file')
    parser.add_argument(
        '--split-en-sitelink-file',
        action="store",
        type=str,
        dest="split_en_sitelink_file",
        default=None,
        help='path to output split English sitelink file')
    parser.add_argument(
        '--split-type-file', '--split-entity-type-file',
        action="store",
        type=str,
        dest="split_type_file",
        default=None,
        help='path to output split entry type file')

    parser.add_argument(
        '--split-property-edge-file',
        action="store",
        type=str,
        dest="split_property_edge_file",
        default=None,
        help='path to output split property edge file')

    parser.add_argument(
        '--split-property-qual-file',
        action="store",
        type=str,
        dest="split_property_qual_file",
        default=None,
        help='path to output split property qualifier file')

    # TODO: Create a seperate file for the sitelinks.

    parser.add_argument(
        "--limit",
        action="store",
        type=int,
        dest="limit",
        default=None,
        help='number of lines of input file to run on, default runs on all')
    parser.add_argument(
        "--lang",
        action="store",
        type=str,
        dest="lang",
        default="en",
        help='languages to extract, comma separated, default en')
    parser.add_argument(
        "--source",
        action="store",
        type=str,
        dest="source",
        default="wikidata",
        help='wikidata version number, default: wikidata')
    parser.add_argument(
        "--deprecated",
        action="store_true",
        dest="deprecated",
        help='option to include deprecated statements, not included by default')
    
    parser.add_argument(
        "--explode-values",
        nargs='?',
        type=optional_bool,
        dest="explode_values",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create columns with exploded value information. (default=%(default)s).",
    )

    parser.add_argument(
        "--use-python-cat",
        nargs='?',
        type=optional_bool,
        dest="use_python_cat",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use portable code to combine file fragments. (default=%(default)s).",
    )

    parser.add_argument(
        "--keep-temp-files",
        nargs='?',
        type=optional_bool,
        dest="keep_temp_files",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, keep temporary files (for debugging). (default=%(default)s).",
    )

    parser.add_argument(
        "--skip-processing",
        nargs='?',
        type=optional_bool,
        dest="skip_processing",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, skip processing the input file (for debugging). (default=%(default)s).",
    )

    parser.add_argument(
        "--skip-merging",
        nargs='?',
        type=optional_bool,
        dest="skip_merging",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, skip merging temporary files (for debugging). (default=%(default)s).",
    )

    parser.add_argument(
        "--interleave",
        nargs='?',
        type=optional_bool,
        dest="interleave",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, output the edges and qualifiers in a single file (the edge file). (default=%(default)s).",
    )

    parser.add_argument(
        "--entry-type-edges",
        nargs='?',
        type=optional_bool,
        dest="entry_type_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for the entry type field. (default=%(default)s).",
    )

    parser.add_argument(
       "--alias-edges",
        nargs='?',
        type=optional_bool,
        dest="alias_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for aliases. (default=%(default)s).",
    )

    
    parser.add_argument(
       "--datatype-edges",
        nargs='?',
        type=optional_bool,
        dest="datatype_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for property datatypes. (default=%(default)s).",
    )

    
    parser.add_argument(
       "--description-edges",
        nargs='?',
        type=optional_bool,
        dest="descr_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for descriptions. (default=%(default)s).",
    )

    
    parser.add_argument(
        "--label-edges",
        nargs='?',
        type=optional_bool,
        dest="label_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for labels. (default=%(default)s).",
    )

    parser.add_argument(
        "--sitelink-edges",
        nargs='?',
        type=optional_bool,
        dest="sitelink_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for sitelinks. (default=%(default)s).",
    )

    parser.add_argument(
        "--sitelink-verbose-edges",
        nargs='?',
        type=optional_bool,
        dest="sitelink_verbose_edges",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create edge records for sitelink details (lang, site, badges). (default=%(default)s).",
    )

    parser.add_argument(
        "--sitelink-verbose-qualifiers",
        nargs='?',
        type=optional_bool,
        dest="sitelink_verbose_qualifiers",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, create qualifier records for sitelink details (lang, site, badges). (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-aliases",
        nargs='?',
        type=optional_bool,
        dest="parse_aliases",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse aliases. (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-descriptions",
        nargs='?',
        type=optional_bool,
        dest="parse_descr",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse descriptions. (default=%(default)s).",
    )
    
    parser.add_argument(
        "--parse-labels",
        nargs='?',
        type=optional_bool,
        dest="parse_labels",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse labels. (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-sitelinks",
        nargs='?',
        type=optional_bool,
        dest="parse_sitelinks",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse sitelinks. (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-claims",
        nargs='?',
        type=optional_bool,
        dest="parse_claims",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse claims. (default=%(default)s).",
    )

    parser.add_argument(
        "--fail-if-missing",
        nargs='?',
        type=optional_bool,
        dest="fail_if_missing",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, fail if expected data is missing. (default=%(default)s).",
    )

    parser.add_argument(
        "--all-languages",
        nargs='?',
        type=optional_bool,
        dest="all_languages",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, override --lang and import aliases, dscriptions, and labels in all languages. (default=%(default)s).",
    )
    
    parser.add_argument(
        "--warn-if-missing",
        nargs='?',
        type=optional_bool,
        dest="warn_if_missing",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, print a warning message if expected data is missing. (default=%(default)s).",
    )

    parser.add_argument(
        '--progress-interval',
        action="store",
        type=int,
        dest="progress_interval",
        default=500000,
        help='How often to report progress. (default=%(default)d)')
    
    parser.add_argument(
        "--use-kgtkwriter",
        nargs='?',
        type=optional_bool,
        dest="use_kgtkwriter",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, use KgtkWriter instead of csv.writer. (default=%(default)s).")

    parser.add_argument(
        "--use-mgzip-for-input",
        nargs='?',
        type=optional_bool,
        dest="use_mgzip_for_input",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use the multithreaded gzip package, mgzip, for input. (default=%(default)s).")

    parser.add_argument(
        "--use-mgzip-for-output",
        nargs='?',
        type=optional_bool,
        dest="use_mgzip_for_output",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use the multithreaded gzip package, mgzip, for output. (default=%(default)s).")

    parser.add_argument(
        "--mgzip-threads-for-input",
        type=int,
        default=KgtkReaderOptions.MGZIP_THREAD_COUNT_DEFAULT,
        dest="mgzip_threads_for_input",
        help="The number of threads per mgzip input streama. (default=%(default)s).")

    parser.add_argument(
        "--mgzip-threads-for-output",
        type=int,
        default=KgtkWriter.MGZIP_THREAD_COUNT_DEFAULT,
        dest="mgzip_threads_for_output",
        help="The number of threads per mgzip output streama. (default=%(default)s).")

    parser.add_argument(
        '--value-hash-width',
        action="store",
        type=int,
        dest="value_hash_width",
        default=8,
        help='How many characters should be used in a value hash? (default=%(default)d)')

    parser.add_argument(
        '--claim-id-hash-width',
        action="store",
        type=int,
        dest="claim_id_hash_width",
        default=0,
        help='How many characters should be used to hash the claim ID? 0 means do not hash the claim ID. (default=%(default)d)')

    parser.add_argument(
        "--clean",
        nargs='?',
        type=optional_bool,
        dest="clean_input_values",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, clean the input values before writing it. (default=%(default)s).")

    parser.add_argument(
        "--clean-verbose",
        nargs='?',
        type=optional_bool,
        dest="clean_verbose",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, give verbose feedback when cleaning input values. (default=%(default)s).")

    parser.add_argument(
        '--invalid-edge-file',
        action="store",
        type=str,
        dest="invalid_edge_file",
        default=None,
        help='path to output edges with invalid input values')

    parser.add_argument(
        '--invalid-qual-file',
        action="store",
        type=str,
        dest="invalid_qual_file",
        default=None,
        help='path to output qual edges with invalid input values')

    parser.add_argument(
        "--skip-validation",
        nargs='?',
        type=optional_bool,
        dest="skip_validation",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, skip output record validation. (default=%(default)s).",
        )
    
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def custom_progress()->bool:
    return True # We want to start a custom progress monitor.

def run(input_file: KGTKFiles,
        procs: int,
        max_size_per_mapper_queue: int,
        node_file: typing.Optional[str],
        detailed_edge_file: typing.Optional[str],
        minimal_edge_file: typing.Optional[str],
        detailed_qual_file: typing.Optional[str],
        minimal_qual_file: typing.Optional[str],
        invalid_edge_file: typing.Optional[str],
        invalid_qual_file: typing.Optional[str],

        node_id_only: bool,
        split_alias_file: typing.Optional[str],
        split_en_alias_file: typing.Optional[str],
        split_datatype_file: typing.Optional[str],
        split_description_file: typing.Optional[str],
        split_en_description_file: typing.Optional[str],
        split_label_file: typing.Optional[str],
        split_en_label_file: typing.Optional[str],
        split_sitelink_file: typing.Optional[str],
        split_en_sitelink_file: typing.Optional[str],
        split_type_file: typing.Optional[str],
        split_property_edge_file: typing.Optional[str],
        split_property_qual_file: typing.Optional[str],

        limit: int,
        lang: str,
        source: str,
        deprecated: bool,
        explode_values: bool,
        use_python_cat: bool,
        keep_temp_files: bool,
        skip_processing: bool,
        skip_merging: bool,
        interleave: bool,
        entry_type_edges: bool,
        alias_edges: bool,
        datatype_edges: bool,
        descr_edges: bool,
        label_edges: bool,
        sitelink_edges: bool,
        sitelink_verbose_edges: bool,
        sitelink_verbose_qualifiers: bool,
        parse_aliases: bool,
        parse_descr: bool,
        parse_labels: bool,
        parse_sitelinks: bool,
        parse_claims: bool,
        fail_if_missing: bool,
        all_languages: bool,
        warn_if_missing: bool,
        collect_results: bool,
        collect_seperately: bool,
        collector_queue_per_proc_size: int,
        progress_interval: int,
        use_shm: bool,
        mapper_batch_size: int,
        collector_batch_size: int,
        single_mapper_queue: bool,
        use_kgtkwriter: bool,
        use_mgzip_for_input: bool,
        use_mgzip_for_output: bool,
        mgzip_threads_for_input: int,
        mgzip_threads_for_output: int,
        value_hash_width: int,
        claim_id_hash_width: int,
        clean_input_values: bool,
        clean_verbose: bool,
        skip_validation: bool,
        **kwargs # Whatever KgtkValueOptions wants.
        ):

    # import modules locally
    import bz2
    import simplejson as json
    import csv
    import hashlib
    import io
    import multiprocessing as mp
    import os
    from pathlib import Path
    import pyrallel
    import sys
    import time
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.cli_argparse import KGTKArgumentParser
    from kgtk.cli_entry import progress_startup
    from kgtk.exceptions import KGTKException
    from kgtk.utils.cats import platform_cat
    from kgtk.value.kgtkvalue import KgtkValue
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    languages=lang.split(',')

    ADDL_SITELINK_LABEL: str = "addl_wikipedia_sitelink"
    ALIAS_LABEL: str = "alias"
    DATATYPE_LABEL: str = "datatype"
    DESCRIPTION_LABEL: str = "description"
    LABEL_LABEL: str = "label"
    SITELINK_LABEL: str = "wikipedia_sitelink"
    SITELINK_BADGE_LABEL: str = "sitelink-badge"
    SITELINK_LANGUAGE_LABEL: str = "sitelink-language"
    SITELINK_SITE_LABEL: str = "sitelink-site"
    SITELINK_TITLE_LABEL: str = "sitelink-title"
    TYPE_LABEL: str = "type"

    SNAKTYPE_NOVALUE: str = "novalue"
    SNAKTYPE_SOMEVALUE: str =  "somevalue"
    SNAKTYPE_VALUE: str = "value"

    NOVALUE_VALUE: str = "novalue"
    SOMEVALUE_VALUE: str =  "somevalue"

    CLAIM_TYPE_STATEMENT: str = "statement"

    MAINSNAK_DATATYPE: str = "datatype"
    MAINSNAK_DATAVALUE: str = "datavalue"
    MAINSNAK_SNAKTYPE: str = "snaktype"

    DATATYPE_WIKIBASE_PREFIX: str = "wikibase"
    DATATYPE_QUANTITY: str = "quantity"
    DATATYPE_GLOBECOORDINATE: str = "globe-coordinate"
    DATATYPE_TIME: str = "time"
    DATATYPE_MONOLINGUALTEXT: str = "monolingualtext"

    collector_q: typing.Optional[pyrallel.ShmQueue] = None
    node_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    edge_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    qual_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    invalid_edge_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    invalid_qual_collector_q: typing.Optional[pyrallel.ShmQueue] = None

    description_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    sitelink_collector_q: typing.Optional[pyrallel.ShmQueue] = None

    class MyMapper(pyrallel.Mapper):

        def enter(self):
            print("Starting worker process {} (pid {}).".format(self._idx, os.getpid()), file=sys.stderr, flush=True)

            self.first=True
            self.cnt=0
            self.write_mode='w'

            
            self.node_f = None
            if node_file and not collect_results:
                self.node_f = open(node_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.node_wr = csv.writer(
                    self.node_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                
            self.edge_f = None
            if detailed_edge_file and not collect_results:
                self.edge_f = open(detailed_edge_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.edge_wr = csv.writer(
                    self.edge_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                
            self.qual_f = None
            if detailed_qual_file and not collect_results:
                self.qual_f = open(detailed_qual_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.qual_wr = csv.writer(
                    self.qual_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)

            self.invalid_edge_f = None
            if invalid_edge_file and not collect_results:
                self.invalid_edge_f = open(invalid_edge_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.invalid_edge_wr = csv.writer(
                    self.invalid_edge_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                
            self.invalid_qual_f = None
            if invalid_qual_file and not collect_results:
                self.invalid_qual_f = open(invalid_qual_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.invalid_qual_wr = csv.writer(
                    self.invalid_qual_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)

            if collect_results and collector_batch_size > 1:
                self.collector_batch_cnt = 0
                self.collector_nrows_batch = [ ]
                self.collector_erows_batch = [ ]
                self.collector_qrows_batch = [ ]
                self.collector_invalid_erows_batch = [ ]
                self.collector_invalid_qrows_batch = [ ]

                self.collector_description_erows_batch = [ ]
                self.collector_sitelink_erows_batch = [ ]

            self.process_row_data = \
                node_file or \
                entry_type_edges or \
                label_edges or \
                alias_edges or \
                descr_edges

        def exit(self, *args, **kwargs):
            print("Exiting worker process {} (pid {}).".format(self._idx, os.getpid()), file=sys.stderr, flush=True)
            if collect_results:
                if collector_batch_size > 1:
                    if len(self.collector_nrows_batch) > 0 or \
                       len(self.collector_erows_batch) > 0 or \
                       len(self.collector_qrows_batch) > 0 or \
                       len(self.collector_invalid_erows_batch) > 0 or \
                       len(self.collector_invalid_qrows_batch) > 0:
                        if collect_seperately:
                            if len(self.collector_nrows_batch) > 0:
                                node_collector_q.put(("rows", self.collector_nrows_batch, [], [], [], [], None))
                            if len(self.collector_erows_batch) > 0:
                                edge_collector_q.put(("rows", [], self.collector_erows_batch, [], [], [], None))
                            if len(self.collector_qrows_batch) > 0:
                                qual_collector_q.put(("rows", [], [], self.collector_qrows_batch, [], [], None))
                            if len(self.collector_invalid_erows_batch) > 0:
                                invalid_edge_collector_q.put(("rows", [], [], [], self.collector_invalid_erows_batch, [], None))
                            if len(self.collector_invalid_qrows_batch) > 0:
                                invalid_qual_collector_q.put(("rows", [], [], [], [], self.collector_invalid_qrows_batch, None))

                            if len(self.collector_description_erows_batch) > 0:
                                description_collector_q.put(("rows", [], self.collector_description_erows_batch, [], [], [], None))
                            if len(self.collector_sitelink_erows_batch) > 0:
                                sitelink_collector_q.put(("rows", [], self.collector_sitelink_erows_batch, [], [], [], None))
                        else:
                            collector_q.put(("rows",
                                             self.collector_nrows_batch,
                                             self.collector_erows_batch,
                                             self.collector_qrows_batch,
                                             self.collector_invalid_erows_batch,
                                             self.collector_invalid_qrows_batch,
                                             None))
                        
            else:
                if self.node_f is not None:
                    self.node_f.close()

                if self.edge_f is not None:
                    self.edge_f.close()

                if self.qual_f is not None:
                    self.qual_f.close()

                if self.invalid_edge_f is not None:
                    self.invalid_edge_f.close()

                if self.invalid_qual_f is not None:
                    self.invalid_qual_f.close()

        def erows_append(self, erows, edge_id, node1, label, node2,
                         rank="",
                         magnitude="",
                         unit="",
                         date="",
                         item="",
                         lower="",
                         upper="",
                         latitude="",
                         longitude="",
                         wikidatatype="",
                         claim_id="",
                         claim_type="",
                         val_type="",
                         entity_type="",
                         datahash="",
                         precision="",
                         calendar="",
                         entrylang="",
                         invalid_erows=None,
        )->bool:
            if len(claim_type) > 0 and claim_type != "statement":
                raise ValueError("Unexpected claim type %s" % claim_type)

            values_are_valid: bool = True
            if clean_input_values:
                error_buffer: io.StringIO = io.StringIO()
                kv: KgtkValue
                kv = KgtkValue(edge_id, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    edge_id = kv.value
                kv = KgtkValue(node1, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    node1 = kv.value
                kv = KgtkValue(label, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    label = kv.value
                kv = KgtkValue(node2, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    node2 = kv.value

                if not values_are_valid and invalid_erows is not None:
                    erows = invalid_erows

                if not values_are_valid and clean_verbose:
                    print("Value validation error in edge %s: %s" % ("|".join([repr(edge_id), repr(node1), repr(label), repr(node2)]),
                                                                     error_buffer.getvalue().rstrip()),
                          file=sys.stderr, flush=True)
                error_buffer.close()

            if explode_values:
                erows.append([edge_id,
                              node1,
                              label,
                              node2,
                              rank,
                              magnitude,
                              unit,
                              date,
                              item,
                              lower,
                              upper,
                              latitude,
                              longitude,
                              precision,
                              calendar,
                              entity_type,
                              wikidatatype,
                              entrylang,
                              ]
                             )
            else:
                erows.append([edge_id,
                              node1,
                              label,
                              node2,
                              rank,
                              wikidatatype,
                              claim_id,
                              # claim_type,
                              val_type,
                              entity_type,
                              datahash,
                              precision,
                              calendar,
                              entrylang,
                              ]
                             )
            return values_are_valid

        def qrows_append(self, qrows, edge_id, node1, label, node2,
                         magnitude="",
                         unit="",
                         date="",
                         item="",
                         lower="",
                         upper="",
                         latitude="",
                         longitude="",
                         wikidatatype="",
                         val_type="",
                         entity_type="",
                         datahash="",
                         precision="",
                         calendar="",
                         invalid_qrows=None,
                         erows=None,
                         invalid_erows=None,
        )->bool:

            values_are_valid: bool = True
            if clean_input_values:
                error_buffer: io.StringIO = io.StringIO()
                kv: KgtkValue
                kv = KgtkValue(edge_id, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    edge_id = kv.value
                kv = KgtkValue(node1, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    node1 = kv.value
                kv = KgtkValue(label, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    label = kv.value
                kv = KgtkValue(node2, options=value_options, error_file=error_buffer, verbose=clean_verbose)
                values_are_valid &= kv.is_valid()
                if kv.repaired:
                    node2 = kv.value

                if not values_are_valid and invalid_qrows is not None:
                    qrows = invalid_qrows

                if not values_are_valid and clean_verbose:
                    print("Value validation error in qual %s: %s" % ("|".join([repr(edge_id), repr(node1), repr(label), repr(node2)]),
                                                                     error_buffer.getvalue().rstrip()),
                          file=sys.stderr, flush=True)
                error_buffer.close()
                    
            if minimal_qual_file is not None or detailed_qual_file is not None:
                if explode_values:
                    qrows.append([edge_id,
                                  node1,
                                  label,
                                  node2,
                                  magnitude,
                                  unit,
                                  date,
                                  item,
                                  lower,
                                  upper,
                                  latitude,
                                  longitude,
                                  precision,
                                  calendar,
                                  entity_type,
                                  wikidatatype,
                    ])
                else:
                    qrows.append([edge_id,
                                  node1,
                                  label,
                                  node2,
                                  wikidatatype,
                                  val_type,
                                  entity_type,
                                  datahash,
                                  precision,
                                  calendar,
                    ])
                    
                
            if interleave:
                self.erows_append(erows,
                                  edge_id=edge_id,
                                  node1=node1,
                                  label=label,
                                  node2=node2,
                                  magnitude=magnitude,
                                  unit=unit,
                                  date=date,
                                  item=item,
                                  lower=lower,
                                  upper=upper,
                                  latitude=latitude,
                                  longitude=longitude,
                                  wikidatatype=wikidatatype,
                                  entity_type=entity_type,
                                  datahash=datahash,
                                  precision=precision,
                                  calendar=calendar,
                                  invalid_erows=invalid_erows)
            return values_are_valid
            
        # def process(self,line,node_file,edge_file,qual_file,languages,source):
        def process(self, line):
            if progress_interval > 0 and self.cnt % progress_interval == 0 and self.cnt>0:
                print("{} lines processed by processor {}".format(self.cnt,self._idx), file=sys.stderr, flush=True)
            self.cnt+=1
            # csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
            nrows=[]
            erows=[]
            qrows=[]
            invalid_erows = [] if invalid_edge_file is not None else None
            invalid_qrows = [] if invalid_qual_file is not None else None

            description_erows = []
            sitelink_erows = []

            # These maps avoid avoid ID collisions due to hash collision or
            # repeated values in the input data.  We assume that a top-level
            # property (obj["id"]) will not occur in multiple input lines.
            alias_id_collision_map: typing.MutableMapping[str, int] = dict()
            edge_id_collision_map: typing.MutableMapping[str, int] = dict()
            qual_id_collision_map: typing.MutableMapping[str, int] = dict()
            sitelink_id_collision_map: typing.MutableMapping[str, int] = dict()

            clean_line = line.strip()
            if clean_line.endswith(b","):
                clean_line = clean_line[:-1]
            if len(clean_line) > 1:
                obj = json.loads(clean_line)
                entry_type = obj["type"]
                keep: bool = False
                if entry_type == "item" or entry_type == "property":
                    keep = True
                elif warn_if_missing:
                    print("Unknown object type {}.".format(entry_type), file=sys.stderr, flush=True)

                if self.process_row_data and keep:
                    row = []
                    qnode = obj["id"]
                    row.append(qnode)

                    if parse_labels:
                        labels = obj.get("labels")
                        if labels is None:
                            if fail_if_missing:
                                raise KGTKException("Qnode %s is missing its labels" % qnode)
                            elif warn_if_missing:
                                print("Object id {} has no labels.".format(qnode), file=sys.stderr, flush=True)
                        label_list=[]
                        if labels:
                            if all_languages:
                                label_languages = labels.keys()
                            else:
                                label_languages = languages
                            for lang in label_languages:
                                lang_label = labels.get(lang, None)
                                if lang_label:
                                    # We needn't worry about duplicate label entries if this check passes.
                                    if lang_label['language'] != lang:
                                        print("*** Conflicting language key %s for the %s label for %s" % (repr(lang_label['language']), repr(lang), qnode),
                                              file=sys.stderr, flush=True)

                                    # lang_label['value']=lang_label['value'].replace('|','\\|')
                                    # label_list.append('\'' + lang_label['value'].replace("'","\\'") + '\'' + "@" + lang)
                                    value = KgtkFormat.stringify(lang_label['value'], language=lang)
                                    label_list.append(value)
                                        
                                    if label_edges:
                                        langid: str = qnode + '-' + LABEL_LABEL + '-' + lang
                                        self.erows_append(erows,
                                                          edge_id=langid,
                                                          node1=qnode,
                                                          label=LABEL_LABEL,
                                                          node2=value,
                                                          entrylang=lang,
                                                          invalid_erows=invalid_erows)


                        if not node_id_only:
                            if len(label_list)>0:
                                row.append("|".join(label_list))
                            else:
                                row.append("")

                    if not node_id_only:
                        row.append(entry_type)
                        
                    if entry_type_edges:
                        typeid: str = qnode + '-' + TYPE_LABEL + '-' + entry_type
                        self.erows_append(erows,
                                          edge_id=typeid,
                                          node1=qnode,
                                          label=TYPE_LABEL,
                                          node2=entry_type,
                                          invalid_erows=invalid_erows)

                    if parse_descr:
                        descriptions = obj.get("descriptions")
                        if descriptions is None:
                            if fail_if_missing:
                                raise KGTKException("Qnode %s is missing its descriptions" % qnode)
                            elif warn_if_missing:
                                print("Object id {} has no descriptions.".format(qnode), file=sys.stderr, flush=True)
                        descr_list=[]
                        if descriptions:
                            if all_languages:
                                desc_languages = descriptions.keys()
                            else:
                                desc_languages = languages
                            for lang in desc_languages:
                                lang_descr = descriptions.get(lang, None)
                                if lang_descr:
                                    # We needn't worry about duplicate description entries if this check passes.
                                    if lang_descr['language'] != lang:
                                        print("*** Conflicting language key %s for the %s description for %s" % (repr(lang_descr['language']), repr(lang), qnode),
                                              file=sys.stderr, flush=True)
                                    # lang_descr['value']=lang_descr['value'].replace('|','\\|')
                                    # descr_list.append('\'' + lang_descr['value'].replace("'","\\'") + '\'' + "@" + lang)
                                    value = KgtkFormat.stringify(lang_descr['value'], language=lang)
                                    descr_list.append(value)
                                    if descr_edges:
                                        descrid: str = qnode + '-' + DESCRIPTION_LABEL + '-' + lang
                                        self.erows_append(description_erows if collect_seperately else erows,
                                                          edge_id=descrid,
                                                          node1=qnode,
                                                          label=DESCRIPTION_LABEL,
                                                          node2=value,
                                                          entrylang=lang,
                                                          invalid_erows=invalid_erows)

                        if not node_id_only:
                            if len(descr_list)>0:
                                row.append("|".join(descr_list))
                            else:
                                row.append("")

                    if parse_aliases:
                        aliases = obj.get("aliases")
                        if aliases is None:
                            if fail_if_missing:
                                raise KGTKException("Qnode %s is missing its aliases" % qnode)
                            elif warn_if_missing:
                                print("Object id {} has no aliasees.".format(qnode), file=sys.stderr, flush=True)
                        alias_list = []
                        if aliases:
                            if all_languages:
                                alias_languages = aliases.keys()
                            else:
                                alias_languages = languages
                            for lang in alias_languages:
                                lang_aliases = aliases.get(lang, None)
                                if lang_aliases:
                                    for item in lang_aliases:
                                        # item['value']=item['value'].replace('|','\\|')
                                        # alias_list.append('\'' + item['value'].replace("'","\\'") + '\'' + "@" + lang)
                                        value = KgtkFormat.stringify(item['value'], language=lang)
                                        alias_list.append(value)
                                        if alias_edges:
                                            # Hash the value to save space and avoid syntactic difficulties.
                                            # Take a subset of the hash value to save space.
                                            alias_value_hash: str = hashlib.sha256(value.encode('utf-8')).hexdigest()[:value_hash_width]
                                            aliasid = qnode + '-' + ALIAS_LABEL + "-" + lang + '-' + alias_value_hash
                                            alias_seq_no: int # In case of hash collision
                                            if aliasid in alias_id_collision_map:
                                                alias_seq_no = alias_id_collision_map[aliasid]
                                                print("\n*** Alias collision #%d detected for %s (%s)" % (alias_seq_no, aliasid, value), file=sys.stderr, flush=True)
                                            else:
                                                alias_seq_no = 0
                                            alias_id_collision_map[aliasid] = alias_seq_no + 1
                                            aliasid += '-' + str(alias_seq_no)
                                            self.erows_append(erows,
                                                              edge_id=aliasid,
                                                              node1=qnode,
                                                              label=ALIAS_LABEL,
                                                              node2=value,
                                                              entrylang=lang,
                                                              invalid_erows=invalid_erows)


                        if not node_id_only:
                            if len(alias_list)>0:
                                row.append("|".join(alias_list))
                            else:
                                row.append("")

                    
                    datatype = obj.get("datatype", "")
                    if not node_id_only:
                        row.append(datatype)
                    if len(datatype) > 0 and datatype_edges:
                        datatypeid: str = qnode + '-' + "datatype"
                        # We expect the datatype to be a valid KGTK symbol, so
                        # there's no need to stringify it.
                        self.erows_append(erows,
                                          edge_id=datatypeid,
                                          node1=qnode,
                                          label=DATATYPE_LABEL,
                                          node2=datatype,
                                          invalid_erows=invalid_erows)
                    
                    #row.append(source)
                    if node_file:
                        nrows.append(row)

                if parse_claims and "claims" not in obj:
                    if fail_if_missing:
                        raise KGTKException("Qnode %s is missing its claims" % obj.get("id", "<UNKNOWN>"))
                    elif warn_if_missing:
                        print("Object id {} is missing its claims.".format(obj.get("id", "<UNKNOWN>")), file=sys.stderr, flush=True)
                    
                if parse_claims and "claims" in obj:
                    claims = obj["claims"]
                    if keep:
                        qnode = obj.get("id", "")
                        if len(qnode) == 0:
                            if fail_if_missing:
                                raise KGTKException("A claim is missing its Qnode id.")
                            elif warn_if_missing:
                                print("A claim is missing its Qnode id", file=sys.stderr, flush=True)
                            qnode = "UNKNOWN" # This will cause trouble down the line.

                        for prop, claim_property in claims.items():
                            for cp in claim_property:
                                if (deprecated or cp['rank'] != 'deprecated'):
                                    mainsnak = cp['mainsnak']
                                    snaktype = mainsnak.get(MAINSNAK_SNAKTYPE)
                                    rank=cp['rank']
                                    claim_id = cp['id']
                                    claim_type = cp['type']
                                    if claim_type != CLAIM_TYPE_STATEMENT:
                                        print("Unknown claim type %s, ignoring claim_property for (%s, %s)." % (repr(claim_type), repr(qnode), repr(prop)),
                                              file=sys.stderr, flush=True)
                                        continue

                                    if snaktype is None:
                                        print("Mainsnak without snaktype, ignoring claim_property for (%s, %s)." % (repr(qnode), repr(prop)),
                                              file=sys.stderr, flush=True)
                                        continue
                                    if snaktype == SNAKTYPE_VALUE:
                                        datavalue = mainsnak[MAINSNAK_DATAVALUE]
                                        val = datavalue.get('value')
                                        val_type = datavalue.get("type", "")
                                        if val is not None:
                                            if val_type in ("string", "wikibase-unmapped-entityid"):
                                                if not isinstance(val, str):
                                                    print("Value type is %s but the value is not a string, ignoring claim_property for (%s, %s)." % (repr(val_type), repr(qnode), repr(prop)),
                                                          file=sys.stderr, flush=True)
                                                    continue
                                            elif not isinstance(val, dict):
                                                print("Value type %s is not a known string type and value is not a dict, ignoring claim_property for (%s, %s)." % (repr(val_type), repr(qnode), repr(prop)),
                                                      file=sys.stderr, flush=True)
                                                continue

                                    elif snaktype == SNAKTYPE_SOMEVALUE:
                                        val = None
                                        val_type = SOMEVALUE_VALUE

                                    elif snaktype == SNAKTYPE_NOVALUE:
                                        val = None
                                        val_type = NOVALUE_VALUE

                                    else:
                                        print("Unknown snaktype %s, ignoring claim_property for (%s, %s)." % (repr(snaktype), repr(qnode), repr(prop)),
                                                                                                        file=sys.stderr, flush=True)
                                        continue
                                    
                                    typ = mainsnak.get(MAINSNAK_DATATYPE)
                                    if typ is None:
                                        print("Mainsnak without datatype, ignoring claim_property for (%s, %s)" % (repr(qnode), repr(prop)),
                                              file=sys.stderr, flush=True)
                                        continue
                                    # if typ != val_type:
                                    #     print("typ %s != val_type %s" % (typ, val_type), file=sys.stderr, flush=True)

                                    value = ''
                                    mag = ''
                                    unit = ''
                                    date=''
                                    item=''
                                    lower = ''
                                    upper = ''
                                    precision = ''
                                    calendar = ''
                                    lat = ''
                                    long = ''
                                    enttype = ''

                                    if val is None:
                                        value = val_type
                                    elif typ.startswith(DATATYPE_WIKIBASE_PREFIX):
                                        if isinstance(val, dict):
                                            enttype = val.get('entity-type')
                                            value = val.get('id', '')
                                        else:
                                            value = val
                                            # TODO: Can we find something less ad-hoc to do here?
                                            if typ == "wikibase-lexeme":
                                                enttype = "lexeme"
                                            else:
                                                enttype = "unknown"

                                        # Older Wikidata dumps do not have an 'id' here.
                                        if len(value) == 0:
                                            if isinstance(val, dict) and 'numeric-id' in val:
                                                numeric_id = str(val['numeric-id'])
                                            else:
                                                raise ValueError("No numeric ID for datatype %s, entity type %s, in (%s, %s)." % (repr(typ), repr(enttype), repr(qnode), repr(prop))) 

                                            if enttype == "item":
                                                value = 'Q' + numeric_id
                                            elif enttype == "property":
                                                value = 'P' + numeric_id
                                            elif enttype == "lexeme":
                                                value = 'L' + numeric_id
                                            else:
                                                raise ValueError('Unknown entity type %s for datatype %s in (%s, %s).' % (repr(enttype), repr(typ), repr(qnode), repr(prop)))
                                        item=value

                                    elif typ == DATATYPE_QUANTITY:
                                        # Strip whitespace from the numeric fields.  Some older Wikidata dumps
                                        # (20150805-20160502) sometimes have trailing newlines in these fields.
                                        # Convert actual numbers to strings before attempting to strip leading
                                        # and trailing whitespace.
                                        value = str(val['amount']).strip()
                                        mag = value
                                        if val.get(
                                                'upperBound',
                                                None) or val.get(
                                                'lowerBound',
                                                None):
                                            lower = str(val.get('lowerBound', '')).strip()
                                            upper = str(val.get('upperBound', '')).strip()
                                            value += '[' + lower + \
                                                ',' + upper + ']'
                                        # TODO: Don't lose the single-character unit code.  At a minimum, verify that it is the value "1".
                                        if len(val.get('unit')) > 1:
                                            unit = val.get(
                                                'unit').split('/')[-1]
                                            if unit not in ["undefined"]:
                                                # TODO: don't lose track of "undefined" units.
                                                value += unit

                                    elif typ == DATATYPE_GLOBECOORDINATE:
                                        # Strip potential leading and trailing whitespace.
                                        lat = str(val['latitude']).strip()
                                        long = str(val['longitude']).strip()
                                        precision = str(val.get('precision', ''))
                                        value = '@' + lat + '/' + long
                                        # TODO: what about "globe"?

                                    elif typ == DATATYPE_TIME:
                                        if val['time'][0]=='-':
                                            pre="^-"
                                        else:
                                            pre="^"
                                        # TODO: Maybe strip leading and traiming whitespace here?
                                        date = pre + val['time'][1:]
                                        # Cautiously strip leading and trailing whitespace from precision?
                                        precision = str(val['precision']).strip()
                                        calendar = val.get('calendarmodel', '').split('/')[-1]
                                        value = date + '/' + precision

                                    elif typ == DATATYPE_MONOLINGUALTEXT:
                                        # value = '\'' + \
                                        # val['text'].replace("'","\\'").replace("|", "\\|") + '\'' + '@' + val['language']
                                        value = KgtkFormat.stringify(val['text'], language=val['language'])

                                    else:
                                        # value = '\"' + val.replace('"','\\"').replace("|", "\\|") + '\"'
                                        value = KgtkFormat.stringify(val)

                                    if minimal_edge_file is not None or detailed_edge_file is not None:
                                        prop_value_hash: str
                                        if value.startswith(('P', 'Q')):
                                            prop_value_hash = value
                                        else:
                                            prop_value_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()[:value_hash_width]
                                        edgeid: str = qnode + '-' + prop + '-' + prop_value_hash + '-'
                                        if claim_id_hash_width == 0:
                                            edgeid += claim_id.lower()
                                        else:
                                            edgeid += hashlib.sha256(claim_id.lower().encode('utf-8')).hexdigest()[:claim_id_hash_width]
                                        prop_seq_no: int # In case of hash collision
                                        if edgeid in edge_id_collision_map:
                                            prop_seq_no = edge_id_collision_map[edgeid]
                                            print("\n*** Edge collision #%d detected for %s (%s)" % (prop_seq_no, edgeid, value), file=sys.stderr, flush=True)
                                        else:
                                            prop_seq_no = 0
                                        edge_id_collision_map[edgeid] = prop_seq_no + 1
                                        edgeid += '-' + str(prop_seq_no)
                                        self.erows_append(erows,
                                                          edge_id=edgeid,
                                                          node1=qnode,
                                                          label=prop,
                                                          node2=value,
                                                          rank=rank,
                                                          magnitude=mag,
                                                          unit=unit,
                                                          date=date,
                                                          item=item,
                                                          lower=lower,
                                                          upper=upper,
                                                          latitude=lat,
                                                          longitude=long,
                                                          wikidatatype=typ,
                                                          claim_id=claim_id,
                                                          claim_type=claim_type,
                                                          val_type=val_type,
                                                          entity_type=enttype,
                                                          precision=precision,
                                                          calendar=calendar,
                                                          invalid_erows=invalid_erows)


                                    if minimal_qual_file is not None or detailed_qual_file is not None or interleave:
                                        if cp.get('qualifiers', None):
                                            quals = cp['qualifiers']
                                            for qual_prop, qual_claim_property in quals.items():
                                                for qcp in qual_claim_property:
                                                    snaktype = qcp[MAINSNAK_SNAKTYPE]

                                                    if snaktype == SNAKTYPE_VALUE:
                                                        datavalue = qcp[MAINSNAK_DATAVALUE]
                                                        val = datavalue.get('value')
                                                        val_type = datavalue.get("type", "")

                                                    elif snaktype == SNAKTYPE_SOMEVALUE:
                                                        val = None
                                                        val_type = SOMEVALUE_VALUE

                                                    elif snaktype == SNAKTYPE_NOVALUE:
                                                        val = None
                                                        val_type = NOVALUE_VALUE

                                                    else:
                                                        raise ValueError("Unknown qualifier snaktype %s" % repr(snaktype))

                                                    if True:
                                                        value = ''
                                                        mag = ''
                                                        unit = ''
                                                        date= ''
                                                        item=''
                                                        lower = ''
                                                        upper = ''
                                                        precision = ''
                                                        calendar = ''
                                                        lat = ''
                                                        long = ''
                                                        enttype = ''
                                                        datahash = '"' + qcp['hash'] + '"'
                                                        typ = qcp.get(MAINSNAK_DATATYPE)
                                                        if typ is None:
                                                            if fail_if_missing:
                                                                raise KGTKException("Found qualifier %s without a datatype for (%s, %s)" % (repr(qual_prop), repr(qnode), repr(prop)))
                                                            elif warn_if_missing:
                                                                if val_type == SOMEVALUE_VALUE:
                                                                    print("Somevalue qualifier %s without a datatype for (%s, %s)" % (repr(qual_prop), repr(qnode), repr(prop)), file=sys.stderr, flush=True)
                                                                elif val_type == NOVALUE_VALUE:
                                                                    print("Novalue qualifier %s without a datatype for (%s, %s)" % (repr(qual_prop), repr(qnode), repr(prop)), file=sys.stderr, flush=True)
                                                                else:
                                                                    print("Found qualifier %s without a datatype for (%s, %s)" % (repr(qual_prop), repr(qnode), repr(prop)), file=sys.stderr, flush=True)
                                                            continue

                                                        if val is None:
                                                            value = val_type

                                                        elif typ.startswith(DATATYPE_WIKIBASE_PREFIX):
                                                            if isinstance(val, dict):
                                                                enttype = val.get('entity-type')
                                                                value = val.get('id', '')
                                                            else:
                                                                value = val
                                                                if typ == "wikibase-lexeme":
                                                                    enttype = "lexeme"
                                                                else:
                                                                    enttype = "unknown"

                                                            # Older Wikidata dumps do not have an 'id' here.
                                                            if len(value) == 0:
                                                                if isinstance(val, dict) and 'numeric-id' in val:
                                                                    numeric_id = str(val['numeric-id'])
                                                                else:
                                                                    raise ValueError("No numeric ID for datatype %s, entity type %s, in (%s, %s)." % (repr(typ), repr(enttype), repr(qnode), repr(prop)))
                                                                
                                                                if enttype == "item":
                                                                    value = 'Q' + numeric_id
                                                                elif enttype == "property":
                                                                    value = 'P' + numeric_id
                                                                elif enttype == "lexeme":
                                                                    value = 'L' + numeric_id
                                                                else:
                                                                    raise ValueError('Unknown entity type %s for datatype %s in (%s, %s).' % (repr(enttype), repr(typ), repr(qnode), repr(prop)))

                                                            item=value

                                                        elif typ == DATATYPE_QUANTITY:
                                                            value = val['amount']
                                                            mag = val['amount']
                                                            if val.get(
                                                                    'upperBound',
                                                                    None) or val.get(
                                                                    'lowerBound',
                                                                    None):
                                                                lower = val.get(
                                                                    'lowerBound', '')
                                                                upper = val.get(
                                                                    'upperBound', '')
                                                                value += '[' + lower + \
                                                                    ',' + upper + ']'
                                                            if len(
                                                                    val.get('unit')) > 1:
                                                                unit = val.get(
                                                                    'unit').split('/')[-1]
                                                                value += unit

                                                        elif typ == DATATYPE_GLOBECOORDINATE:
                                                            lat = str(
                                                                val['latitude'])
                                                            long = str(
                                                                val['longitude'])
                                                            precision = str(val.get(
                                                                'precision', ''))
                                                            value = '@' + lat + '/' + long

                                                        elif typ == DATATYPE_TIME:
                                                            if val['time'][0]=='-':
                                                                pre="^-"
                                                            else:
                                                                pre="^"
                                                            date = pre + \
                                                                val['time'][1:]
                                                            precision = str(
                                                                val['precision'])
                                                            calendar = val.get(
                                                                'calendarmodel', '').split('/')[-1]
                                                            value = pre + \
                                                                val['time'][1:] + '/' + str(val['precision'])

                                                        elif typ == DATATYPE_MONOLINGUALTEXT:
                                                            # value = '\'' + \
                                                            #     val['text'].replace("'","\\'") + '\'' + '@' + val['language']
                                                            value = KgtkFormat.stringify(val['text'], language=val['language'])
                                                        else:
                                                            # value = '\"' + val.replace('"','\\"') + '\"'
                                                            value = KgtkFormat.stringify(val)

                                                        qual_value_hash: str
                                                        if value.startswith(('P', 'Q')):
                                                            qual_value_hash = value
                                                        else:
                                                            qual_value_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()[:value_hash_width]
                                                        qualid: str  = edgeid + '-' + qual_prop + '-' + qual_value_hash
                                                        qual_seq_no: int # In case of hash collision
                                                        if qualid in qual_id_collision_map:
                                                            qual_seq_no = qual_id_collision_map[qualid]
                                                            print("\n*** Qualifier collision #%d detected for %s (%s)" % (qual_seq_no, qualid, value), file=sys.stderr, flush=True)
                                                        else:
                                                            qual_seq_no = 0
                                                        qual_id_collision_map[qualid] = qual_seq_no + 1
                                                        qualid += '-' + str(qual_seq_no)
                                                        self.qrows_append(qrows=qrows,
                                                                          edge_id=qualid,
                                                                          node1=edgeid,
                                                                          label=qual_prop,
                                                                          node2=value,
                                                                          magnitude=mag,
                                                                          unit=unit,
                                                                          date=date,
                                                                          item=item,
                                                                          lower=lower,
                                                                          upper=upper,
                                                                          latitude=lat,
                                                                          longitude=long,
                                                                          wikidatatype=typ,
                                                                          entity_type=enttype,
                                                                          datahash=datahash,
                                                                          precision=precision,
                                                                          calendar=calendar,
                                                                          invalid_qrows=invalid_qrows,
                                                                          erows=erows,
                                                                          invalid_erows=invalid_erows)
                                                        
                        if parse_sitelinks:
                            sitelinks=obj.get('sitelinks',None)
                        else:
                            sitelinks = None
                        if sitelinks:
                            for link in sitelinks:
                                # TODO: If the title might contain vertical bar, more work is needed
                                # to make the sitetitle safe for KGTK.
                                if link.endswith('wiki') and link not in ('commonswiki', 'simplewiki'):
                                    linklabel = SITELINK_LABEL
                                    sitetitle='_'.join(sitelinks[link]['title'].split())

                                    # The following leads to ambuiguity if there are both
                                    # "afwiki" and "afwikibooks".
                                    #
                                    # TODO: Need to research the sitelink structure more fully.
                                    sitelang=link.split('wiki')[0].replace('_','-')

                                    sitelink='http://'+sitelang+'.wikipedia.org/wiki/'+sitetitle
                                else:
                                    linklabel = ADDL_SITELINK_LABEL
                                    sitetitle='_'.join(sitelinks[link]['title'].split())
                                    if "wiki" in link:
                                        # TODO: needs more work here.
                                        sitelang=link.split("wiki")[0]
                                        if sitelang in ("commons", "simple"):
                                            sitelang = "en" # TODO: Need to retain the distinction we lose here.
                                    else:
                                        sitelang=""
                                    sitehost=link+'.org' # TODO: Needs more work here
                                    sitelink = 'http://'+sitehost+'/wiki/'+sitetitle

                                if sitelink is not None:
                                    serows = sitelink_erows if collect_seperately else erows
                                    sitelink_value_hash: str = hashlib.sha256(sitelink.encode('utf-8')).hexdigest()[:value_hash_width]
                                    sitelinkid: str = qnode + '-' + linklabel + '-' + sitelink_value_hash
                                    sitelink_seq_no: int = 0
                                    if sitelinkid in sitelink_id_collision_map:
                                        sitelink_seq_no = sitelink_id_collision_map[sitelinkid]
                                        print("\n*** Sitelink collision #%d detected for %s (%s)" % (sitelink_seq_no, sitelinkid, sitelink), file=sys.stderr, flush=True)
                                    else:
                                        sitelink_seq_no = 0
                                    sitelink_id_collision_map[sitelinkid] = sitelink_seq_no + 1
                                    sitelinkid += '-' + str(sitelink_seq_no)

                                    if sitelink_edges:
                                        self.erows_append(serows,
                                                          edge_id=sitelinkid,
                                                          node1=qnode,
                                                          label=linklabel,
                                                          node2=sitelink,
                                                          entrylang=sitelang,
                                                          invalid_erows=invalid_erows)

                                    if sitelink_verbose_edges:
                                        if len(sitelang) > 0:
                                            self.erows_append(serows,
                                                              edge_id=sitelinkid + '-language-0',
                                                              node1=sitelinkid,
                                                              label=SITELINK_LANGUAGE_LABEL,
                                                              node2=sitelang,
                                                              entrylang=sitelang,
                                                              invalid_erows=invalid_erows)
                                            
                                        self.erows_append(serows,
                                                          edge_id=sitelinkid + '-site-0',
                                                          node1=sitelinkid,
                                                          label=SITELINK_SITE_LABEL,
                                                          node2=link,
                                                          entrylang=sitelang,
                                                          invalid_erows=invalid_erows)

                                        self.erows_append(serows,
                                                          edge_id=sitelinkid + '-title-0',
                                                          node1=sitelinkid,
                                                          label=SITELINK_TITLE_LABEL,
                                                          node2=KgtkFormat.stringify(sitelinks[link]['title']),
                                                          entrylang=sitelang, invalid_erows=invalid_erows)

                                        for badge in sitelinks[link]['badges']:
                                            badgeid = sitelinkid + '-badge-' + badge
                                            self.erows_append(serows,
                                                              edge_id=badgeid,
                                                              node1=sitelinkid,
                                                              label=SITELINK_BADGE_LABEL,
                                                              node2=badge,
                                                              entrylang=sitelang,
                                                              invalid_erows=invalid_erows)

                                    if sitelink_verbose_qualifiers:
                                        if len(sitelang) > 0:
                                            self.qrows_append(qrows,
                                                              edge_id=sitelinkid + '-language-0',
                                                              node1=sitelinkid,
                                                              label=SITELINK_LANGUAGE_LABEL,
                                                              node2=sitelang,
                                                              invalid_qrows=invalid_qrows,
                                                              erows=erows,
                                                              invalid_erows=invalid_erows)
                                            
                                        self.qrows_append(qrows,
                                                          edge_id=sitelinkid + '-site-0',
                                                          node1=sitelinkid,
                                                          label=SITELINK_SITE_LABEL,
                                                          node2=link,
                                                          invalid_qrows=invalid_qrows,
                                                          erows=erows,
                                                          invalid_erows=invalid_erows)

                                        self.qrows_append(qrows,
                                                          edge_id=sitelinkid + '-title-0',
                                                          node1=sitelinkid,
                                                          label=SITELINK_TITLE_LABEL,
                                                          node2=KgtkFormat.stringify(sitelinks[link]['title']),
                                                          invalid_qrows=invalid_qrows,
                                                          erows=erows,
                                                          invalid_erows=invalid_erows)

                                        for badge in sitelinks[link]['badges']:
                                            badgeid = sitelinkid + '-badge-' + badge
                                            self.qrows_append(qrows,
                                                              edge_id=badgeid,
                                                              node1=sielinkid,
                                                              label=SITELINK_BADGE_LABEL,
                                                              node2=badge,
                                                              invalid_qrows=invalid_qrows,
                                                              erows=erows,
                                                              invalid_erows=invalid_erows)

            if len(nrows) > 0 or \
               len(erows) > 0 or \
               len(qrows) > 0 or \
               len(invalid_erows) > 0 or \
               len(invalid_qrows) > 0 or \
               len(description_erows) > 0 or \
               len(sitelink_erows) > 0:
                if collect_results:
                    if collector_batch_size == 1:
                        if collect_seperately:
                            if len(nrows) > 0 and node_collector_q is not None:
                                node_collector_q.put(("rows", nrows, [], [], [], [], None))

                            if len(erows) > 0 and edge_collector_q is not None:
                                edge_collector_q.put(("rows", [], erows, [], [], [], None))

                            if len(qrows) > 0 and qual_collector_q is not None:
                                qual_collector_q.put(("rows", [], [], qrows, [], [], None))

                            if invalid_erows is not None and len(invalid_erows) > 0 and invalid_edge_collector_q is not None:
                                invalid_edge_collector_q.put(("rows", [], [], [], invalid_erows, [], None))

                            if invalid_qrows is not None and len(invalid_qrows) > 0 and invalid_qual_collector_q is not None:
                                invalid_qual_collector_q.put(("rows", [], [], [], [], invalid_qrows, None))

                            if len(description_erows) > 0 and description_collector_q is not None:
                                description_collector_q.put(("rows", [], description_erows, [], [], [], None))

                            if len(sitelink_erows) > 0 and sitelink_collector_q is not None:
                                sitelink_collector_q.put(("rows", [], sitelink_erows, [], [], [], None))
                        elif collector_q is not None:
                            collector_q.put(("rows", nrows, erows, qrows, invalid_erows, invalid_qrows, None))
                    else:
                        self.collector_nrows_batch.extend(nrows)
                        self.collector_erows_batch.extend(erows)
                        self.collector_qrows_batch.extend(qrows)
                        if invalid_erows is not None:
                            self.collector_invalid_erows_batch.extend(invalid_erows)
                        if invalid_qrows is not None:
                            self.collector_invalid_qrows_batch.extend(invalid_qrows)

                        if collect_seperately:
                            self.collector_description_erows_batch.extend(description_erows)
                            self.collector_sitelink_erows_batch.extend(sitelink_erows)
                            
                        self.collector_batch_cnt += 1
                        
                        if self.collector_batch_cnt >= collector_batch_size:
                            if collect_seperately:
                                if len(self.collector_nrows_batch) > 0 and node_collector_q is not None:
                                    node_collector_q.put(("rows", self.collector_nrows_batch, [], [], [], [], None))

                                if len(self.collector_erows_batch) > 0 and edge_collector_q is not None:
                                    edge_collector_q.put(("rows", [], self.collector_erows_batch, [], [], [], None))

                                if len(self.collector_qrows_batch) > 0 and qual_collector_q is not None:
                                    qual_collector_q.put(("rows", [], [], self.collector_qrows_batch, [], [], None))

                                if len(self.collector_invalid_erows_batch) > 0 and invalid_edge_collector_q is not None:
                                    invalid_edge_collector_q.put(("rows", [], [], [], self.collector_invalid_erows_batch, [], None))

                                if len(self.collector_invalid_qrows_batch) > 0 and invalid_qual_collector_q is not None:
                                    invalid_qual_collector_q.put(("rows", [], [], [], [], self.collector_invalid_qrows_batch, None))

                                if len(self.collector_description_erows_batch) > 0 and description_collector_q is not None:
                                    description_collector_q.put(("rows", [], self.collector_description_erows_batch, [], [], [], None))
                                    self.collector_description_erows_batch.clear()

                                if len(self.collector_sitelink_erows_batch) > 0 and sitelink_collector_q is not None:
                                    sitelink_collector_q.put(("rows", [], self.collector_sitelink_erows_batch, [], [], [], None))
                                    self.collector_sitelink_erows_batch.clear()
                                
                            elif collector_q is not None:
                                collector_q.put(("rows",
                                                 self.collector_nrows_batch,
                                                 self.collector_erows_batch,
                                                 self.collector_qrows_batch,
                                                 self.collector_invalid_erows_batch,
                                                 self.collector_invalid_qrows_batch,
                                                 None))

                            self.collector_nrows_batch.clear()
                            self.collector_erows_batch.clear()
                            self.collector_qrows_batch.clear()
                            self.collector_invalid_erows_batch.clear()
                            self.collector_invalid_qrows_batch.clear()
                            self.collector_batch_cnt = 0

                else:
                    if node_file:
                        for row in nrows:
                            self.node_wr.writerow(row)

                    if detailed_edge_file:
                        for row in erows:
                            if skip_validation or validate(row, "detailed edge uncollected"):
                                self.edge_wr.writerow(row)

                    if detailed_qual_file:
                        for row in qrows:
                            if skip_validation or validate(row, "detailed qual uncollected"):
                                self.qual_wr.writerow(row)
    
                    if invalid_edge_file:
                        for row in invalid_erows:
                            self.invalid_edge_wr.writerow(row)

                    if invalid_qual_file:
                        for row in invalid_qrows:
                            self.invalid_qual_wr.writerow(row)
    
    class MyCollector:

        def __init__(self):
            # Prepare to use the collector.
            self.node_f: typing.Optional[typing.TextIO] = None
            self.node_wr = None
            self.nrows: int = 0

            self.minimal_edge_f: typing.Optional[typing.TextIO] = None
            self.minimal_edge_wr = None

            self.detailed_edge_f: typing.Optional[typing.TextIO] = None
            self.detailed_edge_wr = None
            self.erows: int = 0

            self.minimal_qual_f: typing.Optional[typing.TextIO] = None
            self.minimal_qual_wr = None

            self.detailed_qual_f: typing.Optional[typing.TextIO] = None
            self.detailed_qual_wr = None
            self.qrows: int = 0

            self.invalid_edge_f: typing.Optional[typing.TextIO] = None
            self.invalid_edge_wr = None
            self.invalid_erows: int = 0

            self.invalid_qual_f: typing.Optional[typing.TextIO] = None
            self.invalid_qual_wr = None
            self.invalid_qrows: int = 0

            self.split_alias_f: typing.Optional[typing.TextIO] = None
            self.split_alias_wr = None
            self.n_alias_rows: int = 0

            self.split_en_alias_f: typing.Optional[typing.TextIO] = None
            self.split_en_alias_wr = None
            self.n_en_alias_rows: int = 0

            self.split_datatype_f: typing.Optional[typing.TextIO] = None
            self.split_datatype_wr = None
            self.n_datatype_rows: int = 0

            self.split_description_f: typing.Optional[typing.TextIO] = None
            self.split_description_wr = None
            self.n_description_rows: int = 0

            self.split_en_description_f: typing.Optional[typing.TextIO] = None
            self.split_en_description_wr = None
            self.n_en_description_rows: int = 0

            self.split_label_f: typing.Optional[typing.TextIO] = None
            self.split_label_wr = None
            self.n_label_rows: int = 0

            self.split_en_label_f: typing.Optional[typing.TextIO] = None
            self.split_en_label_wr = None
            self.n_en_label_rows: int = 0

            self.split_sitelink_f: typing.Optional[typing.TextIO] = None
            self.split_sitelink_wr = None
            self.n_sitelink_rows: int = 0

            self.split_en_sitelink_f: typing.Optional[typing.TextIO] = None
            self.split_en_sitelink_wr = None
            self.n_en_sitelink_rows: int = 0

            self.split_type_f: typing.Optional[typing.TextIO] = None
            self.split_type_wr = None
            self.n_type_rows: int = 0

            self.split_property_edge_f: typing.Optional[typing.TextIO] = None
            self.split_property_edge_wr = None
            self.n_property_edge_rows: int = 0

            self.split_property_qual_f: typing.Optional[typing.TextIO] = None
            self.split_property_qual_wr = None
            self.n_property_qual_rows: int = 0

            self.process_split_files: bool = False
            self.setup_split_dispatcher()

            self.cnt: int = 0

            self.started: bool = False

        def run(self,
                collector_q,
                who: str):
            print("The %s collector is starting (pid %d)." % (who, os.getpid()), file=sys.stderr, flush=True)
                
            while True:
                action, nrows, erows, qrows, invalid_erows, invalid_qrows, header = collector_q.get()
                # print("Collector action %s." % action, file=sys.stderr, flush=True)

                if action == "rows":
                    self.collect(nrows, erows, qrows, invalid_erows, invalid_qrows, who)

                elif action == "node_header":
                    self.open_node_file(header, who)

                elif action == "minimal_edge_header":
                    self.open_minimal_edge_file(header, who)
                    self.process_split_files = True

                elif action == "detailed_edge_header":
                    self.open_detailed_edge_file(header, who)

                elif action == "minimal_qual_header":
                    self.open_minimal_qual_file(header, who)

                elif action == "detailed_qual_header":
                    self.open_detailed_qual_file(header, who)

                elif action == "invalid_edge_header":
                    self.open_invalid_edge_file(header, who)

                elif action == "invalid_qual_header":
                    self.open_invalid_qual_file(header, who)

                elif action == "split_alias_header":
                    self.open_split_alias_file(header, who)
                    self.process_split_files = True

                elif action == "split_en_alias_header":
                    self.open_split_en_alias_file(header, who)
                    self.process_split_files = True

                elif action == "split_datatype_header":
                    self.open_split_datatype_file(header, who)
                    self.process_split_files = True

                elif action == "split_description_header":
                    self.open_split_description_file(header, who)
                    self.process_split_files = True

                elif action == "split_en_description_header":
                    self.open_split_en_description_file(header, who)
                    self.process_split_files = True

                elif action == "split_label_header":
                    self.open_split_label_file(header, who)
                    self.process_split_files = True

                elif action == "split_en_label_header":
                    self.open_split_en_label_file(header, who)
                    self.process_split_files = True

                elif action == "split_sitelink_header":
                    self.open_split_sitelink_file(header, who)
                    self.process_split_files = True

                elif action == "split_en_sitelink_header":
                    self.open_split_en_sitelink_file(header, who)
                    self.process_split_files = True

                elif action == "split_type_header":
                    self.open_split_type_file(header, who)
                    self.process_split_files = True

                elif action == "split_property_edge_header":
                    self.open_split_property_edge_file(header, who)
                    self.process_split_files = True

                elif action == "split_property_qual_header":
                    self.open_split_property_qual_file(header, who)

                elif action == "shutdown":
                    self.shutdown(who)
                    break

        def _open_file(self, the_file: typing.Optional[str], header: typing.List[str], file_type: str, who: str):
            if the_file is None or len(the_file) == 0:
                raise ValueError("%s header without a %s file in the %s collector." % (file_type, file_type, who))

            f: typing.Optional[typing.TextIO]
            wr: typing.Any
            if use_kgtkwriter:
                from kgtk.io.kgtkwriter import KgtkWriter
                print("Opening the %s file in the %s collector with KgtkWriter: %s" % (file_type, who, the_file), file=sys.stderr, flush=True)
                wr = KgtkWriter.open(header, Path(the_file), who=who + " collector", use_mgzip=use_mgzip_for_output, mgzip_threads=mgzip_threads_for_output)
                return None, wr
                
            else:
                print("Opening the %s file in the %s collector with csv.writer." % (file_type, who), file=sys.stderr, flush=True)
                csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
                f = open(the_file, "w", newline='')
                wr = csv.writer(
                    f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                wr.writerow(header)
                return f, wr

        def open_node_file(self, header: typing.List[str], who: str):
            self.node_f, self.node_wr = self._open_file(node_file, header, "node", who)

        def open_minimal_edge_file(self, header: typing.List[str], who: str):
            self.minimal_edge_f, self.minimal_edge_wr = self._open_file(minimal_edge_file, header, "minimal edge", who)

        def open_detailed_edge_file(self, header: typing.List[str], who: str):
            self.detailed_edge_f, self.detailed_edge_wr = self._open_file(detailed_edge_file, header, "detailed edge", who)

        def open_minimal_qual_file(self, header: typing.List[str], who: str):
            self.minimal_qual_f, self.minimal_qual_wr = self._open_file(minimal_qual_file, header, "minimal qual", who)
            
        def open_detailed_qual_file(self, header: typing.List[str], who: str):
            self.detailed_qual_f, self.detailed_qual_wr = self._open_file(detailed_qual_file, header, "qual", who)
            
        def open_invalid_edge_file(self, header: typing.List[str], who: str):
            self.invalid_edge_f, self.invalid_edge_wr = self._open_file(invalid_edge_file, header, "invalid edge", who)

        def open_invalid_qual_file(self, header: typing.List[str], who: str):
            self.invalid_qual_f, self.invalid_qual_wr = self._open_file(invalid_qual_file, header, "qual", who)
            
        def open_split_alias_file(self, header: typing.List[str], who: str):
            self.split_alias_f, self.split_alias_wr = self._open_file(split_alias_file, header, ALIAS_LABEL, who)

        def open_split_en_alias_file(self, header: typing.List[str], who: str):
            self.split_en_alias_f, self.split_en_alias_wr = self._open_file(split_en_alias_file, header, "English " + ALIAS_LABEL, who)

        def open_split_datatype_file(self, header: typing.List[str], who: str):
            self.split_datatype_f, self.split_datatype_wr = self._open_file(split_datatype_file, header, DATATYPE_LABEL, who)

        def open_split_description_file(self, header: typing.List[str], who: str):
            self.split_description_f, self.split_description_wr = self._open_file(split_description_file, header, DESCRIPTION_LABEL, who)

        def open_split_en_description_file(self, header: typing.List[str], who: str):
            self.split_en_description_f, self.split_en_description_wr = self._open_file(split_en_description_file, header, "English " + DESCRIPTION_LABEL, who)

        def open_split_label_file(self, header: typing.List[str], who: str):
            self.split_label_f, self.split_label_wr = self._open_file(split_label_file, header, LABEL_LABEL, who)

        def open_split_en_label_file(self, header: typing.List[str], who: str):
            self.split_en_label_f, self.split_en_label_wr = self._open_file(split_en_label_file, header, "English " + LABEL_LABEL, who)

        def open_split_sitelink_file(self, header: typing.List[str], who: str):
            self.split_sitelink_f, self.split_sitelink_wr = self._open_file(split_sitelink_file, header, SITELINK_LABEL, who)

        def open_split_en_sitelink_file(self, header: typing.List[str], who: str):
            self.split_en_sitelink_f, self.split_en_sitelink_wr = self._open_file(split_en_sitelink_file, header, "English " + SITELINK_LABEL, who)

        def open_split_type_file(self, header: typing.List[str], who: str):
            self.split_type_f, self.split_type_wr = self._open_file(split_type_file, header, TYPE_LABEL, who)

        def open_split_property_edge_file(self, header: typing.List[str], who: str):
            self.split_property_edge_f, self.split_property_edge_wr = self._open_file(split_property_edge_file, header, "property edge", who)

        def open_split_property_qual_file(self, header: typing.List[str], who: str):
            self.split_property_qual_f, self.split_property_qual_wr = self._open_file(split_property_qual_file, header, "property qual", who)

        def shutdown(self, who: str):
            print("Exiting the %s collector (pid %d)." % (who, os.getpid()), file=sys.stderr, flush=True)

            if use_kgtkwriter:
                if self.node_wr is not None:
                    self.node_wr.close()

                if self.minimal_edge_wr is not None:
                    self.minimal_edge_wr.close()

                if self.detailed_edge_wr is not None:
                    self.detailed_edge_wr.close()

                if self.invalid_edge_wr is not None:
                    self.invalid_edge_wr.close()

                if self.minimal_qual_wr is not None:
                    self.minimal_qual_wr.close()

                if self.detailed_qual_wr is not None:
                    self.detailed_qual_wr.close()

                if self.invalid_qual_wr is not None:
                    self.invalid_qual_wr.close()

                if self.split_alias_wr is not None:
                    self.split_alias_wr.close()

                if self.split_en_alias_wr is not None:
                    self.split_en_alias_wr.close()

                if self.split_datatype_wr is not None:
                    self.split_datatype_wr.close()

                if self.split_description_wr is not None:
                    self.split_description_wr.close()

                if self.split_en_description_wr is not None:
                    self.split_en_description_wr.close()

                if self.split_label_wr is not None:
                    self.split_label_wr.close()

                if self.split_en_label_wr is not None:
                    self.split_en_label_wr.close()

                if self.split_sitelink_wr is not None:
                    self.split_sitelink_wr.close()

                if self.split_en_sitelink_wr is not None:
                    self.split_en_sitelink_wr.close()

                if self.split_type_wr is not None:
                    self.split_type_wr.close()

                if self.split_property_edge_wr is not None:
                    self.split_property_edge_wr.close()

                if self.split_property_edge_wr is not None:
                    self.split_property_edge_wr.close()

            else:
                if self.node_f is not None:
                    self.node_f.close()

                if self.minimal_edge_f is not None:
                    self.minimal_edge_f.close()

                if self.detailed_edge_f is not None:
                    self.detailed_edge_f.close()

                if self.minimal_qual_f is not None:
                    self.minimal_qual_f.close()

                if self.detailed_qual_f is not None:
                    self.detailed_qual_f.close()

                if self.invalid_edge_f is not None:
                    self.invalid_edge_f.close()

                if self.invalid_qual_f is not None:
                    self.invalid_qual_f.close()

                if self.split_alias_f is not None:
                    self.split_alias_f.close()

                if self.split_en_alias_f is not None:
                    self.split_en_alias_f.close()

                if self.split_datatype_f is not None:
                    self.split_datatype_f.close()

                if self.split_description_f is not None:
                    self.split_description_f.close()

                if self.split_en_description_f is not None:
                    self.split_en_description_f.close()

                if self.split_label_f is not None:
                    self.split_label_f.close()

                if self.split_en_label_f is not None:
                    self.split_en_label_f.close()

                if self.split_sitelink_f is not None:
                    self.split_sitelink_f.close()

                if self.split_en_sitelink_f is not None:
                    self.split_en_sitelink_f.close()

                if self.split_type_f is not None:
                    self.split_type_f.close()

                if self.split_property_edge_f is not None:
                    self.split_property_edge_f.close()

                if self.split_property_qual_f is not None:
                    self.split_property_qual_f.close()

            print("The %s collector has closed its output files." % who, file=sys.stderr, flush=True)

        def collect(self,
                    nrows: typing.List[typing.List[str]],
                    erows: typing.List[typing.List[str]],
                    qrows: typing.List[typing.List[str]],
                    invalid_erows: typing.List[typing.List[str]],
                    invalid_qrows: typing.List[typing.List[str]],
                    who: str):
            self.nrows += len(nrows)
            self.erows += len(erows)
            self.qrows += len(qrows)
            self.invalid_erows += len(invalid_erows)
            self.invalid_qrows += len(invalid_qrows)

            self.cnt += 1
            if progress_interval > 0 and self.cnt % progress_interval == 0:
                print("The {} collector called {} times: {} nrows, {} erows, {} qrows, {} invalid erows, {} invalid qrows".format(who,
                                                                                                                                  self.cnt,
                                                                                                                                  self.nrows,
                                                                                                                                  self.erows,
                                                                                                                                  self.qrows,
                                                                                                                                  self.invalid_erows,
                                                                                                                                  self.invalid_qrows),
                      file=sys.stderr, flush=True)
            row: typing.List[str]
            if len(nrows) > 0:
                if self.node_wr is None:
                    raise ValueError("Unexpected node rows in the %s collector." % who)

                if use_kgtkwriter:
                    for row in nrows:
                        self.node_wr.write(row)
                else:
                    self.node_wr.writerows(nrows)

            if len(erows) > 0:
                if use_kgtkwriter:
                    if not self.process_split_files:
                        if self.detailed_edge_wr is None:
                            raise ValueError("Unexpected edge rows in the %s collector." % who)
                        for row in erows:
                            if skip_validation or validate(row, "unsplit detailed edge"):
                                self.detailed_edge_wr.write(row)
                    else:
                        for row in erows:
                            split: bool = False
                            label: str = row[2] # Hack: knows the structure of the row.
                            method: typing.Optional[typing.Callable[[typing.List[str]], bool]] = self.split_dispatcher.get(label)
                            if method is not None:
                                split = method(row)
                            if not split:
                                if self.minimal_edge_wr is None and self.detailed_edge_wr is None and self.split_property_edge_wr is None:
                                    raise ValueError("Unexpected %s edge rows in the %s collector." % (label, who))

                                if self.split_property_edge_wr is not None and row[1].startswith("P"): # Hack: knows the structure of the row.
                                    # For now, split property files are minimal.
                                    if skip_validation or validate(row, "split property edge"):
                                        self.split_property_edge_wr.write((row[0], row[1], row[2], row[3], row[4], row[5])) # Hack: knows the structure of the row.

                                elif self.minimal_edge_wr is not None:
                                    if skip_validation or validate(row, "minimal edge"):
                                        self.minimal_edge_wr.write((row[0], row[1], row[2], row[3], row[4], row[5])) # Hack: knows the structure of the row.

                                if self.detailed_edge_wr is not None:
                                    if skip_validation or validate(row, "split detailed edge"):
                                        self.detailed_edge_wr.write(row)
                else:
                    if self.minimal_edge_wr is None:
                        raise ValueError("Unexpected edge rows in the %s collector." % who)

                    if skip_validation:
                        self.minimal_edge_wr.writerows(erows)
                    else:
                        for row in erows:
                            if validate(row, "minimal edge csv"):
                                self.minimal_edge_wr.write(row)

            if len(qrows) > 0:
                if use_kgtkwriter:
                    if self.minimal_qual_wr is None and self.detailed_qual_wr is None:
                        raise ValueError("Unexpected qual rows in the %s collector." % who)
                    
                    for row in qrows:
                        if self.split_property_qual_wr is not None and row[0].startswith("P"): # Hack: knows the structure of the row.
                            if skip_validation or validate(row, "split property qual"):
                                self.split_property_qual_wr.write((row[0], row[1], row[2], row[3], row[4])) # Hack: knows the structure of the row.
                                                              
                        elif self.minimal_qual_wr is not None:
                            if skip_validation or validate(row, "minimal qual"):
                                self.minimal_qual_wr.write((row[0], row[1], row[2], row[3], row[4])) # Hack: knows the structure of the row.

                        if self.detailed_qual_wr is not None:
                            if skip_validation or validate(row, "detailed qual"):
                                self.detailed_qual_wr.write(row)
                else:
                    if self.detailed_qual_wr is None:
                        raise ValueError("Unexpected qual rows in the %s collector." % who)
                    if skip_validation:
                        self.detailed_qual_wr.writerows(qrows)
                    else:
                        for row in qrows:
                            if validate(row, "detailed qual csv"):
                                self.detailed_qual_wr.write(row)

            if len(invalid_erows) > 0:
                # print("Writing invalid erows", file=sys.stderr, flush=True) # ***
                if self.invalid_edge_wr is None:
                    raise ValueError("Unexpected invalid edge rows in the %s collector." % who)

                if use_kgtkwriter:
                    for row in invalid_erows:
                        if minimal_edge_file is not None: # messy
                            self.invalid_edge_wr.write((row[0], row[1], row[2], row[3], row[4], row[5])) # Hack: knows the structure of the row.
                        else:
                            self.invalid_edge_wr.write(row)
                else:
                    self.invalid_edge_wr.writerows(invalid_erows)
                    
            if len(invalid_qrows) > 0:
                if self.invalid_qual_wr is None:
                    raise ValueError("Unexpected invalid qual rows in the %s collector." % who)

                if use_kgtkwriter:
                    for row in invalid_qrows:
                        if minimal_qual_file is not None: # messy
                            self.invalid_qual_wr.write((row[0], row[1], row[2], row[3], row[4])) # Hack: knows the structure of the row.
                        else:
                            self.invalid_qual_wr.write(row)
                else:
                    self.invalid_qual_wr.writerows(invalid_qrows)
                    
        def setup_split_dispatcher(self):
            self.split_dispatcher: typing.MutableMapping[str, typing.Callable[[typing.List[str]], bool]] = dict()
            self.split_dispatcher[ADDL_SITELINK_LABEL] = self.split_sitelink
            self.split_dispatcher[ALIAS_LABEL] = self.split_alias
            self.split_dispatcher[DATATYPE_LABEL] = self.split_datatype
            self.split_dispatcher[DESCRIPTION_LABEL] = self.split_description
            self.split_dispatcher[LABEL_LABEL] = self.split_label
            self.split_dispatcher[SITELINK_LABEL] = self.split_sitelink
            self.split_dispatcher[SITELINK_BADGE_LABEL] = self.split_sitelink
            self.split_dispatcher[SITELINK_LANGUAGE_LABEL] = self.split_sitelink
            self.split_dispatcher[SITELINK_SITE_LABEL] = self.split_sitelink
            self.split_dispatcher[SITELINK_TITLE_LABEL] = self.split_sitelink
            self.split_dispatcher[TYPE_LABEL] = self.split_type

        def split_alias(self, row: typing.List[str])->bool:
            split: bool = False

            lang: str = row[-1] # Hack: knows the structure of the row.

            if self.split_alias_wr is not None:
                self.split_alias_wr.write((row[0], row[1], row[2], row[3], lang)) # Hack: knows the structure of the row.
                split= True
                                    
            if self.split_en_alias_wr is not None and lang == "en":
                self.split_en_alias_wr.write((row[0], row[1], row[2], row[3])) # Hack: knows the structure of the row.
                split = True

            return split

        def split_datatype(self, row: typing.List[str])->bool:
            split: bool = False

            if self.split_datatype_wr is not None:
                self.split_datatype_wr.write((row[0], row[1], row[2], row[3])) # Hack: knows the structure of the row.
                split = True

            return split

        def split_description(self, row: typing.List[str])->bool:
            split: bool = False

            lang: str = row[-1] # Hack: knows the structure of the row.

            if self.split_description_wr is not None:
                self.split_description_wr.write((row[0], row[1], row[2], row[3], lang)) # Hack: knows the structure of the row.
                split = True

            if self.split_en_description_wr is not None and lang == "en":
                self.split_en_description_wr.write((row[0], row[1], row[2], row[3])) # Hack: knows the structure of the row.
                split = True
                
            return split

        def split_label(self, row: typing.List[str])->bool:
            split: bool = False

            lang: str = row[-1] # Hack: knows the structure of the row.

            if self.split_label_wr is not None:
                self.split_label_wr.write((row[0], row[1], row[2], row[3], lang)) # Hack: knows the structure of the row.
                split = True

            if self.split_en_label_wr is not None and lang == "en":
                self.split_en_label_wr.write((row[0], row[1], row[2], row[3])) # Hack: knows the structure of the row.
                split = True

            return split

        def split_sitelink(self, row: typing.List[str])->bool:
            split: bool = False

            lang: str = row[-1] # Hack: knows the structure of the row.

            if self.split_sitelink_wr is not None:
                self.split_sitelink_wr.write((row[0], row[1], row[2], row[3], lang)) # Hack: knows the structure of the row.
                split = True

            if self.split_en_sitelink_wr is not None and lang == "en":
                self.split_en_sitelink_wr.write((row[0], row[1], row[2], row[3])) # Hack: knows the structure of the row.
                split = True

            return split

        def split_type(self, row: typing.List[str])->bool:
            split: bool = False

            if self.split_type_wr is not None:
                self.split_type_wr.write((row[0], row[1], row[2], row[3])) # Hack: knows the structure of the row.
                split = True

            return split


    try:
        UPDATE_VERSION: str = "2021-02-24T21:11:49.602037+00:00#sgB3FM8zpy/0bbx1RwyRawYnB1spAUBS+FVVQBL8DtJVxXE8mYCTTLr2lHJqbKVe5fBPp+k5iQjTDmJ6GRVf8Q=="
        print("kgtk import-wikidata version: %s" % UPDATE_VERSION, file=sys.stderr, flush=True)
        print("Starting main process (pid %d)." % os.getpid(), file=sys.stderr, flush=True)
        inp_path = KGTKArgumentParser.get_input_file(input_file)
        
        csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
        
        start=time.time()

        if not skip_processing:
            from gzip import GzipFile
            print("Processing.", file=sys.stderr, flush=True)

            # Open the input file first to make it easier to monitor with "pv".
            input_f: typing.Union[GzipFile, typing.IO[typing.Any]]
            if str(inp_path) == "-":
                print('Processing wikidata from standard input', file=sys.stderr, flush=True)
                # It is not well documented, but this is how you read binary data
                # from stdin in Python 3.
                #
                # TODO: Add decompression.
                input_f = sys.stdin.buffer

            else:
                print('Processing wikidata file %s' % str(inp_path), file=sys.stderr, flush=True)
                input_f = open(inp_path, mode='rb')
                progress_startup(fd=input_f.fileno()) # Start the custom progress monitor.
            
                if str(inp_path).endswith(".bz2"):
                    print('Decompressing (bz2)', file=sys.stderr, flush=True)
                    # TODO: Optionally use a system decompression program.
                    input_f = bz2.open(input_f)

                elif str(inp_path).endswith(".gz"):
                    # TODO: Optionally use a system decompression program.
                    if use_mgzip_for_input:
                        import mgzip
                        print('Decompressing (mgzip)', file=sys.stderr, flush=True)
                        input_f = mgzip.open(input_f, thread=mgzip_threads_for_input)
                    else:
                        import gzip
                        print('Decompressing (gzip)', file=sys.stderr, flush=True)
                        input_f = gzip.open(input_f)

            collector_p = None
            node_collector_p = None
            edge_collector_p = None
            qual_collector_p = None
            invalid_edge_collector_p = None
            invalid_qual_collector_p = None

            description_collector_p = None
            sitelink_collector_p = None

            if collect_results:
                print("Creating the collector queue.", file=sys.stderr, flush=True)
                # collector_q = pyrallel.ShmQueue()
                collector_q_maxsize = procs*collector_queue_per_proc_size
                if collect_seperately:

                    if node_file is not None:
                        node_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector node queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)
                
                        print("Creating the node_collector.", file=sys.stderr, flush=True)
                        node_collector: MyCollector = MyCollector()
                        print("Creating the node collector process.", file=sys.stderr, flush=True)
                        node_collector_p = mp.Process(target=node_collector.run, args=(node_collector_q, "node"))
                        print("Starting the node collector process.", file=sys.stderr, flush=True)
                        node_collector_p.start()
                        print("Started the node collector process.", file=sys.stderr, flush=True)

                    if minimal_edge_file is not None or detailed_edge_file is not None:
                        edge_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector edge queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the edge_collector.", file=sys.stderr, flush=True)
                        edge_collector: MyCollector = MyCollector()
                        print("Creating the edge collector process.", file=sys.stderr, flush=True)
                        edge_collector_p = mp.Process(target=edge_collector.run, args=(edge_collector_q, "edge"))
                        print("Starting the edge collector process.", file=sys.stderr, flush=True)
                        edge_collector_p.start()
                        print("Started the edge collector process.", file=sys.stderr, flush=True)

                    if minimal_qual_file is not None or detailed_qual_file is not None:
                        qual_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector qual queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the qual_collector.", file=sys.stderr, flush=True)
                        qual_collector: MyCollector = MyCollector()
                        print("Creating the qual collector process.", file=sys.stderr, flush=True)
                        qual_collector_p = mp.Process(target=qual_collector.run, args=(qual_collector_q, "qual"))
                        print("Starting the qual collector process.", file=sys.stderr, flush=True)
                        qual_collector_p.start()
                        print("Started the qual collector process.", file=sys.stderr, flush=True)

                    if invalid_edge_file is not None:
                        invalid_edge_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector invalid edge queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the invalid_edge_collector.", file=sys.stderr, flush=True)
                        invalid_edge_collector: MyCollector = MyCollector()
                        print("Creating the invalid edge collector process.", file=sys.stderr, flush=True)
                        invalid_edge_collector_p = mp.Process(target=invalid_edge_collector.run, args=(invalid_edge_collector_q, "invalid edge"))
                        print("Starting the invalid edge collector process.", file=sys.stderr, flush=True)
                        invalid_edge_collector_p.start()
                        print("Started the invalid edge collector process.", file=sys.stderr, flush=True)

                    if invalid_qual_file is not None:
                        invalid_qual_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector invalid qual queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the invalid_qual_collector.", file=sys.stderr, flush=True)
                        invalid_qual_collector: MyCollector = MyCollector()
                        print("Creating the invalid qual collector process.", file=sys.stderr, flush=True)
                        invalid_qual_collector_p = mp.Process(target=invalid_qual_collector.run, args=(invalid_qual_collector_q, "invalid qual"))
                        print("Starting the invalid qual collector process.", file=sys.stderr, flush=True)
                        invalid_qual_collector_p.start()
                        print("Started the invalid qual collector process.", file=sys.stderr, flush=True)

                    if split_description_file is not None:
                        description_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector description queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the description collector.", file=sys.stderr, flush=True)
                        description_collector: MyCollector = MyCollector()
                        print("Creating the description collector process.", file=sys.stderr, flush=True)
                        description_collector_p = mp.Process(target=description_collector.run, args=(description_collector_q, "description"))
                        print("Starting the description collector process.", file=sys.stderr, flush=True)
                        description_collector_p.start()
                        print("Started the description collector process.", file=sys.stderr, flush=True)

                    if split_sitelink_file is not None:
                        sitelink_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector sitelink queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the sitelink collector.", file=sys.stderr, flush=True)
                        sitelink_collector: MyCollector = MyCollector()
                        print("Creating the sitelink collector process.", file=sys.stderr, flush=True)
                        sitelink_collector_p = mp.Process(target=sitelink_collector.run, args=(sitelink_collector_q, "sitelink"))
                        print("Starting the sitelink collector process.", file=sys.stderr, flush=True)
                        sitelink_collector_p.start()
                        print("Started the sitelink collector process.", file=sys.stderr, flush=True)

                else:
                    collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                    print("The common collector queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)
                
                    print("Creating the common collector.", file=sys.stderr, flush=True)
                    collector: MyCollector = MyCollector()
                    print("Creating the common collector process.", file=sys.stderr, flush=True)
                    collector_p = mp.Process(target=collector.run, args=(collector_q, "common"))
                    print("Starting the common collector process.", file=sys.stderr, flush=True)
                    collector_p.start()
                    print("Started the common collector process.", file=sys.stderr, flush=True)

            if node_file:
                if node_id_only:
                    node_file_header = ['id']
                else:
                   node_file_header = ['id','label','type','description','alias','datatype']

                ncq = collector_q if collector_q is not None else node_collector_q
                if ncq is not None:
                    print("Sending the node header to the collector.", file=sys.stderr, flush=True)
                    ncq.put(("node_header", None, None, None, None, None, node_file_header))
                    print("Sent the node header to the collector.", file=sys.stderr, flush=True)

                else:
                    with open(node_file+'_header', 'w', newline='') as myfile:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='',
                            lineterminator=csv_line_terminator)
                        wr.writerow(node_file_header)

            if explode_values:
                edge_file_header = ['id','node1','label','node2','rank','node2;magnitude','node2;unit','node2;date','node2;item','node2;lower','node2;upper',
                                    'node2;latitude','node2;longitude','node2;precision','node2;calendar','node2;entity-type','node2;wikidatatype', 'lang']
            else:
                edge_file_header = ['id','node1','label','node2',
                                    'rank', 'node2;wikidatatype',
                                    'claim_id', 'val_type', 'entity_type', 'datahash', 'precision', 'calendar', 'lang']

            ecq = collector_q if collector_q is not None else edge_collector_q
            if detailed_edge_file:
                if ecq is not None:
                    print("Sending the detailed edge header to the collector.", file=sys.stderr, flush=True)
                    ecq.put(("detailed_edge_header", None, None, None, None, None, edge_file_header))
                    print("Sent the detailed edge header to the collector.", file=sys.stderr, flush=True)

                else:
                    with open(detailed_edge_file+'_header', 'w', newline='') as myfile:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='',
                            lineterminator=csv_line_terminator)
                        wr.writerow(edge_file_header)

            if minimal_edge_file and ecq is not None:
                print("Sending the minimal edge file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("minimal_edge_header", None, None, None, None, None, edge_file_header[0:6]))
                print("Sent the minimal edge file header to the collector.", file=sys.stderr, flush=True)

            if split_alias_file and ecq is not None:
                alias_file_header = ['id', 'node1', 'label', 'node2', 'lang']
                print("Sending the alias file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_alias_header", None, None, None, None, None, alias_file_header))
                print("Sent the alias file header to the collector.", file=sys.stderr, flush=True)

            if split_en_alias_file and ecq is not None:
                en_alias_file_header = ['id', 'node1', 'label', 'node2']
                print("Sending the English alias file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_en_alias_header", None, None, None, None, None, en_alias_file_header))
                print("Sent the English alias file header to the collector.", file=sys.stderr, flush=True)

            if split_datatype_file and ecq is not None:
                datatype_file_header = ['id', 'node1', 'label', 'node2']
                print("Sending the datatype file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_datatype_header", None, None, None, None, None, datatype_file_header))
                print("Sent the datatype file header to the collector.", file=sys.stderr, flush=True)

            dcq = collector_q if collector_q is not None else description_collector_q
            if split_description_file and dcq is not None:
                description_file_header = ['id', 'node1', 'label', 'node2', 'lang']
                print("Sending the description file header to the collector.", file=sys.stderr, flush=True)
                dcq.put(("split_description_header", None, None, None, None, None, description_file_header))
                print("Sent the description file header to the collector.", file=sys.stderr, flush=True)

            if split_en_description_file and dcq is not None:
                en_description_file_header = ['id', 'node1', 'label', 'node2']
                print("Sending the English description file header to the collector.", file=sys.stderr, flush=True)
                dcq.put(("split_en_description_header", None, None, None, None, None, en_description_file_header))
                print("Sent the English description file header to the collector.", file=sys.stderr, flush=True)

            if split_label_file and ecq is not None:
                label_file_header = ['id', 'node1', 'label', 'node2', 'lang']
                print("Sending the label file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_label_header", None, None, None, None, None, label_file_header))
                print("Sent the label file header to the collector.", file=sys.stderr, flush=True)

            if split_en_label_file and ecq is not None:
                en_label_file_header = ['id', 'node1', 'label', 'node2']
                print("Sending the English label file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_en_label_header", None, None, None, None, None, en_label_file_header))
                print("Sent the English label file header to the collector.", file=sys.stderr, flush=True)

            scq = collector_q if collector_q is not None else sitelink_collector_q
            if split_sitelink_file and scq is not None:
                sitelink_file_header = ['id', 'node1', 'label', 'node2', 'lang']
                print("Sending the sitelink file header to the collector.", file=sys.stderr, flush=True)
                scq.put(("split_sitelink_header", None, None, None, None, None, sitelink_file_header))
                print("Sent the sitelink file header to the collector.", file=sys.stderr, flush=True)

            if split_en_sitelink_file and scq is not None:
                en_sitelink_file_header = ['id', 'node1', 'label', 'node2']
                print("Sending the English sitelink file header to the collector.", file=sys.stderr, flush=True)
                scq.put(("split_en_sitelink_header", None, None, None, None, None, en_sitelink_file_header))
                print("Sent the English sitelink file header to the collector.", file=sys.stderr, flush=True)

            if split_type_file and ecq is not None:
                type_file_header = ['id', 'node1', 'label', 'node2']
                print("Sending the entry type file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_type_header", None, None, None, None, None, type_file_header))
                print("Sent the entry type file header to the collector.", file=sys.stderr, flush=True)

            if split_property_edge_file and ecq is not None:
                print("Sending the property edge file header to the collector.", file=sys.stderr, flush=True)
                ecq.put(("split_property_edge_header", None, None, None, None, None, edge_file_header[0:6]))
                print("Sent the property edge file header to the collector.", file=sys.stderr, flush=True)

            if invalid_edge_file and invalid_edge_collector_q is not None:
                if detailed_edge_file:
                    print("Sending the detailed invalid edge header to the collector.", file=sys.stderr, flush=True)
                    invalid_edge_collector_q.put(("invalid_edge_header", None, None, None, None, None, edge_file_header))
                    print("Sent the detailed invalid edge header to the collector.", file=sys.stderr, flush=True)
                elif minimal_edge_file:
                    print("Sending the minimal invalid edge header to the collector.", file=sys.stderr, flush=True)
                    invalid_edge_collector_q.put(("invalid_edge_header", None, None, None, None, None, edge_file_header[0:6]))
                    print("Sent the minimal invalid edge header to the collector.", file=sys.stderr, flush=True)
                
            if minimal_qual_file is not None or detailed_qual_file is not None or split_property_qual_file is not None:
                qual_file_header = edge_file_header.copy()
                if "rank" in qual_file_header:
                    qual_file_header.remove('rank')
                if "claim_type" in qual_file_header:
                    qual_file_header.remove('claim_type')
                if "claim_id" in qual_file_header:
                    qual_file_header.remove('claim_id')
                if "lang" in qual_file_header:
                    qual_file_header.remove('lang')

                qcq = collector_q if collector_q is not None else qual_collector_q

                if detailed_qual_file is not None:
                    if qcq is not None:
                        print("Sending the detailed qual file header to the collector.", file=sys.stderr, flush=True)
                        qcq.put(("detailed_qual_header", None, None, None, None, None, qual_file_header))
                        print("Sent the detailed qual file header to the collector.", file=sys.stderr, flush=True)

                    else:
                        with open(detailed_qual_file+'_header', 'w', newline='') as myfile:
                            wr = csv.writer(
                                myfile,
                                quoting=csv.QUOTE_NONE,
                                delimiter="\t",
                                escapechar="\n",
                                quotechar='',
                                lineterminator=csv_line_terminator)
                            wr.writerow(qual_file_header)
                if minimal_qual_file is not None and qcq is not None:
                    print("Sending the minimal qual file header to the collector.", file=sys.stderr, flush=True)
                    qcq.put(("minimal_qual_header", None, None, None, None, None, qual_file_header[0:5]))
                    print("Sent the minimal qual file header to the collector.", file=sys.stderr, flush=True)
                        
                if split_property_qual_file and qcq is not None:
                    print("Sending the property qual file header to the collector.", file=sys.stderr, flush=True)
                    qcq.put(("split_property_qual_header", None, None, None, None, None, qual_file_header[0:5]))
                    print("Sent the property qual file header to the collector.", file=sys.stderr, flush=True)

                if invalid_qual_file and invalid_qual_collector_q is not None:
                    if detailed_qual_file:
                        print("Sending the detailed invalid qual header to the collector.", file=sys.stderr, flush=True)
                        invalid_qual_collector_q.put(("invalid_qual_header", None, None, None, None, None, qual_file_header))
                        print("Sent the detailed invalid qual header to the collector.", file=sys.stderr, flush=True)
                    elif minimal_qual_file:
                        print("Sending the minimal invalid qual header to the collector.", file=sys.stderr, flush=True)
                        invalid_qual_collector_q.put(("invalid_qual_header", None, None, None, None, None, qual_file_header[0:5]))
                        print("Sent the minimal invalid qual header to the collector.", file=sys.stderr, flush=True)
                
            print('Creating parallel processor for {}'.format(str(inp_path)), file=sys.stderr, flush=True)
            if use_shm or single_mapper_queue:
                pp = pyrallel.ParallelProcessor(procs, MyMapper,enable_process_id=True, max_size_per_mapper_queue=max_size_per_mapper_queue,
                                                use_shm=use_shm, enable_collector_queues=False, batch_size=mapper_batch_size,
                                                single_mapper_queue=single_mapper_queue)
            else:
                pp = pyrallel.ParallelProcessor(procs, MyMapper,enable_process_id=True, max_size_per_mapper_queue=max_size_per_mapper_queue,
                                                batch_size=mapper_batch_size)
            print('Start parallel processing', file=sys.stderr, flush=True)
            pp.start()
            for cnt, line in enumerate(input_f):
                if limit and cnt >= limit:
                    break
                # pp.add_task(line,node_file,edge_file,qual_file,languages,source)
                pp.add_task(line)

            print('Done processing {}'.format(str(inp_path)), file=sys.stderr, flush=True)
            input_f.close()
            
            print('Telling the workers to shut down.', file=sys.stderr, flush=True)
            pp.task_done()
            print('Waiting for the workers to shut down.', file=sys.stderr, flush=True)
            pp.join()
            print('Worker shut down is complete.', file=sys.stderr, flush=True)

            if collector_q is not None:
                print('Telling the collector to shut down.', file=sys.stderr, flush=True)
                collector_q.put(("shutdown", None, None, None, None, None, None))
            if collector_p is not None:
                print('Waiting for the collector to shut down.', file=sys.stderr, flush=True)
                collector_p.join()
                print('Collector shut down is complete.', file=sys.stderr, flush=True)
            if collector_q is not None:
                collector_q.close()

            if node_collector_q is not None:
                print('Telling the node collector to shut down.', file=sys.stderr, flush=True)
                node_collector_q.put(("shutdown", None, None, None, None, None, None))
            if node_collector_p is not None:
                print('Waiting for the node collector to shut down.', file=sys.stderr, flush=True)
                node_collector_p.join()
                print('Node collector shut down is complete.', file=sys.stderr, flush=True)
            if node_collector_q is not None:
                node_collector_q.close()

            if edge_collector_q is not None:
                print('Telling the edge collector to shut down.', file=sys.stderr, flush=True)
                edge_collector_q.put(("shutdown", None, None, None, None, None, None))
            if edge_collector_p is not None:
                print('Waiting for the edge collector to shut down.', file=sys.stderr, flush=True)
                edge_collector_p.join()
                print('Edge collector shut down is complete.', file=sys.stderr, flush=True)
            if edge_collector_q is not None:
                edge_collector_q.close()

            if qual_collector_q is not None:
                print('Telling the qual collector to shut down.', file=sys.stderr, flush=True)
                qual_collector_q.put(("shutdown", None, None, None, None, None, None))
            if qual_collector_p is not None:
                print('Waiting for the qual collector to shut down.', file=sys.stderr, flush=True)
                qual_collector_p.join()
                print('Qual collector shut down is complete.', file=sys.stderr, flush=True)
            if qual_collector_q is not None:
                qual_collector_q.close()

            if invalid_edge_collector_q is not None:
                print('Telling the invalid edge collector to shut down.', file=sys.stderr, flush=True)
                invalid_edge_collector_q.put(("shutdown", None, None, None, None, None, None))
            if invalid_edge_collector_p is not None:
                print('Waiting for the invalid edge collector to shut down.', file=sys.stderr, flush=True)
                invalid_edge_collector_p.join()
                print('Invalid edge collector shut down is complete.', file=sys.stderr, flush=True)
            if invalid_edge_collector_q is not None:
                invalid_edge_collector_q.close()

            if invalid_qual_collector_q is not None:
                print('Telling the invalid qual collector to shut down.', file=sys.stderr, flush=True)
                invalid_qual_collector_q.put(("shutdown", None, None, None, None, None, None))
            if invalid_qual_collector_p is not None:
                print('Waiting for the invalid qual collector to shut down.', file=sys.stderr, flush=True)
                invalid_qual_collector_p.join()
                print('Invalid qual collector shut down is complete.', file=sys.stderr, flush=True)
            if invalid_qual_collector_q is not None:
                invalid_qual_collector_q.close()

            if description_collector_q is not None:
                print('Telling the description collector to shut down.', file=sys.stderr, flush=True)
                description_collector_q.put(("shutdown", None, None, None, None, None, None))
            if description_collector_p is not None:
                print('Waiting for the description collector to shut down.', file=sys.stderr, flush=True)
                description_collector_p.join()
                print('Description collector shut down is complete.', file=sys.stderr, flush=True)
            if description_collector_q is not None:
                description_collector_q.close()

            if sitelink_collector_q is not None:
                print('Telling the sitelink collector to shut down.', file=sys.stderr, flush=True)
                sitelink_collector_q.put(("shutdown", None, None, None, None, None, None))
            if sitelink_collector_p is not None:
                print('Waiting for the sitelink collector to shut down.', file=sys.stderr, flush=True)
                sitelink_collector_p.join()
                print('Sitelink collector shut down is complete.', file=sys.stderr, flush=True)
            if sitelink_collector_q is not None:
                sitelink_collector_q.close()

        if not skip_merging and not collect_results:
            # We've finished processing the input data, possibly using multiple
            # server processes.  We need to assemble the final output file(s) with
            # the header first, then the fragments produced by parallel
            # processing.
            #
            # If we assume that we are on Linux, then os.sendfile(...)
            # should provide the simplest, highest-performing solution.
            if node_file:
                print('Combining the node file fragments', file=sys.stderr, flush=True)
                node_file_fragments=[node_file+'_header']
                for n in range(procs):
                    node_file_fragments.append(node_file+'_'+str(n))
                platform_cat(node_file_fragments, node_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

            if detailed_edge_file:
                print('Combining the edge file fragments', file=sys.stderr, flush=True)
                edge_file_fragments=[detailed_edge_file+'_header']
                for n in range(procs):
                    edge_file_fragments.append(detailed_edge_file+'_'+str(n))
                platform_cat(edge_file_fragments, detailed_edge_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

            if detailed_qual_file:
                print('Combining the qualifier file fragments', file=sys.stderr, flush=True)
                qual_file_fragments=[detailed_qual_file+'_header']
                for n in range(procs):
                    qual_file_fragments.append(detailed_qual_file+'_'+str(n))
                platform_cat(qual_file_fragments, detailed_qual_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

        print('import complete', file=sys.stderr, flush=True)
        end=time.time()
        print('time taken : {}s'.format(end-start), file=sys.stderr, flush=True)
    except Exception as e:
        raise KGTKException(str(e))

def validate(row: typing.List[str], who: str)->bool:
    """Ensure that output edge rows meet minimal validation criteria."""
    import sys

    # There must be at least four fields (id, node1, label, node2):
    if len(row) < 4:
        print("%s row too short: %s" % (who, repr(row)), file=sys.stderr, flush=True)
        return False

    # Ensure that the first four fields (id, node1, label, node2) are all
    # non-empty.
    if len(row[0]) == 0 or len(row[1]) == 0 or len(row[2]) == 0 or len(row[3]) ==0:
        print("Invalid %s row: (%s, %s, %s, %s)" % (who, repr(row[0]), repr(row[1]), repr(row[2]), repr(row[3])), file=sys.stderr, flush=True)
        return False

    return True
