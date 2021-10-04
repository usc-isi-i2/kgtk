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
         auto_display_md: bool = os.getenv("KGTK_AUTO_DISPLAY_MD", "false").lower() in ["true", "yes", "y"],
         auto_display_json: bool = os.getenv("KGTK_AUTO_DISPLAY_JSON", "true").lower() in ["true", "yes", "y"],
         auto_display_html: bool = os.getenv("KGTK_AUTO_DISPLAY_HTML", "true").lower() in ["true", "yes", "y"],
         kgtk_command: str = os.getenv("KGTK_KGTK_COMMAND", "kgtk"),
         bash_command: str = os.getenv("KGTK_BASH_COMMAND", "bash"),
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
    
    This is an alternat method for specifying an input DataFrame.

    auto_display_md=True/False (default False)

    This parameter controls the processing of MarkDown output.  See below.

    auto_display_json=True/False (default True)

    This parameter controls the processing of JSON output.  See below.

    auto_display_html=True/False (default True)

    This parameter controls the processing of HTML output.  See below.

    kgtk_command=CMD (default 'kgtk')

    This parameter specifies the kgtk shell command.

    bash_command=CMD (default 'bash')

    This parameter specifies the name of the shell interpreter.

    Output Processing
    ====== =========

    If the output of the pipeline is MarkDown format (typically by ending the
    pipeline in `... / md` or `... /table`, identified as starting with `|`,
    the output will be printed.  However, if `auto_display_md=True` is passed
    in the `kgtk(...)` call, or if the envar `KGTK_AUTO_DISPLAY_MD` is set to
    `true`, then the MarkDown will be displayed using
    `display(Markdown(output))`.

    If the output of the pipeline is in JSON format (`--output-format JSON`),
    identified as starting with `[` or '{', the output will be displayed with
    `display(JSON(output))`.  However, if `kgtk(... auto_display_json=False)`
    or if the envar `KGTK_AUTO_DISPLAY_JSON` set to `false`, then the output
    will be printed.

    If the output of the pipeline is in HTML format (`--output-format HTML` or
    `kgtk("... /html")`), identified by starting with `<!DOCTYPE html>`, the
    output will be displayed with `display(HTML(output))`.  However, if
    `kgtk(... auto_display_json=False)` or if the envar
    `KGTK_AUTO_DISPLAY_HTML` set to `false`, then the output will be printed.

    If the output starts with anything other than `|`, `[`, or `<!DOCTYPE
    html>`, then the output is assumed to be in KGTK format.  It is converted
    to a Pandas DataFrame, which is returned to the caller.

    TODO: Capture standard error from the subprocess and print it on standard output.
    """

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
        if in_df is not Nont:
            raise ValueError("kgtk(): df= is not allowed when arg1 is a DataFrame")

    if len(pipeline) == 0:
        raise ValueError("kgtk(...): the pipeline is empty")
    pipeline = kgtk_command + " " + pipeline

    in_tsv: typing.Optional[str] = None
    if in_df is not None:
        in_tsv = in_df.to_csv(sep='\t',
                              index=False,
                              quoting=csv.QUOTE_NONNUMERIC,
                              quotechar='"',
                              doublequote=False,
                              escapechar='\\',
                              )

    outbuf: StringIO = StringIO()

    sh_bash = sh.Command(bash_command)
    sh_bash("-c", pipeline, _in=in_tsv, _out=outbuf, _err=sys.stderr)

    output: str = outbuf.getvalue()
    outbuf.close()

    # Decide what to do based on the start of the output:
    result: typing.Optional[pandas.DataFrame] = None
    if output.startswith("|"):
        if auto_display_md:
            display(Markdown(output))
        else:
            print(output)

    elif output.startswith("[") or output.startswith("{"):
        if auto_display_json:
            display(JSON(json.loads(output)))
        else:
            print(output)

    elif output.startswith("<!DOCTYPE html>"):
        if auto_display_html:
            display(HTML(output))
        else:
            print(output)

    else:
        result = pandas.read_csv(StringIO(output), sep='\t')

    return result
