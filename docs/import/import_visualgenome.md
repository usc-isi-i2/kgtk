Import [Visual Genome](https://visualgenome.org/) into KGTK format.

## Usage
```
usage: kgtk import-visualgenome [-h] [-i INPUT_FILE]
                                [--attr-synsets ATTR_SYN_FILE]
                                [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Visual Genome scene graph file (May be omitted or '-'
                        for stdin.)
  --attr-synsets ATTR_SYN_FILE
                        Visual Genome file with attribute synsets. (May be
                        omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
```

## Examples

Import Visual Genome into KGTK. 

```
kgtk import-visualgenome -i scene_graphs.json --attr-synsets attribute_synsets.json -o vg.tsv
```

Example output (first and last 10 lines):

| node1             | relation           | node2            | node1;label      | node2;label | relation;label      | relation;dimension | source | sentence |
| ----------------- | ------------------ | ---------------- | ---------------- | ----------- | ------------------- | ------------------ | ------ | -------- |
| wn:clock.n.01     | mw:MayHaveProperty | wn:green.s.01    | "clock"          | "green"     | "may have property" |                    | "VG"   |          |
| wn:clock.n.01     | mw:MayHaveProperty | wn:tall.a.01     | "clock"          | "tall"      | "may have property" |                    | "VG"   |          |
| wn:gym_shoe.n.01  | mw:MayHaveProperty | wn:grey.s.01     | "sneakers"       | "grey"      | "may have property" |                    | "VG"   |          |
| wn:headlight.n.01 | mw:MayHaveProperty | wn:off.a.01      | "headlight"      | "off"       | "may have property" |                    | "VG"   |          |
| wn:bicycle.n.01   | mw:MayHaveProperty | wn:parked.a.01   | "bike"           | "parked"    | "may have property" |                    | "VG"   |          |
| wn:bicycle.n.01   | mw:MayHaveProperty | wn:away.s.01     | "bike"           | "far away"  | "may have property" |                    | "VG"   |          |
| wn:bicycle.n.01   | mw:MayHaveProperty | wn:chained.s.01  | "bike"           | "chained"   | "may have property" |                    | "VG"   |          |
| wn:sign.n.02      | mw:MayHaveProperty | wn:black.a.01    | "sign"           | "black"     | "may have property" |                    | "VG"   |          |
| wn:building.n.01  | mw:MayHaveProperty | wn:tall.a.01     | "building"       | "tall"      | "may have property" |                    | "VG"   |          |
| ...               |                    |                  |                  |             |                     |                    |        |          |
| wn:bus.n.01       | mw:MayHaveProperty | wn:large.a.01    | "bus"            | "large"     | "may have property" |                    | "VG"   |          |
| wn:sky.n.01       | mw:MayHaveProperty | wn:blue.s.01     | "sky"            | "blue"      | "may have property" |                    | "VG"   |          |
| wn:range.n.04     | /r/LocatedNear     | wn:distance.n.01 | "mountain range" | "distance"  | "in"                |                    | "VG"   |          |
| wn:bus.n.01       | /r/LocatedNear     | wn:road.n.01     | "bus"            | "road"      | "on"                |                    | "VG"   |          |
| wn:grillroom.n.01 | /r/LocatedNear     | wn:bus.n.01      | "grill"          | "bus"       | "on"                |                    | "VG"   |          |
| wn:numeral.n.01   | /r/LocatedNear     | wn:bus.n.01      | "number"         | "bus"       | "on"                |                    | "VG"   |          |
| wn:plate.n.04     | /r/LocatedNear     | wn:bus.n.01      | "plate"          | "bus"       | "on"                |                    | "VG"   |          |
| wn:bus.n.01       | /r/LocatedNear     | wn:desert.n.01   | "bus"            | "desert"    | "in"                |                    | "VG"   |          |
| wn:bus.n.01       | /r/LocatedNear     | wn:door.n.01     | "bus"            | "doors"     | "with"              |                    | "VG"   |          |
| wn:door.n.01      | /r/LocatedNear     | wn:bus.n.01      | "door"           | "bus"       | "on"                |                    | "VG"   |          |

