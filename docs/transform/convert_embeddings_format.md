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
usage: kgtk convert-embeddings-format [-h] [-i INPUT_FILE] [--node-file NODE_FILE] [-o OUTPUT_FILE]
                                      [--metadata-file METADATA_FILE] [--input-property INPUT_PROPERTY]
                                      [--output-format OUTPUT_FORMAT] [--metadata-columns METADATA_COLUMNS]

Converts KGTK edge embeddings file to word2vec or Google Projector format.Takes an optional node file for Google Project format to create a metadata file. Processes only top 10,000 rows from the edge file for Google Projector as it only accepts 10,000 rows.
Additional options are shown in expert help.
kgtk --expert convert-embeddings-format --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        KGTK input files (May be omitted or '-' for stdin.)
  --node-file NODE_FILE
                        The KGTK node file for creating Google Projector Metadata. All the columns in the node file
                        will be added to the metadata file by default. You can customise this with the --metadata-
                        columns option. (Optional)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --metadata-file METADATA_FILE
                        The output metadata file for Google Projector. If --output-format == gprojector and--metadata-
                        file is not specified, a file named `kgtk_embeddings_gprojector_metadata.tsv` will be created
                        in USER_HOME (Optional)
  --input-property INPUT_PROPERTY
                        The property name for embeddings in the input KGTK edge file. (default=embeddings).
  --output-format OUTPUT_FORMAT
                        The desired output file format: word2vec|gprojector (default=word2vec)
  --metadata-columns METADATA_COLUMNS
                        A comma separated string of columns names in the input file or the --node-file to be used for
                        creating the metadata file for Google projector. Only to be used when --output-format ==
                        'gprojector'. If --node-file is specified, the command will look for --metadata-columns in the
                        --node-file, otherwise input file.The command will throw an error if the columns specified are
                        not in either of the files.
```

## Examples

###