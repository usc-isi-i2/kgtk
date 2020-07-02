Import WordNet v3.0 into KGTK format. Currently, four relations are included: hypernymy, membership holonymy, part-of holonymy, and substance meronymy. The resulting KGTK file consists of 12 columns.

## Usage
```
usage: kgtk import-wordnet [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## Examples

Importing WordNet can be done as follows (no arguments should be provided, as WordNet is read through the NLTK package):

```
kgtk import-wordnet
```

Example output (first and last 10 lines):
```
node1	label	node2	node1;label	label;label	node2;label	label;dimension	source	weight	creator	sentence	question
physical_entity.n.01	/r/IsA	entity.n.01	physical entity	is a	entity		WN	1.0		physical entity is a entity	What is physical entity?
abstraction.n.06	/r/IsA	entity.n.01	abstraction|abstract entity	is a	entity		WN	1.0		abstraction is a entity	What is abstraction?
thing.n.12	/r/IsA	physical_entity.n.01	thing	is a	physical entity		WN	1.0		thing is a physical entity	What is thing?
object.n.01	/r/IsA	physical_entity.n.01	object|physical object	is a	physical entity		WN	1.0		object is a physical entity	What is object?
whole.n.02	/r/IsA	object.n.01	whole|unit	is a	object|physical object		WN	1.0		whole is a object	What is whole?
congener.n.03	/r/IsA	whole.n.02	congener	is a	whole|unit		WN	1.0		congener is a whole	What is congener?
living_thing.n.01	/r/IsA	whole.n.02	living thing|animate thing	is a	whole|unit		WN	1.0		living thing is a whole	What is living thing?
organism.n.01	/r/IsA	living_thing.n.01	organism|being	is a	living thing|animate thing		WN	1.0		organism is a living thing	What is organism?
benthos.n.02	/r/IsA	organism.n.01	benthos	is a	organism|being		WN	1.0		benthos is a organism	What is benthos?
...
fertile_period.n.01	/r/PartOf	menstrual_cycle.n.01	fertile period|fertile phase	is a part of	menstrual cycle		WN	1.0		fertile period is a part of menstrual cycle	Fertile period is a part of what?
menstrual_phase.n.01	/r/PartOf	menstrual_cycle.n.01	menstrual phase	is a part of	menstrual cycle		WN	1.0		menstrual phase is a part of menstrual cycle	Menstrual phase is a part of what?
secretory_phase.n.01	/r/PartOf	menstrual_cycle.n.01	secretory phase|luteal phase	is a part of	menstrual cycle		WN	1.0		secretory phase is a part of menstrual cycle	Secretory phase is a part of what?
phase.n.03	/r/PartOf	cycle.n.01	phase|phase angle	is a part of	cycle|rhythm|round		WN	1.0		phase is a part of cycle	Phase is a part of what?
shift.n.03	/r/PartOf	workday.n.02	shift|work shift|duty period	is a part of	workday|working day		WN	1.0		shift is a part of workday	Shift is a part of what?
safe_period.n.01	/r/PartOf	menstrual_cycle.n.01	safe period	is a part of	menstrual cycle		WN	1.0		safe period is a part of menstrual cycle	Safe period is a part of what?
rotational_latency.n.01	/r/PartOf	access_time.n.01	rotational latency|latency	is a part of	access time		WN	1.0		rotational latency is a part of access time	Rotational latency is a part of what?
command_processing_overhead_time.n.01	/r/PartOf	access_time.n.01	command processing overhead time|command processing overhead|command overhead|overhead	is a part of	access time		WN	1.0		command processing overhead time is a part of access time	Command processing overhead time is a part of what?
study_hall.n.01	/r/PartOf	school.n.05	study hall	is a part of	school|schooltime|school day		WN	1.0		study hall is a part of school	Study hall is a part of what?
9/11.n.01	/r/PartOf	september.n.01	9/11|9-11|September 11|Sept. 11|Sep 11	is a part of	September|Sep|Sept		WN	1.0		9/11 is a part of September	9/11 is a part of what?
```
