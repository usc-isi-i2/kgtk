# KGTK Text Embedding Utilities

## Assumptions
The input is an edge file sorted by subject. 

## Usage
```
kgtk text-embedding OPTIONS
```
Computes embeddings of nodes using properties of nodes. The values are concatenated into sentences defined by a template, and embedded using a pre-trained language model.

The output is an edge file where each node appears once; a user defined property is used to store the embedding, and the value is a string containing the embedding. For example:

To generate the embeddings, the command first generates a sentence for each node using the properties listed in the label-properties, description-properties, isa-properties and has-properties options. Each sentence is generated using the following template:

```
{label-properties}, {description-properties} is a {isa-properties}, and has {has-properties}
```

An example sentence is “Saint David, patron saint of Wales is a human, Catholic priest, Catholic bishop, and has date of death, religion and canonization status”

```
subject        predicate        object
Q1        text_embedding    “0.222, 0.333, ..”
Q2        text_embedding    “0.444, 0.555, ..”
```

### Run
You can call the functions directly with given args as 
```
kgtk text-embedding \ 
    -input-file / -i <string> \ # * optional, path to the file
    --input-data-format / -f <string> \ # optional, default is `kgtk_format`
    --model / -m <list_of_string> \  # optional, default is `bert-base-wikipedia-sections-mean-tokens`
    --label-properties <list_of_string> \ # optional, default is ["label"]
    --description-properties <list_of_string> \ # optional, default is ["description"]
    --isa-properties <list_of_string> \ # optional, default is ["P31"]
    --has-properties <list_of_string> \ # optional, default is ["all"]
    --property-labels-file/ -p <string> \ #optional
    --output-data-format <string> # optional, default is `kgtk_format`
    --output-property <string> \ # optional, default is "text_embedding"
    --embedding-projector-metatada <list_of_string> \ # optional
    --embedding-projector-path/ -o <string> # optional, default is the home directory of current user
    --black-list / -b <string> # optional,default is None
    --logging-level / -l <string> \ # optional, default is `info`
    --dimensional-reduction pca \ # optional, default is none
    --dimension 5 \ #optional, default is 2
    --parallel 4 # optional, default is 1
    --save-embedding-sentence # optional
```
##### Example 1:
For easiest running, just give the input file and let it write output to `output_embeddings.csv` at current folder
`kgtk text-embedding < input_file.csv > output_embeddings.csv`
##### Example 2:
Running with more specific parameters and then run TSNE to reduce output dimension:
```
kgtk text-embedding --debug \ 
    --input-file test_edges_file.tsv \
    --model bert-base-wikipedia-sections-mean-tokens bert-base-nli-cls-token \
    --label-properties P1449 P1559 \
    --description-properties P94 \
    --dimensional-reduction tsne
```
##### Example 3:
Running with test format input and tsv output(for visulization at google embedding projector)
```
kgtk text-embedding \ 
    --input-file countries_candidates.csv \
    --model bert-base-wikipedia-sections-mean-tokens bert-base-nli-cls-token \
    --black-list all_instances_of_Q732577.tsv.zip \
    --output-data-format tsv_format
```

#### --input-file / -i (input file)
The path to the input file. For example: `input_file1.csv`, it also support to send like `< input_file1.csv`

#### --input-data-format/ -f (input format)
The input file should be a CSV file or a KGTK file.

##### KGTK edges format (`kgtk_format`)
This follow KGTK requirement, the file need to have at least following 3 columns. For detail definitions, please refer to KGTK document.
1. `node` column
This is represented as a Q node
2. `property` column
This is represented as a P node
3. `value` column
This is represtend as value type
If the input file has more than 3 columns, the input file has to have following 3 column names as : `node, property, value`
If the input file has only 3 columns, the input file will be treated as the input format as the 3 columns mentioned.
Otherwise, the function will raise the error.

##### Test data format (`test_format`)
Please refer to `countries_candidates.csv` at this folder for the example.
The file should contains following 3 columns.
1. `label` Column
Atring indicate the representation of the candidates
2. `candidates` Column
Splitted with splitting mark `|`, each Q nodes represent one possible candidate for the label
3. `GT_kg_id` Column
The correct Q node representation for the label.


#### --model/ -m Embedding_Model(s)
The embedding models want to apply on the sentences. If multiple models given, they will be applied to the same data one by one and output the results with all models.

currently followly 16 models are pretrained and could be used. If not specified, the default model will be `bert-base-wikipedia-sections-mean-tokens`
```
bert-base-nli-cls-token
bert-base-nli-max-tokens
bert-base-nli-mean-tokens
bert-base-nli-stsb-mean-tokens
bert-base-wikipedia-sections-mean-tokens
bert-large-nli-cls-token
bert-large-nli-max-tokens
bert-large-nli-mean-tokens
bert-large-nli-stsb-mean-tokens
distilbert-base-nli-mean-tokens
distilbert-base-nli-stsb-mean-tokens
distiluse-base-multilingual-cased
roberta-base-nli-mean-tokens
roberta-base-nli-stsb-mean-tokens
roberta-large-nli-mean-tokens
roberta-large-nli-stsb-mean-tokens
```
#### Sentence Embedding Vectors
##### --label-properties
an ordered list of properties. The output is the value of the first property that returns a non-empty value. 
If not given, the program will try to use the default edge(property) name as `label`. Those words in properties will be for vector embedding later.

