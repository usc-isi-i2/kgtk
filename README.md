<img src="https://github.com/usc-isi-i2/kgtk/raw/master/docs/images/kgtk_logo_200x200.png" width="150"/>

# KGTK: Knowledge Graph Toolkit

[![doi](https://zenodo.org/badge/DOI/10.5281/zenodo.3828068.svg)](https://doi.org/10.5281/zenodo.3828068)  ![travis ci](https://travis-ci.org/usc-isi-i2/kgtk.svg?branch=master)  [![Coverage Status](https://coveralls.io/repos/github/usc-isi-i2/kgtk/badge.svg?branch=master)](https://coveralls.io/github/usc-isi-i2/kgtk?branch=master)

KGTK is a Python toolkit for building applications using knowledge graphs (KG). KGTK is designed for ease of use, scalability and speed. It represents KGs as simple TSV files with four columns to represent the head, relation and tail of a triple, as well as an identifier for each triple. This simple model allows KGTK to operate on property graphs and on RDF graphs. KGTK offers a comprehensive collection of 20+ commands to import, transform, query and analyze KGs, including wrappers for state of the art graph analytics and deep learning libraries. KGTK is optimized for batch processing, making it easy to write KG pipelines that process large KGs such as Wikidata on a laptop to produce datasets for use in downstream applications. KGTK is open-source software released under the MIT license.


## Getting started

### Documentation

https://kgtk.readthedocs.io/en/latest/

### Demo: try KGTK online with MyBinder
The easiest, no-cost way of trying out KGTK is through [MyBinder](https://mybinder.org/). We have made available several **example notebooks** to show some of the features of KGTK, which can be run in two environments:

* **Basic KGTK functionality**: This notebook may take **5-10 minutes** to launch, please be patient. Note that in this notebook some KGTK commands (graph analytics and embeddings) **will not run**. To launch the notebook in your browser, click on the "Binder" icon: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/usc-isi-i2/kgtk/master?filepath=examples%2FExample5%20-%20AIDA%20AIF.ipynb)

* **Advanced KGTK functionality**: This notebook may take **10-20 minutes to launch**. It includes basic KGTK functionality and **graph analytics and embedding capabilities** of KGTK:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dgarijo/kgtk/dev?filepath=%2Fkgtk%2Fexamples%2FCSKG%20Use%20Case.ipynb)

For executing KGTK with large datasets, **we recommend a Docker/local installation**.

### KGTK notebooks

The [examples folder](examples/) provides a larger and constantly increasing number of easy-to-follow Jupyter Notebooks which showcase different functionalities of KGTK. These include computing:
* Embeddings for ConceptNet nodes
* Graph statistics over a curated subset of Wikidata
* Reachable occupations for selected people in Wikidata
* PageRank over Wikidata
* etc.

## Releases

* See all [source code releases](https://github.com/usc-isi-i2/kgtk/releases)

## Installation


### Installation through Docker

```
docker pull uscisii2/kgtk
```

To run KGTK in the command line:

```
docker run -it --rm  --user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes uscisii2/kgtk:latest /bin/bash
```

Note: if you want to load data from your local machine, you will need to [mount a volume](https://docs.docker.com/storage/volumes/).
For example, to mount the current directory (`$PWD`) and launch KGTK in command line mode:

```
docker run -it --rm -v $PWD:/out --user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes uscisii2/kgtk:latest /bin/bash
```

If you want to run KGTK in a **Jupyter notebook**, mounting the current directory (`$PWD`) as a folder called `/out` then you will have to type:
```
docker run -it -v $PWD:/out -p 8888:8888 uscisii2/kgtk:latest /bin/bash -c "jupyter notebook --ip='*' --port=8888 --no-browser"
```

More information about versions and tags is available here: https://hub.docker.com/repository/docker/uscisii2/kgtk. For example, the `dev` branch is available at `uscisii2/kgtk:latest-dev`.

See additional examples in [the documentation](https://kgtk.readthedocs.io/en/latest/install/).

### Local installation

Our installation will be in a **conda environment**. If you don't have conda installed, follow [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to install it. Once installed, follow the instructions below:

1. Set up your own conda environment:
```
conda create -n kgtk-env python=3.7
conda activate kgtk-env
```
 **Note:** Installing Graph-tool is problematic on python 3.8 and out of a virtual environment. Thus: **the advised installation path is by using a virtual environment.**

2. Install (the dev branch at this point): `pip install kgtk`

You can test if `kgtk` is installed properly now with: `kgtk -h`.

3. Download the English model of SpaCY: `python -m spacy download en_core_web_sm`

4. Install `graph-tool`: `conda install -c conda-forge graph-tool`. If you don't use conda or run into problems, see these [instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).

5. Python library rdflib has a known [issue](https://github.com/RDFLib/rdflib/issues/1043), where the ttl serialization of decimal values is incorrect. The library will add a `.0` at the end of decimal values in scientific notation. This will make the ttl invalid and cannot be loaded into a triplestore.

To solve this issue, run the following commands after the `kgtk` installation is complete.
```
pip uninstall rdflib
pip install git+https://github.com/RDFLib/rdflib.git@master
```

The code fix for this bug is already merged into the library, but has not been released as a `pypi` package. This step will be removed after `rdflib` version 6 is released.

### Updating your KGTK installation
To update your version of KGTK, just follow the instructions below:

- If you installed KGTK with through Docker, then just pull the most recent image: `docker pull <image_name>`, where `<image_name>` is the tag of the image of interest (e.g. uscisii2/kgtk:latest)
- If you installed KGTK from pip, then type `pip install -U kgtk`.
- If you installed KGTK from GitHub, then type `git pull && pip install` . Alternatively, you may execute:  `git pull && python setup.py install`.
- If you installed KGTK in development mode, (i.e., `pip install -e`); then you only need to do update your repository: `git pull`.

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

## Running unit tests locally
```
cd kgtk/tests
python -W ignore -m unittest discover
```

## How to cite

```
@inproceedings{ilievski2020kgtk,
  title={{KGTK}: A Toolkit for Large Knowledge Graph Manipulation and Analysis}},
  author={Ilievski, Filip and Garijo, Daniel and Chalupsky, Hans and Divvala, Naren Teja and Yao, Yixiang and Rogers, Craig and Li, Ronpeng and Liu, Jun and Singh, Amandeep and Schwabe, Daniel and Szekely, Pedro},
  booktitle={International Semantic Web Conference},
  pages={278--293},
  year={2020},
  organization={Springer}
  url={https://arxiv.org/pdf/2006.00088.pdf}
}
```