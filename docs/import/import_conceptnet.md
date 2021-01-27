Import the entire [ConceptNet](https://conceptnet.io/), or just its English part, into KGTK format. Weights could optionally be stored in an auxiliary KGTK file. 

## Usage
```
usage: kgtk import-conceptnet [-h] [-i INPUT_FILE] [--english_only]
                              [-o OUTPUT_FILE] [--weights-file WEIGHTS_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  --english_only        Only english conceptnet?
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --weights-file WEIGHTS_FILE
                        A KGTK output file that will contain only the weights.
                        (Optional, use '-' for stdout.)
```

## Examples

Import the English part of ConceptNet into KGTK. Don't import the weights. 

```
kgtk import-conceptnet --english_only -i examples/conceptnet-assertions-5.7.0.csv -o conceptnet_en.tsv
```

Example output (first and last 10 lines):

| node1                    | relation           | node2                        | node1;label     | node2;label             | relation;label | relation;dimension | source | sentence |
| ------------------------ | ------------------ | ---------------------------- | --------------- | ----------------------- | -------------- | ------------------ | ------ | -------- |
| /c/en/0/n                | /r/Antonym         | /c/en/1                      | "0"             | "1"                     | "antonym"      |                    | "CN"   |          |
| /c/en/12_hour_clock/n    | /r/Antonym         | /c/en/24_hour_clock          | "12 hour clock" | "24 hour clock"         | "antonym"      |                    | "CN"   |          |
| /c/en/24_hour_clock/n    | /r/Antonym         | /c/en/12_hour_clock          | "24 hour clock" | "12 hour clock"         | "antonym"      |                    | "CN"   |          |
| /c/en/5/n                | /r/Antonym         | /c/en/3                      | "5"             | "3"                     | "antonym"      |                    | "CN"   |          |
| /c/en/a.c/n              | /r/Antonym         | /c/en/d.c                    | "a.c"           | "d.c"                   | "antonym"      |                    | "CN"   |          |
| /c/en/a.m/r              | /r/Antonym         | /c/en/afternoon              | "a.m"           | "afternoon"             | "antonym"      |                    | "CN"   |          |
| /c/en/a.m/r              | /r/Antonym         | /c/en/p.m                    | "a.m"           | "p.m"                   | "antonym"      |                    | "CN"   |          |
| /c/en/a.m/r              | /r/Antonym         | /c/en/pm                     | "a.m"           | "pm"                    | "antonym"      |                    | "CN"   |          |
| /c/en/ab_extra/r         | /r/Antonym         | /c/en/ab_intra               | "ab extra"      | "ab intra"              | "antonym"      |                    | "CN"   |          |
| ...                      |                    |                              |                 |                         |                |                    |        |          |
| /c/en/xebec/n/wp/studio  | /r/dbpedia/product | /c/en/film                   | "xebec"         | "film"                  | "product"      |                    | "CN"   |          |
| /c/en/xerox              | /r/dbpedia/product | /c/en/image_scanner          | "xerox"         | "image scanner"         | "product"      |                    | "CN"   |          |
| /c/en/xerox              | /r/dbpedia/product | /c/en/management_consulting  | "xerox"         | "management consulting" | "product"      |                    | "CN"   |          |
| /c/en/xerox              | /r/dbpedia/product | /c/en/outsourcing            | "xerox"         | "outsourcing"           | "product"      |                    | "CN"   |          |
| /c/en/xerox              | /r/dbpedia/product | /c/en/printer/n/wp/computing | "xerox"         | "printer"               | "product"      |                    | "CN"   |          |
| /c/en/xerox              | /r/dbpedia/product | /c/en/projector              | "xerox"         | "projector"             | "product"      |                    | "CN"   |          |
| /c/en/zanella            | /r/dbpedia/product | /c/en/moped                  | "zanella"       | "moped"                 | "product"      |                    | "CN"   |          |
| /c/en/zanella            | /r/dbpedia/product | /c/en/motorcycle             | "zanella"       | "motorcycle"            | "product"      |                    | "CN"   |          |
| /c/en/zara/n/wp/retailer | /r/dbpedia/product | /c/en/clothing               | "zara"          | "clothing"              | "product"      |                    | "CN"   |          |
| /c/en/zeeman/n/wp/store  | /r/dbpedia/product | /c/en/clothing               | "zeeman"        | "clothing"              | "product"      |                    | "CN"   |          |

