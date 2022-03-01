# Configure KGTK Notebooks

[KGTK Notebooks](https://github.com/usc-isi-i2/kgtk-notebooks) has a rich set of notebooks to demonstrate [KGTK](https://github.com/usc-isi-i2/kgtk) commands 
and use cases.

The KGTK notebooks often have similar setup cells at the start. For example, setting up the SQLite Cache DB, environment variables, a TEMP directory and so on. 
[Configure KGTK Notebooks](https://github.com/usc-isi-i2/kgtk/blob/master/kgtk/configure_kgtk_notebooks.py) is written to make the notebook setup easy and consistent.

We will go through the steps to initialize this class and discuss the parameters and functions in detail.

## Initialize ConfigureKGTK
Import the class ,

```
from kgtk.configure_kgtk_notebooks import ConfigureKGTK
```

Create the class object ,

```
ck = ConfigureKGTK(file_list: List[str],
                   kgtk_path: str = None,
                   input_files_url: str = None)
```

The class constructor has 3 parameters, let's discuss each of them in detail.

#### file_list

`file_list` is a **required** parameter and is a list of file ***names***. KGTK has standard *names* for the common KGTK Edge files, for example:


- **alias**: aliases.en.tsv.gz
- **monolingualtext**: claims.monolingualtext.tsv.gz
- **label**: labels.en.tsv.gz
- **datatypes**: metadata.property.datatypes.tsv.gz and so on...

There are a total of 93 file `names`, the full list is [here](https://github.com/usc-isi-i2/kgtk/blob/master/kgtk/files_config.py)

`file_list` is a list of files in the input path, which will be used in the current KGTK notebook.

#### kgtk_path

`kgtk_path` is the absolute path to the cloned `kgtk` folder. This parameter is **optional**. It is required when the current KGTK notebook will call 
another KGTK notebook as part of its execution.

If not specified, `kgtk_path` will be set to the parent of current directory.

#### input_files_url

`input_files_url` is an **optional** parameter to specify the URL to download the `file_list` from, in case the input path is not specified.

If not specified, this parameter will be set to `https://github.com/usc-isi-i2/kgtk-tutorial-files/raw/main/datasets/arnold` which contains the files for ISWC tutorial.

## Configure the Environment Variables

Call the function `configure_kgtk`, signature:

```
ck.configure_kgtk(input_graph_path: str = None,
               project_name: str = "kgtk",
               output_path: str = None,
               graph_cache_path: str = None,
               json_config_file: str = None,
               additional_files: dict = None,
               debug=False)
```

The parameters are all **optional** with reasonable defaults. Details ,

#### input_graph_path

`input_graph_path` is an absolute path to a folder where the files specified by **file_list** should be present.

If not specified, the default value of this parameter will be: `USER_HOME/isi-kgtk-tutorial`.

#### project_name

`project_name` is the name of the folder where the output files will be created. Defaults to `kgtk`.

#### output_path

`output_path` is the absolute path where the output files will be created. If not specified, the default value will be set to 
`USER_HOME/isi-kgtk-tutorial/kgtk`

#### graph_cache_path

`graph_cache_path` point to the SQLite graph cache used in `kypher`.

If not specified, the default value will be calculated as: `{output_path}/{project_name}/temp.{project_name}/wikidata.sqlite3.db`.

For example, if `output_path` = **/data/amandeep/wikidata-20211027-dwd-v3** and 
                `project_name` = **useful-files**, then
                `graph_cache_path` = **/data/amandeep/wikidata-20211027-dwd-v3/temp.useful-files/wikidata.sqlite3.db**

#### json_config_file

`json_config_file` is absolute path to a json file with additional `names` to file name mapping. 

Suppose there are additional files you want to use that are 
outside the [official kgtk file list](https://github.com/usc-isi-i2/kgtk/blob/master/kgtk/files_config.py), you can then create a json file and specify the path
to `json_config_file`.

For example, the file can look like: 
```
{
  'augmented_datatypes': 'augmented_datatypes.tsv.gz',
  'augmented_wikianchor': 'wikitables.anchor.tsv.gz'
}
```

#### additional_files

`additional_files` is a dictionary of the same format as `json_config_file`, it can also be used to specify additional files to be used while processing the 
current notebook.

For example, the following dictionary can be supplied ,
```
{
  'augmented_datatypes': 'augmented_datatypes.tsv.gz',
  'augmented_wikianchor': 'wikitables.anchor.tsv.gz'
}
```

#### debug

`debug` adds the option `--debug` to all the kgtk commands being used in the current notebook.

## Print Environment variables

You can call the function `print_env_variables`,
```
ck.print_env_variables()
```
to print out all the environment variables setup by `ConfigureKGTK` class.

In addition to all the files you specify using the `file_list` parameter, this class will setup a few additional environment variables.

For example, if you have the following files, 
```
['claims', 'label_all', 'alias_all', 'description_all']
```
the output of `ck.print_env_variables()` can look like ,

```
KGTK_OPTION_DEBUG: false
TEMP: /data/amandeep/wikidata-20211027-dwd-v3/useful-files/temp.useful-files
EXAMPLES_DIR: /Users/amandeep/github/kgtk/examples
KGTK_LABEL_FILE: /data/amandeep/wikidata-20211027-dwd-v3/labels.en.tsv.gz
STORE: /data/amandeep/wikidata-20211027-dwd-v3/useful-files/temp.useful-files/wikidata.sqlite3.db
kgtk: kgtk
KGTK_GRAPH_CACHE: /data/amandeep/wikidata-20211027-dwd-v3/useful-files/temp.useful-files/wikidata.sqlite3.db
GRAPH: /data/amandeep/wikidata-20211027-dwd-v3
USE_CASES_DIR: /Users/amandeep/github/kgtk/use-cases
OUT: /data/amandeep/wikidata-20211027-dwd-v3/useful-files
kypher: kgtk query --graph-cache /data/amandeep/wikidata-20211027-dwd-v3/useful-files/temp.useful-files/wikidata.sqlite3.db
claims: /data/amandeep/wikidata-20211027-dwd-v3/claims.tsv.gz
label_all: /data/amandeep/wikidata-20211027-dwd-v3/labels.tsv.gz
alias_all: /data/amandeep/wikidata-20211027-dwd-v3/aliases.tsv.gz
description_all: /data/amandeep/wikidata-20211027-dwd-v3/descriptions.tsv.gz
```

A few notable mentions ,

- `STORE` =  `KGTK_GRAPH_CACHE`: the path to kypher graph cache.
- `GRAPH`: path where all input files should be present.
- `OUT`: output path.
- `TEMP`: a folder inside the `OUT` path to keep temporary files.

## Load Files into Cache

Next step is to load the files in `file_list` into graph cache.
```
ck.load_files_into_cache()
```

This function call will load all the files in `file_list` plus any additional files specified by `json_config_file` and `additional_files` in to the cache.

The file `names` will be used as aliases for the files, for example, continuing from the previous step,
```
kgtk query --graph-cache /data/amandeep/wikidata-20211027-dwd-v3/useful-files/temp.useful-files/wikidata.sqlite3.db 
  -i "/data/amandeep/wikidata-20211027-dwd-v3/claims.tsv.gz" --as claims  
  -i "/data/amandeep/wikidata-20211027-dwd-v3/labels.tsv.gz" --as label_all  
  -i "/data/amandeep/wikidata-20211027-dwd-v3/aliases.tsv.gz" --as alias_all  
  -i "/data/amandeep/wikidata-20211027-dwd-v3/descriptions.tsv.gz" --as description_all  --limit 3
```

|id                         |node1|label|node2                                |rank  |node2;wikidatatype|
|---------------------------|-----|-----|-------------------------------------|------|------------------|
|P10-P1628-32b85d-7927ece6-0|P10  |P1628|http://www.w3.org/2006/vcard/ns#Video|normal|url               |
|P10-P1628-acf60d-b8950832-0|P10  |P1628|https://schema.org/video             |normal|url               |
|P10-P1629-Q34508-bcc39400-0|P10  |P1629|Q34508                               |normal|wikibase-item     |


Notice the files are loaded with an alias, `"/data/amandeep/wikidata-20211027-dwd-v3/claims.tsv.gz" --as claims`.

At this step, the notebook setup is complete with set environment variables.
