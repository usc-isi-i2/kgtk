## Using KGTK with Docker

If you have Docker installed, we have prepared a Docker image with KGTK (current version: 0.2.1):

```bash
docker pull uscisii2/kgtk
```

To run KGTK in the command line just type:

```bash
docker run -it uscisii2/kgtk /bin/bash
```

To test KGTK, you can simply type:
```bash
kgtk --help
```
And you should see a long message which starts with:

```bash
usage: kgtk [options] command [ / command]*

kgtk --- Knowledge Graph Toolkit

positional arguments:
  command
    add_id              Copy a KGTK file, adding ID values.
...
```

If you want to run KGTK in a Jupyter notebook, then you will have to type:
```
docker run -it -p 8888:8888 uscisii2/kgtk /bin/bash -c "jupyter notebook --ip='*' --port=8888 --allow-root --no-browser"
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

If everuthing goes well, you should be able to see a similar message to the one depicted below:

![Diagram](images/nb.png)

**Note**: if you want to load data from your local machine, you will need to [mount a volume](https://docs.docker.com/storage/volumes/).

More information about versions and tags is available here: https://hub.docker.com/repository/docker/uscisii2/kgtk

## Installing KGTK from pip

**Before you start**:  Our installation will use a conda environment. If you don't have a conda installed, follow this [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to install it.

1. Set up your own conda environment:
```
conda create -n kgtk-env python=3.7
conda activate kgtk-env
```
 **Note:** Installing Graph-tool is problematic on python 3.8 and out of a virtual environment. Thus: **the advised installation path is by using a virtual environment.**

1. Install: `pip install kgtk`

You can test if `kgtk` is installed properly now with: `kgtk -h`.

3. Install `graph-tool`: `conda install -c conda-forge graph-tool`. If you don't use conda or run into problems, see these [instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions). 

4. Install `mlr`. Depending on your environment, you can run one of the following:
  * `brew update && brew install miller` (on mac)
  * `sudo port selfupdate && sudo port install miller` (on mac)
  * `sudo apt-get install miller` (linux)
  * `sudo apt install miller` (linux)
  * `sudo yum install miller` (linux)
  
More installation options for `mlr` can be found [here](https://johnkerl.org/miller/doc/build.html).

## Running KGTK commands

To list all the available KGTK commands, run:

```
kgtk -h
```

To see the arguments of a particular commands, run:

```
kgtk <command> -h
```

An example command that computes instances of the subclasses of two classes:

```
kgtk instances --transitive --class Q13442814,Q12345678
```

## Additional information

### The Miller Package

1. Our code uses the "miller" package to manipulate formatted data.

2. TheGitHub repository for miller is:
```
https://github.com/johnkerl/miller
```
3. The documentaton is:
```
https://www.mankier.com/1/mlr
```
4. You may need to install the miller command (mlr) on your system.
   * OpenSUSE Tumbleweed Linux: install package `miller` from Main Repository (OSS)
