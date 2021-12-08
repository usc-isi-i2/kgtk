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

## Installation

> The following instructions install KGTK and the KGTK Jupyter Notebooks on
    Linux and MacOS systems.

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
conda create -n kgtk-env python=3.9
conda activate kgtk-env
conda install -c conda-forge graph-tool
conda install -c conda-forge jupyterlab
pip --no-cache install -U kgtk
python -m spacy download en_core_web_sm
```

Please see our [installation document](/docs/install.md) for more details.  If
you encounter problems with your installation, or are interested in a detailed
explanation of these commands, [read more about the installation procedure
here](docs/KGTK-Installation-Procedure-Details.md).

### Installing KGTK with Docker

Please refer to [this document](docs/install-with-docker.md) for installing KGTK with Docker

## Getting started

### Online Documentation

You can read our latest documentation online with:

https://kgtk.readthedocs.io/en/latest/


### KGTK Notebooks

For examples of using KGTK, please see our [Tutorial Notebooks](https://github.com/usc-isi-i2/kgtk-notebooks ).

## Releases

* See all [source code releases](https://github.com/usc-isi-i2/kgtk/releases)

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
