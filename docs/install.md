## Installing KGTK

!!! info
    The following instructions install KGTK and the KGTK Jupyter Notebooks on
    Linux and MacOS systems.

!!! note
    If you want to install KGTK on a Microsoft Windows system, please
    contact the KGTK team.

Our KGTK installations use a Conda virtual environment. If you
don't have the Conda tools installed, follow this
[guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to
install it. We recommend installing Miniconda installation rather than the
full Anaconda installation.

Next, execute the following steps to install the latest stable release
of KGTK:

```bash
conda create -n kgtk-env python=3.8
conda activate kgtk-env
conda install -c conda-forge graph-tool
conda install -c conda-forge jupyterlab
pip --no-cache install -U kgtk
python -m spacy download en_core_web_sm
```

!!! note
    You may sometimes need to install a specific release of KGTK, such as
    a prerelease that incorporates the latest changes.  For example,
    if you need to install KGTK release `0.8.3b0`, use the following
    `pip` command instead of the `pip` command shown above:

     ```bash
     pip --no-cache install kgtk==0.8.3b0
     ```

If you encounter problems with your installation, or are interested in a
detailed explanation of these commands,
[read more about the installation procedure here](KGTK-Installation-Procedure-Details.md).

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

## Installing the KGTK Tutorial and Other Jupyter Notebooks

Choose a folder in which you want to install the KGTK Tutorial and
other Jupyter notebooks.  Change your current working directory
to that foder.

```bash
cd /path/to/install/kgtk/tutorial
```

!!! note
    `/path/to/install/kgtk/tutorial` is an appropriate filesystem
    path of your choice.

Next, execute the following command:

```bash
git clone https://github.com/usc-isi-i2/kgtk-notebooks.git
```

This will create a new folder (`kgtk-notebooks`) in your existing folder,
then download the KGTK Tutorial and other Jupyter notebook files into
the new folder.

Change your current working directory to the `kgtk-notebooks` folder:

```bash
cd kgtk-notebooks
```

You are now in your `kgtk-notebooks` folder and ready to start the
KGTK Tutorial using Jupyter Lab.

## Running the KGTK Tutorial and Other Jupyter Notebooks

In your `kgtk-notebooks` folder, start the first KGTK Tutorial notebook using the
following command:

```bash
jupyter lab part1-kgtk-intro.ipynb
```

This will start a Jupyter Lab notebook server in your current terminal
session.  Depending upon your system configuration, a Jupyter Lab interface
will automatically open in one of your Web browser windows, or you can use
the URI that the Jupyter Labs server prints to open a Jupyter Lab interface
in your Web browser manually.

### Resuming Work with KGTK in a New Terminal Session

If you have started a new terminal session and want to resume work with
KGTK, first execute the following command in the new terminal session in order
to activate your `kgtk-env` Conda virtual environment:

```bash
conda activate kgtk-env
```

You should now be able to execute KGTK commands on the command line.

If you want to start a new Jupiter Lab notebook server, activate your
Conda virtual environment as shown above and then enter:

```bash
cd /path/to/install/kgtk/tutorial/kgtk-notebooks
jupyter lab
```

!!! note
    `/path/to/install/kgtk/tutorial` is the path you originally
    choose for installation of the KGTK Tutorial and other Jupyter notebooks.

Use the Jupyter Lab interface to select the KGTK Tutorial notebook on which you
wish to resume work, or to select a new notebook to begin.

!!! note
    If you know the name of the notebook you want to start, you may
    put it on the end of the `jupyter lab` command line:

    ```bash
    jupiter lab some-notebook-name.ipynb
    ```

## Updating your KGTK installation

To get the latest stable release of the KGTK commands, execute
the following commands:

```bash
conda activate kgtk-env
pip --no-cache install -U kgtk
```

To get the latest KGTK Jupyter notebooks, 

Execute the following commands
installed KGTK:

```
conda activate kgtk-env
cd /path/to/install/kgtk/tutorial/kgtk-notebooks
git pull
```

!!! note
    The `conda activate kgtk-env` commands shown above are not needed
    if you have already activated your `kgtk-env` Conda virtual environment
    in your current terminal session.
