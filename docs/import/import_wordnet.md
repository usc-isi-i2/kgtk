Import WordNet v3.0 into KGTK format. Currently, four relations are included: hypernymy, membership holonymy, part-of holonymy, and substance meronymy. The resulting KGTK file consists of 9 columns.

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
```
node1	relation	node2	node1;label	node2;label	relation;label	relation;dimension	weight	source	origin	sentence	question
physical_entity.n.01	/r/IsA	entity.n.01	physical entity	entity	is a			WN		physical entity is a entity	What is physical entity?
abstraction.n.06	/r/IsA	entity.n.01	abstraction|abstract entity	entity	is a			WN		abstraction is a entity	What is abstraction?
thing.n.12	/r/IsA	physical_entity.n.01	thing	physical entity	is a			WN		thing is a physical entity	What is thing?
object.n.01	/r/IsA	physical_entity.n.01	object|physical object	physical entity	is a			WN		object is a physical entity	What is object?
whole.n.02	/r/IsA	object.n.01	whole|unit	object|physical object	is a			WN		whole is a object	What is whole?
congener.n.03	/r/IsA	whole.n.02	congener	whole|unit	is a			WN		congener is a whole	What is congener?
living_thing.n.01	/r/IsA	whole.n.02	living thing|animate thing	whole|unit	is a			WN		living thing is a whole	What is living thing?
organism.n.01	/r/IsA	living_thing.n.01	organism|being	living thing|animate thing	is a			WN		organism is a living thing	What is organism?
benthos.n.02	/r/IsA	organism.n.01	benthos	organism|being	is a			WN		benthos is a organism	What is benthos?
...
wood.n.01	/r/MadeOf	lignin.n.01	wood	lignin	is made of			WN		wood is made of lignin	Wood is made of what?
wolframite.n.01	/r/MadeOf	tungsten.n.01	wolframite|iron manganese tungsten	tungsten|wolfram|W|atomic number 74	is made of			WN		wolframite is made of tungsten	Wolframite is made of what?
xenotime.n.01	/r/MadeOf	thulium.n.01	xenotime	thulium|Tm|atomic number 69	is made of			WN		xenotime is made of thulium	Xenotime is made of what?
xenotime.n.01	/r/MadeOf	ytterbium.n.01	xenotime	ytterbium|Yb|atomic number 70	is made of			WN		xenotime is made of ytterbium	Xenotime is made of what?
xenotime.n.01	/r/MadeOf	yttrium.n.01	xenotime	yttrium|Y|atomic number 39	is made of			WN		xenotime is made of yttrium	Xenotime is made of what?
zinc_blende.n.01	/r/MadeOf	indium.n.01	zinc blende|blende|sphalerite	indium|In|atomic number 49	is made of			WN		zinc blende is made of indium	Zinc blende is made of what?
zinc_blende.n.01	/r/MadeOf	thallium.n.01	zinc blende|blende|sphalerite	thallium|Tl|atomic number 81	is made of			WN		zinc blende is made of thallium	Zinc blende is made of what?
zinc_white.n.01	/r/MadeOf	zinc_oxide.n.01	zinc white|Chinese white	zinc oxide|flowers of zinc|philosopher's wool|philosophers' wool	is made of			WN		zinc white is made of zinc oxide	Zinc white is made of what?
zinnwaldite.n.01	/r/MadeOf	lithium.n.01	zinnwaldite	lithium|Li|atomic number 3	is made of			WN		zinnwaldite is made of lithium	Zinnwaldite is made of what?
zircon.n.01	/r/MadeOf	zirconium.n.01	zircon|zirconium silicate	zirconium|Zr|atomic number 40	is made of			WN		zircon is made of zirconium	Zircon is made of what?
```
