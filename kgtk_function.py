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
         auto_display_md: bool = os.getenv("KGTK_AUTO_DISPLAY_MD", "false").lower in ["true", "yes", "y"],
         auto_display_json: bool = os.getenv("KGTK_AUTO_DISPLAY_JSON", "true").lower in ["true", "yes", "y"],
         auto_display_html: bool = os.getenv("KGTK_AUTO_DISPLAY_HTML", "true").lower in ["true", "yes", "y"],
         kgtk_command: str = os.getenv("KGTK_KGTK_COMMAND", "kgtk"),
         bash_command: str = os.getenv("KGTK_BASH_COMMAND", "bash"),
         )->typing.Optional[pandas.DataFrame]:
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
    sh_bash("-c", kgtk_command + " " + pipeline, _in=in_tsv, _out=outbuf, _err=sys.stderr)

    output: str = outbuf.getvalue()
    outbuf.close()

    # Decide what to do based on the start of the output:
    result: typing.Optional[pandas.DataFrame] = None
    if output.startswith("|"):
        if auto_display_md:
            display(Markdown(output))
        else:
            print(output)

    elif output.startswith("["):
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
