from argparse import ArgumentParser, RawDescriptionHelpFormatter, Namespace
from functools import partial
from pathlib import Path
import typing

from kgtk.exceptions import KGTKArgumentParseException, KGTKSyntaxException


KGTKFiles = typing.Optional[typing.List[typing.Optional[Path]]]

class KGTKArgumentParser(ArgumentParser):
    SUPPORT_POSITIONAL_ARGS: bool = True
    DEFAULT_INPUT_FILE_HELP: str = "The KGTK input file"
    DEFAULT_OUTPUT_FILE_HELP: str = "The KGTK file to write"

    def __init__(self, *args, **kwargs):
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = RawDescriptionHelpFormatter

        self.shared_arguments = set()
        self.default_arguments = set()
        self.add_default_argument_funcs = {}

        super(KGTKArgumentParser, self).__init__(*args, **kwargs)

    def add_default_argument(self, *args, **kwargs):
        if 'dest' not in kwargs:
            raise KGTKSyntaxException('Default argument error: dest not defined')
        self.add_default_argument_funcs[kwargs['dest']] = partial(self.add_argument, *args, **kwargs)

    def accept_shared_argument(self, dest):
        self.shared_arguments.add(dest)

    def accept_default_argument(self, dest):
        # load default arguments
        self.add_default_argument_funcs[dest]()

    def exit(self, status=0, message=None):
        if status == 2:
            status = KGTKArgumentParseException.return_code
        super(KGTKArgumentParser, self).exit(status, message)

    def add_input_file(self,
                       dest: str,
                       positional: bool = False,
                       options: typing.List[str] = ["-i", "--input-file"],
                       help: typing.Optional[str] = None,
                       metavar: str = "INPUT_FILE",
                       nargs: str = "?",
                       default_stdin: bool = True
    ):

        if help is None:
            help = self.DEFAULT_INPUT_FILE_HELP
        if default_stdin:
            help += ". May be omitted or '-' for stdin."
        else:
            help += "."
            
        if positional and self.SUPPORT_POSITIONAL_ARGS:
            self.add_argument(dest, nargs=nargs, type=Path, help=help, metavar=metavar, action="append")

        self.add_argument(*options, dest=dest, nargs=nargs, type=Path, metavar=metavar, help=help, action="append")

    def add_output_file(self,
                        dest: str,
                        positional: bool = False,
                        options: typing.List[str] = ["-o", "--output-file"],
                        help: typing.Optional[str] = None,
                        metavar: str = "OUTPUT_FILE",
                        nargs: str = "?",
                        default_stdout: bool = True,
    ):

        if help is None:
            help = self.DEFAULT_OUTPUT_FILE_HELP
        if default_stdout:
            help += ". May be omitted or '-' for stdout."
        else:
            help += "."
            
        if positional and self.SUPPORT_POSITIONAL_ARGS:
            self.add_argument(dest, nargs=nargs, type=Path, help=help, metavar=metavar, action="append")

        self.add_argument(*options, dest=dest, nargs=nargs, type=Path, metavar=metavar, help=help, action="append")

    @classmethod
    def get_required_input_file(cls,
                                paths: KGTKFiles,
                                help: typing.Optional[str] = None,
                                default_stdin: bool = True,
                       
    )->Path:
    
        from kgtk.exceptions import KGTKException

        if help is None:
            help = cls.DEFAULT_INPUT_FILE_HELP

        if paths is None:
            if default_stdin:
                return Path("-")
            else:
                raise KGTKException("Please supply %s." % help)

        elif len(paths) == 0:
            if default_stdin:
                return Path("-")
            else:
                raise KGTKException("Please supply %s." % help)
        
        elif len(paths) == 1:
            if paths[0] is None:
                if default_stdin:
                    return Path("-")
                else:
                    raise KGTKException("Please supply %s." % help)
            return paths[0]
    
        elif len(paths) == 2 and paths[0] is not None and paths[1] is None:
            return paths[0]
        elif len(paths) == 2 and paths[0] is not None and paths[1] is not None:
            raise KGTKException("Duplicate input files:  '%s' and '%s'." % (str(paths[1]), str(paths[0])))
        else:
            raise KGTKException("Error: please supply %s" % help)

    @classmethod
    def get_optional_input_file(cls,
                                paths: KGTKFiles,
                                help: typing.Optional[str] = None,
                       
    )->typing.Optional[Path]:
    
        from kgtk.exceptions import KGTKException

        if help is None:
            help = cls.DEFAULT_INPUT_FILE_HELP

        if paths is None:
            return None

        elif len(paths) == 0:
            return None
        
        elif len(paths) == 1:
            return paths[0]
    
        elif len(paths) == 2 and paths[0] is not None and paths[1] is None:
            return paths[0]
        elif len(paths) == 2 and paths[0] is not None and paths[1] is not None:
            raise KGTKException("Duplicate input files:  '%s' and '%s'." % (str(paths[1]), str(paths[0])))
        else:
            raise KGTKException("Error: please supply %s" % help)

    @classmethod
    def get_required_output_file(cls,
                                 paths: typing.Optional[typing.List[typing.Optional[Path]]],
                                 help: typing.Optional[str] = None,
                                 default_stdout: bool = True,
    )->Path:
    
        from kgtk.exceptions import KGTKException

        if help is None:
            help = cls.DEFAULT_OUTPUT_FILE_HELP

        if paths is None:
            if default_stdout:
                return Path("-")
            else:
                raise KGTKException("Please supply %s." % help)
        
        elif len(paths) == 0:
            if default_stdout:
                return Path("-")
            else:
                raise KGTKException("Please supply %s." % help)
        
        elif len(paths) == 1:
            if paths[0] is None:
                if default_stdout:
                    return Path("-")
                else:
                    raise KGTKException("Please supply %s." % help)
            return paths[0]
    
        elif len(paths) == 2 and paths[0] is not None and paths[1] is None:
            return paths[0]
        elif len(paths) == 2 and paths[0] is not None and paths[1] is not None:
            raise KGTKException("Duplicate output files:  '%s' and '%s'." % (str(paths[1]), str(paths[0])))
        else:
            raise KGTKException("Error: please supply %s" % help)

    @classmethod
    def get_optional_output_file(cls,
                                 paths: typing.Optional[typing.List[typing.Optional[Path]]],
                                 help: typing.Optional[str] = None,
    )->typing.Optional[Path]:
    
        from kgtk.exceptions import KGTKException

        if help is None:
            help = cls.DEFAULT_OUTPUT_FILE_HELP

        if paths is None:
            return None
        
        elif len(paths) == 0:
            return None
        
        elif len(paths) == 1:
            return paths[0]
    
        elif len(paths) == 2 and paths[0] is not None and paths[1] is None:
            return paths[0]
        elif len(paths) == 2 and paths[0] is not None and paths[1] is not None:
            raise KGTKException("Duplicate output files:  '%s' and '%s'." % (str(paths[1]), str(paths[0])))
        else:
            raise KGTKException("Error: please supply %s" % help)

def add_shared_arguments(parser):
    # set shared arguments here
    # 1. no flag, only name (starts with two dashes: --XXX)
    # 2. need to have default value
    # 3. need to specify dest, which value starts with underscore
    # e.g., parser.add_argument('--debug', dest='_debug', action='store_true', default=False, help='enable debug mode')
    pass


def add_default_arguments(parser):
    # set default arguments here
    # need to specify dest
    # e.g., parser.add_default_argument('--save', dest='save', action='store', help='save to file')
    pass
