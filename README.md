<img src="https://github.com/usc-isi-i2/kgtk/raw/master/docs/images/kgtk_logo_200x200.png" width="150"/>

# KGTK: Knowledge Graph Toolkit

[![doi](https://zenodo.org/badge/DOI/10.5281/zenodo.3828068.svg)](https://doi.org/10.5281/zenodo.3828068)  ![travis ci](https://travis-ci.org/usc-isi-i2/kgtk.svg?branch=master)  [![Coverage Status](https://coveralls.io/repos/github/usc-isi-i2/kgtk/badge.svg?branch=master)](https://coveralls.io/github/usc-isi-i2/kgtk?branch=master)


The Knowledge Graph Toolkit (KGTK) is a comprehensive framework for the creation and exploitation of large hyper-relational knowledge graphs (KGs), designed for ease of use, scalability, and speed. KGTK represents KGs in tab-separated (TSV) files with four columns: edge-identifier, head, edge-label, and tail. All KGTK commands consume and produce KGs represented in this simple format, so they can be composed into pipelines to perform complex transformations on KGs. KGTK provides:

- a suite of **import** commands to import Wikidata, RDF and popular graph representations into KGTK format;
- a rich collection of **transformation** commands make it easy to clean, union, filter, and sort KGs;
- **graph combination** commands support efficient intersection, subtraction, and joining of large KGs;
- a **query** language using a variant of Cypher, optimized for querying KGs stored on disk supports efficient ad hoc queries;
- **graph analytics** commands support scalable computation of centrality metrics such as PageRank, degrees, connected components and shortest paths;
- advanced commands support **lexicalization** of graph nodes, and computation of multiple variants of **text and graph embeddings** over the whole graph;
- a suite of **export** commands supports the transformation of KGTK KGs into commonly used formats, including the Wikidata JSON format, RDF triples, JSON documents for ElasticSearch indexing and graph-tool;
- a **development environmen**t using Jupyter notebooks provides seamless integration with Pandas.

KGTK can process Wikidata-sized KGs with billions of edges on a laptop. We have used KGTK in multiple use cases, focusing primarily on construction of subgraphs of Wikidata, analysis of over 300 Wikidata dumps since the inception of the Wikidata project, linking tables to Wikidata, construction of a commonsense KG combining multiple existing sources, creation of Wikidata extensions for food security and the pharmaceutical industry.

KGTK is open source software, well documented, actively used and developed, and released using the MIT license. We invite the community to try KGTK. It is easy to get started with our tutorial notebooks available and executable online.



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

## KGTK Text Search API

The documentation for the KGTK Text Search API is [here](https://github.com/usc-isi-i2/kgtk-search)

## KGTK Semantic Similarity API

The documentation for the KGTK Semantic Similarity API is [here](https://github.com/usc-isi-i2/wikidata-semantic-similarity)

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
