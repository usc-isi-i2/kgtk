# graph-embeddings

## Overview
Given a kgtk format file, this command will compute the the embeddings of this files' entities. We are using structure of nodes and their relations to compute embeddings of nodes. The set of metrics to compute are specified by the user. 

## Input format
The input is an kgtk format .tsv file where each line of these files contains information about nodes and relation. Each line is separated by tabs into columns which contains the node and relation data. For example:

```
id    node1    relation    node2    node1;label    node2;label    relation;label    relation;dimension    source    sentence
/c/en/000-/r/RelatedTo-/c/en/112-0000    /c/en/000 /r/RelatedTo    /c/en/112    000    112    related to    CN ...
```
For further format details, please refer to the KGTK data specification.

## Output format

There are three  supported formats: glove, w2v, and kgtk.

### glove format
When using this format, the output is a .tsv file where each line is the embedding for a node.  Each line is represented by a single node followed respectively by the components of its embedding, each in a different column, all separated by tabs. For example: 
```
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
```

### w2v format (default)
When using this format, the output is a .tsv file which it is almost the same as glove format, the only difference is that the word2vec format has a first line which indicates the shape of the embedding (e.g., "9 4" for 9 entities with 4 dimensions), each column of first line is separated by tabs. Here we use w2v as our default output format. For example:
```
16213    100 
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
"home"    -0.014021411    -0.090830070    -0.012534120    -0.073111301    -0.068317516 ...
```
Here 16231 represents the number of nodes, 100 represents the dimension number of each node embedding.

### kgtk format
When using this format, the output is a .tsv file where each line is the embedding for a node.  Each line has 3 columns, first column represents entity node, second node represent its embedding type (here is `graph_embeddings`), third column represents the entity's embeddings. For example: 
```
Q5    graph_embeddings   014022544,-0.062030070,-0.012535412,0.038317516 
Q6    graph_embeddings   014022544,-0.062030070,-0.012535412,0.038317516 
```

## Algorithm

