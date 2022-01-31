# KGTK Text Embedding Utilities

## Assumptions
The input is a KGTK edge file.

## Usage
```
kgtk text-embedding OPTIONS
```
Computes embeddings of nodes using properties of nodes using a pre-trained language model.

The output is an edge file where each node appears once; a user defined property is used to store the embedding, and the value is a string containing the embedding. For example:

To create a sentence for a Qnode using the properties, please run the [kgtk lexicalize](../transform/lexicalize.md) command.

An example input sentence is “Saint David, patron saint of Wales is a human, Catholic priest, Catholic bishop, and has date of death, religion and canonization status”


| subject  |  predicate  |  object  |
| -- | -- | -- |
|  Q1    |   text_embedding   | “0.222, 0.333, ..” |
|  Q2    |   text_embedding   | “0.444, 0.555, ..” |


### Run
You can call the functions directly with given args as 

```
kgtk text-embedding \ 
    -input-file / -i <string> \ # * optional, path to the file
    --model / -m <list_of_string> \  # optional, default is `bert-base-wikipedia-sections-mean-tokens`
    --output-data-format <string> {w2v, kgtk}, default is `kgtk`
    --output-property <string> \ # optional, default is "text_embedding"
    --out-file/ -o <string> \ by default embeddings to console
    --sentence-property \ The name of the property with sentence for each Qnode. Default is 'sentence'
    --batch-size The number of sentences to be processed at a time. Default is 100000. Set this value to '-1' to process the whole file as one batch
```
##### Example 1:
For easiest running, just give the input file and let it write output to `output_embeddings.csv` at current folder
using `kgtk text-embedding -i input_file.csv -o output_embeddings.csv`
##### Example 2:
Running with more specific parameters:
```
kgtk text-embedding --debug \ 
    --input-file test_edges_file.tsv \
    --model bert-base-wikipedia-sections-mean-tokens bert-base-nli-cls-token \
    --sentence-property sentence
```

#### --input-file / -i (input file)
The path to the input file. For example: `input_file1.csv`, it also support to send like `< input_file1.csv`

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

#### --output-property
the property used to record the embedding. If not given, the program will use the edge(property) name as `text_embedding`.
This option is only available when output format is set to `kgtk`.

####  --sentence-property 
The name of the property with sentence for each Qnode. Default is 'sentence'

####  --batch-size 
The number of sentences to be processed at a time. Default is 100000. Set this value to '-1' to process the whole file as one batch

### Output files
There will be 3 part of files:
##### Logger file
If passed with global parameter `--debug`, an extra debugging logger file will be stored at user's home directory.

##### Embedding Vectors
This will have all the embedded vectors values for each Q nodes. This will be print on stddout and can be redirected to a file.
Note: There will only texet embedding related things outputed, please run other commands 

If output as `kgtk`, the output file will looks like:

|  |  |  |
| -- | -- | -- |
| Q1 | text_embedding | 0.2,0.3,0.4,0.5 |
| Q2 | text_embedding | 0.3,0.4,-0.5,-0.6 |


The output will be a TSV file with 3 columns:
First column is the node name.
Second column is the property name as required, default is `text_embedding`.
Third column is the embeded vecotrs.

