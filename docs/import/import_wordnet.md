Import [WordNet](https://wordnet.princeton.edu/) v3.0 into KGTK format. Currently, four relations are included: hypernymy, membership holonymy, part-of holonymy, and substance meronymy. The resulting KGTK file consists of 9 columns.

## Usage
```
usage: kgtk import-wordnet [-h] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
```

## Examples

Importing WordNet can be done as follows (no inputs should be provided, as WordNet is read through the NLTK package):

```
kgtk import-wordnet -o wordnet.tsv
```

Example output (first and last 10 lines):

| node1                   | relation  | node2                   | node1;label                             | node2;label                                                                     | relation;label | relation;dimension | source | sentence |
| ----------------------- | --------- | ----------------------- | --------------------------------------- | ------------------------------------------------------------------------------- | -------------- | ------------------ | ------ | -------- |
| wn:physical_entity.n.01 | /r/IsA    | wn:entity.n.01          | "physical entity"                       | "entity"                                                                        | "is a"         |                    | "WN"   |          |
| wn:abstraction.n.06     | /r/IsA    | wn:entity.n.01          | "abstraction"\|"abstract entity"        | "entity"                                                                        | "is a"         |                    | "WN"   |          |
| wn:thing.n.12           | /r/IsA    | wn:physical_entity.n.01 | "thing"                                 | "physical entity"                                                               | "is a"         |                    | "WN"   |          |
| wn:object.n.01          | /r/IsA    | wn:physical_entity.n.01 | "object"\|"physical object"             | "physical entity"                                                               | "is a"         |                    | "WN"   |          |
| wn:whole.n.02           | /r/IsA    | wn:object.n.01          | "whole"\|"unit"                         | "object"\|"physical object"                                                     | "is a"         |                    | "WN"   |          |
| wn:congener.n.03        | /r/IsA    | wn:whole.n.02           | "congener"                              | "whole"\|"unit"                                                                 | "is a"         |                    | "WN"   |          |
| wn:living_thing.n.01    | /r/IsA    | wn:whole.n.02           | "living thing"\|"animate thing"         | "whole"\|"unit"                                                                 | "is a"         |                    | "WN"   |          |
| wn:organism.n.01        | /r/IsA    | wn:living_thing.n.01    | "organism"\|"being"                     | "living thing"\|"animate thing"                                                 | "is a"         |                    | "WN"   |          |
| wn:benthos.n.02         | /r/IsA    | wn:organism.n.01        | "benthos"                               | "organism"\|"being"                                                             | "is a"         |                    | "WN"   |          |
| ...                     |           |                         |                                         |                                                                                 |                |                    |        |          |
| wn:wood.n.01            | /r/MadeOf | wn:lignin.n.01          | "wood"                                  | "lignin"                                                                        | "is made of"   |                    | "WN"   |          |
| wn:wolframite.n.01      | /r/MadeOf | wn:tungsten.n.01        | "wolframite"\|"iron manganese tungsten" | "tungsten"\|"wolfram"\|"W"\|"atomic number 74"                                  | "is made of"   |                    | "WN"   |          |
| wn:xenotime.n.01        | /r/MadeOf | wn:thulium.n.01         | "xenotime"                              | "thulium"\|"Tm"\|"atomic number 69"                                             | "is made of"   |                    | "WN"   |          |
| wn:xenotime.n.01        | /r/MadeOf | wn:ytterbium.n.01       | "xenotime"                              | "ytterbium"\|"Yb"\|"atomic number 70"                                           | "is made of"   |                    | "WN"   |          |
| wn:xenotime.n.01        | /r/MadeOf | wn:yttrium.n.01         | "xenotime"                              | "yttrium"\|"Y"\|"atomic number 39"                                              | "is made of"   |                    | "WN"   |          |
| wn:zinc_blende.n.01     | /r/MadeOf | wn:indium.n.01          | "zinc blende"\|"blende"\|"sphalerite"   | "indium"\|"In"\|"atomic number 49"                                              | "is made of"   |                    | "WN"   |          |
| wn:zinc_blende.n.01     | /r/MadeOf | wn:thallium.n.01        | "zinc blende"\|"blende"\|"sphalerite"   | "thallium"\|"Tl"\|"atomic number 81"                                            | "is made of"   |                    | "WN"   |          |
| wn:zinc_white.n.01      | /r/MadeOf | wn:zinc_oxide.n.01      | "zinc white"\|"Chinese white"           | "zinc oxide"\|"flowers of zinc"\|"philosopher\\'s wool"\|"philosophers\\' wool" | "is made of"   |                    | "WN"   |          |
| wn:zinnwaldite.n.01     | /r/MadeOf | wn:lithium.n.01         | "zinnwaldite"                           | "lithium"\|"Li"\|"atomic number 3"                                              | "is made of"   |                    | "WN"   |          |
| wn:zircon.n.01          | /r/MadeOf | wn:zirconium.n.01       | "zircon"\|"zirconium silicate"          | "zirconium"\|"Zr"\|"atomic number 40"                                           | "is made of"   |                    | "WN"   |          |

