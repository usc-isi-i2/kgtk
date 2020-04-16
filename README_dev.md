# KGTK developer instruction

This instruction shows how to create a cli module. Please follow this strictly.

## Create a module

Create a module under [`kgtk.cli`](https://github.com/usc-isi-i2/kgtk/tree/dev/kgtk/cli), module name should NOT start with underscore.

A typical module ([`kgtk.cli.dummy`](https://github.com/usc-isi-i2/kgtk/blob/dev/kgtk/cli/dummy.py)) looks like this:

```
"""
Example CLI module
Please DON'T import specific modules globally, import them in `run`.
Please DON'T initialize resource (e.g., variable) globally.
"""
from kgtk.cli_argparse import KGTKArgumentParser


def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        'help': 'this is example',
        'description': 'this is a basic example'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (kgtk.cli_argparse.KGTKArgumentParser)
    """
    parser.add_argument(action="store", type=str, metavar="name", dest="name")
    parser.add_argument("-i", "--info", action="store", type=str, dest="info")
    parser.add_argument("-e", "--error", action="store_true", help="raise an error")
    parser.accept_shared_argument('_debug')


def run(name, info, error, _debug):
    """
    Arguments here should be defined in `add_arguments` first.
    The return should be 0 or None. Though you can return a non-zero value to indicate error, raise exceptions defined in kgtk.exceptions is preferred
    since this gives user an unified error code and message.
    """
    # import modules locally
    import socket
    from kgtk.exceptions import KGTKException

    if _debug:
        print('DEBUG MODE')

    if error:
        raise KGTKException('An error here\n')

    print('name: {}, info: {}\nhost: {}'.format(name, info, socket.gethostname()))
```

## Module functions

- Function `parse` defines settings of a sub parser.
- Function `add_arguments` defines all accepted arguments.
- Function `run` takes all parsed arguments.

Internally, kgtk scans all submodules in `kgtk.cli`, then calls `parse` to initialize each sub parser and `add_arguments` to register all arguments. You should AVOID using unnecessary global variables, global import, etc, because all these will be loaded while initializing and drop performance. A cli command will be converted into a `run` function call. For example, if the command is `kgtk dummy hello`, it will finally be `run(name='hello')`.

## Exceptions

kgtk has an unified exception handling process in [`kgtk.exceptions`](https://github.com/usc-isi-i2/kgtk/blob/dev/kgtk/exceptions.py). All errors, including intended and unintended, should be an instance or an instance of subclass of `KGTKException` which defines return code and message.

```
class KGTKException(BaseException):
    return_code = 1
    message = 'KGTKException found\n'

    def __init__(self, message):
        self.message = message
```

## Shared arguments

If some arguments are sharing among many cli modules, they can be defined globally in [`kgtk.cli_argparse.add_shared_arguments`](https://github.com/usc-isi-i2/kgtk/blob/dev/kgtk/cli_argparse.py).

```
def add_shared_arguments(parser):
    # set shared arguments here
    # 1. no flag, only name (starts with two dashes: --XXX)
    # 2. need to have default value
    # 3. need to specify dest, which value starts with underscore
    # e.g., parser.add_argument('--debug', dest='_debug', action='store_true', default=False, help='enable debug mode')
    pass
```

If your submodule is interested in a shared argument, register it with `parser.accept_shared_argument` in `add_arguments` function. Then your `run` function will be invoked with it.

```
def add_arguments(parser: KGTKArgumentParser):
    ...
    parser.accept_shared_argument('_debug')

def run(..., _debug):
    ...
```

## Default arguments

Similar to shared arguments, default arguments are also globally defined. But it has several differences comparing to shared arguments:

- It performs the same as normal arguments.
- It defines some common, unified but not globally set arguments. For developer, it's more like a parent parser: arguments only need to be defined once but can be used in all registered sub modules.
- If it's used in pipe, each sub command can set it to different values.

Using it is also similar to shared arguments: define default arguments in [`kgtk.cli_argparse.add_default_arguments`](https://github.com/usc-isi-i2/kgtk/blob/dev/kgtk/cli_argparse.py).

Then in submodule, register interested default arguments with `parser.accept_default_argument` in `add_arguments` function and change the signature of `run` to accept these arguments.

```
def add_arguments(parser: KGTKArgumentParser):
    ...
    parser.accept_default_argument('save')

def run(..., save):
    ...
```

Examples usage:

```
kgtk --shared-arg command --opt foo --default-arg bar
kgtk --shared-arg command1 --default-arg bar1 / command2 --default-arg bar2
```

## Debug mode

A special shared argument `--debug` can turn kgtk into debug mode. Once it's enabled, all exceptions captured in function `run` will have their traceback information printed into stderr.

```
kgtk --debug dummy -e "trouble maker"
```

## Pipe

kgtk's pipe works similar to Linux bash's pipe, but it saves you from typing in `kgtk` and shared arguments multiple times. In the future, we may also make all sub commands in pipe optimized.

The delimiter of pipe is ` / ` (with heading and trailing white-spaces).

In general, the usage is
```
kgtk [options] command [ / command]*
```

Typically, 
```
kgtk --shared-arg1 --shared-arg2 foo cmd1 --option1 | kgtk --shared-arg1 --shared-arg2 foo cmd2 --option2 bar
``` 
compacts to 
```
kgtk --shared-arg1 --shared-arg2 foo cmd1 --option1 / cmd2 --option2 bar
```
