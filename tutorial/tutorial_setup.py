import io
import os
import subprocess
import sys
import tempfile
import re

import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from gensim.models import KeyedVectors

import altair as alt

import papermill as pm


########################
# Parameters

# Folder on local machine where to create the output and temporary folders
output_path = "/Users/pedroszekely/Downloads/kypher"

# The location of the KGTK installation
kgtk_path = "/Users/pedroszekely/Documents/GitHub/kgtk"

# The names of the output and temporary folders
output_folder = "wikidata_os_v5"
temp_folder = "temp.wikidata_os_v5"

# The location of input Wikidata files
wikidata_folder = "/Volumes/GoogleDrive/Shared drives/KGTK/datasets/wikidata-20200803-v4/"
wikidata_folder = "/Users/pedroszekely/Downloads/kypher/wikidata_os_v1/"
# The wikidata_os files can be downloaded from https://drive.google.com/drive/folders/1V6oAQKmwQ4LJnrBai-uv5gHWphFSCt50?usp=sharing

# Location of the cache database for kypher
cache_path = "/Users/pedroszekely/Downloads/kypher/temp.useful_wikidata_files_v4"

# Whether to delete the cache database
delete_database = False

# shortcuts to commands
kgtk = "time kgtk --debug"
# kgtk = "kgtk --debug"

########################

# The names of files in the KGTK Wikidata distirbution that we will use in this notebook.
file_names = {
    "claims": "claims.tsv.gz",
    "label": "labels.en.tsv.gz",
    "all": "all.tsv.gz",
    "alias": "aliases.en.tsv.gz",
    "description": "descriptions.en.tsv.gz",
    "item": "claims.wikibase-item.tsv.gz",
    "qualifiers": "qualifiers.tsv.gz",
    "sitelinks": "sitelinks.tsv.gz",
    "qualifiers_time": "qualifiers.time.tsv.gz",
    "property_datatypes": "metadata.property.datatypes.tsv.gz",
    "isa": "derived.isa.tsv.gz",
    "p279star": "derived.P279star.tsv.gz",
    "p279": "derived.P279.tsv.gz"
}

# We will define environment variables to hold the full paths to the files as we will use them in the shell commands
kgtk_environment_variables = []

os.environ['WIKIDATA'] = wikidata_folder
kgtk_environment_variables.append('WIKIDATA')

for key, value in file_names.items():
    variable = key.upper()
    os.environ[variable] = wikidata_folder + value
    kgtk_environment_variables.append(variable)

    
# KGTK creates a SQLite database to index the knowledge graph.
if cache_path:
    os.environ['STORE'] = "{}/wikidata.sqlite3.db".format(cache_path)
else:
    os.environ['STORE'] = "{}/{}/wikidata.sqlite3.db".format(output_path, temp_folder)
kgtk_environment_variables.append('STORE')

# We will create many temporary files, so set up a folder for outputs and one for the temporary files.
os.environ['TEMP'] = "{}/{}".format(output_path, temp_folder) 
os.environ['OUT'] = "{}/{}".format(output_path, output_folder) 
kgtk_environment_variables.append('TEMP')
kgtk_environment_variables.append('OUT')

# Envronment variables with shortcuts to the commands we use often
os.environ['kgtk'] = kgtk
os.environ['kypher'] = "kgtk query --graph-cache " + os.environ['STORE']
os.environ['kypherd'] = "time kgtk --debug query --graph-cache " + os.environ['STORE']
os.environ['kypher_raw'] = "kgtk query --graph-cache " + os.environ['STORE']
kgtk_environment_variables.append('kgtk')
kgtk_environment_variables.append('kypher')

# Directory where the notebooks live
os.environ["EXAMPLES_DIR"] = kgtk_path + "/examples"
kgtk_environment_variables.append('EXAMPLES_DIR')

# Directories for the embeddings
os.environ['GE'] = os.environ['TEMP'] + "/graph-embedding"
os.environ['TE'] = os.environ['TEMP'] + "/text-embedding"
kgtk_environment_variables.append('GE')
kgtk_environment_variables.append('TE')

for key, value in file_names.items():
    q154_variable = "Q154" + key.upper()
    os.environ[q154_variable] = os.environ['OUT'] + "/parts/" + value
    kgtk_environment_variables.append(q154_variable)

kgtk_environment_variables.sort()
for variable in kgtk_environment_variables:
    print("{}: \"{}\"".format(variable, os.environ[variable]))

############################################



def kgtk_to_dataframe(kgtk):
    columns = kgtk[0].split("\t")
    data = []
    for line in kgtk[1:]:
        data.append(line.split("\t"))
    return pd.DataFrame(data, columns=columns)
    