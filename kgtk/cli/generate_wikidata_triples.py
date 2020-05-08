"""
Generate wikidata triples from two edge files:
1. A statement and qualifier edge file that contains an edge id, node1, label, and node2
2. A kgtk file that contains the mapping information from property identifier to its datatype

"""

def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        "help": "Generates wikidata triples from kgtk file",
        "description": "Generating Wikidata triples.",
    }
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


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
        prop_file: str, labelSet: str, aliasSet: str, descriptionSet: str, n: str, dest: Any  --output-n-lines --generate-truthy
    """
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
        default="aliases",
        help="alias identifiers which will create labels, separated by comma','.",
        dest="aliases",
    )
    parser.add_argument(
        "-dp",
        "--description-property",
        action="store",
        type=str,
        required = False,
        default="descriptions",
        help="description identifiers which will create labels, separated by comma','.",
        dest="descriptions",
    )
    parser.add_argument(
        "-pf",
        "--property-types",
        action="store",
        type=str,
        required = True,
        help="path to the file which contains the property datatype mapping in kgtk format.",
        dest="prop_file",
    )
    parser.add_argument(
        "-n",
        "--output-n-lines",
        action="store",
        type=int,
        required = False,
        default=1000,
        help="output triples approximately every {n} lines of reading stdin.",
        dest="n",
    )
    parser.add_argument(
        "-gt",
        "--generate-truthy",
        action="store",
        type=str2bool,
        required = False,
        default="yes",
        help="the default is to not generate truthy triples. Specify this option to generate truthy triples.",
        dest="truthy",
    )
    parser.add_argument(
        "-ig",
        "--ignore",
        action="store",
        type=str2bool,
        required = False,
        default="no",
        help="if set to yes, ignore various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping. logging",
        dest="ignore",
    )
    parser.add_argument(
        "-gz",
        "--use-gz",
        action="store",
        type=str2bool,
        required = False,
        default="no",
        help="if set to yes, read from compressed gz file",
        dest="use_gz",
    )
    parser.add_argument(
        "-sid",
        "--use-id",
        action="store",
        type=str2bool,
        required = False,
        default="no",
        help="if set to yes, the id in the edge will be used as statement id when creating statement or truthy statement",
        dest="use_id",
    )


def run(
    labels: str,
    aliases: str,
    descriptions: str,
    prop_file: str,
    n: int,
    truthy: bool,
    ignore: bool,
    use_gz: bool,
    use_id:bool
):
    # import modules locally
    import gzip
    from kgtk.triple_generator import TripleGenerator
    import sys
    generator = TripleGenerator(
        prop_file=prop_file,
        label_set=labels,
        alias_set=aliases,
        description_set=descriptions,
        n=n,
        ignore=ignore,
        truthy=truthy,
        use_id=use_id
    )
    # process stdin
    if use_gz:
        fp = gzip.open(sys.stdin.buffer, 'rt')
    else:
        fp = sys.stdin
        # not line by line
    for line_num, edge in enumerate(fp):
        if edge.startswith("#"):
            continue
        else:
            generator.entry_point(line_num+1,edge)
    generator.finalize()
