## KGTK Installation Procedure Details

### Install KGTK and the KGTK Jupyter Notebooks

Here is the standard set of steps to install KGTK and the
KGTK Jupyter Notebooks:

```
conda create -n kgtk-env python=3.8
conda activate kgtk-env
conda install -c conda-forge graph-tool
pip --no-cache install -U kgtk
python -m spacy download en_core_web_sm
git clone https://github.com/usc-isi-i2/kgtk-notebooks.git
cd kgtk-notebooks
```

The following sections discuss the details behind the installation
steps.

### We Recommend Python 3.8

Some of KGTK's features require Python 3.8 or later. As of 12-Oct-2021, Python
version 3.8, 3.9, and 3.10 are available. We currently devleop and test using
Python 3.8, and are not routinely checking for compatability with later versions
of Python.  At the present time, we recommend running KGTK on Python 3.8.

This is not to say that KGTK will not necessarily run on a later version of
Python.  However, the removal of deprecated features, or unxpected
incompatibilities between later releases of Python and KGTK or KGTK's required
external modules, may lead to unanticipated problems.  If your project would
like to run KGTK, but you require a later version of Python, please contact
the KGTK project for support.

### We Recommand a Virtual Environment

Some of KGTK's advanced commands depend upon Graph-tool. Installing Graph-tool
is problematic using Python 3.8 outside of a virtual environment. Thus: **the
advised installation path is by using a virtual environment**,
such as [Mamba](https://github.com/mamba-org/mamba#readme)
or [Conda](https://docs.conda.io/en/latest/).

### Install Conda

Our installation procedure usees a [Conda](https://docs.conda.io/en/latest/) virtual environment. If you don't have a conda installed,
follow this
[link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to
install it.

!!! info
    If you are new to Conda, we recommend a Miniconda installation rather than the
    full Anaconda installation.


!!! note
    [Mamba](https://github.com/mamba-org/mamba#readme) is a faster, drop-in
    replacement for Conda that has been developed recently.  We may recommend
    Mamba in the future, but do not do so at the present itme.

### Set Up Your Own Conda Environment

Create a Conda environment named `kgtk-env`.  You may use a
different name, substituting it where `kgtk-env` appears in
these and following commands:

```bash
conda create -n kgtk-env python=3.8
```

### Activating Your Conda Environment

```bash
conda activate kgtk-env
```

This command activates your Conda environment.  Once activated, your terminal
session will have access to the resources that have been installed into
that environment.

!!! note
    You will need to re-execute this command whenever you open a fresh terminal
    session for working with KGTK.

### Install `graph-tool`

Assuming that you used the recommended Conda environment, you should install
`graph-tool` to support the KGTK subcommands that require it:

```bash
conda install -c conda-forge graph-tool
```

If you don't use Conda, or if you run into problems, see the
[graph-tool installation instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).

!!! note
    We recommend installing `graph-tool` from the `conda-forge` channel (`-c conda-forge`)
    to ensure that you receive a recent version of `graph-tool`.

### Install KGTK Using `pip`

Installing KGTK using `pip` will give you access to the `kgtk` command
and its subcommands.

```bash
pip --no-cache install -U kgtk
```

The `--no-cache` and `-U` options tell `pip` to install the latest
version of KGTK and its required modules.

You can test if `kgtk` is installed properly now with:

```bash
kgtk -h
```

### Download the English Model of SpaCY

SpaCY is used by the `kgtk text-embeddings` command.  We download
Spacy's English language module using the following command:

```bash
python -m spacy download en_core_web_sm
```

!!! note
    If you wisk to use KGTK to conduct text embedding analyses using
    languages other then English, please contact the KGTK tesm for
    assistance.

### Install the KGTK Jupyter Notebooks

The following commands download the KGTK Jupyter Notebooks
from GitHub.  The notebooks are installed in the folder
`kgtk-notebooks` below your current working folder.

```bash
git clone https://github.com/usc-isi-i2/kgtk-notebooks.git
cd kgtk-notebooks
```

## Running KGTK commands

To list all the available KGTK commands, run:

```
kgtk -h
```

To see the arguments of a particular KGTK command, run:

```
kgtk <command> -h
```

See our [online documentation](https://kgtk.readthedocs.io/en/latest/) for
additional suggestions.

## Running the KGTK Jupyter Notebooks

In your `kgtk-notebooks` folder, execute a command such as:

```bash
jupyter lab 'examples/Example1 - Embeddings.ipynb'
```

This will start a Jupyter Lab notebook server in your current terminal
session.  Depending upon your system configuration, a Jupyter Lab interface
will automatically open in one of your Web browser windows, or you can use
the URI that the Jupyter Labs server prints to open a Jupyter Lab interface
in your Web browser manually.

## Updating your KGTK installation

To get the latest stable release of the KGTK commands and the latest KGTK
Jupyter Notebooks, execute the following steps starting from where you
installed KGTK:

```
pip --no-cache install -U kgtk
cd kgtk-notebooks
git pull
```

The first step, `pip --no-cache install -U kgtk`, installs
