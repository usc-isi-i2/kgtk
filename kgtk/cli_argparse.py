from argparse import ArgumentParser, RawDescriptionHelpFormatter
from kgtk.exceptions import KGTKArgumentParseException


class KGTKArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = RawDescriptionHelpFormatter

        self.shared_arguments = set()

        super(KGTKArgumentParser, self).__init__(*args, **kwargs)

    def accept_shared_argument(self, dest_name):
        self.shared_arguments.add(dest_name)

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
