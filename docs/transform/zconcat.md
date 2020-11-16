This command concatenates any mixture of plain or gzip/bzip2/xz-compressed files.

## Usage
```
usage: kgtk zconcat [-h] [-o OUTPUT] [--gz] [--bz2] [--xz] [-i INPUT_FILE [INPUT_FILE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --out OUTPUT
                        output file to write to, otherwise output goes to stdout
  --gz, --gzip          compress result with gzip
  --bz2, --bzip2        compress result with bzip2
  --xz                  compress result with xz
  -i INPUT_FILE [INPUT_FILE ...], --input-file INPUT_FILE [INPUT_FILE ...]
                        The KGTK input file. (May be omitted or '-' for stdin.)
```

Inputs are zero or more input files. The files can be plain or compressed in a
mix of different formats. If the input argument is empty, the script expects
piped input from another command.  A "-" at any position in the input list
will splice in input from stdin there, which allows arbitrary concatenation of
named files with input from stdin.

## Examples
Concatenate 2 unzipped files and store them in a file:
```
kgtk zconcat -o dest.tsv -i file1.tsv file2.tsv
```

Concatenate 2 unzipped files and output to stdout:
```
kgtk zconcat -i file1.tsv file2.tsv
```

Concatenate 2 gzipped files and store as gzip 
```
kgtk zconcat --gz -o dest.tsv.gz -i file1.tsv.gz file2.tsv.gz
```

Concatenate a mixture of compressed and plain files to a compressed result:
```
cat file1.gz  |  kgtk zconcat --gz  -o dest.gz -i file2.bz2 - file3
```
