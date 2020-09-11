Import the entire ATOMIC into KGTK format. 

## Usage
```
usage: kgtk import-atomic [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [INPUT_FILE]

positional arguments:
  INPUT_FILE            The KGTK input file. (May be omitted or '-' for
                        stdin.) (Deprecated, use -i INPUT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)

```

## Examples

Import ATOMIC into KGTK. 

```
kgtk import-atomic -i v4_atomic_all_agg.csv -o atomic.tsv
```

Example output (first and last 10 lines):
```
node1	relation	node2	node1;label	node2;label	relation;label	relation;dimension	weight	source	origin	sentence	question
at:personx_'d_better_go	at:xAttr	at:avoidant	personx 'd better go|'d better go	avoidant	person x has attribute			AT		If personx 'd better go, then person x has attribute avoidant.	If personx 'd better go, then person x has attribute?
at:personx_'d_better_go	at:xAttr	at:weak	personx 'd better go|'d better go	weak	person x has attribute			AT		If personx 'd better go, then person x has attribute weak.	If personx 'd better go, then person x has attribute?
at:personx_'d_better_go	at:xAttr	at:hurried	personx 'd better go|'d better go	hurried	person x has attribute			AT		If personx 'd better go, then person x has attribute hurried.	If personx 'd better go, then person x has attribute?
at:personx_'d_better_go	at:xAttr	at:late	personx 'd better go|'d better go	late	person x has attribute			AT		If personx 'd better go, then person x has attribute late.	If personx 'd better go, then person x has attribute?
at:personx_'d_better_go	at:xAttr	at:tardy	personx 'd better go|'d better go	tardy	person x has attribute			AT		If personx 'd better go, then person x has attribute tardy.	If personx 'd better go, then person x has attribute?
at:personx_'d_better_go	at:xAttr	at:busy	personx 'd better go|'d better go	busy	person x has attribute			AT		If personx 'd better go, then person x has attribute busy.	If personx 'd better go, then person x has attribute?
at:personx_'d_better_go	at:xEffect	at:she_ran_to_the_bathroom	personx 'd better go|'d better go	she ran to the bathroom	effect on person x			AT		If personx 'd better go, then effect on person x she ran to the bathroom.	If personx 'd better go, then effect on person x?
at:personx_'d_better_go	at:xEffect	at:she_finally_made_it	personx 'd better go|'d better go	she finally made it	effect on person x			AT		If personx 'd better go, then effect on person x she finally made it.	If personx 'd better go, then effect on person x?
at:personx_'d_better_go	at:xEffect	at:leaves	personx 'd better go|'d better go	leaves	effect on person x			AT		If personx 'd better go, then effect on person x leaves.	If personx 'd better go, then effect on person x?
...
at:personx_zig_when_personx_shoulds_zag	at:xAttr	at:objective	personx zig when personx shoulds zag|zig when shoulds zag	objective	person x has attribute			AT		If personx zig when personx shoulds zag, then person x has attribute objective.	If personx zig when personx shoulds zag, then person x has attribute?
at:personx_zig_when_personx_shoulds_zag	at:xAttr	at:confrontational	personx zig when personx shoulds zag|zig when shoulds zag	confrontational	person x has attribute			AT		If personx zig when personx shoulds zag, then person x has attribute confrontational.	If personx zig when personx shoulds zag, then person x has attribute?
at:personx_zig_when_personx_shoulds_zag	at:xEffect	at:stumble_over_someone_else	personx zig when personx shoulds zag|zig when shoulds zag	stumble over someone else	effect on person x			AT		If personx zig when personx shoulds zag, then effect on person x stumble over someone else.	If personx zig when personx shoulds zag, then effect on person x?
at:personx_zig_when_personx_shoulds_zag	at:xEffect	at:gets_hurt	personx zig when personx shoulds zag|zig when shoulds zag	gets hurt	effect on person x			AT		If personx zig when personx shoulds zag, then effect on person x gets hurt.	If personx zig when personx shoulds zag, then effect on person x?
at:personx_zig_when_personx_shoulds_zag	at:xEffect	at:misses_an_opportunity	personx zig when personx shoulds zag|zig when shoulds zag	misses an opportunity	effect on person x			AIf personx zig when personx shoulds zag, then effect on person x misses an opportunity.	If personx zig when personx shoulds zag, then effect on person x?
at:personx_zig_when_personx_shoulds_zag	at:xEffect	at:learns_a_valuable_lesson	personx zig when personx shoulds zag|zig when shoulds zag	learns a valuable lesson	effect on person x			AT		If personx zig when personx shoulds zag, then effect on person x learns a valuable lesson.	If personx zig when personx shoulds zag, then effect on person x?
at:personx_zig_when_personx_shoulds_zag	at:xReact	at:regretful	personx zig when personx shoulds zag|zig when shoulds zag	regretful	person x feels			AT		If personx zig when personx shoulds zag, then person x feels regretful.	If personx zig when personx shoulds zag, then person x feels?
at:personx_zig_when_personx_shoulds_zag	at:xReact	at:like_he_did_the_wrong_thing,_he_should_have_zagged	personx zig when personx shoulds zag|zig when shoulds zag	like he did the wrong thing, he should have zagged	person x feels			AT		If personx zig when personx shoulds zag, then person x feels like he did the wrong thing, he should have zagged.	If personx zig when personx shoulds zag, then person x feels?
at:personx_zig_when_personx_shoulds_zag	at:xWant	at:to_sit_down_and_rest	personx zig when personx shoulds zag|zig when shoulds zag	to sit down and rest	person x wants			AT		If personx zig when personx shoulds zag, then person x wants to sit down and rest.	If personx zig when personx shoulds zag, then person x wants?
at:personx_zig_when_personx_shoulds_zag	at:xWant	at:to_find_out_their_time_in_the_race	personx zig when personx shoulds zag|zig when shoulds zag	to find out their time in the race	person x wants		AT		If personx zig when personx shoulds zag, then person x wants to find out their time in the race.	If personx zig when personx shoulds zag, then person x wants?
```
