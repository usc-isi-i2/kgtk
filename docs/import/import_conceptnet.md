Import the entire ConceptNet, or just its English part, into KGTK format. 

## Usage
```
kgtk import_conceptnet [-h] [--english_only] filename
```

positional arguments:
```
  filename        filename here
```

optional arguments:
```
  -h, --help      show this help message and exit
  --english_only  Only english conceptnet?
```

## Examples

Import the English part of ConceptNet into KGTK. 

```
kgtk import_conceptnet --english_only examples/conceptnet-assertions-5.7.0.csv
```

Example output (first and last 10 lines):
```
node1	label	node2	node1;label	label;label	node2;label	label;dimension	source	weight	creator	sentence	question
/c/en/0/n	/r/Antonym	/c/en/1	0	antonym	1		CN	1.0	/d/wiktionary/fr		What is the opposite from 0?
/c/en/12_hour_clock/n	/r/Antonym	/c/en/24_hour_clock	12 hour clock	antonym	24 hour clock		CN	1.0	/d/wiktionary/en		What is the opposite from 12 hour clock?
/c/en/24_hour_clock/n	/r/Antonym	/c/en/12_hour_clock	24 hour clock	antonym	12 hour clock		CN	1.0	/d/wiktionary/en		What is the opposite from 24 hour clock?
/c/en/5/n	/r/Antonym	/c/en/3	5	antonym	3		CN	1.0	/d/wiktionary/en		What is the opposite from 5?
/c/en/a.c/n	/r/Antonym	/c/en/d.c	a.c	antonym	d.c		CN	1.0	/d/wiktionary/fr		What is the opposite from a.c?
/c/en/a.m/r	/r/Antonym	/c/en/afternoon	a.m	antonym	afternoon		CN	1.0	/d/wiktionary/en		What is the opposite from a.m?
/c/en/a.m/r	/r/Antonym	/c/en/p.m	a.m	antonym	p.m		CN	3.464	/d/wiktionary/en		What is the opposite from a.m?
/c/en/a.m/r	/r/Antonym	/c/en/pm	a.m	antonym	pm		CN	1.0	/d/wiktionary/fr		What is the opposite from a.m?
/c/en/ab_extra/r	/r/Antonym	/c/en/ab_intra	ab extra	antonym	ab intra		CN	1.0	/d/wiktionary/en		What is the opposite from ab extra?
...
/c/en/zoom_lens	/r/UsedFor	/c/en/examine_in_greater_detail	zoom lens	used for	examine in greater detail		CN	1.0	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[examine in greater detail]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/get_better_photographs	zoom lens	used for	get better photographs		CN	1.0	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[get better photographs]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/making_objects_appear_closer	zoom lens	used for	making objects appear closer		CN	1.0	/d/conceptnet/4/en	[[a zoom lens]] is used for [[making objects appear closer]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/observing_distant_object	zoom lens	used for	observing distant object		CN	1.0	/d/conceptnet/4/en	[[a zoom lens]] is for [[observing a distant object]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/photography	zoom lens	used for	photography		CN	1.0	/d/conceptnet/4/en	[[a zoom lens]] is used for [[photography]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/procure_better_shot	zoom lens	used for	procure better shot		CN	1.0	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[procure a better shot]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/see_things_bigger	zoom lens	used for	see things bigger		CN	1.0	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[see things bigger]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/seeing_distant_object_more_closely	zoom lens	used for	seeing distant object more closely		CN	1.0	/d/conceptnet/4/en	[[a zoom lens]] is for [[seeing a distant object more closely]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/take_pictures	zoom lens	used for	take pictures		CN	1.0	/d/conceptnet/4/en	You can use [[a zoom lens]] to [[take pictures]]	What is zoom lens used for?
/c/en/zoom_lens	/r/UsedFor	/c/en/varying_camera_focal_point	zoom lens	used for	varying camera focal point		CN	1.0	/d/conceptnet/4/en	[[a zoom lens]] is used for [[varying a camera focal point]]	What is zoom lens used for?
```
