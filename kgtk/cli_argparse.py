from argparse import ArgumentParser, RawDescriptionHelpFormatter
from functools import partial
from kgtk.exceptions import KGTKArgumentParseException, KGTKSyntaxException


class KGTKArgumentParser(ArgumentParser):
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
