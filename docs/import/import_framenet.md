Import [FrameNet](https://framenet.icsi.berkeley.edu/fndrupal/) v1.7 into KGTK format. The resulting KGTK file consists of 9 columns.

## Usage
```
usage: kgtk import-framenet [-h] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
```

## Examples

Importing FrameNet can be done as follows (no inputs should be provided, as FrameNet is read through the NLTK package):

```
kgtk import-framenet / head -n 10
```

Example output (first 10 lines):

| node1 | relation | node2 | node1;label | node2;label | relation;label | relation;dimension | source | sentence |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| fn:abandonment | /r/IsA | fn:intentionally_affect | "abandonment" | "intentionally affect" | "/r/is a" |  | "FN" |  |
| fn:abandonment | fn:HasLexicalUnit | fn:lu:abandonment:abandon | "abandonment" | "abandon" | "has lexical unit" |  | "FN" |  |
| fn:abandonment | fn:HasLexicalUnit | fn:lu:abandonment:leave | "abandonment" | "leave" | "has lexical unit" |  | "FN" |  |
| fn:abandonment | fn:HasLexicalUnit | fn:lu:abandonment:abandonment | "abandonment" | "abandonment" | "has lexical unit" |  | "FN" |  |
| fn:abandonment | fn:HasLexicalUnit | fn:lu:abandonment:abandoned | "abandonment" | "abandoned" | "has lexical unit" |  | "FN" |  |
| fn:abandonment | fn:HasLexicalUnit | fn:lu:abandonment:forget | "abandonment" | "forget" | "has lexical unit" |  | "FN" |  |
| fn:abandonment | /r/HasA | fn:fe:agent | "abandonment" | "agent" | "/r/has a" |  | "FN" |  |
| fn:abandonment | /r/HasA | fn:fe:theme | "abandonment" | "theme" | "/r/has a" |  | "FN" |  |
| fn:abandonment | /r/HasA | fn:fe:place | "abandonment" | "place" | "/r/has a" |  | "FN" |  |
| fn:abandonment | /r/HasA | fn:fe:time | "abandonment" | "time" | "/r/has a" |  | "FN" |  |

The following feedback messages are generated:

    [nltk_data] Downloading package framenet_v17 to
    [nltk_data]     /home/rogers/nltk_data...
    [nltk_data]   Package framenet_v17 is already up-to-date!

```
kgtk import-framenet / tail -n 10
```

Example output (tail 10 lines):

| node1 | relation | node2 | node1;label | node2;label | relation;label | relation;dimension | source | sentence |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:contrary | "word relations" | "contrary" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:hyponym | "word relations" | "hyponym" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:hypernym | "word relations" | "hypernym" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:synonymous | "word relations" | "synonymous" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:meronym | "word relations" | "meronym" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:holonym | "word relations" | "holonym" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:homophone | "word relations" | "homophone" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:homograph | "word relations" | "homograph" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:collocate | "word relations" | "collocate" | "has lexical unit" |  | "FN" |  |
| fn:word_relations | fn:HasLexicalUnit | fn:lu:word_relations:collocate | "word relations" | "collocate" | "has lexical unit" |  | "FN" |  |

The following feedback messages are generated:

    [nltk_data] Downloading package framenet_v17 to
    [nltk_data]     /home/rogers/nltk_data...
    [nltk_data]   Package framenet_v17 is already up-to-date!
