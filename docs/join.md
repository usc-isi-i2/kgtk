
Join two KGTK edge files or two KGTK node files.

## Usage
```
kgtk join [-h] [--join-on-label [JOIN_ON_LABEL]]
                 [--join-on-node2 [JOIN_ON_NODE2]]
                 [--left-file-join-columns LEFT_JOIN_COLUMNS [LEFT_JOIN_COLUMNS ...]]
                 [--left-join [LEFT_JOIN]] [-o OUTPUT_FILE_PATH]
                 [--prefix PREFIX]
                 [--right-file-join-columns RIGHT_JOIN_COLUMNS [RIGHT_JOIN_COLUMNS ...]]
                 [--right-join [RIGHT_JOIN]] [-v]
                 left_file_path right_file_path
```
## Usage considerations

* Join keys are extracted from one or both input files and stored in memory,
then the data files are processed in a second pass.  
* stdin will not work as an input file if join keys are needed from it.
* The output file contains the union of the columns in the two
input files, adjusted for predefined name aliasing.
* Specify --left-join to get a left outer join.
* Specify --right-join to get a right outer join.
* Specify both to get a full outer join (equivalent to cat).
* Specify neither to get an inner join.
* By default, node files are joined on the id column, while edge files are joined on the node1 column. The label and node2 columns may be added to the edge file join criteria.  Alternatively, the left and right file join columns may be
listed explicitly.

To join an edge file to a node file, or to join quasi-KGTK files, use the
following option (enable expert mode for more information):

```
--mode=NONE
Expert mode provides additional command arguments.
positional arguments:
  left_file_path        The left-side KGTK file to join (required).
  right_file_path       The right-side KGTK file to join (required).
optional arguments:
  -h, --help            show this help message and exit
  --join-on-label [JOIN_ON_LABEL]
                        If both input files are edge files, include the label
                        column in the join (default=False).
  --join-on-node2 [JOIN_ON_NODE2]
                        If both input files are edge files, include the node2
                        column in the join (default=False).
  --left-file-join-columns LEFT_JOIN_COLUMNS [LEFT_JOIN_COLUMNS ...]
                        Left file join columns (default=None).
  --left-join [LEFT_JOIN]
                        Perform a left outer join (default=False).
  -o OUTPUT_FILE_PATH, --output-file OUTPUT_FILE_PATH
                        The KGTK file to write (default=-).
  --prefix PREFIX       An optional prefix applied to right file column names
                        in the output file (default=None).
  --right-file-join-columns RIGHT_JOIN_COLUMNS [RIGHT_JOIN_COLUMNS ...]
                        Right file join columns (default=None).
  --right-join [RIGHT_JOIN]
                        Perform a right outer join (default=False).
  -v, --verbose         Print additional progress messages (default=False).
```