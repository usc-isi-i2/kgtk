## Installing KGTK

The following steps install KGTK and the KGTK Jupyter Notebooks.

Our pip and GitHub installations will use a Conda virtual environment. If you
don't have th Conda tools installed, follow this
[guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to
install it. We recommend installing Miniconda installation rather than the
full Anaconda installation.

Next, execute the following steps to install the latest stable release
of KGTK:

```
conda create -n kgtk-env python=3.8
conda activate kgtk-env
conda install -c conda-forge graph-tool
pip --no-cache install -U kgtk
python -m spacy download en_core_web_sm
git clone https://github.com/usc-isi-i2/kgtk-notebooks.git
cd kgtk-notebooks
```

For an explanation of these commands, [here is a detailed description](install-details.md).

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
