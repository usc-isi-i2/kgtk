# Run the following commands before running the notebooks

0. [Install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), if not already installed.
1. Create a virtual environment
```
  conda create -n kgtk-env python=3.7
  conda activate kgtk-env
```
2. Install `kgtk` from the `dev` branch,
```
  cd <kgtk_root_folder>
  git checkout dev
  pip install -e .
```
3. Download `spacy` language model
```
  python -m spacy download en_core_web_sm
```
4. Install graph tools
```
  conda install -c conda-forge graph-tool
```
5. Install `rdflib` from the `master` branch
```
  pip uninstall rdflib
  pip install git+https://github.com/RDFLib/rdflib.git@2077524d43a103c3b9bf9fdd009a4942c7fff032
```
6. Install python packages for the tutorial
```
  pip install jupyterlab altair gensim papermill ipywidgets iprogress plotly
```
7. Link the virtual environment to jupyter kernel
```
  python -m ipykernel install --user --name=kgtk-env
```
8. Download the files `wikidata.sqlite3.db` (~77GB) and `text-embedding.tsv` (162 MB) from here: https://drive.google.com/drive/folders/19Swrp2ZzyHcdVE-ytapw21ug4dMeHW9y?usp=sharing beforehand.
9. Create the config file required for tutorial
```
    cd tutorial
    cp tutorial.conf.json.template tutorial.conf.json
```
Update the required parameters in the `tutorial.conf.json` file as:
 - `output_path`: Path to the output folder where the files created by the tutorial notebooks will stored.
 - `kgtk_path`: Path to the folder where `kgtk` repository is cloned
 - `wikidata_folder`: Path to the input wikidata files folder
 - `wikidata_sqlite3_db_path`: Path to the `wikidata.sqlite3.db` file downloaded in the previous step
 - `text_embedding_path`: Path to the `text-embedding.tsv` file downloaded in the previous step

A sample `tutorial.conf.json file:
```
{
	"output_path": "/Users/amandeep/Documents/kypher",
	"kgtk_path": "/Users/amandeep/Github/kgtk",
	"wikidata_folder": "/Volumes/GoogleDrive/Shared drives/KGTK/datasets/wikidataos-v4/",
	"wikidata_sqlite3_db_path": "/Users/amandeep/Downloads/wikidata.sqlite3.db",
	"text_embedding_path": "/Users/amandeep/Downloads/text-embedding.tsv"
}
```
10. Start jupyter lab
```
  jupyter lab
```
