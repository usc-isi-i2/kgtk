## Try KGTK Online with MyBinder
The easiest, no-cost way of trying out KGTK is through [MyBinder](https://mybinder.org/). We have made available several **example notebooks** to show some of the features of KGTK, which can be run in two environments: 

* Basic KGTK functionality: This notebook may take 5-10 minutes to launch, please be patient. Note that in this notebook some KGTK commands (graph analytics and embeddings) **will not run**. To launch the notebook in your browser, click on the "Binder" icon: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/usc-isi-i2/kgtk/master?filepath=examples%2FExample5%20-%20AIDA%20AIF.ipynb)

* Advanced KGTK functionality: This notebook may take 10-20 minutes to launch. It includes basic KGTK functionality and **graph analytics and embedding capabilities** of KGTK:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dgarijo/kgtk/dev?filepath=%2Fkgtk%2Fexamples%2FCSKG%20Use%20Case.ipynb)

For executing KGTK with large datasets, **we recommend a Docker/local installation**.

## KGTK Notebooks

The examples folder (`examples/`) provides a larger and constantly increasing
number of easy-to-follow Jupyter Notebooks which showcase different
functionalities of KGTK. These include computing:
 
* Embeddings for ConceptNet nodes
* Graph statistics over a curated subset of Wikidata
* Reachable occupations for selected people in Wikidata
* PageRank over Wikidata
* etc.

These examples are available once KGTK has been installed from Docker or GitHub
using one of the methods described below.

## Using KGTK with Docker

If you have Docker installed, you can pull the latest KGTK image with::

```bash
docker pull uscisii2/kgtk
```

You can build the Docker image yourself after installing KGTK from GitHub (see below).

### Run KGTK on a Docker Command Line

To run KGTK in the command line type (note that if you built the image
yourself, you should replace `uscisii2/kgtk:latest` by `kgtk-local` in this
and the following commands):

```bash
docker run -it --rm  --user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes uscisii2/kgtk:latest /bin/bash
```

### Accessing Local Data with the Docker Command Line

If you want to load data from your local machine, you will need to [mount a volume](https://docs.docker.com/storage/volumes/).
For example, to mount the current directory (`$PWD`) and launch KGTK in command line mode:

```bash
docker run -it --rm -v $PWD:/out --user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes uscisii2/kgtk:latest /bin/bash
```

### Runnning KGTK in a Jupyter Notebook using Docker

If you want to run KGTK in a **Jupyter notebook**, mounting the current directory (`$PWD`) as a folder called `/out` then you will have to type:

```bash
docker run -it -v $PWD:/out -p 8888:8888 uscisii2/kgtk:latest /bin/bash -c "jupyter notebook --ip='*' --port=8888 --no-browser"
```

You will see a message similar to:

```bash
[C 22:36:40.418 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://092260f3740e:8888/?token=83945df95e9b1f5f7594597d3925960fc89dbefaed4ada7d
     or http://127.0.0.1:8888/?token=83945df95e9b1f5f7594597d3925960fc89dbefaed4ada7d
```

Copy the localhost URL (in the case above `http://127.0.0.1:8888/?token=83945df95e9b1f5f7594597d3925960fc89dbefaed4ada7d`, this is random every time) and paste it in your browser. In order to run KGTK commands in a notebook, remember to add `%%bash` in the line before your command, as shown below:

```bash
%%bash
kgtk --help
```

As a result, now you should be able to see a help message similar to the one depicted below:

![Diagram](images/nb.png)

!!! note
    if you want to load data from your local machine or save the results obtained with KGTK, you will need to [mount a volume](https://docs.docker.com/storage/volumes/) as described above. **Notebooks stored inside the container will be erased after the container finishes its execution**.

!!! note
    Older versions of KGTK (0.3.2 and 0.2.1) require `--allow-root` as part of the jupyter notebook command `jupyter notebook --ip='*' --port=8888 --allow-root --no-browser`

### Additional Docker Images

More information about all available versions and tags is available here:
[https://hub.docker.com/repository/docker/uscisii2/kgtk](https://hub.docker.com/repository/docker/uscisii2/kgtk). For
example, the `dev` branch is available at `uscisii2/kgtk:latest-dev`.

## Installing KGTK from pip or GitHub

### We Recommand Python 3.8

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
advised installation path is by using a virtual environment.**

### Install Conda

Our pip and GitHub installations will use a Conda virtual environment. If you
don't have a conda installed, follow this
[link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to
install it.

If you are new to Conda, we recommend a Miniconda installation rather than the
full Anaconda installation.

### Set Up Your Own Conda Environment

Create a Conda environment named `kgtk-env`.  You may use a
different name, substituting it where `kgtk-env` appears in
these and following commands:

```
conda create -n kgtk-env python=3.8
conda activate kgtk-env
```

### Install KGTK using pip

Installing KGTK using pip will give you access to the `kgtk` command
and its subcommands.

You will not have access to the `examples/` folder
with KGTK's example Jupyter notebooks.  To access the examples,
install the Docker or GitHub releases.

`pip install kgtk`

You can test if `kgtk` is installed properly now with: `kgtk -h`.

### Install KGTK using GitHub

You can also install KGTK from our GitHub repository.  To install the
latest release, install using:

`git clone git@github.com:usc-isi-i2/kgtk.git`
`cd kgtk`

or:

`git clone https://github.com/usc-isi-i2/kgtk.git`
`cd kgtk`

This will give you access to the `examples/` folder with examples of
KGTK usage in Jupyter notebooks.

You may install KGTK from GitHub without installing KGTK
using `pip` at the same time, but you may need to set the
PYTHONPATH environment variable to point to your KGTK checkout
location:

export PYTHONPATH=<KGTK checkout path>

### Installing Required Modules after Installtion from GitHub

After installing KGTK from GitHub, you may need to use pip to download
additional modules that are required bu KGTK.  For a minimal installation,
execute:

`pip install -r requirements.txt`

Some KGTK subcommands may not run under the minimal installation.
We recommend also installing the full set of required modules:

`pip install -r requirements-full.txt`

If you intend to develop using KGTK's source code, you should also install the
modules required for development:

`pip install -r requirements-dev.txt`

You can test if `kgtk` is installed properly now with: `kgtk -h`.

### Install Graph-tool

After installing KGTK from pip or GitHub, and assuming that you used
the recommended Conda environment, you should install Graph-tool to
support the KGTK subcommands that require it:

`conda install -c conda-forge graph-tool`.

If you don't use Conda, or if you run into problems, see these
[instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).

## Building a Docker Image

You can build a local Docker image after installing KGTK from GitHub:

```
cd kgtk/docker/
docker build -t kgtk-local .
```

## Updating your KGTK installation

To update your version of KGTK, just follow the instructions below:

- If you installed KGTK with through Docker, then just pull the most recent image: `docker pull <image_name>`, where `<image_name>` is the tag of the image of interest (e.g. uscisii2/kgtk:latest)
- If you installed KGTK from pip, then type `pip install -U kgtk`.
- If you installed KGTK from GitHub, then type `git pull && pip install -r requirements.txt`.  If you previously installed the `-full`- or `-development` modules, you should repeat those commands, too.


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

## Running KGTK's Unit Tests Locally

After a Docker or GitHub installation, you may run KGTK's unit tests to
verify that the installation was complete.  You may use either of the two
following command sequences to run the unittests:

```
make unittest
```

or:

```
cd kgtk/tests
python -W ignore -m unittest discover
```

If you develop your own extensions to KGTK, you should run the
unit tests frequently.

