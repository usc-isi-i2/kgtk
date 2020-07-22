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
```

## Examples

Import Visual Genome into KGTK. 

```
kgtk import-visualgenome -i scene_graphs.json --attr-synsets attribute_synsets.json
```

Example output (first and last 10 lines):
```
node1	relation	node2	node1;label	node2;label	relation;label	relation;dimension	weight	source	origin	sentence	question
clock.n.01	mw:MayHaveProperty	green.s.01	clock	green	may have property			VG		I1		
clock.n.01	mw:MayHaveProperty	tall.a.01	clock	tall	may have property			VG		I1		
gym_shoe.n.01	mw:MayHaveProperty	grey.s.01	sneakers	grey	may have property			VG		I1		
headlight.n.01	mw:MayHaveProperty	off.a.01	headlight	off	may have property			VG		I1		
bicycle.n.01	mw:MayHaveProperty	parked.a.01	bike	parked	may have property			VG		I1		
bicycle.n.01	mw:MayHaveProperty	away.s.01	bike	far away	may have property			VG		I1		
bicycle.n.01	mw:MayHaveProperty	chained.s.01	bike	chained	may have property			VG		I1		
sign.n.02	mw:MayHaveProperty	black.a.01	sign	black	may have property			VG		I1		
building.n.01	mw:MayHaveProperty	tall.a.01	building	tall	may have property			VG		I1
...
bus.n.01	mw:MayHaveProperty	large.a.01	bus	large	may have property			VG		I2417997		
sky.n.01	mw:MayHaveProperty	blue.s.01	sky	blue	may have property			VG		I2417997		
range.n.04	/r/LocatedNear	distance.n.01	mountain range	distance	in			VG		I2417997		
bus.n.01	/r/LocatedNear	road.n.01	bus	road	on			VG		I2417997		
grillroom.n.01	/r/LocatedNear	bus.n.01	grill	bus	on			VG		I2417997		
numeral.n.01	/r/LocatedNear	bus.n.01	number	bus	on			VG		I2417997		
plate.n.04	/r/LocatedNear	bus.n.01	plate	bus	on			VG		I2417997		
bus.n.01	/r/LocatedNear	desert.n.01	bus	desert	in			VG		I2417997		
bus.n.01	/r/LocatedNear	door.n.01	bus	doors	with			VG		I2417997		
door.n.01	/r/LocatedNear	bus.n.01	door	bus	on			VG		I2417997
```