The algorithm is defined with the `operator` (`-op`) parameter. By default, it is `ComplEx`. It could be switched to: `TransE`, `DistMult`, or `RESCAL`. The `operator` is case insensitive, for example, users can input the string like `complex` to assign embedding method. For more details and pointers, see [this documentation page](https://torchbiggraph.readthedocs.io/en/latest/related.html).

## Usage
You can call the functions directly with given args as 
```
usage: kgtk graph-embeddings [-h] [-i INPUT_FILE_PATH] [-o OUTPUT_FILE_PATH]
                             [-l] [-T] [-ot] [-r True|False] [-d] [-s]
                             [-c dot|cos|l2|squared_l2]
                             [-op linear|diagonal|complex_diagonal|translation]
                             [-e] [-b True|False] [-w] [-bs]
                             [-lf ranking|logistic|softmax] [-lr] [-ef]
                             [-dr True|False] [-ge True|False]
                             [-v [optional True|False]]
                             [--column-separator COLUMN_SEPARATOR]
                             [--input-format INPUT_FORMAT]
                             [--compression-type COMPRESSION_TYPE]
                             [--error-limit ERROR_LIMIT]
                             [--use-mgzip [optional True|False]]
                             [--mgzip-threads MGZIP_THREADS]
                             [--gzip-in-parallel [optional True|False]]
                             [--gzip-queue-size GZIP_QUEUE_SIZE]
                             [--mode {NONE,EDGE,NODE,AUTO}]
                             [--force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                             [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--skip-header-record [optional True|False]]
                             [--unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--initial-skip-count INITIAL_SKIP_COUNT]
                             [--every-nth-record EVERY_NTH_RECORD]
                             [--record-limit RECORD_LIMIT]
                             [--tail-count TAIL_COUNT]
                             [--repair-and-validate-lines [optional True|False]]
                             [--repair-and-validate-values [optional True|False]]
                             [--blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--fill-short-lines [optional True|False]]
                             [--invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--prohibited-list-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                             [--truncate-long-lines [TRUNCATE_LONG_LINES]]
                             [--whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE_PATH, --input-file INPUT_FILE_PATH
                        The KGTK input file. (default=-)
  -o OUTPUT_FILE_PATH, --output-file OUTPUT_FILE_PATH
                        The KGTK output file. (default=-).
  -l , --log            Setting the log path [Default: None]
  -T , --temporary_directory 
                        Sepecify the directory location to store temporary
                        file
  -ot , --output_format 
                        Outputformat for embeddings [Default: w2v] Choice: kgtk
                        | w2v | glove
  -r True|False, --retain_temporary_data True|False
                        When opearte graph, some tempory files will be
                        generated, set True to retain these files
  -d , --dimension      Dimension of the real space the embedding live in
                        [Default: 100]
  -s , --init_scale     Generating the initial embedding with this standard
                        deviation [Default: 0.001]If no initial embeddings are
                        provided, they are generated by sampling each
                        dimensionfrom a centered normal distribution having
                        this standard deviation.
  -c dot|cos|l2|squared_l2, --comparator dot|cos|l2|squared_l2
                        How the embeddings of the two sides of an edge (after
                        having already undergone some processing) are compared
                        to each other to produce a score[Default: dot],Choice:
                        dot|cos|l2|squared_l2
  -op RESCAL|DistMult|ComplEx|TransE, --operator RESCAL|DistMult|ComplEx|TransE
                        The transformation to apply to the embedding of one of
                        the sides of the edge (typically the right-hand one)
                        before comparing it with the other one. It reflects
                        which model that embedding uses. [Default:ComplEx]
  -e , --num_epochs     The number of times the training loop iterates over
                        all the edges.[Default:100]
  -b True|False, --bias True|False
                        Whether use the bias choice [Default: False],If
                        enabled, withhold the first dimension of the
                        embeddings from the comparator and instead use it as a
                        bias, adding back to the score. Makes sense for
                        logistic and softmax loss functions.
  -w , --workers        The number of worker processes for training. If not
                        given, set to CPU count.
  -bs , --batch_size    The number of edges per batch.[Default:1000]
  -lf ranking|logistic|softmax, --loss_fn ranking|logistic|softmax
                        How the scores of positive edges and their
                        corresponding negatives are evaluated.[Default:
                        ranking], Choice: ranking|logistic|softmax
  -lr , --learning_rate 
                        The learning rate for the optimizer.[Default: 0.1]
  -ef , --eval_fraction 
                        The fraction of edges withheld from training and used
                        to track evaluation metrics during training.
                        [Defalut:0.0 training all edges ]
  -dr True|False, --dynamic_relaitons True|False
                        Whether use dynamic relations (when graphs with a
                        large number of relations) [Default: True]
  -ge True|False, --global_emb True|False
                        Whether use global embedding, if enabled, add to each
                        embedding a vector that is common to all the entities
                        of a certain type. This vector is learned during
                        training.[Default: False]

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).

File options:
  Options affecting processing.

  --column-separator COLUMN_SEPARATOR
                        Column separator (default=<TAB>).
  --input-format INPUT_FORMAT
                        Specify the input format (default=None).
  --compression-type COMPRESSION_TYPE
                        Specify the compression type (default=None).
  --error-limit ERROR_LIMIT
                        The maximum number of errors to report before failing
                        (default=1000)
  --use-mgzip [optional True|False]
                        Execute multithreaded gzip. (default=False).
  --mgzip-threads MGZIP_THREADS
                        Multithreaded gzip thread count. (default=3).
  --gzip-in-parallel [optional True|False]
                        Execute gzip in parallel. (default=False).
  --gzip-queue-size GZIP_QUEUE_SIZE
                        Queue size for parallel gzip. (default=1000).
  --mode {NONE,EDGE,NODE,AUTO}
                        Determine the KGTK file mode
                        (default=KgtkReaderMode.AUTO).

Header parsing:
  Options affecting header parsing.

  --force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]
                        Force the column names (default=None).
  --header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a header error is detected.
                        Only ERROR or EXIT are supported
                        (default=ValidationAction.EXIT).
  --skip-header-record [optional True|False]
                        Skip the first record when forcing column names
                        (default=False).
  --unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a column name is unsafe
                        (default=ValidationAction.REPORT).

Pre-validation sampling:
  Options affecting pre-validation data line sampling.

  --initial-skip-count INITIAL_SKIP_COUNT
                        The number of data records to skip initially
                        (default=do not skip).
  --every-nth-record EVERY_NTH_RECORD
                        Pass every nth record (default=pass all records).
  --record-limit RECORD_LIMIT
                        Limit the number of records read (default=no limit).
  --tail-count TAIL_COUNT
                        Pass this number of records (default=no tail
                        processing).

Line parsing:
  Options affecting data line parsing.

  --repair-and-validate-lines [optional True|False]
                        Repair and validate lines (default=False).
  --repair-and-validate-values [optional True|False]
                        Repair and validate values (default=False).
  --blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a line with a blank node1,
                        node2, or id field (per mode) is detected
                        (default=ValidationAction.EXCLUDE).
  --comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a comment line is detected
                        (default=ValidationAction.EXCLUDE).
  --empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when an empty line is detected
                        (default=ValidationAction.EXCLUDE).
  --fill-short-lines [optional True|False]
                        Fill missing trailing columns in short lines with
                        empty values (default=False).
  --invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell value is invalid
                        (default=ValidationAction.COMPLAIN).
  --long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a long line is detected
                        (default=ValidationAction.COMPLAIN).
  --prohibited-list-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell contains a
                        prohibited list (default=ValidationAction.COMPLAIN).
  --short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a short line is detected
                        (default=ValidationAction.COMPLAIN).
  --truncate-long-lines [TRUNCATE_LONG_LINES]
                        Remove excess trailing columns in long lines
                        (default=False).
  --whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a whitespace line is detected
                        (default=ValidationAction.EXCLUDE).

```
## Examples

### Example 1
For easiest running, just give the input file and let it write its output to `output_embeddings.csv` at current folder
`kgtk graph-embeddings -i input_file.tsv  -o output_file.tsv`

The output_file.tsv may look like:
```
172131    100
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
"home"    -0.014021411    -0.090830070    -0.012534120    -0.073111301    -0.068317516 ...
```


### Example 2
Running with more specific parameters (TransE algorithm and 200-dimensional vectors):
```
kgtk graph-embeddings 
    --input-file input_file.tsv \
    --output-file output_file.tsv \
    --dimension 200 \
    --comparator dot \
    --operator translation \
    --loss_fn softmax \
    --learning_rate 0.1
```

The `output_file.tsv` may look like:
```
172131    100
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
"home"    -0.014021411    -0.090830070    -0.012534120    -0.073111301    -0.068317516 ...
```

### Example 3
Using glove format to generate graph embeddings
```
kgtk graph-embeddings 
    --input-file input_file.tsv \
    --output-file output_file.tsv \
    --output_format glove
```

The `output_file.tsv` may look like:
```
"work"    -0.014022544    -0.062030070    -0.012535412    -0.023111001    -0.038317516 ...
"home"    -0.014021411    -0.090830070    -0.012534120    -0.073111301    -0.068317516 ...
```

### Example 4
Using kgtk format to generate graph embeddings
```
kgtk graph-embeddings 
    --input-file input_file.tsv \
    --output-file output_file.tsv \
    --output_format kgtk
```

The `output_file.tsv` may look like:
```
"work"    graph_embeddings   -0.014022544,-0.062030070,-0.012535412,-0.023111001,-0.038317516 ...
"home"    graph_embeddings   -0.014021411,-0.090830070,-0.012534120,-0.073111301,-0.068317516 ...
```


