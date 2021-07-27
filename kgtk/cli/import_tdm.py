"""
Convert one ore more TDM JSON files to a KGTK file.

The TDM (Trade Data Monitor) data i a JSON file downloaded from
a query for a specific country and its major trading partners.
The query must specify an annual time series (where each year starts
in January).

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

    # Wikidata codes (we should have a file from which to import these):
    wikidata_P17: str = "P17" # Country
    wikidata_P248: str = "P248" # Stated in
    wikidata_P585: str = "P585" # Point in time
    wikidata_P5471: str = "P5471" # Harmonized System Code
    wikidata_Q4917: str = "Q4917" # United States dollar amount
    wikidata_Q97355106: str = "Q97355106" # Trade Data Monitor

    # Define the amount columns in the input JSON file and their offsets from
    # the base year.
    vcols: typing.Mapping[str, int] = {
        "V1": 0,
        "V2": 1,
        "V3": 2,
        "V4": 3,
        "V5": 4,
        "V6": 5,
        "V7": 6,
        "V8": 7,
        "V9": 8,
    }

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
        oc: typing.List[str] = ["id",
                                "node1",
                                "label",
                                "node2",
                                wikidata_P17,
                                wikidata_P585,
                                "PTDMmonetary_value",
                                wikidata_P248]

        harmonized_system_code_map: typing.MutableMapping[str, str] = dict()
        label_map: typing.MutableMapping[str, str] = dict()

        # Create the ID builder:
        idb: KgtkIdBuilder = KgtkIdBuilder.from_column_names(oc, idbuilder_options)

        kw: KgtkWriter = KgtkWriter.open(idb.column_names,
                                         output_file_path,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        error_count: int = 0

        file_number: int = 0
        input_file_path: Path
        for input_file_path in input_file_paths:
            file_number += 1
            if verbose:
                print("File %d: processing %s" % (file_number, repr(str(input_file_path))), file=error_file, flush=True)

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
            if len(source_iso_code) != 2:
                # The source ISO code must be two characters wide.
                print("Incorrect length for ISO code: %s" % repr(source_iso_code), file=error_file, flush=True)
                error_count += 1
                continue

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
            harmonized_system_code_map[node2] = KgtkFormat.stringify(hs_code)
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

            # Next, extract the year for the first column.  We will use this value as
            # we parse the columnar data.
            first_year_str: str = pheader2[len(initial_pheader2):len(initial_pheader2)+4]
            # print("FIRST_YEAR: %s" % first_year, file=error_file, flush=True)
            first_year: int = int(first_year_str)

            # Locate the data records:
            if "DATA" not in tdm:
                print("DATA not found", file=error_file, flush=True)
                error_count += 1
                continue
            data_list: typing.List[dict] = tdm["DATA"]

            partner_country_count: int = 0
            cells_imported_count: int = 0

            # Process each data entry.
            data_entry: dict
            for data_entry in data_list:
                # Look for the trading partner country:
                if "COL2" not in data_entry:
                    print("COL2 not found in DATA entry.", file=error_file, flush=True)
                    error_count += 1
                    continue
                partner_country_name: str = data_entry["COL2"]

                # Skip the "_World" entry:
                if partner_country_name == "_World":
                    continue

                partner_country_count += 1

                # Create a Q node for the trading partner country:
                p17_value: str = "QTDM_country_" + partner_country_name.replace(" ", "_")
                label_map[p17_value] = KgtkFormat.stringify(partner_country_name, language="en")

                # Verify that the unit of measure is US Dollars:
                if "UOM" not in data_entry:
                    print("UOM not found in DATA entry", file=error_file, flush=True)
                    error_count += 1
                    continue

                if data_entry["UOM"] != "USD":
                    print("UOM %s is not USD" % data_entry["UOM"], file=error_file, flush=True)
                    error_count += 1
                    continue

                vstr: str
                offset: int
                for vstr, offset in vcols.items():
                    if vstr not in data_entry:
                        continue
                    amountstr: str = data_entry[vstr]
                    ptdmmonetary_value: str = amountstr + wikidata_Q4917 # Build a KGTK quantity.
                    p585_value: str = KgtkFormat.year(first_year + offset) # Build a KGTK date and times string.

                    newrow: typing.List[str] = [ "", node1, label, node2, p17_value, p585_value, ptdmmonetary_value, wikidata_Q97355106 ]
                    kw.write(idb.build(newrow, file_number))
                    cells_imported_count += 1

            if verbose:
                print("%d trading partners processed, %d cells imported." % (partner_country_count, cells_imported_count), file=error_file, flush=True)

        # Dump the harmonized system codes we encountered:
        if verbose:
            print("%d harmonized system codes processed" % len(harmonized_system_code_map), file=error_file, flush=True)
        p5471_key: str
        for hsc_key in sorted(harmonized_system_code_map.keys()):
            hsc_row: typing.List[str] = [ "", hsc_key, wikidata_P5471, harmonized_system_code_map[hsc_key], "", "", "", "" ]
            kw.write(idb.build(hsc_row, file_number))

        # Dump the labels we encountered:
        if verbose:
            print("%d labels processed" % len(label_map), file=error_file, flush=True)
        label_key: str
        for label_key in sorted(label_map.keys()):
            label_row: typing.List[str] = [ "", label_key, "label", label_map[label_key],  "", "", "", "" ]
            kw.write(idb.build(label_row, file_number))

        kw.close()

        if error_count > 0:
            print("%d errors encountered" % error_count, file=error_file, flush=True)

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

