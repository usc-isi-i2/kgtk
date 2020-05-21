import os
import sys
import io
import sh # type: ignore

from kgtk.exceptions import KGTKException
import kgtk.cli.zconcat as zcat


def parser():
    return {
        'help': 'Sort file based on one or more columns'
    }

def add_arguments(parser):
    parser.add_argument('-o', '--out', default=None, action='store', dest='output',
                        help='output file to write to, otherwise output goes to stdout')
    parser.add_argument('-c', '--column', '--columns', default='1', action='store', dest='columns',
                        help="comma-separated list of column names or numbers (1-based) to sort on, defaults to 1")
    parser.add_argument('-r', '--reverse', action='store_true', dest='reverse',
                        help="generate output in reverse sort order")
    parser.add_argument('--tsv', action='store_true', dest='tsv',
                        help="assume tab-separated input (default)")
    parser.add_argument('--csv', action='store_true', dest='csv',
                        help="assume comma-separated input (for non-KGTK files)")
    parser.add_argument('--space', action='store_true', dest='space',
                        help="space-optimized configuration for sorting large files")
    parser.add_argument('--speed', action='store_true', dest='speed',
                        help="speed-optimized configuration for sorting large files")
    parser.add_argument('-X', '--extra', default='', action='store', dest='extra',
                        help="extra options to supply to the sort program")
    parser.add_argument('-dt', '--datatype', default='tsv', action='store', dest='_dt',
                        help="Deprecated: datatype of the input file, e.g., tsv (default) or csv.")
    parser.add_argument('input', metavar='INPUT', nargs='?', action='store',
                        help="input file to sort, if empty or `-' process stdin")


# for now: these might require some more refinement:
space_config = '--compress-program=gzip'
speed_config = '--parallel=4'

column_spec_split_regex = '[, |\t]+'
reserved_name_columns = {
    'id': 1, 'ID': 1, 'node1': 1, 'from': 1, 'subject': 1,
    'label': 2, 'predicate': 2, 'property': 2, 'relation': 2, 'relationship': 2,
    'node2': 3, 'to': 3, 'object': 3,
}

def build_sort_key_spec(header, columns, colsep='\t'):
    """Given a KGTK file `header' line and a user-provided `columns' spec, generate a sequence of
    Unix sort key definitions representative of those columns.  For example, columns=subject,object
    will translate into '-k 1,1 -k 3,3'.  Columns can be specified by the names used in the file
    header line, as 1-based positions, or through the pre-defined positions of reserved names such
    as `subject', etc.  Columns found in the header will override any predefined positions.
    """
    import re
    columns = [c.strip() for c in re.split(column_spec_split_regex, columns.strip())]
    header = [c.strip() for c in header.split(colsep)]
    keys = []
    for col in columns:
        if col == '':
            continue
        index = None
        if col in header:
            index = header.index(col) + 1
        else:
            try:
                index = int(col)
            except:
                pass
        if index is None:
            index = reserved_name_columns.get(col)
        if index is None:
            raise KGTKException('Unknown column: ' + col)
        keys.append('-k %d,%d' % (index, index))
    # special whitespace at the end is used by `wait_for_key_spec' below:
    return ' '.join(keys) + ' \t'
    
