## Install KGTK and the KGTK Jupyter Notebooks

Here is the standard set of steps to install KGTK and the
KGTK Jupyter Notebooks:

```
conda create -n kgtk-env python=3.8
conda activate kgtk-env
conda install -c conda-forge graph-tool
conda install -c conda-forge jupyterlab
pip --no-cache install -U kgtk
python -m spacy download en_core_web_sm

cd /path/to/install/kgtk/tutorial
git clone https://github.com/usc-isi-i2/kgtk-notebooks.git
cd kgtk-notebooks
```

The following sections discuss the details behind the installation
steps.

### We Recommend Python 3.8

Some of KGTK's features require Python 3.8 or later. As of 12-Oct-2021, Python
version 3.8, 3.9, and 3.10 are available. We currently develop and test using
Python 3.8, and are not routinely checking for compatibility with later versions
of Python.  At the present time, we recommend running KGTK on Python 3.8.

This is not to say that KGTK will fail to run on a later version of
Python.  However, the removal of deprecated features, or unxpected
incompatibilities between later releases of Python and KGTK or KGTK's required
external modules, may lead to unanticipated problems.  If your project would
like to run KGTK, but you require a later version of Python, please contact
the KGTK team.

### We Recommand a Virtual Environment

Some of KGTK's advanced commands depend upon Graph-tool. Installing Graph-tool
is problematic using Python 3.8 outside of a virtual environment. Thus: **the
advised installation path is by using a virtual environment**,
such as [Mamba](https://github.com/mamba-org/mamba#readme)
or [Conda](https://docs.conda.io/en/latest/).

## Install Conda

Our installation procedure usees a [Conda](https://docs.conda.io/en/latest/) virtual environment. If you don't have a conda installed,
follow this
[link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to
install it.

> If you are new to Conda, we recommend a Miniconda installation rather than the
    full Anaconda installation.


> [Mamba](https://github.com/mamba-org/mamba#readme) is a faster, drop-in
    replacement for Conda that has been developed recently.  We may recommend
    Mamba in the future, but do not do so at the present itme.

## Create Your Conda Environment

Create a Conda environment named `kgtk-env`.  You may use a
different name, substituting it where `kgtk-env` appears in
these and following commands:

```bash
conda create -n kgtk-env python=3.8
```

## Activate Your Conda Environment

```bash
conda activate kgtk-env
```

This command activates your Conda environment.  Once activated, your terminal
session will have access to the resources that have been installed into
that environment.

> You will need to re-execute this command whenever you open a fresh terminal
    session for working with KGTK.

> `conda activate kgtk-env` operates in part through changes that Conda made to
    your terminal shell's initialization file when Conda was installed.
    The [Conda documentation on managing environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) may help you resolve any problems you encounter with this process.

    For example, you may have to execute:

    `conda init SHELL`

    where SHELL is the name of your command shell.  If you are using
    the `bash` shell:

    `conda init bash`

    Next, exit your terminal session, start a fresh terminal session,
    and retry:

    `conda activate kgtk-env`

## Install `graph-tool` Using `conda`

Assuming that you used the recommended Conda environment, you should install
`graph-tool` to support the KGTK subcommands that require it (e.g., `connected-components`,
`export-gt`, `graph-statistics`, `paths`, `reachable-nodes`):

```bash
conda install -c conda-forge graph-tool
```

If you don't use Conda, or if you run into problems, see the
[graph-tool installation instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).

> We recommend installing `graph-tool` from the `conda-forge` channel (`-c conda-forge`)
    to ensure that you receive a recent version of `graph-tool`.

## Install KGTK Using `pip`

Installing KGTK using `pip` will give you access to the `kgtk` command
and its subcommands.

```bash
pip --no-cache install -U kgtk
```

> The `--no-cache` and `-U` options tell `pip` to install the latest
    version of KGTK and its required modules.

> You may sometimes need to install a specific release of KGTK, such as
   a prerelease that incorporates the latest changes.  For example,
   if you need to install KGTK release `0.8.3b0`, use the following
   `pip` command instead of the `pip` command shown above:

```bash
pip --no-cache install kgtk==0.8.3b0
```
     
## Download the English Model of SpaCY

SpaCY is used by the `kgtk text-embeddings` command.  We download
Spacy's English language module using the following command:

```bash
python -m spacy download en_core_web_sm
```

> If you wisk to use KGTK for text embedding analyses using
    languages other then English, please contact the KGTK team.

## Running KGTK Commands in the Terminal Session

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

## Install `jupyter lab` Using `conda`

Assuming that you used the recommended Conda environment, you should install
Jupyter Lab to run the example Jupyter Notebooks from the `kgtk-notebooks`
repository that will be installed below.

```bash
conda install -c conda-forge jupyterlab
```

## Install the KGTK Tutorial and Other Jupyter Notebooks from GitHub

The following commands download the KGTK Jupyter Notebooks
from GitHub.


First, choose a folder in which you want to begin the
installation of the KGTK Tutorial and other Jupyter notebooks.

```bash
cd /path/to/install/kgtk/tutorial
```

A new folder, `kgtk-notebooks`, will be created.
The KGTK Tutorial and other Jupyter notebooks will downloaded from GitHub
and installed in `kgtk-notebooks`

```bash
git clone https://github.com/usc-isi-i2/kgtk-notebooks.git
```

Change your current working directory to the `kgtk-notebooks`
folder:

``` bash
cd kgtk-notebooks
```

You are now ready to run the KGTK Tutorial.

## Running the KGTK Jupyter Notebooks

In your `kgtk-notebooks` folder, execute a command such as:

```bash
jupyter lab part1-kgtk-intro.ipynb
```

This will start a Jupyter Lab notebook server in your current terminal
session.  Depending upon your system configuration, a Jupyter Lab interface
will automatically open in one of your Web browser windows, or you can use
the URI that the Jupyter Labs server prints to open a Jupyter Lab interface
in your Web browser manually.

## Resuming Work with KGTK in a New Terminal Session

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

> `/path/to/install/kgtk/tutorial` is the path you originally
    choose for installation of the KGTK Tutorial and other Jupyter notebooks.

Use the Jupyter Lab interface to select the KGTK Tutorial notebook on which you
wish to resume work, or to select a new notebook to begin.

> If you know the name of the notebook you want to start, you may
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
execute the following commands:

```
conda activate kgtk-env
cd /path/to/install/kgtk/tutorial/kgtk-notebooks
git pull
```

> The `conda activate kgtk-env` commands shown above are not needed
    if you have already activated your `kgtk-env` Conda virtual environment
    in your current terminal session.
