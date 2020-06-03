"""
Generate wikidata triples from two a kgtk edge file

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
        "-pf",
        "--property-file",
        action="store",
        type=str,
        required = False,
        default="NONE",
        help="path to the file which contains the property datatype mapping in kgtk format.",
        dest="prop_file",
    )
    parser.add_argument(
        "-pd",
        "--property-declaration-in-file",
        action="store",
        type=str2bool,
        required = False,
        default=False,
        help="wehther read properties in the kgtk file. If set to yes, use `cat input.tsv input.tsv` to pipe the input file twice",
        dest="prop_declaration",
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


def run(
    labels: str,
    aliases: str,
    descriptions: str,
    prop_file: str,
    n: int,
    truthy: bool,
    warning: bool,
    use_gz: bool,
    use_id:bool,
    log_path:str,
    prop_declaration:bool,
):
    # import modules locally
    import gzip
    # from kgtk.triple_generator import TripleGenerator
    from kgtk.generator import TripleGenerator
    import sys

    generator = TripleGenerator(
        prop_file=prop_file,
        label_set=labels,
        alias_set=aliases,
        description_set=descriptions,
        n=n,
        warning=warning,
        truthy=truthy,
        use_id=use_id,
        dest_fp=sys.stdout,
        log_path = log_path,
        prop_declaration= prop_declaration,
    )

    # loop first round
    if use_gz:
        fp = gzip.open(sys.stdin.buffer, 'rt')
    else:
        fp = sys.stdin
        # not line by line
    
    if prop_declaration:
        file_lines = 0
        begining_edge = None
        start_generation = False
        for line_num, edge in enumerate(fp):
            if line_num == 0:
                begining_edge = edge
                generator.entry_point(line_num+1,edge)
                file_lines += 1
            else:
                if start_generation:
                    # start triple generation because reached the starting position of the second `cat`
                    line_num -= file_lines
                    # print("creating triples at line {} {} with total number of lines: {}".format(line_num+1, edge, file_lines))
                    generator.entry_point(line_num+1,edge) # file generator
                    # print("# {}".format(generator.read_num_of_lines))
                else:
                    if edge == begining_edge:
                        start_generation = True
                    else:
                        file_lines += 1
                        # print("creating property declarations at line {} {}".format(line_num, edge))
                        generator.read_prop_declaration(line_num+1,edge)
                    
        generator.finalize()
    else:
        for line_num, edge in enumerate(fp):
            if edge.startswith("#") or len(edge.strip("\n")) == 0:
                continue
            else:
                generator.entry_point(line_num+1,edge)
    
        generator.finalize()
