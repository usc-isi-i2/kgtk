"""This file defines the `kgtk(...)` function, which simplifies KGTK command
usage in JupyterLab.  The `kypher(...)` command is also defined for convenience.

Importing
=========


from kgtk.functions import kgtk, kypher

"""
import csv
from io import StringIO
from IPython.core.display import display, HTML, JSON, Markdown
import json
import os
import pandas
import sh
import sys
import typing

def kgtk(arg1: typing.Union[str, pandas.DataFrame],
         arg2: typing.Optional[str] = None,
         df: typing.Optional[pandas.DataFrame] = None,
         auto_display_html: typing.Optional[bool] = None,
         auto_display_json: typing.Optional[bool] = None,
         auto_display_md: typing.Optional[bool] = None,
         unquote_column_names: typing.Optional[bool] = None,
         bash_command: typing.Optional[str] = None,
         kgtk_command: typing.Optional[str] = None,
         )->typing.Optional[pandas.DataFrame]:
    """This function simplifies using KGTK commands in a Jupyter Lab environment.
    Invocation
    ==========

    kgtk("pipeline")

        Execute the command pipeline.  The results are printed, displayed, or
    returned as a Pandas DataFrame.

    kgtk(df, "pipeline")

        The `df` in the call is a Pandas DataFrame, which is converted to KGTK
    format and passed to the pipeline as standard input. The results are
    printed, displayed, or returned as a Pandas DataFrame.

    Optional Parameters
    ======== ==========

    df=DF (default None)
    
        This is an alternate method for specifying an input DataFrame.

    auto_display_html=True/False (default True)

        This parameter controls the processing of HTML output.  See below.

    auto_display_json=True/False (default True)

        This parameter controls the processing of JSON output.  See below.

    auto_display_md=True/False (default False)

        This parameter controls the processing of MarkDown output.  See below.

    unquote_column_names=True/False (default True)

        Convert string column names to symbols.

    bash_command=CMD (default 'bash')

        This parameter specifies the name of the shell interpreter.  If the
    envar KGTK_BASH_COMMAND is present, it will supply the default value for
    the name of the shell interpreter.

    kgtk_command=CMD (default 'kgtk')

        This parameter specifies the kgtk shell command.  If the envar
    KGTK_KGTK_COMMAND is present, it will supply the default value for the
    name of the `kgtk` command.

        One use for this feature is to redefine the `kgtk` command to include
    `time` as a prefix, and/or to include common options.

    Standard Output Processing
    ======== ====== =========

    If the standard output of the pipeline is in HTML format (`--output-format HTML` or
    `kgtk("... /html")`), identified by starting with `<!DOCTYPE html>`, the
    output will be displayed with `display(HTML(output))` by default.
    However, if `kgtk(... auto_display_json=False)` or if the envar
    `KGTK_AUTO_DISPLAY_HTML` set to `false`, then the output will be printed.

    If the standard output of the pipeline is in JSON format (`--output-format JSON`),
    identified as starting with `[` or '{', the output will be displayed with
    `display(JSON(output))` by default.  However, if
    `kgtk(... auto_display_json=False)` or if the envar
    `KGTK_AUTO_DISPLAY_JSON` set to `false`, then the output will be printed.

    If the standard output of the pipeline is MarkDown format (typically by
    ending the pipeline in `... / md` or `... /table`, identified as starting
    with `|`, the output will be printed by default.  However, if
    `auto_display_md=True` is passed in the `kgtk(...)` call, or if the envar
    `KGTK_AUTO_DISPLAY_MD` is set to `true`, then the MarkDown will be
    displayed using `display(Markdown(output))`.

    If the standard output of the pipeline begins with "usage:", then it is
    treated as output from `--help` and printed.

    If the standard output starts with anything other than the cases listed
    above, then the output is assumed to be in KGTK format.  It is converted
    to a Pandas DataFrame, which is returned to the caller.

    Error Output Processing
    ===== ====== ==========

    If standard output was printed or displayed, then any error output will be printed
    immediately after it.

    If standard output was convertd to a DataFrame and returned, and
    subsequently displayed by the iPython shell, then any error output will be
    printed before the DataFrame is displayed.

    Environment Variables
    =========== =========

    This module directly uses the following environment variables:

    KGTK_AUTO_DISPLAY_HTML
    KGTK_AUTO_DISPLAY_JSON
    KGTK_AUTO_DISPLAY_MD
    KGTK_UNQUOTE_COLUMN_NAMES
    KGTK_BASH_COMMAND
    KGTK_KGTK_COMMAND

    """

    # Important prefixes to look for in standard output:
    MD_SIGIL: str = "|"
    JSON_SIGIL: str = "["
    JSONL_MAP_SIGIL: str = "{"
    HTML_SIGIL: str = "<!DOCTYPE html>"
    USAGE_SIGIL: str = "usage:" # Output from `kgtk --help` or `kgtk command --help`
    GRAPH_CACHE_SIGIL: str = "Graph Cache" # Output from `kgtk query --show-cache`

    # Set the defaults:
    if auto_display_html is None:
        auto_display_html = os.getenv("KGTK_AUTO_DISPLAY_HTML", "true").lower() in ["true", "yes", "y"]
    if auto_display_json is None:
        auto_display_json = os.getenv("KGTK_AUTO_DISPLAY_JSON", "true").lower() in ["true", "yes", "y"]
    if auto_display_md is None:
        auto_display_md = os.getenv("KGTK_AUTO_DISPLAY_MD", "false").lower() in ["true", "yes", "y"]
    if unquote_column_names is None:
        unquote_column_names = os.getenv("KGTK_UNQUOTE_COLUMN_NAMES", "true").lower() in ["true", "yes", "y"]

    # Why not os.getenv("KGTK_BASH_COMMAND", "bash")? Splitting it up makes
    # mypy happier.
    if bash_command is None:
        bash_command = os.getenv("KGTK_BASH_COMMAND")
    if bash_command is None:
        bash_command = "bash"

    if kgtk_command is None:
        kgtk_command = os.getenv("KGTK_KGTK_COMMAND")
    if kgtk_command is None:
        kgtk_command = "kgtk"

    # Figure out the input DataFrame and pipeline arguments:
    in_df: typing.Optional[pandas.DataFrame] = None
    pipeline: str
    if isinstance(arg1, str):
        if arg2 is not None:
            raise ValueError("kgtk(arg1, arg2): arg2 is not allowed when arg1 is a string")
        pipeline = arg1
    elif isinstance(arg1, pandas.DataFrame):
        if arg2 is None:
            raise ValueError("kgtk(arg1, arg2): arg2 is required when arg1 is a DataFrame")
        in_df = arg1
        pipeline = arg2

    if df is not None:
        if in_df is not None:
            raise ValueError("kgtk(): df= is not allowed when arg1 is a DataFrame")
        in_df = df

    if len(pipeline) == 0:
        raise ValueError("kgtk(...): the pipeline is empty")
    pipeline = kgtk_command + " " + ' '.join(pipeline.splitlines())

    # If we were supplied an input DataFrame, convert it to KGTK format.
    #
    # TODO: The conversion should optionally escape internal `|` characters as `\|`.
    in_tsv: typing.Optional[str] = None
    if in_df is not None:
        in_tsv = in_df.to_csv(sep='\t',
                              index=False,
                              quoting=csv.QUOTE_NONNUMERIC,
                              quotechar='"',
                              doublequote=False,
                              escapechar='\\',
                              )
        if unquote_column_names:
            # Pandas will have treated the column names as strings and quoted
            # them.  By convention, KGTK column names are symbols.  So, we will
            # remove double quotes from the outside of each column name.
            #
            # TODO: Handle the troublesome case of a double quote inside a column
            # name.
            header, body = in_tsv.split('\n', 1)
            column_names = header.split('\t')
            column_names = [x[1:-1] if x.startswith('"') else x for x in column_names ]
            header = "\t".join(column_names)
            in_tsv = header + "\n" + body

    # Execute the KGTK command pipeline:
    outbuf: StringIO = StringIO()
    errbuf: StringIO = StringIO()

    try:
        sh_bash = sh.Command(bash_command)
        p = sh_bash("-c", pipeline, _in=in_tsv, _out=outbuf, _err=errbuf, _bg=True)
        try:
            p.wait()

        except KeyboardInterrupt:
            print("kgtk: received KeyboardInterrupt", file=sys.stderr, flush=True)
            try:
                p.terminate()
            except Exception:
                pass

    except sh.ErrorReturnCode as e:
        # The pipeline returned an error.  stderr should hav ean error message.
        errmsg: str = errbuf.getvalue()
        if len(errmsg) > 0:
            print(errbuf.getvalue())
        else:
            print(str(e))
        return None

    output: str = outbuf.getvalue()

    # Decide what to do based on the start of the output:
    result: typing.Optional[pandas.DataFrame] = None
    if len(output) == 0:
        pass # No standard output
    
    elif output.startswith(MD_SIGIL):
        # Process Markdown output.
        if auto_display_md:
            display(Markdown(output))
        else:
            print(output)

    elif output.startswith(JSON_SIGIL) or output.startswith(JSONL_MAP_SIGIL):
        # Process JSON output.
        if auto_display_json:
            display(JSON(json.loads(output)))
        else:
            print(output)

    elif output[:len(HTML_SIGIL)].casefold() == HTML_SIGIL.casefold():
        # Process HTML output.
        if auto_display_html:
            display(HTML(output))
        else:
            print(output)

    elif output[:len(USAGE_SIGIL)].casefold() == USAGE_SIGIL.casefold():
        # Process --help output.
        print(output)

    elif output[:len(GRAPH_CACHE_SIGIL)].casefold() == GRAPH_CACHE_SIGIL.casefold():
        # Process `kgtk query --show-cache` output.
        print(output)

    else:
        # Assume that anything else is KGTK formatted output.  Convert it to a
        # pandas DataFrame and return it.
        #
        # TODO: Test this conversion with all KTK datatypes.  Language-qualified
        # strings are problematic.  Check what happens to quantites, date/times,
        # and locations.
        #
        # TODO: Remove the escape character from internal `|` characters?
        # If we do that, should we detect KGTK lists and complain?
        # `\|` -> `|`
        outbuf.seek(0)
        result = pandas.read_csv(outbuf,
                                 sep='\t',
                                 quotechar='"',
                                 doublequote=False,
                                 escapechar='\\',
                                 )

    outbuf.close()

    # Any error messages? If so, print the at the end.
    errout: str = errbuf.getvalue()
    if len(errout) > 0:
        print(errout)

    return result

