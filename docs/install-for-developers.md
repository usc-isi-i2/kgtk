### Install KGTK using GitHub

You can install KGTK from our GitHub repository.  A GitHub installation will
give you access to the `examples/` folder with examples of KGTK usage in
Jupyter notebooks.

To install the latest release, use one of the following two commands:

`git clone git@github.com:usc-isi-i2/kgtk.git`

or:

`git clone https://github.com/usc-isi-i2/kgtk.git`

This will install KGTK in a folder called `kgtk`.  Connect to this
folder before executing any of the commands in the sections below:

`cd kgtk`

You may install KGTK from GitHub without installing KGTK
using `pip` at the same time, but you may need to set the
PYTHONPATH environment variable to point to your KGTK checkout
location:

export PYTHONPATH=<KGTK checkout path>

### Installing Required Modules after Installation from GitHub

After installing KGTK from GitHub, you may need to use pip to download
additional modules that are required by KGTK.  For a minimal installation,
execute:

`pip install -r requirements.txt`

Some KGTK subcommands may not run under the minimal installation.
We recommend also installing the full set of required modules:

`pip install -r requirements-full.txt`

If you intend to develop using KGTK's source code, you should also install the
modules required for development:

`pip install -r requirements-dev.txt`

You can test if `kgtk` is installed properly now with: `kgtk -h`.

## Running KGTK's Unit Tests Locally

After a Docker or GitHub installation, you may run KGTK's unit tests to
verify that the installation was complete.  You may use either of the two
following command sequences to run the unittests, starting at your
KGTK installation folder:

```
make unittest
```

or:

```
cd tests
python -W ignore -m unittest discover
```

If you develop your own extensions to KGTK, you should run the
unit tests frequently.

## Updating your KGTK installation

To get the latest stable release of the KGTK commands and the latest KGTK
Jupyter Notebooks, execute the following steps starting from where you
installed KGTK:

To update your version of KGTK, just follow the instructions below:

```bash
pip --no-cache install -U kgtk
pip install -r requirements.txt
pip install -r requirements-full.txt
pip install -r requirements-dev.txt
cd kgtk
git pull
cd kgtk-notebooks
git pull
```
