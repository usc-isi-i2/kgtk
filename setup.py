from distutils.core import setup
from setuptools import find_packages # type: ignore
from kgtk import __version__

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

packages = find_packages()

setup(
    name='kgtk',
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
)
