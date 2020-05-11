"""
Generate mediawiki API json files from kgtk file

This command line tool will create three json files. Each will mimic the return of the following media wiki API for each entity existed in the kgtk file.

"""

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
        "description": "Generating json files that mimic mediawiki *wbgetentities* api call response.",
    }

def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
        prop_file: str, labelSet: str, aliasSet: str, descriptionSet: str, n: str, dest: Any  --output-n-lines --generate-truthy
    """
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
        "-gz",
        "--use-gz",
        action="store",
        type=str2bool,
        required = False,
        default="no",
        help="if set to yes, read from compressed gz file",
        dest="use_gz",
    )


def run(
    prop_file:str = prop_file,
    use_gz:bool = use_gz
):
    # import modules locally
    from kgtk.json_generator import JsonGenerator
    import sys
    import gzip
    generator = JsonGenerator(
        prop_file=prop_file,
        use_gz = use_gz
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
