## Overview

The convert-embeddings-command converts a [KGTK edge file](../specification.md/#edge-file-format)
to word2vec format or Google Projector files format. Currently, only these two file formats are supported, more file formats will be added in a later revision of the command.

The vectors produced by the [text-embeddings](../analysis/text_embedding.md) and the [graph-embeddings](../analysis/graph_embeddings.md)
commands are stored as `,`(comma) separated string in `node2`.

### Word2vec Format

The word2vec is a text file, where the first line has the number of vectors in the file and the dimension of each vector.

There is one line per entity, with entity id and the vector components separated by `space`.

### Google Projector File(s) Format

[Google Projector](https://projector.tensorflow.org/) allows users to visualize high dimensional vectors. Google projector
requires two files, an `embeddings` file and a `metadata` file.

The `embeddings` file contains vectors for each entity, with vector components separated by `tabs`.

The `metadata` file contains information about each entity like label, description, counts etc. The order of entities in the `metadata`
file should be same as the `embeddings` file.


## Usage
```
usage: kgtk convert-embeddings-format [-h] [-i INPUT_FILE]
                                      [--node-file NODE_FILE] [-o OUTPUT_FILE]
                                      [--metadata-file METADATA_FILE]
                                      [--input-property INPUT_PROPERTY]
                                      [--output-format OUTPUT_FORMAT]
                                      [--metadata-columns METADATA_COLUMNS]

Converts KGTK edge embeddings file to word2vec or Google Projector format.Takes an optional node file for Google Project format to create a metadata file. Processes only top 10,000 rows from the edge file for Google Projector as it only accepts 10,000 rows.
Additional options are shown in expert help.
kgtk --expert convert-embeddings-format --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        KGTK input files (May be omitted or '-' for stdin.)
  --node-file NODE_FILE
                        The KGTK node file for creating Google Projector
                        Metadata. All the columns in the node file will be
                        added to the metadata file by default. You can
                        customise this with the --metadata-columns option.
                        (Optional)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --metadata-file METADATA_FILE
                        The output metadata file for Google Projector. If
                        --output-format == gprojector and--metadata-file is
                        not specified, a file named
                        `kgtk_embeddings_gprojector_metadata.tsv` will be
                        created in USER_HOME (Optional)
  --input-property INPUT_PROPERTY
                        The property name for embeddings in the input KGTK
                        edge file. (default=embeddings).
  --output-format OUTPUT_FORMAT
                        The desired output file format: word2vec|gprojector
                        (default=word2vec)
  --metadata-columns METADATA_COLUMNS
                        A comma separated string of columns names in the input
                        file or the --node-file to be used for creating the
                        metadata file for Google projector. Only to be used
                        when --output-format == 'gprojector'. If --node-file
                        is specified, the command will look for --metadata-
                        columns in the --node-file, otherwise input file.The
                        command will throw an error if the columns specified
                        are not in either of the files.
```

## Examples

### Convert KGTK to word2vec format

```
kgtk convert-embeddings-format -i examples/doc/convert_embeddings_edge.tsv --input-property graph_embeddings -o embeddings_word2vec.txt
```

Let's look at the output word2vec file ,
```
>>>head embeddings_word2vec.txt

19 30
Q494335 -0.162911773 0.071842454 -0.223435551 -0.289004564 0.834948838 ...
Q1278301 0.039679553 -0.115788229 -0.179974616 0.590080559 0.158913493 ...
Q611586 -0.015744781 -0.020170633 -0.313573331 0.515067458 0.039014913 ...
Q816369 0.488982528 -0.719077468 0.109514274 0.301486224 -0.402110636 ...
Q26833575 0.095825180 -0.207610607 -0.293776900 0.226735979 0.113529690 ...

```

### Convert KGTK to gprojector format, use all columns in the node file for metadata

```
kgtk convert-embeddings-format \
  -i examples/doc/convert_embeddings_edge.tsv  \
  --node-file examples/doc/convert_embeddings_node.tsv \
  --output-format gprojector \
  --input-property graph_embeddings \
  --metadata-file gprojector_metadata.tsv \
  -o embeddings_gprojector.tsv
```

Let's take a look at the `metadata` and `embeddings` file ,

```
>>> head gprojector_metadata.tsv
```

|id       |label       |type        |type_label  |
|---------|------------|------------|------------|
|Q494335  |Tours University|Q3551775    |university in France|
|Q1278301 |Robert Bouline|Q5          |human       |
|Q611586  |William Monahan|Q5          |human       |
|Q816369  |rated voltage|Q25428      |voltage     |

```
>>> head embeddings_gprojector.tsv
```

|-0.162911773|0.071842454 |-0.223435551|-0.289004564|0.834948838 |-0.373376131|1.436196566|-0.942946911|...         |
|------------|------------|------------|------------|------------|------------|-----------|------------|------------|
|0.039679553 |-0.115788229|-0.179974616|0.590080559 |0.158913493 |0.008464743 |0.712676883|0.380636603 |...         |
|-0.015744781|-0.020170633|-0.313573331|0.515067458 |0.039014913 |-0.114478707|0.770638645|0.304640383 |...         |
|0.488982528 |-0.719077468|0.109514274 |0.301486224 |-0.402110636|0.291337997 |0.829619348|-0.365474463|...         |
|0.095825180 |-0.207610607|-0.293776900|0.226735979 |0.113529690 |0.536592960 |0.747583449|-0.221452087|...         |




### Convert KGTK to gprojector format, use columns: `label` and `type_label` in the node file for metadata

```
kgtk convert-embeddings-format \
  -i examples/doc/convert_embeddings_edge.tsv  \
  --node-file examples/doc/convert_embeddings_node.tsv \
  --metadata-columns label,type_label \
  --output-format gprojector \
  --input-property graph_embeddings \
  --metadata-file gprojector_metadata.tsv \
  -o embeddings_gprojector.tsv
```

Let's take a look at the customized metadata file

```
>>> head gprojector_metadata.tsv
```

|label    |type_label  |
|---------|------------|
|Tours University|university in France|
|Robert Bouline|human       |
|William Monahan|human       |
|rated voltage|voltage     |
|France-Guernsey border|international border|

### Convert KGTK to gprojector format, use columns: `node1_label` and `type` in the edge file for metadata

```
kgtk convert-embeddings-format \
  -i examples/doc/convert_embeddings_edge.tsv  \
  --metadata-columns node1_label,type \
  --output-format gprojector \
  --input-property graph_embeddings \
  --metadata-file gprojector_metadata.tsv \
  -o embeddings_gprojector.tsv
```

Let's take a look at the customized metadata file

```
>>> head gprojector_metadata.tsv
```

|node1_label|type        |
|-----------|------------|
|Tours University|university in France|
|Robert Bouline|human       |
|William Monahan|human       |
|rated voltage|voltage     |
|France-Guernsey border|international border|