##### --description-properties
an ordered list of properties. The output is the value of the first property that returns a non-empty value.
If not given, the program will try to use the default edge(property) name as `description`. Those words in properties will be for vector embedding later.

##### --isa-properties
an ordered list of properties. When a property contains multiple values, the first value will selected. When a property value is not a literal, output the label of the property value. When multiple isa-properties are present, the values are output comma-separated.
If not given, the program will try to use the default edge(property) name as `P31`. Those words in properties will be for vector embedding later.

##### --has-properties
an ordered list of properties. The output consists of a comma-separated text with the labels of the properties, using and for the last item, e.g., “country, place of birth, religion and canonization status” .
If not given, the program will use all of the found properties found for the node. Those words in properties will be for vector embedding later.

##### --property-value
If the properties in `has-properties` is a property which need to check for details, specify the edge name here and the system will go further to get the property values of this node instead of use the name of this edge (using template `{property} {value}`) instead of `{property}` to represent this has-property). Default is empty `[]`

For example: For wikidata node `Q41421` (Michael Jordan) `P544` (member of sports team), if specified here, the generated sentence will be `Michael Jordan, ..., has member of sports team Chicago Bulls` instead of `Michael Jordan,..., has member of sports team`. 

##### --out-properties
the property used to record the embedding. If not given, the program will use the edge(property) name as `text_embedding`.
This option is only available when output format is set to `kgtk_format`.

##### --property-labels-file
This parameter only works for KGTK format input. For some condition, KGTK format's value is just a reference to another P node. In this condition, user need to specify another label file for KGTK to read.

For example, if run without the labels file on the wikidata dump file, we will get some generated sentence like:
`WALS genus code is a Q19847637, Q20824104, and has P1855 and P2302` (sentence generated for P1467). After add the labels file, we will get the correct sentence as: `WALS genus code is a Wikidata property for an identifier, Wikidata property for items about languages, and has WALS family code and WALS lect code`.
This property labels file should also be a KGTK format file. One example file is [here](https://drive.google.com/open?id=1F7pb4LEx5MT1YTqycUCQcs8H2OWmBbB6 "here") (accessable only for KGTK developers).


#### Dimensional Reduction Algorithm

##### --dimensional-reduction
User can choose to whether run some dimensional reduction algorithm to reduce the output vector dimensions. Default is not run. 
Currently 3 choices can be made:
- `none`: not run dimensional reduction algorithm)
- `tsne`: run TSNE algorithm, note that TSNE only works for some special dimensional number
- `pca`: run PCA alogirhtm

##### --dimension
If specified to run dimensional algorithm, user can run with this choice to specify how many dimensions to keep for the final vector output.

### Output files
There will be 3 part of files:
##### Logger file
If passed with global parameter `--debug`, an extra debugging logger file will be stored at user's home directory.

##### Metadata File
User can specify where to store the metadata file for the vectors. If not given, the default is to save the metadata file at user's home directly. If set with value `none`, no metadata file will generate.

##### Embedding Vectors
This will have all the embedded vectors values for each Q nodes. This will be print on stddout and can be redirected to a file.
Note: There will only texet embedding related things outputed, please run other commands 

If output as `kgtk_format`, the output file will looks like:
```
Q1  text_embedding  0.2,0.3,0.4,0.5 
Q2  text_embedding  0.3,0.4,-0.5,-0.6
...
```
The oupput will be a TSV file with 3 columns:
First column is the node name.
Second column is the property name as required, default is `text_embedding`.
Third column is the embeded vecotrs.

##### Embedding Sentences
There is an extra optional flag `--save-embedding-sentence` for output.
If send with this flag, the embedding sentence will also generated as part of output file.
First column is the node name.
Second column is the property name `embedding_sentence`.
Third column is the embeded sentence.

##### parallel
You can also set up the parallel count to some number larger than 1 to run in multiprocess mode. Currently only support for kgtk format input data. For example: `--parallel 4`

##### Reduced Embedding Vectors
This will have embedded vectors values after running dimensional reduction algorithm and reduced dimension to 2-dimensions for each Q nodes. This is used for visulization. (for example, you can view it at Google's online tools here: http://projector.tensorflow.org/)
3. Metadata for the generated vectors: This will contains the metadata information for the Q nodes generated from 2 files mentioned above. It will contains the Q node value of each vector, the type (it is a `candidate` or a `ground truth` node), the given label of the Q node and corresponding fetched description information from wikidata.

#### Query / cache related
##### --query-server
You can change the query wikidata server address when the input format is `test_format`. The default is to use wikidata official query server, but it has limit on query time and frequency. Alternatively, you can choose to use dsbox02's one as `https://dsbox02.isi.edu:8888/bigdata/namespace/wdq/sparql` (vpn needed, only for ISI users).

##### --use-cache
If set to be true, the system will try to get the cached results for embedding computations. The default value is False, not to use cache. Basically the cache service is a Redis server.

##### --cache-host
The host address for the Redis cache service. Default is `dsbox01.isi.edu`

##### --cache-port
The host port for the Redis cache service. Default is `6379`

#### Usage of vector projector
You can apply any of the tsv vector files along with the metadata file to display it on google's tools for further experiment.
Step 1: Click the `Load` button on the left side of the web.
Step 2: Upload the vector file and metadata file.
Step 3: If you uploaded the 2 dimension version, click `Custom` view button on the left lower side.

The function will also print the average distance to the centroid (calculate by the mean value) of the ground truth nodes. Basically, the smaller the average distance is, the better clustering results are.
