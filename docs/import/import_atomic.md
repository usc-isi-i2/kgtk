Import the entire ATOMIC knowledge graph into KGTK format. 

## Background

ATOMIC ([Sap et al., 2019](https://arxiv.org/pdf/1811.00146.pdf)) is a recently constructed knowledge graph of common sense statements for events. It consists of over 700k statements that describe 24k base events with 9 relations. The knowledge covered in ATOMIC expresses event causality and implications on their (human) participants. Since its creation, ATOMIC has been a common resource in KG-augmented downstream reasoning systems, built for tasks such as question answering or natural language inference.

## Usage
```
usage: kgtk import-atomic [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)

```

## Obtaining the data

ATOMIC can be downloaded [here](https://storage.googleapis.com/ai2-mosaic/public/atomic/v1.0/atomic_data.tgz). The KGTK importer uses its aggregated file: `v4_atomic_all_agg.csv`.

## Examples

Import ATOMIC into KGTK. 

```
kgtk import-atomic -i v4_atomic_all_agg.csv -o atomic.tsv
```

Example output (first and last 10 lines):

| node1                                   | relation   | node2                                                 | node1;label                                                                                                       | node2;label                          | relation;label           | relation;dimension | source | sentence |
| --------------------------------------- | ---------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------ | ------------------ | ------ | -------- |
| at:personx_'d_better_go                 | at:xAttr   | at:avoidant                                           | "personx \\'d better go"\|"\\'d better go"                                                                        | "avoidant"                           | "person x has attribute" |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xAttr   | at:weak                                               | "personx \\'d better go"\|"\\'d better go"                                                                        | "weak"                               | "person x has attribute" |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xAttr   | at:hurried                                            | "personx \\'d better go"\|"\\'d better go"                                                                        | "hurried"                            | "person x has attribute" |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xAttr   | at:late                                               | "personx \\'d better go"\|"\\'d better go"                                                                        | "late"                               | "person x has attribute" |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xAttr   | at:tardy                                              | "personx \\'d better go"\|"\\'d better go"                                                                        | "tardy"                              | "person x has attribute" |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xAttr   | at:busy                                               | "personx \\'d better go"\|"\\'d better go"                                                                        | "busy"                               | "person x has attribute" |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xEffect | at:she_ran_to_the_bathroom                            | "personx \\'d better go"\|"\\'d better go"                                                                        | "she ran to the bathroom"            | "effect on person x"     |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xEffect | at:she_finally_made_it                                | "personx \\'d better go"\|"\\'d better go"                                                                        | "she finally made it"                | "effect on person x"     |                    | "AT"   |          |
| at:personx_'d_better_go                 | at:xEffect | at:leaves                                             | "personx \\'d better go"\|"\\'d better go"                                                                        | "leaves"                             | "effect on person x"     |                    | "AT"   |          |
| ...                                     |            |                                                       |                                                                                                                   |                                      |                          |                    |        |          |
| at:personx_zig_when_personx_shoulds_zag | at:xAttr   | at:objective                                          | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "objective"                          | "person x has attribute" |                    | "AT"   |          |
| at:personx_zig_when_personx_shoulds_zag | at:xAttr   | at:confrontational                                    | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "confrontational"                    | "person x has attribute" |                    | "AT"   |          |
| at:personx_zig_when_personx_shoulds_zag | at:xEffect | at:stumble_over_someone_else                          | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "stumble over someone else"          | "effect on person x"     |                    | "AT"   |          |
| at:personx_zig_when_personx_shoulds_zag | at:xEffect | at:gets_hurt                                          | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "gets hurt"                          | "effect on person x""AT" |                    |        |          |
| at:personx_zig_when_personx_shoulds_zag | at:xEffect | at:misses_an_opportunity                              | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "misses an opportunity"              | "effect on person x"     |                    | "AT"   |          |
| at:personx_zig_when_personx_shoulds_zag | at:xEffect | at:learns_a_valuable_lesson                           | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "learns a valuable lesson"           | "effect on person x"     |                    | "AT"   |          |
| at:personx_zig_when_personx_shoulds_zag | at:xReact  | at:regretful                                          | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "regretful"                          | "person x feels"         | "AT"               |        |          |
| at:personx_zig_when_personx_shoulds_zag | at:xReact  | at:like_he_did_the_wrong_thing | "personx zig when personx shoulds zag"\|"zig when shoulds zag"like he did the wrong thing, he should have zagged" | "person x feels"                     |                          | "AT"               |        |          |
| at:personx_zig_when_personx_shoulds_zag | at:xWant   | at:to_sit_down_and_rest                               | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "to sit down and rest"               | "person x wants"         |                    | "AT"   |          |
| at:personx_zig_when_personx_shoulds_zag | at:xWant   | at:to_find_out_their_time_in_the_race                 | "personx zig when personx shoulds zag"\|"zig when shoulds zag"                                                    | "to find out their time in the race" | "person x wants"         |                    | "AT"   |          |

