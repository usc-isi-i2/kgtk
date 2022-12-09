"""
Compute paths between nodes in a KGTK graph.

TODO: Add --output-file
"""
from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Compute paths between nodes in a KGTK graph.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True)
    parser.add_output_file()
    parser.add_input_file(who="KGTK file with path start and end nodes.",
                          options=["--path-file", "--path_file"], dest="path_file", metavar="PATH_FILE", optional=False)

    parser.add_argument('--statistics-only', dest='statistics_only',
                        help='If this flag is set, output only the statistics edges. Else, append the statistics to the original graph. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--undirected', dest="undirected",
                        help="Is the graph undirected or not? (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--max-hops', '--max_hops', action="store", type=int, dest="max_hops",
                        help="Maximum number of hops allowed.")

    parser.add_argument("--path-source", action="store", type=str, dest="source_column_name",
                        help='Name of the source column in the path file. (default: node1 or its alias)')
    parser.add_argument("--path-target", action="store", type=str, dest="target_column_name",
                        help='Name of the source column in the path file. (default: node2 or its alias)')

    parser.add_argument("--shortest-path", dest="shortest_path", metavar="True|False",
                        help="When true, shortest paths are returned. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="path", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        path_file: KGTKFiles,
        output_file: KGTKFiles,
        statistics_only: bool,
        undirected: bool,
        max_hops: int,
        source_column_name: typing.Optional[str],
        target_column_name: typing.Optional[str],
        shortest_path: bool,
        errors_to_stdout: bool,
        verbose: bool,
        very_verbose: bool,
        **kwargs,  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    # import modules locally
    from pathlib import Path
    import sys

    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions

    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    from kgtk.exceptions import KGTKException
    from kgtk.graph_analysis.paths import Paths
    try:

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
        path_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="path", fallback=True)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        path_kgtk_file: Path = KGTKArgumentParser.get_input_file(path_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        gp = Paths(input_kgtk_file=input_kgtk_file,
                   path_kgtk_file=path_kgtk_file,
                   output_kgtk_file=output_kgtk_file,
                   statistics_only=statistics_only,
                   undirected=undirected,
                   max_hops=max_hops,
                   source_column_name=source_column_name,
                   target_column_name=target_column_name,
                   shortest_path=shortest_path,
                   input_reader_options=input_reader_options,
                   path_reader_options=path_reader_options,
                   value_options=value_options,
                   error_file=error_file,
                   verbose=verbose,
                   very_verbose=very_verbose)
        gp.process()


    except Exception as e:
        raise KGTKException('Error: ' + str(e))
