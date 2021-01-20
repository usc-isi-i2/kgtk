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
  pip install jupyterlab altair gensim papermill ipywidgets iprogress
```
7. Link the virtual environment to jupyter kernel
```
  python -m ipykernel install --user --name=kgtk-env
```
8. Start jupyter lab
```
  cd tutorial
  jupyter lab
```
