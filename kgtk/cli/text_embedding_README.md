# KGTK Text Embedding Utilities
## Install
The program requires Python vesion >= `3` and `kgtk` package installed.
The corresponding packages requirement are stored at `text_embedding_requirement.txt`

## Usage
### Run
You can call the functions directly with given args as 
```
kgtk text_embedding \ 
    --input/ -i <string> \ # * required, path to the file
    --format/ -f <string> \ # optional, default is `kgtk_format`
    --model/ -m <list_of_string> \  # optional, default is `bert-base-wikipedia-sections-mean-tokens`
    --label-properties <list_of_string> \ # optional, default is ["label"]
    --description-properties <list_of_string> \ # optional, default is ["description"]
    --isa-properties <list_of_string> \ # optional, default is ["P279"]
    --has-properties <list_of_string> \ # optional, default is ["all"]
    --property-labels-file/ -p <string> \ #optional
    --output-format <string> # optional, default is `kgtk_format`
    --output-property <string> \ # optional, default is "text_embedding"
    --embedding-projector-metatada <list_of_string> \ # optional
    --embedding-projector-path/ -o <string> # optional, default is the home directory of current user
    --black-list/ -b <string> # optional,default is None
    --logging-level/ -l <string> \ # optional, default is `info`
    --run-TSNE False # optional, default is True
```
##### Example 1:
For easiest running, just give the input file as 
`kgtk text_embedding -i input_file.csv`
##### Example 2:
Running with more specific parameters and not run TSNE (output original embedding vectors):
```
kgtk text_embedding \ 
    --input test_edges_file.tsv \
    --model bert-base-wikipedia-sections-mean-tokens bert-base-nli-cls-token \
    --label-properties P1449 P1559 \
    --description-properties P94 \
    --logging-level debug \
    --run-TSNE false
```
##### Example 3:
Running with test format input and tsv output(for visulization at google embedding projector)
```
kgtk text_embedding \ 
    --countries_candidates.csv \
    --model bert-base-wikipedia-sections-mean-tokens bert-base-nli-cls-token \
    --black-list all_instances_of_Q732577.tsv.zip \
    --output-format tsv_format
```

#### --input / -i (input files)
The path to the input file(s). If multiple file given, please separate each with a white space ` `.

For example: `input_file1.csv input_file2.csv`

#### --format/ -f (input format)
The input file should be a CSV file, it support 2 different type of input for different purposes.

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
#### sentence embedding vectors
##### --label-properties
an ordered list of properties. The output is the value of the first property that returns a non-empty value. 
If not given, the program will try to use the default edge(property) name as `label`. Those words in properties will be for vector embedding later.

##### --description-properties
an ordered list of properties. The output is the value of the first property that returns a non-empty value.
If not given, the program will try to use the default edge(property) name as `description`. Those words in properties will be for vector embedding later.

##### --isa-properties
an ordered list of properties. When a property contains multiple values, the first value will selected. When a property value is not a literal, output the label of the property value. When multiple isa-properties are present, the values are output comma-separated.
If not given, the program will try to use the default edge(property) name as `P279`. Those words in properties will be for vector embedding later.

##### --has-properties
an ordered list of properties. The output consists of a comma-separated text with the labels of the properties, using and for the last item, e.g., “country, place of birth, religion and canonization status” 
If not given, the program will use all of the found properties found for the node. Those words in properties will be for vector embedding later.

##### --out-properties
the property used to record the embedding. If not given, the program will use the edge(property) name as `text_embedding`.
This option is only available when output format is set to `kgtk_format`.

### Output
There will be 2 part of files:
##### --run-TSNE
User can choose to whether run TSNE to reduce the dimension of the output vectors after getting the embeding vectors or not. The default is True.

##### Original Embedding Vectors
This will have all the embedded vectors values for each Q nodes. This will be print on stddout and can be redirected to a file.

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

##### Reduced Embedding Vectors
This will have embedded vectors values after running TSNE and reduced dimension to 2-dimensions for each Q nodes. This is used for visulization. (for example, you can view it at Google's online tools here: http://projector.tensorflow.org/)
3. Metadata for the generated vectors: This will contains the metadata information for the Q nodes generated from 2 files mentioned above. It will contains the Q node value of each vector, the type (it is a `candidate` or a `ground truth` node), the given label of the Q node and corresponding fetched description information from wikidata.

#### Usage of vector projector
You can apply any of the tsv vector files along with the metadata file to display it on google's tools for further experiment.
Step 1: Click the `Load` button on the left side of the web.
Step 2: Upload the vector file and metadata file.
Step 3: If you uploaded the 2 dimension version, click `Custom` view button on the left lower side.

The function will also print the average distance to the centroid (calculate by the mean value) of the ground truth nodes. Basically, the smaller the average distance is, the better clustering results are.