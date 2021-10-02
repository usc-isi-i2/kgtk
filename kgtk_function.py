import csv
from io import StringIO
from IPython.core.display import display, HTML, JSON
import pandas
import sh
import typing

def kgtk(arg1: typing.Union[str, pandas.DataFrame],
         arg2: typing.Optional[str],
         df: typing.Optional[pandas.DataFrame] = None,
         bash_command: str = "bash",
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
    sh_bash("-c", cmd, _in=in_tsv, _out=outbuf, _err=sys.stderr)

    output: str = outbuf.get_value()
    outbuf.close()

    # Decide what to do based on the start of the output:
    if output.startswith("|"):
        display(output)
        return None

    elif output.startswith("["):
        display(JSON(output))
        return None

    elif output.startswith("<!DOCTYPE html>"):
        display(HTML(output))
        return None

    else:
        return pandas.DataFrame(output, sep='\t')
    
