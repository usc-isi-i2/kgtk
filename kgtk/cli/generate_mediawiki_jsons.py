"""
Generate mediawiki API json files from kgtk file

This command line tool will create three json files. Each will mimic the return of the following media wiki API for each entity existed in the kgtk file. 

"""

from argparse import Namespace, SUPPRESS
import typing
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def str2bool(v):
    import argparse
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        "help": "Generates mediawiki json responses from kgtk file",
        "description": "Generating json files that mimic mediawiki *wbgetentities* api call response. This tool assumes statements and qualifiers related to one entity will be bundled close as the `generate-wikidata-triples` function assumes. If this requirement is not met, please set `n` to a number LARGER than the total number of entities in the kgtk file",
    }

def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
        prop_file: str
    """
    from kgtk.utils.argparsehelpers import optional_bool

    # parser.add_argument(
    #    "-i",
    #    "--input-file",
    #    action="store",
    #    type=str,
    #    required = False,
    #    default="",
    #    help="set the path of the input kgtk file if not from standard input",
    #    dest="input_file",
    #)
    parser.add_input_file()

    # parser.add_argument(
    #    "-pf",
    #    "--property-file",
    #     action="store",
    #     type=str,
    #     required = False,
    #     default="NONE",
    #     help="path to the file which contains the property datatype mapping in kgtk format.",
    #     dest="prop_file",
    # )
    parser.add_input_file(who="the file which contains the property datatype mapping in kgtk format",
                          options=["-pf", "--property-file"],
                          dest="prop_file",
                          metavar="PROPERTY_FILE",
                          optional=True,
    )

    parser.add_argument(
        "-lp",
        "--label-property",
        action="store",
        type=str,
        default="label",
        required=False,
        help="property identifiers which will create labels, separated by comma','.",
        dest="labels",
    )
    parser.add_argument(
        "-ap",
        "--alias-property",
        action="store",
        type=str,
        required = False,
        default="alias",
        help="alias identifiers which will create labels, separated by comma','.",
        dest="aliases",
    )
    parser.add_argument(
        "-dp",
        "--description-property",
        action="store",
        type=str,
        required = False,
        default="description",
        help="description identifiers which will create labels, separated by comma','.",
        dest="descriptions",
    )
    parser.add_argument(
        "-pd",
        "--property-declaration-in-file",
        action="store",
        type=str2bool,
        required = False,
        default=False,
        help="whether to read properties from the input kgtk file. If set to yes, make sure the property declaration happens before its usage.  default=%(default)s",
        dest="prop_declaration",
    )
    parser.add_argument(
        "-pr",
        "--output-file-prefix",
        action="store",
        type=str,
        default = "kgtk",
        required = False,
        help="set the prefix of the output files. Default to `kgtk`",
        dest="output_prefix",
    )
    parser.add_argument(
        "-n",
        "--output-n-lines",
        action="store",
        type=int,
        required = False,
        default=1000,
        help="output json file when the corresponding dictionary size reaches n. Default to 1000",
        dest="n",
    )
    parser.add_argument(
        "-log",
        "--log-path",
        action="store",
        type=str,
        required = False,
        default="warning.log",
        help="set the path of the log file",
        dest="log_path",
    )
    parser.add_argument(
        "-w",
        "--warning",
        action="store",
        type=str2bool,
        required = False,
        default="no",
        help="if set to yes, warn various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping. logging",
        dest="warning",
    )
    parser.add_argument(
        "-r",
        "--rank",
        action="store",
        type=bool,
        required = False,
        default=False,
        help="Whether the input file contains a rank column. Please refer to the `import_wikidata` command for the header information. Default to False, then all the ranks will be `normal`, therefore `NormalRank`.",
        dest="has_rank",
    )
    parser.add_argument(
        "--error-action",
        action="store",
        type=str,
        required = False,
        default="log",
        choices=['ignore', 'log', 'raise'],
        help="When errors occur, either ignore them ('ignore'), log them (`log`), or raise an exception (`raise`). Default='%(default)s'.",
        dest="error_action",
    )
    parser.add_argument(
        "-pl",
        "--property-declaration-label",
        action="store",
        type=str,
        required=False,
        default="data_type",
        help="The edge label in a property file that indicates a property declaration. default='%(default)s'",
        dest="property_declaration_label",
    )

    parser.add_argument(
        "-fp",
        "--filter-prop-file",
        dest="filter_prop_file",
        help="If true and a property file has been specified, filter the prop file, processing only edges with the property declaration label. (default=%(default)s)",
        type=optional_bool, nargs='?', const=True, default=True, metavar="True/False",
    )

    parser.add_argument(
        "-ip",
        "--ignore-property-declarations-in-file",
        dest="ignore_property_declarations_in_file",
        help="If true, ignore input edges with the property declaration label. (default=%(default)s)",
        type=optional_bool, nargs='?', const=True, default=True, metavar="True/False",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="If true, provide additional feedback. (default=%(default)s)",
        type=optional_bool, nargs='?', const=True, default=False, metavar="True/False",
    )

def run(
    input_file: KGTKFiles,
    prop_file: KGTKFiles,

    labels: str,
    aliases: str,
    descriptions: str,
    prop_declaration:bool,
    output_prefix: str,
    n: int,
    log_path: str,
    warning: bool,
    has_rank:bool,
    error_action: str,
    property_declaration_label: str,
    ignore_property_declarations_in_file: bool,
    filter_prop_file: bool,
    verbose: bool,
):
    # import modules locally
    from pathlib import Path
    from kgtk.generator import JsonGenerator
    import sys
    import gzip
    from kgtk.exceptions import KGTKException
    
    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    prop_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_input_file(prop_file, who="KGTK prop file")

    generator = JsonGenerator(
        input_file = input_kgtk_file,
        prop_file=prop_kgtk_file,
        label_set=labels,
        alias_set=aliases,
        description_set=descriptions,
        output_prefix = output_prefix,
        n = n,
        log_path = log_path,
        warning = warning,
        prop_declaration = prop_declaration,
        has_rank = has_rank,
        error_action = error_action,
        property_declaration_label=property_declaration_label,
        ignore_property_declarations_in_file = ignore_property_declarations_in_file,
        filter_prop_file = filter_prop_file,
        verbose = verbose,
    )
    generator.process()
