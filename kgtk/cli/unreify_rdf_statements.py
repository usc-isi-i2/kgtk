"""Unreify RDF statements in a KGTK file.

TODO: Need KgtkWriterOptions
"""

from argparse import _MutuallyExclusiveGroup, Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Unreify RDF statements in a KGTK file.',
        'description': 'Read a KGTK file, such as might have been created by importing an ntriples file.  ' +
        'Search for reified RFD statements and transform them into an unreified form.' +
        '\n\nAn ID column will be added to the output file if not present in the input file.  ' +
        '\n\n--reified-file PATH, if specified, will get a copy of the input records that were ' +
        'identified as reified RDF statements. ' +
        '\n\n--uninvolved-file PATH, if specified, will get a copy of the input records that were ' +
        ' identified as not being reified RDF statements. ' +
        '\n\n--unreified-file PATH, if specified, will get a copy of the unreified output records, which ' +
        ' will still be written to the main output file.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert unreify-rdb-statements --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.unreify.kgtkunreifyrdfstatements import KgtkUnreifyRdfStatements
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(who="The KGTK input file with the reified data.")
    parser.add_output_file()
    parser.add_output_file(who="A KGTK output file that will contain only the reified RDF statements.",
                           dest="reified_file",
                           options=["--reified-file"],
                           metavar="REIFIED_FILE",
                           optional=True)
    parser.add_output_file(who="A KGTK output file that will contain only the unreified RDF statements.",
                           dest="unreified_file",
                           options=["--unreified-file"],
                           metavar="UNREIFIED_FILE",
                           optional=True)
    parser.add_output_file(who="A KGTK output file that will contain only the uninvolved input.",
                           dest="uninvolved_file",
                           options=["--uninvolved-file"],
                           metavar="UNINVOLVED_FILE",
                           optional=True)

    KgtkUnreifyRdfStatements.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reified_file: KGTKFiles,
        unreified_file: KGTKFiles,
        uninvolved_file: KGTKFiles,

        trigger_label_value: str,
        trigger_node2_value: str,
        rdf_subject_label_value: str,
        rdf_predicate_label_value: str,
        rdf_object_label_value: str,

        allow_multiple_subjects: bool,
        allow_multiple_predicates: bool,
        allow_multiple_objects: bool,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.unreify.kgtkunreifyrdfstatements import KgtkUnreifyRdfStatements
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    reified_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reified_file, who="KGTK reified file")
    unreified_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(unreified_file, who="KGTK unreified file")
    uninvolved_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(uninvolved_file, who="KGTK uninvolved file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-files %s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if reified_kgtk_file is not None:
            print("--reified-file=%s" % str(reified_kgtk_file), file=error_file, flush=True)
        if unreified_kgtk_file is not None:
            print("--unreified-file=%s" % str(unreified_kgtk_file), file=error_file, flush=True)
        if uninvolved_kgtk_file is not None:
            print("--uninvolved-file=%s" % str(uninvolved_kgtk_file), file=error_file, flush=True)
        
        print("--trigger-label=%s" % trigger_label_value, file=error_file, flush=True)
        print("--trigger-node2=%s" % trigger_node2_value, file=error_file, flush=True)
        print("--node1-role=%s" % rdf_subject_label_value, file=error_file, flush=True)
        print("--label-role=%s" % rdf_predicate_label_value, file=error_file, flush=True)
        print("--node2-role=%s" % rdf_object_label_value, file=error_file, flush=True)

        print("--allow-multiple-subjects=%s" % str(allow_multiple_subjects), file=error_file, flush=True)
        print("--allow-multiple-predicates=%s" % str(allow_multiple_predicates), file=error_file, flush=True)
        print("--allow-multiple-objects=%s" % str(allow_multiple_objects), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kurs: KgtkUnreifyRdfStatements = KgtkUnreifyRdfStatements(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            reified_file_path=reified_kgtk_file,
            unreified_file_path=unreified_kgtk_file,
            uninvolved_file_path=uninvolved_kgtk_file,

            trigger_label_value=trigger_label_value,
            trigger_node2_value=trigger_node2_value,
            rdf_object_label_value=rdf_object_label_value,
            rdf_predicate_label_value=rdf_predicate_label_value,
            rdf_subject_label_value=rdf_subject_label_value,

            allow_multiple_subjects=allow_multiple_subjects,
            allow_multiple_predicates=allow_multiple_predicates,
            allow_multiple_objects=allow_multiple_objects,

            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose)

        kurs.process()
    
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

