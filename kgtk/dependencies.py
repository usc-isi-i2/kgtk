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


def check_deps_sqlite():
    print('sqlite is not properly installed, please follow the instructions in https://foo.bar')
    return False
