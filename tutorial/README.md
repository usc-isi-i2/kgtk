# Run the following commands before running the notebooks

0. [Install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), if not already installed.
1. Create a virtual environment
```
conda create -n kgtk-env python=3.7
conda activate kgtk-env
```
2. Install `kgtk` from the `dev` branch,
```
git clone https://github.com/usc-isi-i2/kgtk
cd kgtk
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
8. Download the files needed for the tutorial from https://drive.google.com/drive/folders/19Swrp2ZzyHcdVE-ytapw21ug4dMeHW9y?usp=sharing 

- `wikidata.sqlite3.small.db` (~8GB). This file is optional. If you downloaded it, the tutorial will run much faster, as it won't have to spend time building this file. It will save you waiting for one to five minutes in some commands. 
- `wikidata.sqlite3.miniwikidata.db` (~30GB). This is a larger version of the subset of wikidata (94 million edges). The embeddings part of the tutorial only works with this version. If you are intersested in the embeddings, download this version.
- `text-embedding.tsv` (672 MB) 

9. If you are not using the cached sqlite file, you need to download the kgtk files that we use for the tutorial. These files contain the TSV files with the edges and are necessary if you want to play with KGTK commands other than `kgtk query`. Download these files from the followiing locations (Right-click on the folder and select `Download`):

- minimal version of Wikidata sufficient for the first parts of the tutoria, but not adequate for the embeddings: 
https://drive.google.com/drive/folders/1nDeNpYF8pdnN9pgD-vhbGNP4mmfiJgRJ?usp=sharing. 
- miniwikidata with 90 million edges, appropriate for running all parts of the tutorial: https://drive.google.com/drive/folders/140iWPMHdmIG2weBgiMqeXs-7qfU3glA7?usp=sharing

10. Create the config file required for tutorial
```
cd tutorial
cp tutorial.conf.json.template tutorial.conf.json
```
Update the required parameters in the `tutorial.conf.json` file as:
 - `output_path`: Path to the output folder where the files created by the tutorial notebooks will be stored.
 - `kgtk_path`: Path to the folder where `kgtk` repository is cloned
 - `wikidata_folder`: Path to the input wikidata files folder
 - `wikidata_sqlite3_db_path`: Path to the `wikidata.sqlite3.db` file downloaded in the previous step
 - `text_embedding_path`: Path to the `text-embedding.tsv` file downloaded in the previous step

A sample `tutorial.conf.json` file:
```
{
	"output_path": "/Users/pedroszekely/Downloads/kgtk-tutorial",
	"kgtk_path": "/Users/pedroszekely/Documents/GitHub/kgtk",
	"wikidata_folder": "/Users/pedroszekely/Downloads/kgtk-tutorial/wikidataos-v4-mm/",
	"wikidata_sqlite3_db_path": "/Users/pedroszekely/Downloads/kgtk-tutorial/wikidata.sqlite3.small.db",
	"text_embedding_path": "/Users/pedroszekely/Downloads/kgtk-tutorial/text-embedding.tsv"
}
```

> If you want to use the downloaded cached sqlite file, then the `wikidata_folder` must be set to one of the following values (the trailing slash is important):

- `"/Users/pedroszekely/Downloads/kgtk-tutorial/wikidataos-v4-mm/"` if you use the small file `wikidata.sqlite3.small.db` or
- `"/Users/pedroszekely/Downloads/kgtk-tutorial/miniwikidata/"` if you use the larger  file `wikidata.sqlite3.miniwikidata.db`

The reason to use this values is that the cache believes the files are in Pedro Szekely's machine, and if you put the files somewhere else, KGTK will think the files changed and will reload them in the database, defeating the benefit of the cache.

This config file corresponds to a simple setup where all the relevant files for the tutorial are placed in the same directory (if you use miniwikidata the structure is similar but the files are different):
```bash
(base) D22ML-PSZEKELY:kgtk-tutorial pedroszekely$ ls -l
total 18733072
-rw-r--r--@  1 pedroszekely  staff   704327851 Jan 23 13:35 text-embedding.tsv
-rw-r--r--@  1 pedroszekely  staff  8881557504 Jan 23 13:56 wikidata.sqlite3.small.db
drwxr-xr-x  13 pedroszekely  staff         416 Jan 23 14:00 wikidataos-v4-mm
(base) D22ML-PSZEKELY:kgtk-tutorial pedroszekely$ ls -l wikidataos-v4-mm/
total 1645104
-rw-r--r--@ 1 pedroszekely  staff   10619848 Jan 22 09:36 aliases.en.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff    2868983 Jan 22 15:52 all.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff  315694467 Jan 22 09:35 claims.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff  107407920 Jan 22 09:48 claims.wikibase-item.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff   11596558 Jan 22 15:09 derived.P279.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff  163532619 Jan 22 14:48 derived.P279star.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff  132037407 Jan 22 14:45 derived.isa.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff   21647502 Jan 22 09:36 descriptions.en.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff   37127213 Jan 22 09:35 labels.en.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff      46075 Jan 22 15:33 metadata.property.datatypes.tsv.gz
-rw-r--r--@ 1 pedroszekely  staff   39692305 Jan 22 09:41 qualifiers.tsv.gz
(base) D22ML-PSZEKELY:kgtk-tutorial pedroszekely$
```

11. Test that kgtk is installed properly
```bash
kgtk --help
```
The shell should show the following (and many more lines):
```bash
usage: kgtk [options] command [ / command]*

kgtk --- Knowledge Graph Toolkit
```
12. Start jupyter lab
```
jupyter lab
```
