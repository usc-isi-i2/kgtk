from distutils.core import setup
from setuptools import find_packages  # type: ignore
from setuptools.command.build_py import build_py
from kgtk import __version__
import sys

lite_build = False
if '--lite' in sys.argv:
    lite_build = True
    sys.argv.remove('--lite')

with open('requirements.txt', 'r') as f:
    install_requires = list()
    dependency_links = list()
    for line in f:
        re = line.strip()
        if re:
            if re.startswith('git+') or re.startswith('svn+') or re.startswith('hg+'):
                dependency_links.append(re)
            else:
                install_requires.append(re)

lite_excluded_modules = {
    'kgtk.cli': {'filter', 'export_gt', 'export_neo4j', 'connected_components', 'graph_statistics', 'gt_loader',
                 'reachable_nodes'}
}


class kgtk_build_py(build_py):

    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        if lite_build and package in lite_excluded_modules:
            modules = list(filter(lambda m: m[1] not in lite_excluded_modules[package], modules))
        return modules


packages = find_packages()

setup(
    name='kgtk' if not lite_build else 'kgtk-lite',
    version=__version__,
    packages=packages,
    url='https://github.com/usc-isi-i2/kgtk',
    license='MIT',
    author='ISI CKGs',
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'kgtk = kgtk.cli_entry:cli_entry',
        ],
    },
    cmdclass={
        'build_py': kgtk_build_py
    }
)
