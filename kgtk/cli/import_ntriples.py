"""Import an ntriples file, writing a KGTK file.

TODO: Need KgtkWriterOptions
"""

from argparse import _MutuallyExclusiveGroup, Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import an ntriples file.',
        'description': 'Import an ntriples file, writing a KGTK file.' + 
        '\n\nAdditional options are shown in expert help.\nkgtk --expert import-ntriples --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.imports.kgtkntriples import KgtkNtriples
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
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

    parser.add_input_file(who="The ntriples file(s) to import.", allow_list=True)
    parser.add_output_file()

    parser.add_output_file(who="The ntriples output file for records that are rejected.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    parser.add_input_file(who="The KGTK input file with known namespaces.",
                          dest="namespace_file",
                          options=["--namespace-file"],
                          metavar="NAMESPACE_FILE",
                          optional=True)

    parser.add_output_file(who="The KGTK output file with updated namespaces.",
                           dest="updated_namespace_file",
                           options=["--updated-namespace-file"],
                           metavar="NAMESPACE_FILE",
                           optional=True)

    KgtkNtriples.add_arguments(parser)
    KgtkIdBuilderOptions.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,

        namespace_file: KGTKFiles,
        updated_namespace_file: KGTKFiles,

        namespace_id_prefix: str,
        namespace_id_use_uuid: bool,
        namespace_id_counter: int,
        namespace_id_zfill: int,
        output_only_used_namespaces: bool,

        allow_lax_uri: bool,

        local_namespace_prefix: str,
        local_namespace_use_uuid: bool,

        prefix_expansion_label: str,
        structured_value_label: str,
        structured_uri_label: str,

        newnode_prefix: str,
        newnode_use_uuid: bool,
        newnode_counter: int,
        newnode_zfill: int,

        build_id: bool,

        escape_pipes: bool,

        validate: bool,

        override_uuid: typing.Optional[str],

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
    from kgtk.imports.kgtkntriples import KgtkNtriples
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    # Select where to send error messages, defaulting to stderr.
    input_file_paths: typing.List[Path] = KGTKArgumentParser.get_input_file_list(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_file_path: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="KGTK reject file")

    namespace_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_input_file(namespace_file, who="KGTK namespace file")
    updated_namespace_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(updated_namespace_file, who="KGTK updated namespace file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_dict(kwargs)    
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-files %s" % " ".join([str(path) for  path in input_file_paths]), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if reject_file_path is not None:
            print("--reject-file=%s" % str(reject_file_path), file=error_file, flush=True)
        if namespace_kgtk_file is not None:
            print("--namespace-file=%s" % str(namespace_kgtk_file), file=error_file, flush=True)
        if updated_namespace_kgtk_file is not None:
            print("--updated-namespace-file=%s" % str(updated_namespace_kgtk_file), file=error_file, flush=True)

        print("--namespace-id-prefix %s" % namespace_id_prefix, file=error_file, flush=True)
        print("--namespace-id-use-uuid %s" % str(namespace_id_use_uuid), file=error_file, flush=True)
        print("--namespace-id-counter %s" % str(namespace_id_counter), file=error_file, flush=True)
        print("--namespace-id-zfill %s" % str(namespace_id_zfill), file=error_file, flush=True)
        print("--output-only-used-namespaces %s" % str(output_only_used_namespaces), file=error_file, flush=True)

        print("--allow-lax-uri %s" % str(allow_lax_uri), file=error_file, flush=True)
        
        print("--local-namespace-prefix %s" % local_namespace_prefix, file=error_file, flush=True)
        print("--local-namespace-use-uuid %s" % str(local_namespace_use_uuid), file=error_file, flush=True)

        print("--prefix-expansion-label %s" % prefix_expansion_label, file=error_file, flush=True)
        print("--structured-value-label %s" % structured_value_label, file=error_file, flush=True)
        print("--structured-uri-label %s" % structured_uri_label, file=error_file, flush=True)
        
        print("--newnode-prefix %s" % newnode_prefix, file=error_file, flush=True)
        print("--newnode-use-uuid %s" % str(newnode_use_uuid), file=error_file, flush=True)
        print("--newnode-counter %s" % str(newnode_counter), file=error_file, flush=True)
        print("--newnode-zfill %s" % str(newnode_zfill), file=error_file, flush=True)
        
        print("--build-id=%s" % str(build_id), file=error_file, flush=True)

        print("--escape-pipes=%s" % str(escape_pipes), file=error_file, flush=True)
        
        print("--validate=%s" % str(validate), file=error_file, flush=True)
        
        print("--override-uuid=%s" % str(override_uuid), file=error_file, flush=True)
        
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kn: KgtkNtriples = KgtkNtriples(
            input_file_paths=input_file_paths,
            output_file_path=output_kgtk_file,
            reject_file_path=reject_file_path,
            updated_namespace_file_path=updated_namespace_kgtk_file,
            namespace_file_path=namespace_kgtk_file,
            namespace_id_prefix=namespace_id_prefix,
            namespace_id_use_uuid=namespace_id_use_uuid,
            namespace_id_counter=namespace_id_counter,
            namespace_id_zfill=namespace_id_zfill,
            output_only_used_namespaces=output_only_used_namespaces,
            newnode_prefix=newnode_prefix,
            newnode_use_uuid=newnode_use_uuid,
            newnode_counter=newnode_counter,
            newnode_zfill=newnode_zfill,
            allow_lax_uri=allow_lax_uri,
            local_namespace_prefix=local_namespace_prefix,
            local_namespace_use_uuid=local_namespace_use_uuid,
            prefix_expansion_label=prefix_expansion_label,
            structured_value_label=structured_value_label,
            structured_uri_label=structured_uri_label,
            build_id=build_id,
            escape_pipes=escape_pipes,
            validate=validate,
            override_uuid=override_uuid,
            idbuilder_options=idbuilder_options,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose)

        kn.process()
    
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

