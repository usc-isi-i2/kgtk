# kgtk

### Installation

0. Our installations will be in a conda environment. If you don't have a conda installed, follow [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to install it.
1. Set up your own conda environment:
```
conda create -n kgtk-env python=3.6 anaconda
source activate kgtk-env
```
2. `pip install -r requirements.txt`
3. Install `graph-tool`. If you use conda, then you can run `conda install -c conda-forge graph-tool`, else see these [instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions). 

### List of supported tools
* `instances`
* `reachable_nodes`
* `filter`
* `text_embedding`
* `remove_columns`
* `sort`
* `merge_identical_nodes`
* `zconcat`

To get an information on how to use each of them, run:
`kgtk [TOOL] -h`

More detailed description of the arguments will be added here promptly.
