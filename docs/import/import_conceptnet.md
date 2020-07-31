Import the entire ConceptNet, or just its English part, into KGTK format. 

## Usage
```
usage: kgtk import-conceptnet [-h] [-i INPUT_FILE] [--english_only] [INPUT_FILE]

positional arguments:
  INPUT_FILE            The KGTK input file. (May be omitted or '-' for stdin.) (Deprecated,
                        use -i INPUT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  --english_only        Only english conceptnet?
```

## Examples

Import the English part of ConceptNet into KGTK. 

```
kgtk import-conceptnet --english_only examples/conceptnet-assertions-5.7.0.csv
```

Example output (first and last 10 lines):
```
node1	relation	node2	node1;label	node2;label	relation;label	relation;dimension	weight	source	origin	sentence	question
/c/en/0/n	/r/Antonym	/c/en/1	0	1	antonym		1.0	CN	/d/wiktionary/fr		What is the opposite from 0?
/c/en/12_hour_clock/n	/r/Antonym	/c/en/24_hour_clock	12 hour clock	24 hour clock	antonym		1.0	CN	/d/wiktionary/en		What is the opposite from 12 hour clock?
/c/en/24_hour_clock/n	/r/Antonym	/c/en/12_hour_clock	24 hour clock	12 hour clock	antonym		1.0	CN	/d/wiktionary/en		What is the opposite from 24 hour clock?
/c/en/5/n	/r/Antonym	/c/en/3	5	3	antonym		1.0	CN	/d/wiktionary/en		What is the opposite from 5?
/c/en/a.c/n	/r/Antonym	/c/en/d.c	a.c	d.c	antonym		1.0	CN	/d/wiktionary/fr		What is the opposite from a.c?
/c/en/a.m/r	/r/Antonym	/c/en/afternoon	a.m	afternoon	antonym		1.0	CN	/d/wiktionary/en		What is the opposite from a.m?
/c/en/a.m/r	/r/Antonym	/c/en/p.m	a.m	p.m	antonym		3.464	CN	/d/wiktionary/en		What is the opposite from a.m?
/c/en/a.m/r	/r/Antonym	/c/en/pm	a.m	pm	antonym		1.0	CN	/d/wiktionary/fr		What is the opposite from a.m?
/c/en/ab_extra/r	/r/Antonym	/c/en/ab_intra	ab extra	ab intra	antonym		1.0	CN	/d/wiktionary/en		What is the opposite from ab extra?
...
/c/en/zoom_lens	/r/UsedFor	/c/en/examine_in_greater_detail	zoom lens	examine in greater detail	used for		1.0	CN	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[examine in greater detail]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/get_better_photographs	zoom lens	get better photographs	used for		1.0	CN	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[get better photographs]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/making_objects_appear_closer	zoom lens	making objects appear closer	used for		1.0	CN	/d/conceptnet/4/en	[[a zoom lens]] is used for [[making objects appear closer]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/observing_distant_object	zoom lens	observing distant object	used for		1.0	CN	/d/conceptnet/4/en	[[a zoom lens]] is for [[observing a distant object]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/photography	zoom lens	photography	used for		1.0	CN	/d/conceptnet/4/en	[[a zoom lens]] is used for [[photography]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/procure_better_shot	zoom lens	procure better shot	used for		1.0	CN	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[procure a better shot]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/see_things_bigger	zoom lens	see things bigger	used for		1.0	CN	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[see things bigger]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/seeing_distant_object_more_closely	zoom lens	seeing distant object more closely	used for		1.0	CN	/d/conceptnet/4/en	[[a zoom lens]] is for [[seeing a distant object more closely]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/take_pictures	zoom lens	take pictures	used for		1.0	CN	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[take pictures]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/varying_camera_focal_point	zoom lens	varying camera focal point	used for		1.0	CN	/d/conceptnet/4/en	[[a zoom lens]] is used for [[varying a camera focal point]]	What is zoom lens used for?
```
