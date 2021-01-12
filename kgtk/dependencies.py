from kgtk.exceptions import KGTKException


def check_dependencies():
    pass_deps_check = True

    # requirements
    # TODO: The requirements.txt file won't be available in installed python package
    # print('checking requirements...')
    # import pkg_resources
    # with open('requirements.txt', 'r') as rf:
    #     requirements = pkg_resources.parse_requirements(rf.read())
    # for requirement in requirements:
    #     try:
    #         pkg_resources.require(str(requirement))
    #     except Exception as e:
    #         print(e)
    #         pass_deps_check = False

    # module level
    # print('checking other external dependencies...')
    if not check_deps_sqlite():
        pass_deps_check = False

    return pass_deps_check


### SQLite3

# The Python sqlite3 package and library is a builtin which does not
# require any special installation.  However some Kypher features such
# as explanation and fast, shell-based data import require a recent
# version of sqlite3 to be available as an executable shell command.
# The functions below check for those dependencies.

SQLITE_COMMAND = 'sqlite3'
SQLITE_MINIMUM_VERSION = '3.30'

def check_sqlite_command():
    """Return True if sqlite3 is available as a shell command and callable via 'sh'.
    """
    try:
        import sh
        sqlite3 = sh.Command(SQLITE_COMMAND)
        return True
    except:
        pass
    return False

def get_sqlite_version():
    try:
        import sh
        from packaging import version
        sqlite3 = sh.Command(SQLITE_COMMAND)
        return sqlite3('--version').stdout.split()[0].decode()
    except:
        return None

def check_sqlite_version():
    """Return True if sqlite3 is available as a shell command and has a recent enough version.
    """
    if check_sqlite_command():
        try:
            from packaging import version
            sqlite3_version = get_sqlite_version()
            return version.parse(sqlite3_version) >= version.parse(SQLITE_MINIMUM_VERSION)
        except:
            pass
    return False

def check_deps_sqlite():
    """Silently return True if sqlite3 is properly installed.
    Otherwise, print an explanation of the problem and return False.
    """
    if not check_sqlite_command():
        print('%s command is not installed or callable (please see manual)' % SQLITE_COMMAND)
        return False
    if not check_sqlite_version():
        print('%s version %s is too old, please upgrade to at least version %s (see manual)'
              % (SQLITE_COMMAND, get_sqlite_version(), SQLITE_MINIMUM_VERSION))
        return False
    return True