def kypher(arg1: typing.Union[str, pandas.DataFrame],
           arg2: typing.Optional[str] = None,
           df: typing.Optional[pandas.DataFrame] = None,
           auto_display_html: typing.Optional[bool] = None,
           auto_display_json: typing.Optional[bool] = None,
           auto_display_md: typing.Optional[bool] = None,
           bash_command: typing.Optional[str] = None,
           kgtk_command: typing.Optional[str] = None,
           )->typing.Optional[pandas.DataFrame]:
    """This function simplifies using kypher (`kgtk query` in a Jupyter Lab environment.

    Invocation
    ==========

    kypher("pipeline")

        Execute the command pipeline with "query " prepended.  The results are
    printed, displayed, or returned as a Pandas DataFrame.

    kypher(df, "pipeline")

        The `df` in the call is a Pandas DataFrame, which is converted to KGTK
    format and passed to the pipeline as standard input. "query " will be
    prepended to the pipeline. The results are printed, displayed, or returned
    as a Pandas DataFrame.

    Environment Variables
    =========== =========

    KGTK_GRAPH_CACHE

        `kgtk query` and other KGTK commands use this environment variable to
    supply the location of the graph cache when `--graph cache` is not
    supplied on the command line.  In the JupyterLab environment
    KGTK_GRAPH_CACHE may be set with:

    %env KGTK_GRAPH_CACHE=/path/to/file.sqlite3.db


    Additional Details
    ========== =======

    See the documentation for the `kgtk(...)` for additional details

    """

    # Figure out the input DataFrame and pipeline arguments:
    in_df: typing.Optional[pandas.DataFrame] = None
    pipeline: str
    if isinstance(arg1, str):
        if arg2 is not None:
            raise ValueError("kypher(arg1, arg2): arg2 is not allowed when arg1 is a string")
        pipeline = arg1
    elif isinstance(arg1, pandas.DataFrame):
        if arg2 is None:
            raise ValueError("kypher(arg1, arg2): arg2 is required when arg1 is a DataFrame")
        in_df = arg1
        pipeline = arg2

    if df is not None:
        if in_df is not None:
            raise ValueError("kypher(): df= is not allowed when arg1 is a DataFrame")
        in_df = df

    pipeline = "query " + pipeline

    return kgtk(pipeline,
                df=in_df,
                auto_display_html=auto_display_html,
                auto_display_json=auto_display_json,
                auto_display_md=auto_display_md,
                bash_command=bash_command,
                kgtk_command=kgtk_command,
                )
