Import a file with concept pairs into KGTK format. The relation to connect them with can be specified through an argument, as well as the source.
The resulting KGTK file consists of 9 columns.

## Usage
```
usage: kgtk import-concept-pairs [-h] [-i INPUT_FILE] [--relation RELATION]
                                 [--source SOURCE] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  --relation RELATION   Relation to connect the word pairs with.
  --source SOURCE       Source identifier
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
```

## Examples

Let's say that we want to import synonym pairs from the ROGET thesaurus, and connect them with the `/r/Synonym` relation.
We will use a subset of the ROGET rhesaurus as our input file:

```
kgtk import-concept-pairs -i tests/data/synonyms.txt --source RG --relation /r/Synonym / head -n 10
```

Example output (first 10 lines):

| node1 | relation | node2 | node1;label | node2;label | relation;label | relation;dimension | source | sentence |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| rg:en_fawn | /r/Synonym | rg:en_defer | "fawn" | "defer" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_kowtow | "fawn" | "kowtow" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_flatter | "fawn" | "flatter" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_stroke | "fawn" | "stroke" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_brownnose | "fawn" | "brownnose" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_submit | "fawn" | "submit" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_toady | "fawn" | "toady" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_creep | "fawn" | "creep" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_cotton | "fawn" | "cotton" | "synonym" |  | "RG" |  |
| rg:en_fawn | /r/Synonym | rg:en_pander | "fawn" | "pander" | "synonym" |  | "RG" |  |

```
kgtk import-concept-pairs -i tests/data/synonyms.txt --source RG --relation /r/Synonym / tail -n 10
```

Example output (last 10 lines):

| node1 | relation | node2 | node1;label | node2;label | relation;label | relation;dimension | source | sentence |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| rg:en_clotted | /r/Synonym | rg:en_coagulable | "clotted" | "coagulable" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_jellylike | "clotted" | "jellylike" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_soupy | "clotted" | "soupy" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_coagulated | "clotted" | "coagulated" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_coagulate | "clotted" | "coagulate" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_thready | "clotted" | "thready" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_grumose | "clotted" | "grumose" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_impenetrable | "clotted" | "impenetrable" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_ropy | "clotted" | "ropy" | "synonym" |  | "RG" |  |
| rg:en_clotted | /r/Synonym | rg:en_curdled | "clotted" | "curdled" | "synonym" |  | "RG" |  |

