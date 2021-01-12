"""
Extract specific statements from a Wikidata JSON file.
"""
import typing
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Extract specific statements from a Wikidata JSON file.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter

    parser.add_input_file()
    parser.add_output_file()
    
    parser.add_argument(
        "--find",
        action="store",
        type=str,
        dest="entity_ids",
        default=None,
        nargs="+",
        help='The entity IDs to find.')

    parser.add_argument(
        "--input-limit", "--limit",
        action="store",
        type=int,
        dest="input_limit",
        default=None,
        help='number of lines of input file to run on, default runs on all')

    parser.add_argument(
        "--output-limit",
        action="store",
        type=int,
        dest="output_limit",
        default=None,
        help='Limit the number of lines of output (default unlimited)')

    parser.add_argument(
        "--use-mgzip-for-input",
        nargs='?',
        type=optional_bool,
        dest="use_mgzip_for_input",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use the multithreaded gzip package, mgzip, for input. (default=%(default)s).")

    parser.add_argument(
        "--use-mgzip-for-output",
        nargs='?',
        type=optional_bool,
        dest="use_mgzip_for_output",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use the multithreaded gzip package, mgzip, for output. (default=%(default)s).")

    parser.add_argument(
        "--mgzip-threads-for-input",
        type=int,
        default=KgtkReaderOptions.MGZIP_THREAD_COUNT_DEFAULT,
        dest="mgzip_threads_for_input",
        help="The number of threads per mgzip input streama. (default=%(default)s).")

    parser.add_argument(
        "--mgzip-threads-for-output",
        type=int,
        default=KgtkWriter.MGZIP_THREAD_COUNT_DEFAULT,
        dest="mgzip_threads_for_output",
        help="The number of threads per mgzip output streama. (default=%(default)s).")

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        entity_ids: typing.List[str],
        input_limit: int,
        output_limit: int,
        use_mgzip_for_input: bool,
        use_mgzip_for_output: bool,
        mgzip_threads_for_input: int,
        mgzip_threads_for_output: int,
        ):

    import simplejson as json
    import sys

    in_path = KGTKArgumentParser.get_input_file(input_file)
    out_path = KGTKArgumentParser.get_output_file(output_file)

    from gzip import GzipFile
    print("Processing.", file=sys.stderr, flush=True)

    # Open the input file first to make it easier to monitor with "pv".
    input_f: typing.Union[GzipFile, typing.IO[typing.Any]]
    if str(in_path) == "-":
        print('Processing wikidata from standard input', file=sys.stderr, flush=True)
        # It is not well documented, but this is how you read binary data
        # from stdin in Python 3.
        input_f = sys.stdin.buffer

    else:
        print('Processing wikidata file %s' % str(in_path), file=sys.stderr, flush=True)
        input_f = open(in_path, mode='rb')
            
        if str(in_path).endswith(".bz2"):
            import bz2
            print('Decompressing (bz2)', file=sys.stderr, flush=True)
            # TODO: Optionally use a system decompression program.
            input_f = bz2.open(input_f)

        elif str(in_path).endswith(".gz"):
            # TODO: Optionally use a system decompression program.
            if use_mgzip_for_input:
                import mgzip
                print('Decompressing (mgzip)', file=sys.stderr, flush=True)
                input_f = mgzip.open(input_f, thread=mgzip_threads_for_input)
            else:
                import gzip
                print('Decompressing (gzip)', file=sys.stderr, flush=True)
                input_f = gzip.open(input_f)

    # Open the input file first to make it easier to monitor with "pv".
    output_f: typing.Union[GzipFile, typing.IO[typing.Any]]
    if str(out_path) == "-":
        print('Sending wikidata JSON to standatd output', file=sys.stderr, flush=True)
        # It is not well documented, but this is how you write binary data
        # from stdin in Python 3.
        output_f = sys.stdout.buffer

    else:
        print('Writing wikidata file %s' % str(out_path), file=sys.stderr, flush=True)
        output_f = open(out_path, mode='wb')
            
        if str(out_path).endswith(".bz2"):
            import bz2
            print('Compressing (bz2)', file=sys.stderr, flush=True)
            # TODO: Optionally use a system decompression program.
            output_f = bz2.open(output_f, "wb")

        elif str(out_path).endswith(".gz"):
            # TODO: Optionally use a compression program.
            if use_mgzip_for_output:
                import mgzip
                print('Compressing (mgzip)', file=sys.stderr, flush=True)
                output_f = mgzip.open(output_f, "wb", thread=mgzip_threads_for_output)
            else:
                import gzip
                print('Compressing (gzip)', file=sys.stderr, flush=True)
                output_f = gzip.open(output_f, "wb")

    entity_id_set: typing.Set[str] = set(entity_ids)

    output_count: int = 0
    input_count: int
    line: bytes
    for input_count, line in enumerate(input_f):
        if input_limit and input_count >= input_limit:
            break
        clean_line = line.strip()
        if clean_line.endswith(b","):
            clean_line = clean_line[:-1]
        if len(clean_line) > 1:
            obj = json.loads(clean_line)
            entity = obj["id"]
            if entity in entity_id_set:
                if output_count == 0:
                    output_f.write(b"[\n")
                else:
                    output_f.write(b",\n")
                output_f.write(clean_line)
                output_count += 1
                if output_limit is not None and output_count >= output_limit:
                    break
            
    print('Done processing {}'.format(str(in_path)), file=sys.stderr, flush=True)
    input_f.close()

    if output_count > 0:
        output_f.write(b"\n]\n")
    output_f.close()
   
    print('Wrote {} records'.format(output_count), file=sys.stderr, flush=True)
