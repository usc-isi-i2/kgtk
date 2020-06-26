from argparse import ArgumentParser, RawDescriptionHelpFormatter, Namespace
from functools import partial
from pathlib import Path
import typing

from kgtk.exceptions import KGTKArgumentParseException, KGTKSyntaxException


KGTKFiles = typing.Optional[typing.Union[Path,
                                         typing.List[typing.Union[typing.Optional[Path],
                                                                  typing.List[Path]]]]]

class KGTKArgumentParser(ArgumentParser):
    SUPPORT_POSITIONAL_ARGS: bool = True
    DEFAULT_INPUT_FILE_WHO: str = "KGTK input file"
    DEFAULT_OUTPUT_FILE_WHO: str = "KGTK output file"

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

    def add_file(self,
                 who: typing.Optional[str],
                 dest: str,
                 options: typing.List[str],
                 metavar: str,
                 optional: bool,
                 allow_list: bool,
                 positional: bool,
                 default_help: str,
                 stdio_name: str,
    ):

        if optional:
            # Not required, no default. Positional output not allowed, lists not allowed.
            self.add_argument(*options, dest=dest, type=Path, metavar=metavar, help=who)

        # This is a required file, defaulting to stdio.
        helpstr: str
        if who is None:
            helpstr = "The " + default_help + "."
        else:
            helpstr = who
        helpstr += " (May be omitted or '-' for %s.)" % stdio_name
            
        positional &= self.SUPPORT_POSITIONAL_ARGS

        if allow_list:
            if positional:
                self.add_argument(dest, nargs="*", type=Path, help=helpstr, metavar=metavar, action="append")
                self.add_argument(*options, dest=dest, nargs="+", type=Path, metavar=metavar, help=helpstr, action="append")
            else:
                self.add_argument(*options, dest=dest, nargs="+", type=Path, metavar=metavar, help=helpstr, default=[Path("-")])

        else:
            if positional:
                self.add_argument(dest, nargs="?", type=Path, help=helpstr, metavar=metavar, action="append")
                self.add_argument(*options, dest=dest, type=Path, metavar=metavar, help=helpstr, action="append")
            else:
                self.add_argument(*options, dest=dest, type=Path, metavar=metavar, help=helpstr, default=Path("-"))


    def add_input_file(self,
                       who: typing.Optional[str] = None,
                       dest: str = "input_file",
                       options: typing.List[str] = ["-i", "--input-file"],
                       metavar: str = "INPUT_FILE",
                       optional: bool = False,
                       allow_list: bool = False,
                       positional: bool = False,
    ):

        return self.add_file(who, dest, options, metavar, optional, allow_list, positional, self.DEFAULT_INPUT_FILE_WHO, "stdin")

    def add_output_file(self,
                       who: typing.Optional[str] = None,
                       dest: str = "output_file",
                       options: typing.List[str] = ["-o", "--output-file"],
                       metavar: str = "OUTPUT_FILE",
                       optional: bool = False,
                       allow_list: bool = False,
                       positional: bool = False,
    ):
        return self.add_file(who, dest, options, metavar, optional, allow_list, positional, self.DEFAULT_OUTPUT_FILE_WHO, "stdout")

    @classmethod
    def get_path_list(cls, paths: KGTKFiles, who: str, default_stdio: bool = False)->typing.List[Path]:
        # Builds a list of paths from the awkward possible returns from argument parsing.
        if paths is None:
            if default_stdio:
                return [ Path("-") ]
            else:
                return [ ]
        elif isinstance(paths, Path):
            return [ paths ]
        elif isinstance(paths, list):
            result: typng.List[Path] = [ ]
            pl: typing.Union[typing.Optional[Path], typing.List[Path]]
            for pl in paths:
                if pl is None:
                    continue
                if isinstance(pl, Path):
                    result.append(pl)
                elif isinstance(pl, List):
                    result.extend(pl)
                else:
                    raise KGTKException("%s: Unexpected component '%s' in path list '%s'." % (who, str(pl), str(paths)))
            if len(result) == 0 and default_stdio:
                return [ Path("-") ]
            else:
                return result
        else:
            raise KGTKException("%s: Unexpected path list '%s'." % (who, str(paths)))

    @classmethod
    def get_input_file(cls,
                       paths: KGTKFiles,
                       who: typing.Optional[str] = None,
                       default_stdin: bool = True,
                       
    )->Path:
    
        from kgtk.exceptions import KGTKException

        if who is None:
            who = cls.DEFAULT_INPUT_FILE_WHO

        p: typing.List[Path] = cls.get_path_list(paths, who, default_stdio=default_stdin)
        if len(p) == 1:
            return p[0]
        elif len(p) == 0:
            raise KGTKException("%s: Please supply a filename path." % who)
        else:
            raise KGTKException("%s: Too many files: '%s'" % (who, str(paths)))

                                
    @classmethod
    def get_optional_input_file(cls,
                                paths: KGTKFiles,
                                who: typing.Optional[str] = None,
                       
    )->typing.Optional[Path]:
    
        from kgtk.exceptions import KGTKException

        if who is None:
            who = cls.DEFAULT_INPUT_FILE_WHO

        p: typing.List[Path] = cls.get_path_list(paths, who, default_stdio=False)
        if len(p) == 0:
            return None                                
        elif len(p) == 1:
            return p[0]
        else:
            raise KGTKException("%s: Too many files: '%s'" % (who, str(paths)))

    @classmethod
    def get_input_file_list(cls,
                            paths: KGTKFiles,
                            who: typing.Optional[str] = None,
                            default_stdin: bool = True,
                       
    )->typing.List[Path]:
    
        from kgtk.exceptions import KGTKException

        if who is None:
            who = cls.DEFAULT_INPUT_FILE_WHO

        return cls.get_path_list(paths, who, default_stdio=default_stdin)


    @classmethod
    def get_output_file(cls,
                       paths: KGTKFiles,
                       who: typing.Optional[str] = None,
                       default_stdin: bool = True,
                       
    )->Path:
    
        from kgtk.exceptions import KGTKException

        if who is None:
            who = cls.DEFAULT_OUTPUT_FILE_WHO

        p: typing.List[Path] = cls.get_path_list(paths, who, default_stdio=default_stdin)
        if len(p) == 1:
            return p[0]
        elif len(p) == 0:
            raise KGTKException("%s: Please supply a filename path." % who)
        else:
            raise KGTKException("%s: Too many files: '%s'" % (who, str(paths)))

                                
    @classmethod
    def get_optional_output_file(cls,
                                paths: KGTKFiles,
                                who: typing.Optional[str] = None,
                       
    )->typing.Optional[Path]:
    
        from kgtk.exceptions import KGTKException

        if who is None:
            who = cls.DEFAULT_OUTPUT_FILE_WHO

        p: typing.List[Path] = cls.get_path_list(paths, who, default_stdio=False)
        if len(p) == 0:
            return None                                
        elif len(p) == 1:
            return p[0]
        else:
            raise KGTKException("%s: Too many files: '%s'" % (who, str(paths)))

    @classmethod
    def get_output_file_list(cls,
                            paths: KGTKFiles,
                            who: typing.Optional[str] = None,
                            default_stdin: bool = True,
                       
    )->typing.List[Path]:
    
        from kgtk.exceptions import KGTKException

        if who is None:
            who = cls.DEFAULT_OUTPUT_FILE_WHO

        return cls.get_path_list(paths, who, default_stdio=default_stdin)


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
