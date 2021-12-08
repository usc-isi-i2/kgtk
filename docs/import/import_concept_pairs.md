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

Let's say that we want to import synonym pairs from the ROGET thesaurus, and connect them with the `/r/Synonym` relation:

```
kgtk import-concept-pairs -i synonyms.txt --source RG --relation /r/Synonym -o roget_syn.tsv
```

Example output (first and last 10 lines):

| node1            | relation   | node2            | node1;label  | node2;label  | relation;label | relation;dimension | source | sentence |
| ---------------- | ---------- | ---------------- | ------------ | ------------ | -------------- | ------------------ | ------ | -------- |
| rg:en_fawn       | /r/Synonym | rg:en_defer      | "fawn"       | "defer"      | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_kowtow     | "fawn"       | "kowtow"     | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_flatter    | "fawn"       | "flatter"    | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_stroke     | "fawn"       | "stroke"     | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_brownnose  | "fawn"       | "brownnose"  | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_submit     | "fawn"       | "submit"     | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_toady      | "fawn"       | "toady"      | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_creep      | "fawn"       | "creep"      | "synonym"      |                    | "RG"   |          |
| rg:en_fawn       | /r/Synonym | rg:en_cotton     | "fawn"       | "cotton"     | "synonym"      |                    | "RG"   |          |
| ...              |            |                  |              |              |                |                    |        |          |
| rg:en_architect  | /r/Synonym | rg:en_engineer   | "architect"  | "engineer"   | "synonym"      |                    | "RG"   |          |
| rg:en_untalented | /r/Synonym | rg:en_talentless | "untalented" | "talentless" | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_jowl       | "jawbone"    | "jowl"       | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_schmoose   | "jawbone"    | "schmoose"   | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_mandible   | "jawbone"    | "mandible"   | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_shmoose    | "jawbone"    | "shmoose"    | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_submaxilla | "jawbone"    | "submaxilla" | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_mandibula  | "jawbone"    | "mandibula"  | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_shmooze    | "jawbone"    | "shmooze"    | "synonym"      |                    | "RG"   |          |
| rg:en_jawbone    | /r/Synonym | rg:en_schmooze   | "jawbone"    | "schmooze"   | "synonym"      |                    | "RG"   |          |	

