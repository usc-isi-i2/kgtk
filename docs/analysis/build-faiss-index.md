## Overview

The `build_faiss` command creates a trained Faiss index for performing nearest neighbor searches on a given set of vectors. This is intended to be used for graph embeddings, so we accept the output formats of the `graph_embeddings` command as input and set default parameter values to those suitable for a graph with ~50M nodes. 

## Input format

There are three  supported formats: glove, w2v, and kgtk.

### glove format
When using this format, the input is a .tsv file where each line is the embedding for a node. Each line is represented by a single node followed respectively by the components of its embedding, each in a different column, all separated by tabs. For example: 
```
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
```

### w2v format (default)
When using this format, the input is a .tsv file which is almost the same as the glove format. The only difference is that the word2vec format has a first line which indicates the shape of the embeddings (e.g., "9 4" for 9 entities with 4 dimensions). Each column of the first line is separated by tabs. For example:
```
16213    100 
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
"home"    -0.014021411    -0.090830070    -0.012534120    -0.073111301    -0.068317516 ...
```
Here 16231 represents the number of nodes, 100 represents the dimension of each node's embedding.

### kgtk format
When using this format, the input is a .tsv file where each line contains three columns describing the embedding for a node. In each line, the first column contains a node, the second contains a label (which we ignore), and the third contains the node's embedding as a comma-separated string of floats. The first row of the file is assumed to contain a header unless specified otherwise by the `--no_input_header` option. For example: 
```
node1   label   node2
Q5    graph_embeddings   014022544,-0.062030070,-0.012535412,0.038317516 
Q6    graph_embeddings   014022544,-0.062030070,-0.012535412,0.038317516 
```

## Output

This command saves the created Faiss index in a `.idx` file and optionally saves a second file that contains a mapping from each node's index in the Faiss index to itself. 

## Usage

```bash
usage: kgtk build-faiss [-h] -i EMBEDDINGS_FILE -o INDEX_FILE_OUT [-id2n INDEX_TO_QNODE_FILE_OUT] [-ef kgtk|w2v|glove]
                        [--no_input_header [True|False]] [-te MAX_TRAIN_EXAMPLES] [-w WORKERS] [-is INDEX_STRING]
                        [-m Inner_product|L2|L1|Linf|Lp|Canberra|BrayCurtis|JensenShannon] [-ma METRIC_ARG]
                        [-v [optional True|False]]

Train and populate a faiss index that can compute nearest neighbors of given embeddings.

optional arguments:
  -h, --help            show this help message and exit
  -i EMBEDDINGS_FILE, --input_file EMBEDDINGS_FILE, --embeddings_file EMBEDDINGS_FILE
                        Input file containing the embeddings for which a Faiss index will be created.
  -o INDEX_FILE_OUT, --output_file INDEX_FILE_OUT, --index_file_out INDEX_FILE_OUT
                        Output .idx file where the index fill be saved.
  -id2n INDEX_TO_NODE_FILE_OUT, --index_to_node_file_out INDEX_TO_NODE_FILE_OUT
                        Output Kgtk-format file containing index --> node.
  -ef kgtk|w2v|glove, --embeddings_format kgtk|w2v|glove
                        Format of the input embeddings [Default: w2v] Choice: kgtk | w2v | glove
  --no_input_header [True|False]
                        If your input embeddings file is in KGTK format, this allows you to specify if it has a header
                        line or not.
  -te MAX_TRAIN_EXAMPLES, --max_train_examples MAX_TRAIN_EXAMPLES
                        The maximum number of embeddings that will be used to train the index.
  -w WORKERS, --workers WORKERS
                        The number of worker processes for training. If not given, set to CPU count.
  -is INDEX_STRING, --index_string INDEX_STRING
                        A string denoting the type of index to be used. This will be passed to faiss.index_factory()
  -m Inner_product|L2|L1|Linf|Lp|Canberra|BrayCurtis|JensenShannon, --metric_type Inner_product|L2|L1|Linf|Lp|Canberra|BrayCurtis|JensenShannon
                        A string denoting the Faiss metric to be used. This will be passed to faiss.index_factory().
  -ma METRIC_ARG, --metric_arg METRIC_ARG
                        If you choose Lp as your metric_type, this parameter should be used to specify the value of p
                        to use.

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Index design considerations

There are several parameters that affect the index's performance in terms of accuracy, space, query time, and training time.

### Index_string

The `index_string` is passed to faiss.index_factory() and controls many options for how the index will be built. For further details on how to format this string, please refer to [the official Faiss documentation](https://github.com/facebookresearch/faiss/wiki/The-index-factory).

When deciding on an index to use, please refer to [this documentation](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index). One important decision to be made is the number of centroids to learn. This decision will impact training-time and query-time. A higher number of centroids will lead to longer training time and shorter query time. A heuristic to follow here is to choose a function of `sqrt(N)` where `N` is the number of nodes to index. As mentioned previously, the default parameter values have been chosen to handle an input size of ~50M nodes. The Faiss documentation linked above advises choosing 262,144 (2^18) as the number of centroids for this input size. However, we instead choose 8,192 (2^13) as this is ~1*sqrt(50M), and this significantly decreases training time while keeping query time reasonable. If query time is too slow for your use-case, increase the number of centroids accordingly.

### Max_train_examples

This parameter limits the number of vectors that will be used to train the index. Having more vectors to train on will make the index more accurate, however there are diminishing returns. Based on [this discussion](https://github.com/facebookresearch/faiss/issues/126), having k*1000 training examples where k is the number of centroids is safely sufficient. Therefore, we set a default value of 10M based on the default number of centroids chosen for the `index_string` parameter.

## Notes on memory usage

Faiss stores all vectors in memory, so running this command (as well as later loading the index it creates) will require that you can fit all vectors in memory. For reference, running this command with the default settings for ~50M vectors of dimension 100 creates a .idx file that is ~21GB. If you have stricter memory requirements, you can choose to compress your vectors (relevant Faiss documentation [here](https://github.com/facebookresearch/faiss/wiki/Lower-memory-footprint) which will have the tradeoff of causing the distance calculations to be estimates. Opting for vector compression can be done via the `index_string`.

Another option for reducing RAM requirements is to [shard the index](https://github.com/facebookresearch/faiss/wiki/Indexes-that-do-not-fit-in-RAM). This command does not support index sharding at this time.


## Examples

### Example 1
Default settings for w2v-format embeddings
```
kgtk build_faiss -i w2v_embeddings.tsv  -o index_file_out.idx
```

The index will be saved in `index_file_out.idx`


### Example 2
Running with more specific parameters (glove format input embeddings, saving the index-->node mapping to a file, 65,536 clusters for the index to learn, 25M vectors to train on, and using inner product as the distance metric):
```
kgtk build_faiss -i glove_embeddings.tsv -o index_file_out.idx 
    --embedding_format glove \
    --index_to_node_file_out id2n_mapping.tsv \
    --index_string IVF65536_HNSW32,Flat \
    --max_train_examples 25000000 \
    --metric_type Inner_product
```

The index will be saved in `index_file_out.idx` and the index-->node mapping file will be saved in `id2n_mapping.tsv`.
`id2n_mapping.tsv` may look like
```
node1   label   node2
0   index_to_node   Q30
1   index_to_node   Q5
...
```