def build_command(input=None, output=None, columns='1', colsep='\t', options='', _piped=False, _out_mode='wb'):
    """Build a sort sh command pipe for a single `input'.
    If `_piped' is True, configure the last command to ignore `output' and write to a pipe
    in which case this can be used to feed into the input of another command.
    `_out_mode' controls whether an `output' file will be truncated or appened to.
    """
    input = input or '-'
    output = (not _piped and (output or sys.stdout.buffer)) or None
    outfile = None
    if isinstance(output, str):
        outfile = open(output, _out_mode)
        output = outfile
    in_bufsize, out_bufsize = zcat.get_buf_sizes(output=None, _tty_out=False, _piped=True)

    # we unconditionally run zconcat, even if we have an explict input file, since we need to
    # handle optional compression on stdin, and we also need to split off and parse the header:
    sort_pipe = zcat.build_command_1(input, _piped=True)

    # extracting the column header: this is tricky for the case where input comes from stdin, since we
    # have to (optionally) uncompress, then capture the first line, then forward the rest of the input
    # to sort, but its arguments depend on what we find in the header line, so this requires some
    # inter-process communication between different stages in the sorting pipe:
    buffer = io.StringIO()
    catcmd = sh.cat.bake(_piped=True)
    if catcmd.__name__ == sort_pipe[-1].__name__:
        # last command of the pipe is a plain cat, use it instead:
        catcmd = sort_pipe[-1]
    else:
        sort_pipe.append(catcmd)
    # we use local environment vars to communicate the split-off header and sort keys:
    sort_env = os.environ.copy()
    sort_env['KGTK_HEADER'] = zcat.make_temp_file('kgtk-header.')
    sort_env['KGTK_SORT_KEY_SPEC'] = zcat.make_temp_file('kgtk-sort-key-spec.')

    # define these in here, so we can pass in some process-local variables via closures:
    def record_key_spec(chunk):
        # starting with sh 1.13 it looks like we can get either strings or bytes here;
        # if we get bytes we convert to an identical string using `latin1' encoding:
        if isinstance(chunk, bytes):
            chunk = chunk.decode('latin1')
        buffer.write(chunk)
        header = buffer.getvalue()
        eol = header.find('\n')
        if eol >= 0:
            with open(sort_env['KGTK_HEADER'], 'w') as out:
                out.write(header[0:eol+1])
            # reencode from latin1 to utf8 for header processing:
            header = header[0:eol].encode('latin1').decode(zcat.kgtk_encoding)
            with open(sort_env['KGTK_SORT_KEY_SPEC'], 'w') as out:
                out.write(build_sort_key_spec(header, columns, colsep))
            # this signals to ignore the callback once we are done collecting the header:
            return True

    # this waits as a precondition to sort so the header and key files will be available when it starts:
    def wait_for_key_spec():
        import time
        for i in range(100): # try for at most 5 secs:
            with open(sort_env['KGTK_SORT_KEY_SPEC'], 'r') as inp:
                if inp.read().endswith('\t'):
                    break
                time.sleep(0.05)
        else:
            raise KGTKException('INTERNAL ERROR: failed to communicate sort key')

    # baking in additional args creates a new command, so we have to update the pipe;
    # for some reason output callbacks don't work with _piped, so we use _bg instead:
    catcmd = catcmd.bake(_bg=True, _piped=False, _out=record_key_spec, _tee='out', _in_bufsize=in_bufsize, _out_bufsize=out_bufsize)
    sort_pipe[-1] = catcmd

    # rest of the pipeline: first skip header line, then sort, then add header back in:
    sort_pipe.append(
        sh.tail.bake('-n', '+2', _piped=True, _in_bufsize=in_bufsize, _out_bufsize=out_bufsize)
    )
    sort_pipe.append(
        sh.sh.bake('-c', """exec sort -t "%s" %s `cat $KGTK_SORT_KEY_SPEC`""" % (colsep, options),
                   _env=sort_env, _piped=True, _preexec_fn=wait_for_key_spec, _in_bufsize=in_bufsize, _out_bufsize=out_bufsize)
    )
    in_bufsize, out_bufsize = zcat.get_buf_sizes(output=output, _piped=_piped)
    cleanup = lambda cmd, status, exit_code: [sh.rm('-f', sort_env['KGTK_HEADER']), sh.rm('-f', sort_env['KGTK_SORT_KEY_SPEC'])]
    sort_pipe.append(
        sh.sh.bake('-c', """exec cat $KGTK_HEADER -""",
                   _env=sort_env, _out=output, _done=cleanup, _piped=_piped, _in_bufsize=in_bufsize, _out_bufsize=out_bufsize)
    )
    return sort_pipe


def run(input=None, output=None, columns='1', reverse=False, space=False, speed=False, extra='', tsv=False, csv=False, _dt=None):
    """Run sort according to the provided command-line arguments.
    """
    try:
        colsep = '\t'
        if not tsv and (csv or _dt == 'csv'):
            colsep = ','

        options = extra
        if reverse:
            options += ' -r'
        if space:
            options += ' ' + space_config
        elif speed:
            options += ' ' + speed_config
            
        pipe = build_command(input=input, output=output, columns=columns, colsep=colsep, options=options)
        return zcat.run_sh_commands(pipe).exit_code
    except sh.SignalException_SIGPIPE:
        # hack to work around Python3 issue when stdout is gone when we try to report an exception;
        # without this we get an ugly 'Exception ignored...' msg when we quit with head or a pager:
        sys.stdout = os.fdopen(1)
    except Exception as e:
        #import traceback
        #traceback.print_tb(sys.exc_info()[2], 10)
        raise KGTKException('INTERNAL ERROR: ' + type(e).__module__ + '.' + str(e) + '\n')

"""
# old mlr-based version:
def run(datatype, column, input): 
    sh.mlr('--%s' % datatype, 'sort', '-f', column, input, _out=sys.stdout, _err=sys.stderr)
"""

"""
# Examples:

> cat /tmp/nodes-v2-slice-shuf.tsv.gz | kgtk sort -c 'label, id' | head
id	label	type	descriptions	aliases	document_id
Q28415		item	'railway station'@en		wikidata-20200203
Q45582		item	'Polish literary award'@en		wikidata-20200203
Q45877		item	'television series'@en		wikidata-20200203
Q45886		item			wikidata-20200203
Q46028		item			wikidata-20200203
Q46103		item	'Wikimedia list article'@en		wikidata-20200203
Q46106		item	'Wikimedia list article'@en		wikidata-20200203
Q46430		item			wikidata-20200203
Q46473		item			wikidata-20200203


# uncompress & sort 9GB file from stdin in about 4 min on laptop (the -X option is just for illustration):

> date; cat nodes-v2.csv.gz | kgtk sort -c 'id, label' --speed -X ' -T /data/tmp' -o /tmp/nodes-v2-sorted.tsv; date
Wed 08 Apr 2020 07:25:46 PM PDT
Wed 08 Apr 2020 07:29:37 PM PDT

> ls -l /tmp/nodes-v2-sorted.tsv
-rw-r--r-- 1 hans isdstaff 8918052340 Apr  8 19:29 /tmp/nodes-v2-sorted.tsv

> head -3 /tmp/nodes-v2-sorted.tsv
id	label	type	descriptions	aliases	document_id
P10	'video'@en	property	'relevant video. For images, use the property P18. For film trailers, qualify with 'object has role' (P3831)='trailer' (Q622550)'@en	'media'@en|'animation'@en|'gif'@en|'trailer (Commons)'@en	wikidata-20200203
P1000	'record held'@en	property	'notable record achieved by a person or entity, include qualifiers for dates held'@en		wikidata-20200203
"""
