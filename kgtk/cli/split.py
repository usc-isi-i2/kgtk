from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Split a sorted KGTK edge file into multiple byte sized files',
        'description': 'split a sorted KGTK edge file into smaller files, keeping the Qnode'
                       'boundaries intact. Helpful in parallel processing and debugging.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file()

    parser.add_argument('--output-path', action='store', type=str, dest="output_path", required=True,
                        help="Path of an existing folder where the split files will be written")

    parser.add_argument('--file-prefix', action='store', type=str, default='split_', dest='file_prefix', required=False,
                        help="file name prefix, will be appended to output file names before a number")

    parser.add_argument('--split-by-qnode', type=optional_bool, default=False,
                        dest='split_by_qnode', metavar='True|False',
                        help="If True, all edges for a qnode will be written to a separate file,  "
                             "qnode will be added to the file name")

    parser.add_argument('--lines', action='store', dest='lines', type=int, default=1000000, required=False,
                        help="number of lines in each split file. The actual number of lines will exceed this number, "
                             "since Qnode boundaries are preserved.")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_path: str,
        file_prefix: str,
        split_by_qnode: bool,
        lines: int,
        errors_to_stdout: bool = False,
        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    # import modules locally
    from pathlib import Path

    import sys
    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)

    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr
    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                     options=reader_options,
                                     value_options=value_options,
                                     error_file=error_file,
                                     verbose=False,
                                     very_verbose=False,
                                     )

    node1_idx: int = kr.get_node1_column_index()
    label_idx: int = kr.get_label_column_index()
    node2_idx: int = kr.get_node2_column_index()

    if node1_idx < 0 or label_idx < 0 or node2_idx < 0:
        print("Error: Not a valid file: {}. A valid edge file should have these columns: node1, label and node2".format(
            input_file), file=error_file, flush=True)
        kr.close()
        raise KGTKException("Missing columns.")

    prev = None
    lines_to_write = list()
    file_number = 0

    for row in kr:
        node = row[node1_idx]
        if node.startswith('Q') or node.startswith('P'):
            if prev is None:
                prev = node

            if not prev.strip() == node.strip():
                prev = node
                if len(lines_to_write) >= lines:
                    output_kgtk_file = Path(f'{output_path}/{file_prefix}{file_number}.tsv')
                    kw = KgtkWriter.open(kr.column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         use_mgzip=reader_options.use_mgzip,  # Hack!
                                         mgzip_threads=reader_options.mgzip_threads,  # Hack!
                                         error_file=error_file,
                                         verbose=False,
                                         very_verbose=False)

                    # kw.write(lines_to_write)
                    for r in lines_to_write:
                        kw.write(r)
                    kw.close()
                    lines_to_write = list()
                    file_number += 1

            lines_to_write.append(row)

    if len(lines_to_write) > 0:
        output_kgtk_file = Path(f'{output_path}/{file_prefix}{file_number}.tsv')
        kw = KgtkWriter.open(kr.column_names,
                             output_kgtk_file,
                             mode=KgtkWriter.Mode[kr.mode.name],
                             use_mgzip=reader_options.use_mgzip,  # Hack!
                             mgzip_threads=reader_options.mgzip_threads,  # Hack!
                             error_file=error_file,
                             verbose=False,
                             very_verbose=False)

        for r in lines_to_write:
            kw.write(r)
        kw.close()
