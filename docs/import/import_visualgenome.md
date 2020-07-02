Import Visual Genome into KGTK format.

## Usage
```
usage: kgtk import-visualgenome [-h] [-i INPUT_FILE]
                                [--attr-synsets ATTR_SYN_FILE]
                                [-o OUTPUT_FILE]
                                [INPUT_FILE]

positional arguments:
  INPUT_FILE            Visual Genome scene graph file (May be omitted or '-'
                        for stdin.) (Deprecated, use -i INPUT_FILE)

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
kgtk import-visualgenome -i scene_graphs.json --attr-synsets attribute_synsets.json
```

Example output (first and last 10 lines):
```
node1	label	node2	node1;label	label;label	node2;label	label;dimension	source	weight	creator	sentence	question
clock.n.01	/r/HasProperty	green.s.01	clock	has property	green		VG	1.0	I1		
clock.n.01	/r/HasProperty	tall.a.01	clock	has property	tall		VG	1.0	I1		
gym_shoe.n.01	/r/HasProperty	grey.s.01	sneakers	has property	grey		VG	1.0	I1		
headlight.n.01	/r/HasProperty	off.a.01	headlight	has property	off		VG	1.0	I1		
bicycle.n.01	/r/HasProperty	parked.a.01	bike	has property	parked		VG	1.0	I1		
bicycle.n.01	/r/HasProperty	away.s.01	bike	has property	far away		VG	1.0	I1		
bicycle.n.01	/r/HasProperty	chained.s.01	bike	has property	chained		VG	1.0	I1		
sign.n.02	/r/HasProperty	black.a.01	sign	has property	black		VG	1.0	I1		
building.n.01	/r/HasProperty	tall.a.01	building	has property	tall		VG	1.0	I1
...
bus.n.01	/r/HasProperty	large.a.01	bus	has property	large		VG	1.0	I2417997		
sky.n.01	/r/HasProperty	blue.s.01	sky	has property	blue		VG	1.0	I2417997		
range.n.04	/r/LocatedNear	distance.n.01	mountain range	in	distance		VG	1.0	I2417997		
bus.n.01	/r/LocatedNear	road.n.01	bus	on	road		VG	1.0	I2417997		
grillroom.n.01	/r/LocatedNear	bus.n.01	grill	on	bus		VG	1.0	I2417997		
numeral.n.01	/r/LocatedNear	bus.n.01	number	on	bus		VG	1.0	I2417997		
plate.n.04	/r/LocatedNear	bus.n.01	plate	on	bus		VG	1.0	I2417997		
bus.n.01	/r/LocatedNear	desert.n.01	bus	in	desert		VG	1.0	I2417997		
bus.n.01	/r/LocatedNear	door.n.01	bus	with	doors		VG	1.0	I2417997		
door.n.01	/r/LocatedNear	bus.n.01	door	on	bus		VG	1.0	I2417997
```
