"""
Convert a TDM JSON file and convert it to a KGTK file.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Convert a TDM JSON file to a KGTK file.',
        'description': 'Convert a TDM JSON input file to a KGTK file on output.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert import-tdm --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(who="The TDM JSON file to import.",
                          dest="input_files",
                          options=["-i", "--input-files"],
                          allow_list=True)
    parser.add_output_file(who="The KGTK file to write.")

    KgtkIdBuilderOptions.add_arguments(parser, expert=True, default_style=KgtkIdBuilderOptions.EMPTY_STYLE) # Show all the options.
    KgtkReader.add_debug_arguments(parser, expert=_expert)

def run(input_files: KGTKFiles,
        output_file: KGTKFiles,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import simplejson as json
    import sys
    import typing
    
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.join.kgtkcat import KgtkCat
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions

    input_file_paths: typing.List[Path] = KGTKArgumentParser.get_input_file_list(input_files)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures:
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_dict(kwargs)


    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(output_file_path), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        
        # Define our output columns:
        oc: typing.List[str] = ["id", "node1", "label", "node2", "P17", "P585", "PTDMmonetary_value", "P248"]

        p5471_map: typing.ModifiableMapping[str, str] = dict()
        label_map: typing.ModifiableMapping[str, str] = dict()

        # Create the ID builder:
        idb: KgtkIdBuilder = KgtkIdBuilder.from_column_names(oc, idbuilder_options)

        kw: KgtkWriter = KgtkWriter.open(idb.column_names,
                                         output_file_path,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        error_count: int = 0

        input_file_path: Path
        for input_file_path in input_file_paths:
            with open(input_file_path, "r") as ifp:
                tdm: dict = json.load(ifp)


                # Find the source ISO code and name.
                source_iso_codes: typing.List[str] = list()
                source_names: typing.List[str] = list()
                if "PHEADER1" not in tdm:
                    print("PHEADER1 not found", file=error_file, flush=True)
                    error_count += 1
                    continue

                pheader1: dict = tdm["PHEADER1"]
                if "SOURCES" not in pheader1:
                    print("SOURCES not found in PHEADER1", file=error_file, flush=True)
                    error_count += 1
                    continue

                sources: typing.List[dict] = pheader1["SOURCES"]
                source: dict
                for source in sources:
                    if "DSN" in source:
                        dsn: str = source["DSN"]
                        if dsn not in source_iso_codes:
                            source_iso_codes.append(dsn)
                    if "REPORTER" in source:
                        reporter: str = source["REPORTER"]
                        if reporter not in source_names:
                            source_names.append(reporter)
                if len(source_iso_codes) == 0:
                    print("No source ISO code found.", file=error_file, flush=True)
                    error_count += 1
                    continue

                if len(source_iso_codes) > 1:
                    print("Conflicting source ISO codes: %s" % repr(source_iso_codes), file=error_file, flush=True)
                    error_count += 1
                    continue

                source_iso_code: str = source_iso_codes[0]
                if len(source_names) == 0:
                    print("No source name found.", file=error_file, flush=True)
                    error_count += 1
                    continue

                if len(source_names) > 1:
                    print("Conflicting source names: %s" % repr(source_names), file=error_file, flush=True)
                    error_count += 1
                    continue

                source_name = source_names[0]
                
                # Find the commodity code and name.
                if "COMMODITY" not in pheader1:
                    print("COMMODITY not found in PHEADER1", file=error_file, flush=True)
                    error_count += 1
                    continue
                hs_code: str = pheader1["COMMODITY"]

                if "COMMODITY_DESCRIPT" not in pheader1:
                    print("COMMODITY_DESCRIPT not found in PHEADER1", file=error_file, flush=True)
                    error_count += 1
                    continue
                hs_name: str = pheader1["COMMODITY_DESCRIPT"]
                    

                # Build the base KGTK record:
                node1: str = "QTDM_iso_country_" + source_iso_code
                label_map[node1] = KgtkFormat.stringify(source_name, language="en")

                label: str = "PTDM_goods_imported"

                node2: str = "QTDM_HS_" + hs_code
                label_map[node2] = KgtkFormat.stringify(hs_name, language="en")
                
                # Determine the time span for each column of the results.
                # This is rather ugly.  First, verify that the results are
                # an annual time series as expected.
                if "PHEADER2" not in tdm:
                    print("PHEADER2 not found.", file=error_file, flush=True)
                    error_count += 1
                    continue
                pheader2 = tdm["PHEADER2"]
                initial_pheader2: str = "<span table-translate='Annual'>Annual</span> <span><span table-translate='Series'>Series</span></span>: <span table-translate='MONTH01'>January</span>, "
                if not pheader2.startswith(initial_pheader2):
                    print("PHEADER2 is not an annual series starting in January: %s" % repr(pheader2), file=error_file, flush=True)
                    error_count += 1
                    continue
                first_year: str = pheader2[len(initial_pheader2):len(initial_pheader2)+4]
                print("FIRST_YEAR: %s" % first_year, file=error_file, flush=True)


        p5471_key: str
        for p5471_key in sorted(p5471_map.keys()):
            kw.writemap({
                "node1": p5471_key,
                "label": "P5471",
                "node2": p5471_map[p5471_key]
                })

        label_key: str
        for label_key in sorted(label_map.keys()):
            kw.writemap({
                "node1": label_key,
                "label": "label",
                "node2": label_map[label_key]
                })

        kw.close()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

