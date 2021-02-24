"""
Generate wikidata triples from two a kgtk edge file

"""
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        "help": "Generates wikidata triples from kgtk file",
        "description": "Generating Wikidata triples.",
    }


def add_arguments_extended(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
        prop_file: str, labelSet: str, aliasSet: str, descriptionSet: str, n: str, dest: Any  --output-n-lines --generate-truthy
    """
    from kgtk.utils.argparsehelpers import optional_bool

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
        required=False,
        default="alias",
        help="alias identifiers which will create labels, separated by comma','.",
        dest="aliases",
    )
    parser.add_argument(
        "-dp",
        "--description-property",
        action="store",
        type=str,
        required=False,
        default="description",
        help="description identifiers which will create labels, separated by comma','.",
        dest="descriptions",
    )
    parser.add_argument(
        "-pf",
        "--property-file",
        action="store",
        type=str,
        required=False,
        default=None,
        help="path to the file which contains the property datatype mapping in kgtk format.",
        dest="property_file",
    )
    parser.add_argument(
        "-pd",
        "--property-declaration-in-file",
        dest="prop_declaration",
        metavar="True|False",
        help="whether read properties in the kgtk file. If set to yes, use `cat input.tsv input.tsv` to pipe the input file twice",
        type=optional_bool,
        nargs='?',
        const=True,
        default=False
    )
    parser.add_argument(
        "-n",
        "--output-n-lines",
        action="store",
        type=int,
        required=False,
        default=1000,
        help="output triples approximately every {n} lines of reading stdin.",
        dest="n",
    )
    parser.add_argument(
        "-gt",
        "--generate-truthy",
        type=optional_bool,
        const=True,
        metavar="True|False",
        default=True,
        help="the default is to not generate truthy triples. Specify this option to generate truthy triples.",
        dest="truthy",
    )
    parser.add_argument(
        "-w",
        "--warning",
        const=True,
        type=optional_bool,
        default=False,
        metavar="True|False",
        help="if specified, "
             "warn various kinds of exceptions and mistakes and log them to a log file with line number in input file, "
             "rather than stopping. logging",
        dest="warning",
    )
    parser.add_argument(
        "-gz",
        "--use-gz",
        const=True,
        type=optional_bool,
        metavar="True|False",
        default=False,
        help="if set to yes, read from compressed gz file",
        dest="use_gz",
    )
    parser.add_argument(
        "-sid",
        "--use-id",
        const=True,
        type=optional_bool,
        metavar="True|False",
        default=False,
        help="if set to yes, the id in the edge will be used as statement id when creating statement or truthy statement",
        dest="use_id",
    )
    parser.add_argument(
        "-log",
        "--log-path",
        action="store",
        type=str,
        required=False,
        default="warning.log",
        help="set the path of the log file",
        dest="log_path",
    )
    parser.add_argument(
        "-prefix",
        "--prefix-path",
        action="store",
        type=str,
        required=False,
        default="NONE",
        help="set the path of the prefix kgtk file that provides customized uri prefix binding",
        dest="prefix_path",
    )
    parser.add_argument(
        "--error-action",
        action="store",
        type=str,
        required=False,
        default="log",
        help="Defines the command behavior in case there are errors in execution, [log|raise]. "
             "'log': log the errors to a log file and continue,  'raise': raise exception and quit. Default: 'log'",
        dest="error_action",
    )
    parser.add_input_file(positional=True)
    parser.add_output_file(
        who="Output triples file path.",
        allow_list=False, dest="output_file")


def run(
        labels: str,
        aliases: str,
        descriptions: str,
        property_file: str,
        n: int,
        truthy: bool,
        warning: bool,
        use_id: bool,
        log_path: str,
        prop_declaration: bool,
        prefix_path: str,
        input_file: KGTKFiles,
        output_file: str,
        error_action: str
):
    # import modules locally

    from kgtk.generator import TripleGenerator
    from kgtk.exceptions import KGTKException

    generator = TripleGenerator(
        prop_file=property_file,
        label_set=labels,
        alias_set=aliases,
        description_set=descriptions,
        n=n,
        warning=warning,
        truthy=truthy,
        use_id=use_id,
        dest_fp=output_file,
        log_path=log_path,
        prop_declaration=prop_declaration,
        prefix_path=prefix_path,
        input_file=input_file,
        error_action=error_action
    )

    try:
        generator.process()
    except Exception as e:
        raise KGTKException(e)
