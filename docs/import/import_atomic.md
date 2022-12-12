Import the entire ATOMIC knowledge graph into KGTK format. 

## Background

The ATOMIC ([Sap et al., 2019](https://arxiv.org/pdf/1811.00146.pdf)) knowlege
graph is a recently constructed knowledge graph of common sense statements for
events. It consists of over 700k statements that describe 24k base events with
9 relations. The knowledge covered in ATOMIC expresses event causality and
implications on their (human) participants. Since its creation, ATOMIC has
been a common resource in KG-augmented downstream reasoning systems, built for
tasks such as question answering or natural language inference.

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

## Obtaining the ATOMIC Knowlege Graph

The ATOMIC knowlege graph can be downloaded [here](https://storage.googleapis.com/ai2-mosaic/public/atomic/v1.0/atomic_data.tgz).
The compressed `tar` file sould be opened by `tar`.

```
mkdir atomic_data
cd atomic_data
wget https://storage.googleapis.com/ai2-mosaic/public/atomic/v1.0/atomic_data.tgz
tar xvzf atomic_data.tgz

```

The KGTK importer uses the aggregated file from the download: `v4_atomic_all_agg.csv`.
This is a comma-separated value file that encodes `if-then` relations.


## Examples

### Sample Data
Here is a sample of the atomic knowlege graph:

```
cat examples/docs/v4_atomic_all_agg_sample.csv
```

~~~
event,oEffect,oReact,oWant,xAttr,xEffect,xIntent,xNeed,xReact,xWant,prefix,split
PersonX 'd better go,"[""none"", ""none""]","[""none"", ""none""]","[""none"", ""none"", ""none""]","[""avoidant"", ""weak"", ""hurried"", ""late"", ""Tardy"", ""busy""]","[""She ran to the bathroom"", ""She finally made it"", ""leaves"", ""runs away""]","[""to go somewhere else more important."", ""none""]","[""none"", ""none"", ""none""]","[""the person feels happy since he arrived at his destination."", ""rushed, in a hurry""]","[""to escape from him"", ""to resign his job"", ""to leave on time"", ""to arrive home"", ""to relax and unwind"", ""to walk away"", ""not speak to anyone""]","[""better"", ""go""]",dev
PersonX abandons ___ altogether,"[""none"", ""none""]","[""dejected""]","[""none"", ""none"", ""to find a new job for him"", ""to support him""]","[""impatient"", ""decisive"", ""undependable"", ""fickle"", ""destructed"", ""sad""]","[""gets a reputation as a quitter"", ""hangs head in shame"", ""Begins the process of change"", ""Turns over a new leaf""]","[""put a stop""]","[""Plows the field."", ""Gets exhausted from it."", ""none"", ""to give a resignation letter"", ""to get permission from his parents""]","[""authoritative""]","[""Sell his land."", ""Was just city."", ""to start something new"", ""to start fresh"", ""to find a new job"", ""to search for a new job""]","[""abandons"", ""altogether""]",trn
PersonX abandons the ___ altogether,"[""none"", ""none"", ""none""]","[""defeat""]","[""none"", ""to do something else as well"", ""they find something better"", ""none""]","[""flaky"", ""irresponsible"", ""desperate"", ""convinced"", ""decisive"", ""frustrated""]","[""eats all the cakes"", ""abandons his diets too"", ""repercussions for leaving all responsibilities"", ""they go home"", ""they try to form a different plan"", ""they search for a different alternative""]","[""to appear not interested""]","[""none"", ""to get frustrated"", ""to determine it's not worth it"", ""none""]","[""pressurized""]","[""to go out"", ""to find other place"", ""find something else to do"", ""to do the project the best he can"", ""sigh in relief"", ""find another project""]","[""abandons"", ""altogether""]",trn
PersonX abolishes ___ altogether,"[""none"", ""none"", ""none""]","[""none""]","[""to be free"", ""to do things of their own wish"", ""for things to change for the better"", ""for their to be a better law""]","[""ruthless"", ""destructive"", ""strict"", ""determined"", ""successful"", ""joyful""]","[""loss money"", ""change house"", ""get loan"", ""person x is free"", ""person x lives"", ""to abolishes to altogether"", ""to gether voice""]","[""give a punishment in person""]","[""to have a plan"", ""to have a reason"", ""to know the law"", ""to not like it""]","[""he was sad""]","[""human to be free"", ""not to feel pain"", ""to make a new law"", ""to change things for the betters""]","[""abolishes"", ""altogether""]",trn
PersonX abolishes ___ in the states,"[""none""]","[""none""]","[""to celebrate"", ""to write about the new law"", ""to move past this event"", ""to be free"", ""none""]","[""bold"", ""authoritative"", ""determined"", ""heroic"", ""empathativ"", ""thoughtful"", ""proud"", ""moral"", ""principaled""]","[""none""]","[""this is unhappiness for people""]","[""to find a problem"", ""to find out to stop that problem"", ""to acquire power and/or influence"", ""to know how the legal system works""]","[""sad""]","[""to enforce the ruling"", ""memorialize the law"", ""fairness"", ""to do the right thing"", ""to go good"", ""to make others happy""]","[""abolishes"", ""states""]",trn
PersonX abolishes the ___ altogether,"[""none"", ""the people lost the documents"", ""the people   loss the  trust""]","[""grateful"", ""disrespected""]","[""to publish an article"", ""to find other pursuits"", ""to follow the laws"", ""to protest""]","[""dedicated"", ""furious"", ""powerful"", ""influencial""]","[""set free"", ""become independent"", ""lost the data"", ""lost the documents""]","[""to end it"", ""to do it his way""]","[""find a lawyer"", ""file a lawsuit"", ""to gather information"", ""to collaborate with others""]","[""happy"", ""like he's the boss""]","[""to celebrate"", ""to write a paper"", ""to implement rules"", ""to communicate the laws with others""]","[""abolishes"", ""altogether""]",trn
PersonX about to get married,"[""their partner is in a legal relationship"", ""their partner's legal status changes"", ""says yes"", ""Gets dress""]","[""like they have a lifelong companion"", ""happy""]","[""to spend the rest of their life with personx"", ""to be happy with personx"", ""to start a family"", ""to go on vacation""]","[""excited"", ""anxious"", ""anxious"", ""nervous"", ""brave""]","[""they are in a legal relationship"", ""their legal status changes"", ""Get a tuxedo"", ""Gets ring""]","[""to share his life with someone"", ""to marry someone""]","[""meet someone"", ""get engaged"", ""to meet someone"", ""to really like them""]","[""like he has someone he feels that way about"", ""happy""]","[""to live happily ever after"", ""to be happily married"", ""to go on a honey moon"", ""to start a family""]","[""get"", ""married""]",trn
PersonX absolutely loved,"[""none"", ""none""]","[""happy.""]","[""none"", ""to marry him"", ""to accompany him all his life""]","[""caring"", ""faithful"", ""Passionate"", ""Caring"", ""gentle"", ""loving""]","[""none"", ""gains knowledge"", ""is entertained""]","[""to marry.""]","[""none"", ""none""]","[""romantic.""]","[""to tell others"", ""write a review"", ""to propose to her"", ""to marry her""]","[""absolutely"", ""loved""]",trn
PersonX absolutely loved ___,"[""none""]","[""none"", ""none"", ""none""]","[""none"", ""none"", ""none""]","[""compassionate"", ""friendly"", ""hungry"", ""excited"", ""enthusiastic"", ""amiable"", ""good-natured""]","[""smiles when they think about the event"", ""smiles when they see dogs""]","[""to see different places"", ""to enjoy"", ""to express devotion"", ""to read""]","[""to see what they want"", ""to try it out"", ""none"", ""none""]","[""happy"", ""satisfied"", ""excited"", ""pleasant"", ""relaxed""]","[""to feel satisfied"", ""to do it again"", ""Visit her often."", ""Takes her for walks."", ""to enjoy more of"", ""to share with others""]","[""absolutely"", ""loved""]",trn
PersonX absolutely loved it,"[""none"", ""none"", ""none""]","[""none"", ""none""]","[""none"", ""none"", ""none""]","[""enthused"", ""appreciative"", ""satisfied"", ""contented"", ""Delighted"", ""Amazed""]","[""stomped feet"", ""laughed"", ""takes it home"", ""buys it"", ""found a new interest"", ""gained knowledge""]","[""none"", ""none""]","[""none"", ""none"", ""none""]","[""ecstatic over his gift"", ""happy"", ""joyful""]","[""to buy more"", ""to eat more"", ""to take pictures."", ""to buy more."", ""to use it"", ""to show it to everyone"", ""to thank the person who gave it to them""]","[""absolutely"", ""loved""]",trn
PersonX absorbs every ___,"[""none""]","[""none"", ""none""]","[""none"", ""none"", ""none""]","[""Conscious"", ""Aware"", ""unwasteful"", ""smart""]","[""none""]","[""moment"", ""to completely understand his position and the alternatives""]","[""none"", ""to walk around and take notes"", ""to relax in the spa"", ""to be a quick learner"", ""to be a good listener"", ""to be at a conference"", ""to be in class""]","[""very nice"", ""well educated on the pros and cons of the matter""]","[""not to waste any detail"", ""to make good use of that knowledge"", ""to know all the information"", ""to be aware of their surroundings"", ""to write notes"", ""to remember every detail"", ""to teach others""]","[""absorbs"", ""every""]",trn
~~~

Here is the same data displayed for easier reading:

```
kgtk cat -i examples/docs/v4_atomic_all_agg_sample.csv --mode=NONE / md
```

| event | oEffect | oReact | oWant | xAttr | xEffect | xIntent | xNeed | xReact | xWant | prefix | split |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| PersonX 'd better go | "[\\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"avoidant\\", \\"weak\\", \\"hurried\\", \\"late\\", \\"Tardy\\", \\"busy\\"]" | "[\\"She ran to the bathroom\\", \\"She finally made it\\", \\"leaves\\", \\"runs away\\"]" | "[\\"to go somewhere else more important.\\", \\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"the person feels happy since he arrived at his destination.\\", \\"rushed, in a hurry\\"]" | "[\\"to escape from him\\", \\"to resign his job\\", \\"to leave on time\\", \\"to arrive home\\", \\"to relax and unwind\\", \\"to walk away\\", \\"not speak to anyone\\"]" | "[\\"better\\", \\"go\\"]" | dev |
| PersonX abandons ___ altogether | "[\\"none\\", \\"none\\"]" | "[\\"dejected\\"]" | "[\\"none\\", \\"none\\", \\"to find a new job for him\\", \\"to support him\\"]" | "[\\"impatient\\", \\"decisive\\", \\"undependable\\", \\"fickle\\", \\"destructed\\", \\"sad\\"]" | "[\\"gets a reputation as a quitter\\", \\"hangs head in shame\\", \\"Begins the process of change\\", \\"Turns over a new leaf\\"]" | "[\\"put a stop\\"]" | "[\\"Plows the field.\\", \\"Gets exhausted from it.\\", \\"none\\", \\"to give a resignation letter\\", \\"to get permission from his parents\\"]" | "[\\"authoritative\\"]" | "[\\"Sell his land.\\", \\"Was just city.\\", \\"to start something new\\", \\"to start fresh\\", \\"to find a new job\\", \\"to search for a new job\\"]" | "[\\"abandons\\", \\"altogether\\"]" | trn |
| PersonX abandons the ___ altogether | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"defeat\\"]" | "[\\"none\\", \\"to do something else as well\\", \\"they find something better\\", \\"none\\"]" | "[\\"flaky\\", \\"irresponsible\\", \\"desperate\\", \\"convinced\\", \\"decisive\\", \\"frustrated\\"]" | "[\\"eats all the cakes\\", \\"abandons his diets too\\", \\"repercussions for leaving all responsibilities\\", \\"they go home\\", \\"they try to form a different plan\\", \\"they search for a different alternative\\"]" | "[\\"to appear not interested\\"]" | "[\\"none\\", \\"to get frustrated\\", \\"to determine it\\'s not worth it\\", \\"none\\"]" | "[\\"pressurized\\"]" | "[\\"to go out\\", \\"to find other place\\", \\"find something else to do\\", \\"to do the project the best he can\\", \\"sigh in relief\\", \\"find another project\\"]" | "[\\"abandons\\", \\"altogether\\"]" | trn |
| PersonX abolishes ___ altogether | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"none\\"]" | "[\\"to be free\\", \\"to do things of their own wish\\", \\"for things to change for the better\\", \\"for their to be a better law\\"]" | "[\\"ruthless\\", \\"destructive\\", \\"strict\\", \\"determined\\", \\"successful\\", \\"joyful\\"]" | "[\\"loss money\\", \\"change house\\", \\"get loan\\", \\"person x is free\\", \\"person x lives\\", \\"to abolishes to altogether\\", \\"to gether voice\\"]" | "[\\"give a punishment in person\\"]" | "[\\"to have a plan\\", \\"to have a reason\\", \\"to know the law\\", \\"to not like it\\"]" | "[\\"he was sad\\"]" | "[\\"human to be free\\", \\"not to feel pain\\", \\"to make a new law\\", \\"to change things for the betters\\"]" | "[\\"abolishes\\", \\"altogether\\"]" | trn |
| PersonX abolishes ___ in the states | "[\\"none\\"]" | "[\\"none\\"]" | "[\\"to celebrate\\", \\"to write about the new law\\", \\"to move past this event\\", \\"to be free\\", \\"none\\"]" | "[\\"bold\\", \\"authoritative\\", \\"determined\\", \\"heroic\\", \\"empathativ\\", \\"thoughtful\\", \\"proud\\", \\"moral\\", \\"principaled\\"]" | "[\\"none\\"]" | "[\\"this is unhappiness for people\\"]" | "[\\"to find a problem\\", \\"to find out to stop that problem\\", \\"to acquire power and/or influence\\", \\"to know how the legal system works\\"]" | "[\\"sad\\"]" | "[\\"to enforce the ruling\\", \\"memorialize the law\\", \\"fairness\\", \\"to do the right thing\\", \\"to go good\\", \\"to make others happy\\"]" | "[\\"abolishes\\", \\"states\\"]" | trn |
| PersonX abolishes the ___ altogether | "[\\"none\\", \\"the people lost the documents\\", \\"the people   loss the  trust\\"]" | "[\\"grateful\\", \\"disrespected\\"]" | "[\\"to publish an article\\", \\"to find other pursuits\\", \\"to follow the laws\\", \\"to protest\\"]" | "[\\"dedicated\\", \\"furious\\", \\"powerful\\", \\"influencial\\"]" | "[\\"set free\\", \\"become independent\\", \\"lost the data\\", \\"lost the documents\\"]" | "[\\"to end it\\", \\"to do it his way\\"]" | "[\\"find a lawyer\\", \\"file a lawsuit\\", \\"to gather information\\", \\"to collaborate with others\\"]" | "[\\"happy\\", \\"like he\\'s the boss\\"]" | "[\\"to celebrate\\", \\"to write a paper\\", \\"to implement rules\\", \\"to communicate the laws with others\\"]" | "[\\"abolishes\\", \\"altogether\\"]" | trn |
| PersonX about to get married | "[\\"their partner is in a legal relationship\\", \\"their partner\\'s legal status changes\\", \\"says yes\\", \\"Gets dress\\"]" | "[\\"like they have a lifelong companion\\", \\"happy\\"]" | "[\\"to spend the rest of their life with personx\\", \\"to be happy with personx\\", \\"to start a family\\", \\"to go on vacation\\"]" | "[\\"excited\\", \\"anxious\\", \\"anxious\\", \\"nervous\\", \\"brave\\"]" | "[\\"they are in a legal relationship\\", \\"their legal status changes\\", \\"Get a tuxedo\\", \\"Gets ring\\"]" | "[\\"to share his life with someone\\", \\"to marry someone\\"]" | "[\\"meet someone\\", \\"get engaged\\", \\"to meet someone\\", \\"to really like them\\"]" | "[\\"like he has someone he feels that way about\\", \\"happy\\"]" | "[\\"to live happily ever after\\", \\"to be happily married\\", \\"to go on a honey moon\\", \\"to start a family\\"]" | "[\\"get\\", \\"married\\"]" | trn |
| PersonX absolutely loved | "[\\"none\\", \\"none\\"]" | "[\\"happy.\\"]" | "[\\"none\\", \\"to marry him\\", \\"to accompany him all his life\\"]" | "[\\"caring\\", \\"faithful\\", \\"Passionate\\", \\"Caring\\", \\"gentle\\", \\"loving\\"]" | "[\\"none\\", \\"gains knowledge\\", \\"is entertained\\"]" | "[\\"to marry.\\"]" | "[\\"none\\", \\"none\\"]" | "[\\"romantic.\\"]" | "[\\"to tell others\\", \\"write a review\\", \\"to propose to her\\", \\"to marry her\\"]" | "[\\"absolutely\\", \\"loved\\"]" | trn |
| PersonX absolutely loved ___ | "[\\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"compassionate\\", \\"friendly\\", \\"hungry\\", \\"excited\\", \\"enthusiastic\\", \\"amiable\\", \\"good-natured\\"]" | "[\\"smiles when they think about the event\\", \\"smiles when they see dogs\\"]" | "[\\"to see different places\\", \\"to enjoy\\", \\"to express devotion\\", \\"to read\\"]" | "[\\"to see what they want\\", \\"to try it out\\", \\"none\\", \\"none\\"]" | "[\\"happy\\", \\"satisfied\\", \\"excited\\", \\"pleasant\\", \\"relaxed\\"]" | "[\\"to feel satisfied\\", \\"to do it again\\", \\"Visit her often.\\", \\"Takes her for walks.\\", \\"to enjoy more of\\", \\"to share with others\\"]" | "[\\"absolutely\\", \\"loved\\"]" | trn |
| PersonX absolutely loved it | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"enthused\\", \\"appreciative\\", \\"satisfied\\", \\"contented\\", \\"Delighted\\", \\"Amazed\\"]" | "[\\"stomped feet\\", \\"laughed\\", \\"takes it home\\", \\"buys it\\", \\"found a new interest\\", \\"gained knowledge\\"]" | "[\\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"ecstatic over his gift\\", \\"happy\\", \\"joyful\\"]" | "[\\"to buy more\\", \\"to eat more\\", \\"to take pictures.\\", \\"to buy more.\\", \\"to use it\\", \\"to show it to everyone\\", \\"to thank the person who gave it to them\\"]" | "[\\"absolutely\\", \\"loved\\"]" | trn |
| PersonX absorbs every ___ | "[\\"none\\"]" | "[\\"none\\", \\"none\\"]" | "[\\"none\\", \\"none\\", \\"none\\"]" | "[\\"Conscious\\", \\"Aware\\", \\"unwasteful\\", \\"smart\\"]" | "[\\"none\\"]" | "[\\"moment\\", \\"to completely understand his position and the alternatives\\"]" | "[\\"none\\", \\"to walk around and take notes\\", \\"to relax in the spa\\", \\"to be a quick learner\\", \\"to be a good listener\\", \\"to be at a conference\\", \\"to be in class\\"]" | "[\\"very nice\\", \\"well educated on the pros and cons of the matter\\"]" | "[\\"not to waste any detail\\", \\"to make good use of that knowledge\\", \\"to know all the information\\", \\"to be aware of their surroundings\\", \\"to write notes\\", \\"to remember every detail\\", \\"to teach others\\"]" | "[\\"absorbs\\", \\"every\\"]" | trn |


### Import the ATOMIC Knowlege Graph into KGTK Format

Import the sample ATOMIC knowlege graph into KGTK format using the `kgtk import-atomic` command:

```
kgtk import-atomic -i examples/docs/v4_atomic_all_agg_sample.csv -o atomic_data.tsv
```

Here is the output:

```
kgtk cat -i atomic_data.tsv
```

| node1 | relation | node2 | node1;label | node2;label | relation;label | relation;dimension | source | sentence |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| at:personx_'d_better_go | at:xAttr | at:avoidant | "personx \\'d better go"\|"\\'d better go" | "avoidant" | "person x has attribute" |  | "AT" |  |
| at:personx_'d_better_go | at:xAttr | at:weak | "personx \\'d better go"\|"\\'d better go" | "weak" | "person x has attribute" |  | "AT" |  |
| at:personx_'d_better_go | at:xAttr | at:hurried | "personx \\'d better go"\|"\\'d better go" | "hurried" | "person x has attribute" |  | "AT" |  |
| at:personx_'d_better_go | at:xAttr | at:late | "personx \\'d better go"\|"\\'d better go" | "late" | "person x has attribute" |  | "AT" |  |
| at:personx_'d_better_go | at:xAttr | at:tardy | "personx \\'d better go"\|"\\'d better go" | "tardy" | "person x has attribute" |  | "AT" |  |
| at:personx_'d_better_go | at:xAttr | at:busy | "personx \\'d better go"\|"\\'d better go" | "busy" | "person x has attribute" |  | "AT" |  |
| at:personx_'d_better_go | at:xEffect | at:she_ran_to_the_bathroom | "personx \\'d better go"\|"\\'d better go" | "she ran to the bathroom" | "effect on person x" |  | "AT" |  |
| at:personx_'d_better_go | at:xEffect | at:she_finally_made_it | "personx \\'d better go"\|"\\'d better go" | "she finally made it" | "effect on person x" |  | "AT" |  |
| at:personx_'d_better_go | at:xEffect | at:leaves | "personx \\'d better go"\|"\\'d better go" | "leaves" | "effect on person x" |  | "AT" |  |
| at:personx_'d_better_go | at:xEffect | at:runs_away | "personx \\'d better go"\|"\\'d better go" | "runs away" | "effect on person x" |  | "AT" |  |
| at:personx_'d_better_go | at:xIntent | at:to_go_somewhere_else_more_important | "personx \\'d better go"\|"\\'d better go" | "to go somewhere else more important" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xReact | at:the_person_feels_happy_since_he_arrived_at_his_destination | "personx \\'d better go"\|"\\'d better go" | "the person feels happy since he arrived at his destination" | "person x feels" |  | "AT" |  |
| at:personx_'d_better_go | at:xReact | at:rushed,_in_a_hurry | "personx \\'d better go"\|"\\'d better go" | "rushed, in a hurry" | "person x feels" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:to_escape_from_him | "personx \\'d better go"\|"\\'d better go" | "to escape from him" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:to_resign_his_job | "personx \\'d better go"\|"\\'d better go" | "to resign his job" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:to_leave_on_time | "personx \\'d better go"\|"\\'d better go" | "to leave on time" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:to_arrive_home | "personx \\'d better go"\|"\\'d better go" | "to arrive home" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:to_relax_and_unwind | "personx \\'d better go"\|"\\'d better go" | "to relax and unwind" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:to_walk_away | "personx \\'d better go"\|"\\'d better go" | "to walk away" | "person x wants" |  | "AT" |  |
| at:personx_'d_better_go | at:xWant | at:not_speak_to_anyone | "personx \\'d better go"\|"\\'d better go" | "not speak to anyone" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:oReact | at:dejected | "personx abandons ___ altogether"\|"abandons altogether" | "dejected" | "others feel" |  | "AT" |  |
| at:personx_abandons_____altogether | at:oWant | at:to_find_a_new_job_for_him | "personx abandons ___ altogether"\|"abandons altogether" | "to find a new job for him" | "others want" |  | "AT" |  |
| at:personx_abandons_____altogether | at:oWant | at:to_support_him | "personx abandons ___ altogether"\|"abandons altogether" | "to support him" | "others want" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xAttr | at:impatient | "personx abandons ___ altogether"\|"abandons altogether" | "impatient" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xAttr | at:decisive | "personx abandons ___ altogether"\|"abandons altogether" | "decisive" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xAttr | at:undependable | "personx abandons ___ altogether"\|"abandons altogether" | "undependable" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xAttr | at:fickle | "personx abandons ___ altogether"\|"abandons altogether" | "fickle" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xAttr | at:destructed | "personx abandons ___ altogether"\|"abandons altogether" | "destructed" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xAttr | at:sad | "personx abandons ___ altogether"\|"abandons altogether" | "sad" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xEffect | at:gets_a_reputation_as_a_quitter | "personx abandons ___ altogether"\|"abandons altogether" | "gets a reputation as a quitter" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xEffect | at:hangs_head_in_shame | "personx abandons ___ altogether"\|"abandons altogether" | "hangs head in shame" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xEffect | at:begins_the_process_of_change | "personx abandons ___ altogether"\|"abandons altogether" | "begins the process of change" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xEffect | at:turns_over_a_new_leaf | "personx abandons ___ altogether"\|"abandons altogether" | "turns over a new leaf" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xIntent | at:put_a_stop | "personx abandons ___ altogether"\|"abandons altogether" | "put a stop" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xNeed | at:plows_the_field | "personx abandons ___ altogether"\|"abandons altogether" | "plows the field" | "person x needs" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xNeed | at:gets_exhausted_from_it | "personx abandons ___ altogether"\|"abandons altogether" | "gets exhausted from it" | "person x needs" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xNeed | at:to_give_a_resignation_letter | "personx abandons ___ altogether"\|"abandons altogether" | "to give a resignation letter" | "person x needs" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xNeed | at:to_get_permission_from_his_parents | "personx abandons ___ altogether"\|"abandons altogether" | "to get permission from his parents" | "person x needs" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xReact | at:authoritative | "personx abandons ___ altogether"\|"abandons altogether" | "authoritative" | "person x feels" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xWant | at:sell_his_land | "personx abandons ___ altogether"\|"abandons altogether" | "sell his land" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xWant | at:was_just_city | "personx abandons ___ altogether"\|"abandons altogether" | "was just city" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xWant | at:to_start_something_new | "personx abandons ___ altogether"\|"abandons altogether" | "to start something new" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xWant | at:to_start_fresh | "personx abandons ___ altogether"\|"abandons altogether" | "to start fresh" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xWant | at:to_find_a_new_job | "personx abandons ___ altogether"\|"abandons altogether" | "to find a new job" | "person x wants" |  | "AT" |  |
| at:personx_abandons_____altogether | at:xWant | at:to_search_for_a_new_job | "personx abandons ___ altogether"\|"abandons altogether" | "to search for a new job" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:oReact | at:defeat | "personx abandons the ___ altogether"\|"abandons altogether" | "defeat" | "others feel" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:oWant | at:to_do_something_else_as_well | "personx abandons the ___ altogether"\|"abandons altogether" | "to do something else as well" | "others want" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:oWant | at:they_find_something_better | "personx abandons the ___ altogether"\|"abandons altogether" | "they find something better" | "others want" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xAttr | at:flaky | "personx abandons the ___ altogether"\|"abandons altogether" | "flaky" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xAttr | at:irresponsible | "personx abandons the ___ altogether"\|"abandons altogether" | "irresponsible" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xAttr | at:desperate | "personx abandons the ___ altogether"\|"abandons altogether" | "desperate" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xAttr | at:convinced | "personx abandons the ___ altogether"\|"abandons altogether" | "convinced" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xAttr | at:decisive | "personx abandons the ___ altogether"\|"abandons altogether" | "decisive" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xAttr | at:frustrated | "personx abandons the ___ altogether"\|"abandons altogether" | "frustrated" | "person x has attribute" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xEffect | at:eats_all_the_cakes | "personx abandons the ___ altogether"\|"abandons altogether" | "eats all the cakes" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xEffect | at:abandons_his_diets_too | "personx abandons the ___ altogether"\|"abandons altogether" | "abandons his diets too" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xEffect | at:repercussions_for_leaving_all_responsibilities | "personx abandons the ___ altogether"\|"abandons altogether" | "repercussions for leaving all responsibilities" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xEffect | at:they_go_home | "personx abandons the ___ altogether"\|"abandons altogether" | "they go home" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xEffect | at:they_try_to_form_a_different_plan | "personx abandons the ___ altogether"\|"abandons altogether" | "they try to form a different plan" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xEffect | at:they_search_for_a_different_alternative | "personx abandons the ___ altogether"\|"abandons altogether" | "they search for a different alternative" | "effect on person x" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xIntent | at:to_appear_not_interested | "personx abandons the ___ altogether"\|"abandons altogether" | "to appear not interested" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xNeed | at:to_get_frustrated | "personx abandons the ___ altogether"\|"abandons altogether" | "to get frustrated" | "person x needs" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xNeed | at:to_determine_it's_not_worth_it | "personx abandons the ___ altogether"\|"abandons altogether" | "to determine it\\'s not worth it"\|"to determine it not worth it" | "person x needs" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xReact | at:pressurized | "personx abandons the ___ altogether"\|"abandons altogether" | "pressurized" | "person x feels" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xWant | at:to_go_out | "personx abandons the ___ altogether"\|"abandons altogether" | "to go out" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xWant | at:to_find_other_place | "personx abandons the ___ altogether"\|"abandons altogether" | "to find other place" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xWant | at:find_something_else_to_do | "personx abandons the ___ altogether"\|"abandons altogether" | "find something else to do" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xWant | at:to_do_the_project_the_best_he_can | "personx abandons the ___ altogether"\|"abandons altogether" | "to do the project the best he can" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xWant | at:sigh_in_relief | "personx abandons the ___ altogether"\|"abandons altogether" | "sigh in relief" | "person x wants" |  | "AT" |  |
| at:personx_abandons_the_____altogether | at:xWant | at:find_another_project | "personx abandons the ___ altogether"\|"abandons altogether" | "find another project" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:oWant | at:to_be_free | "personx abolishes ___ altogether"\|"abolishes altogether" | "to be free" | "others want" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:oWant | at:to_do_things_of_their_own_wish | "personx abolishes ___ altogether"\|"abolishes altogether" | "to do things of their own wish" | "others want" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:oWant | at:for_things_to_change_for_the_better | "personx abolishes ___ altogether"\|"abolishes altogether" | "for things to change for the better" | "others want" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:oWant | at:for_their_to_be_a_better_law | "personx abolishes ___ altogether"\|"abolishes altogether" | "for their to be a better law" | "others want" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xAttr | at:ruthless | "personx abolishes ___ altogether"\|"abolishes altogether" | "ruthless" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xAttr | at:destructive | "personx abolishes ___ altogether"\|"abolishes altogether" | "destructive" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xAttr | at:strict | "personx abolishes ___ altogether"\|"abolishes altogether" | "strict" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xAttr | at:determined | "personx abolishes ___ altogether"\|"abolishes altogether" | "determined" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xAttr | at:successful | "personx abolishes ___ altogether"\|"abolishes altogether" | "successful" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xAttr | at:joyful | "personx abolishes ___ altogether"\|"abolishes altogether" | "joyful" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:loss_money | "personx abolishes ___ altogether"\|"abolishes altogether" | "loss money" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:change_house | "personx abolishes ___ altogether"\|"abolishes altogether" | "change house" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:get_loan | "personx abolishes ___ altogether"\|"abolishes altogether" | "get loan" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:person_x_is_free | "personx abolishes ___ altogether"\|"abolishes altogether" | "person x is free"\|"is free" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:person_x_lives | "personx abolishes ___ altogether"\|"abolishes altogether" | "person x lives"\|"lives" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:to_abolishes_to_altogether | "personx abolishes ___ altogether"\|"abolishes altogether" | "to abolishes to altogether" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xEffect | at:to_gether_voice | "personx abolishes ___ altogether"\|"abolishes altogether" | "to gether voice" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xIntent | at:give_a_punishment_in_person | "personx abolishes ___ altogether"\|"abolishes altogether" | "give a punishment in person" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xNeed | at:to_have_a_plan | "personx abolishes ___ altogether"\|"abolishes altogether" | "to have a plan" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xNeed | at:to_have_a_reason | "personx abolishes ___ altogether"\|"abolishes altogether" | "to have a reason" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xNeed | at:to_know_the_law | "personx abolishes ___ altogether"\|"abolishes altogether" | "to know the law" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xNeed | at:to_not_like_it | "personx abolishes ___ altogether"\|"abolishes altogether" | "to not like it" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xReact | at:he_was_sad | "personx abolishes ___ altogether"\|"abolishes altogether" | "he was sad" | "person x feels" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xWant | at:human_to_be_free | "personx abolishes ___ altogether"\|"abolishes altogether" | "human to be free" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xWant | at:not_to_feel_pain | "personx abolishes ___ altogether"\|"abolishes altogether" | "not to feel pain" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xWant | at:to_make_a_new_law | "personx abolishes ___ altogether"\|"abolishes altogether" | "to make a new law" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____altogether | at:xWant | at:to_change_things_for_the_betters | "personx abolishes ___ altogether"\|"abolishes altogether" | "to change things for the betters" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:oWant | at:to_celebrate | "personx abolishes ___ in the states"\|"abolishes in the states" | "to celebrate" | "others want" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:oWant | at:to_write_about_the_new_law | "personx abolishes ___ in the states"\|"abolishes in the states" | "to write about the new law" | "others want" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:oWant | at:to_move_past_this_event | "personx abolishes ___ in the states"\|"abolishes in the states" | "to move past this event" | "others want" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:oWant | at:to_be_free | "personx abolishes ___ in the states"\|"abolishes in the states" | "to be free" | "others want" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:bold | "personx abolishes ___ in the states"\|"abolishes in the states" | "bold" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:authoritative | "personx abolishes ___ in the states"\|"abolishes in the states" | "authoritative" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:determined | "personx abolishes ___ in the states"\|"abolishes in the states" | "determined" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:heroic | "personx abolishes ___ in the states"\|"abolishes in the states" | "heroic" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:empathativ | "personx abolishes ___ in the states"\|"abolishes in the states" | "empathativ" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:thoughtful | "personx abolishes ___ in the states"\|"abolishes in the states" | "thoughtful" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:proud | "personx abolishes ___ in the states"\|"abolishes in the states" | "proud" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:moral | "personx abolishes ___ in the states"\|"abolishes in the states" | "moral" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xAttr | at:principaled | "personx abolishes ___ in the states"\|"abolishes in the states" | "principaled" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xIntent | at:this_is_unhappiness_for_people | "personx abolishes ___ in the states"\|"abolishes in the states" | "this is unhappiness for people" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xNeed | at:to_find_a_problem | "personx abolishes ___ in the states"\|"abolishes in the states" | "to find a problem" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xNeed | at:to_find_out_to_stop_that_problem | "personx abolishes ___ in the states"\|"abolishes in the states" | "to find out to stop that problem" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xNeed | at:to_acquire_power_and/or_influence | "personx abolishes ___ in the states"\|"abolishes in the states" | "to acquire power and/or influence" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xNeed | at:to_know_how_the_legal_system_works | "personx abolishes ___ in the states"\|"abolishes in the states" | "to know how the legal system works" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xReact | at:sad | "personx abolishes ___ in the states"\|"abolishes in the states" | "sad" | "person x feels" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xWant | at:to_enforce_the_ruling | "personx abolishes ___ in the states"\|"abolishes in the states" | "to enforce the ruling" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xWant | at:memorialize_the_law | "personx abolishes ___ in the states"\|"abolishes in the states" | "memorialize the law" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xWant | at:fairness | "personx abolishes ___ in the states"\|"abolishes in the states" | "fairness" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xWant | at:to_do_the_right_thing | "personx abolishes ___ in the states"\|"abolishes in the states" | "to do the right thing" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xWant | at:to_go_good | "personx abolishes ___ in the states"\|"abolishes in the states" | "to go good" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_____in_the_states | at:xWant | at:to_make_others_happy | "personx abolishes ___ in the states"\|"abolishes in the states" | "to make others happy" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oEffect | at:the_people_lost_the_documents | "personx abolishes the ___ altogether"\|"abolishes altogether" | "the people lost the documents" | "the effect on others" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oEffect | at:the_people___loss_the__trust | "personx abolishes the ___ altogether"\|"abolishes altogether" | "the people   loss the  trust"\|"the people loss the trust" | "the effect on others" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oReact | at:grateful | "personx abolishes the ___ altogether"\|"abolishes altogether" | "grateful" | "others feel" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oReact | at:disrespected | "personx abolishes the ___ altogether"\|"abolishes altogether" | "disrespected" | "others feel" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oWant | at:to_publish_an_article | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to publish an article" | "others want" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oWant | at:to_find_other_pursuits | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to find other pursuits" | "others want" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oWant | at:to_follow_the_laws | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to follow the laws" | "others want" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:oWant | at:to_protest | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to protest" | "others want" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xAttr | at:dedicated | "personx abolishes the ___ altogether"\|"abolishes altogether" | "dedicated" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xAttr | at:furious | "personx abolishes the ___ altogether"\|"abolishes altogether" | "furious" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xAttr | at:powerful | "personx abolishes the ___ altogether"\|"abolishes altogether" | "powerful" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xAttr | at:influencial | "personx abolishes the ___ altogether"\|"abolishes altogether" | "influencial" | "person x has attribute" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xEffect | at:set_free | "personx abolishes the ___ altogether"\|"abolishes altogether" | "set free" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xEffect | at:become_independent | "personx abolishes the ___ altogether"\|"abolishes altogether" | "become independent" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xEffect | at:lost_the_data | "personx abolishes the ___ altogether"\|"abolishes altogether" | "lost the data" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xEffect | at:lost_the_documents | "personx abolishes the ___ altogether"\|"abolishes altogether" | "lost the documents" | "effect on person x" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xIntent | at:to_end_it | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to end it" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xIntent | at:to_do_it_his_way | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to do it his way" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xNeed | at:find_a_lawyer | "personx abolishes the ___ altogether"\|"abolishes altogether" | "find a lawyer" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xNeed | at:file_a_lawsuit | "personx abolishes the ___ altogether"\|"abolishes altogether" | "file a lawsuit" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xNeed | at:to_gather_information | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to gather information" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xNeed | at:to_collaborate_with_others | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to collaborate with others" | "person x needs" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xReact | at:happy | "personx abolishes the ___ altogether"\|"abolishes altogether" | "happy" | "person x feels" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xReact | at:like_he's_the_boss | "personx abolishes the ___ altogether"\|"abolishes altogether" | "like he\\'s the boss"\|"like he the boss" | "person x feels" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xWant | at:to_celebrate | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to celebrate" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xWant | at:to_write_a_paper | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to write a paper" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xWant | at:to_implement_rules | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to implement rules" | "person x wants" |  | "AT" |  |
| at:personx_abolishes_the_____altogether | at:xWant | at:to_communicate_the_laws_with_others | "personx abolishes the ___ altogether"\|"abolishes altogether" | "to communicate the laws with others" | "person x wants" |  | "AT" |  |
| at:personx_about_to_get_married | at:oEffect | at:their_partner_is_in_a_legal_relationship | "personx about to get married"\|"about to get married" | "their partner is in a legal relationship" | "the effect on others" |  | "AT" |  |
| at:personx_about_to_get_married | at:oEffect | at:their_partner's_legal_status_changes | "personx about to get married"\|"about to get married" | "their partner\\'s legal status changes"\|"their partner legal status changes" | "the effect on others" |  | "AT" |  |
| at:personx_about_to_get_married | at:oEffect | at:says_yes | "personx about to get married"\|"about to get married" | "says yes" | "the effect on others" |  | "AT" |  |
| at:personx_about_to_get_married | at:oEffect | at:gets_dress | "personx about to get married"\|"about to get married" | "gets dress" | "the effect on others" |  | "AT" |  |
| at:personx_about_to_get_married | at:oReact | at:like_they_have_a_lifelong_companion | "personx about to get married"\|"about to get married" | "like they have a lifelong companion" | "others feel" |  | "AT" |  |
| at:personx_about_to_get_married | at:oReact | at:happy | "personx about to get married"\|"about to get married" | "happy" | "others feel" |  | "AT" |  |
| at:personx_about_to_get_married | at:oWant | at:to_spend_the_rest_of_their_life_with_personx | "personx about to get married"\|"about to get married" | "to spend the rest of their life with personx"\|"to spend the rest of their life with" | "others want" |  | "AT" |  |
| at:personx_about_to_get_married | at:oWant | at:to_be_happy_with_personx | "personx about to get married"\|"about to get married" | "to be happy with personx"\|"to be happy with" | "others want" |  | "AT" |  |
| at:personx_about_to_get_married | at:oWant | at:to_start_a_family | "personx about to get married"\|"about to get married" | "to start a family" | "others want" |  | "AT" |  |
| at:personx_about_to_get_married | at:oWant | at:to_go_on_vacation | "personx about to get married"\|"about to get married" | "to go on vacation" | "others want" |  | "AT" |  |
| at:personx_about_to_get_married | at:xAttr | at:excited | "personx about to get married"\|"about to get married" | "excited" | "person x has attribute" |  | "AT" |  |
| at:personx_about_to_get_married | at:xAttr | at:anxious | "personx about to get married"\|"about to get married" | "anxious" | "person x has attribute" |  | "AT" |  |
| at:personx_about_to_get_married | at:xAttr | at:anxious | "personx about to get married"\|"about to get married" | "anxious" | "person x has attribute" |  | "AT" |  |
| at:personx_about_to_get_married | at:xAttr | at:nervous | "personx about to get married"\|"about to get married" | "nervous" | "person x has attribute" |  | "AT" |  |
| at:personx_about_to_get_married | at:xAttr | at:brave | "personx about to get married"\|"about to get married" | "brave" | "person x has attribute" |  | "AT" |  |
| at:personx_about_to_get_married | at:xEffect | at:they_are_in_a_legal_relationship | "personx about to get married"\|"about to get married" | "they are in a legal relationship" | "effect on person x" |  | "AT" |  |
| at:personx_about_to_get_married | at:xEffect | at:their_legal_status_changes | "personx about to get married"\|"about to get married" | "their legal status changes" | "effect on person x" |  | "AT" |  |
| at:personx_about_to_get_married | at:xEffect | at:get_a_tuxedo | "personx about to get married"\|"about to get married" | "get a tuxedo" | "effect on person x" |  | "AT" |  |
| at:personx_about_to_get_married | at:xEffect | at:gets_ring | "personx about to get married"\|"about to get married" | "gets ring" | "effect on person x" |  | "AT" |  |
| at:personx_about_to_get_married | at:xIntent | at:to_share_his_life_with_someone | "personx about to get married"\|"about to get married" | "to share his life with someone" | "person x wants" |  | "AT" |  |
| at:personx_about_to_get_married | at:xIntent | at:to_marry_someone | "personx about to get married"\|"about to get married" | "to marry someone" | "person x wants" |  | "AT" |  |
| at:personx_about_to_get_married | at:xNeed | at:meet_someone | "personx about to get married"\|"about to get married" | "meet someone" | "person x needs" |  | "AT" |  |
| at:personx_about_to_get_married | at:xNeed | at:get_engaged | "personx about to get married"\|"about to get married" | "get engaged" | "person x needs" |  | "AT" |  |
| at:personx_about_to_get_married | at:xNeed | at:to_meet_someone | "personx about to get married"\|"about to get married" | "to meet someone" | "person x needs" |  | "AT" |  |
| at:personx_about_to_get_married | at:xNeed | at:to_really_like_them | "personx about to get married"\|"about to get married" | "to really like them" | "person x needs" |  | "AT" |  |
| at:personx_about_to_get_married | at:xReact | at:like_he_has_someone_he_feels_that_way_about | "personx about to get married"\|"about to get married" | "like he has someone he feels that way about" | "person x feels" |  | "AT" |  |
| at:personx_about_to_get_married | at:xReact | at:happy | "personx about to get married"\|"about to get married" | "happy" | "person x feels" |  | "AT" |  |
| at:personx_about_to_get_married | at:xWant | at:to_live_happily_ever_after | "personx about to get married"\|"about to get married" | "to live happily ever after" | "person x wants" |  | "AT" |  |
| at:personx_about_to_get_married | at:xWant | at:to_be_happily_married | "personx about to get married"\|"about to get married" | "to be happily married" | "person x wants" |  | "AT" |  |
| at:personx_about_to_get_married | at:xWant | at:to_go_on_a_honey_moon | "personx about to get married"\|"about to get married" | "to go on a honey moon" | "person x wants" |  | "AT" |  |
| at:personx_about_to_get_married | at:xWant | at:to_start_a_family | "personx about to get married"\|"about to get married" | "to start a family" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved | at:oReact | at:happy | "personx absolutely loved"\|"absolutely loved" | "happy" | "others feel" |  | "AT" |  |
| at:personx_absolutely_loved | at:oWant | at:to_marry_him | "personx absolutely loved"\|"absolutely loved" | "to marry him" | "others want" |  | "AT" |  |
| at:personx_absolutely_loved | at:oWant | at:to_accompany_him_all_his_life | "personx absolutely loved"\|"absolutely loved" | "to accompany him all his life" | "others want" |  | "AT" |  |
| at:personx_absolutely_loved | at:xAttr | at:caring | "personx absolutely loved"\|"absolutely loved" | "caring" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved | at:xAttr | at:faithful | "personx absolutely loved"\|"absolutely loved" | "faithful" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved | at:xAttr | at:passionate | "personx absolutely loved"\|"absolutely loved" | "passionate" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved | at:xAttr | at:caring | "personx absolutely loved"\|"absolutely loved" | "caring" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved | at:xAttr | at:gentle | "personx absolutely loved"\|"absolutely loved" | "gentle" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved | at:xAttr | at:loving | "personx absolutely loved"\|"absolutely loved" | "loving" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved | at:xEffect | at:gains_knowledge | "personx absolutely loved"\|"absolutely loved" | "gains knowledge" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved | at:xEffect | at:is_entertained | "personx absolutely loved"\|"absolutely loved" | "is entertained" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved | at:xIntent | at:to_marry | "personx absolutely loved"\|"absolutely loved" | "to marry" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved | at:xReact | at:romantic | "personx absolutely loved"\|"absolutely loved" | "romantic" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved | at:xWant | at:to_tell_others | "personx absolutely loved"\|"absolutely loved" | "to tell others" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved | at:xWant | at:write_a_review | "personx absolutely loved"\|"absolutely loved" | "write a review" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved | at:xWant | at:to_propose_to_her | "personx absolutely loved"\|"absolutely loved" | "to propose to her" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved | at:xWant | at:to_marry_her | "personx absolutely loved"\|"absolutely loved" | "to marry her" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:compassionate | "personx absolutely loved ___"\|"absolutely loved" | "compassionate" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:friendly | "personx absolutely loved ___"\|"absolutely loved" | "friendly" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:hungry | "personx absolutely loved ___"\|"absolutely loved" | "hungry" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:excited | "personx absolutely loved ___"\|"absolutely loved" | "excited" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:enthusiastic | "personx absolutely loved ___"\|"absolutely loved" | "enthusiastic" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:amiable | "personx absolutely loved ___"\|"absolutely loved" | "amiable" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xAttr | at:good-natured | "personx absolutely loved ___"\|"absolutely loved" | "good-natured" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xEffect | at:smiles_when_they_think_about_the_event | "personx absolutely loved ___"\|"absolutely loved" | "smiles when they think about the event" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xEffect | at:smiles_when_they_see_dogs | "personx absolutely loved ___"\|"absolutely loved" | "smiles when they see dogs" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xIntent | at:to_see_different_places | "personx absolutely loved ___"\|"absolutely loved" | "to see different places" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xIntent | at:to_enjoy | "personx absolutely loved ___"\|"absolutely loved" | "to enjoy" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xIntent | at:to_express_devotion | "personx absolutely loved ___"\|"absolutely loved" | "to express devotion" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xIntent | at:to_read | "personx absolutely loved ___"\|"absolutely loved" | "to read" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xNeed | at:to_see_what_they_want | "personx absolutely loved ___"\|"absolutely loved" | "to see what they want" | "person x needs" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xNeed | at:to_try_it_out | "personx absolutely loved ___"\|"absolutely loved" | "to try it out" | "person x needs" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xReact | at:happy | "personx absolutely loved ___"\|"absolutely loved" | "happy" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xReact | at:satisfied | "personx absolutely loved ___"\|"absolutely loved" | "satisfied" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xReact | at:excited | "personx absolutely loved ___"\|"absolutely loved" | "excited" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xReact | at:pleasant | "personx absolutely loved ___"\|"absolutely loved" | "pleasant" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xReact | at:relaxed | "personx absolutely loved ___"\|"absolutely loved" | "relaxed" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xWant | at:to_feel_satisfied | "personx absolutely loved ___"\|"absolutely loved" | "to feel satisfied" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xWant | at:to_do_it_again | "personx absolutely loved ___"\|"absolutely loved" | "to do it again" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xWant | at:visit_her_often | "personx absolutely loved ___"\|"absolutely loved" | "visit her often" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xWant | at:takes_her_for_walks | "personx absolutely loved ___"\|"absolutely loved" | "takes her for walks" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xWant | at:to_enjoy_more_of | "personx absolutely loved ___"\|"absolutely loved" | "to enjoy more of" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved____ | at:xWant | at:to_share_with_others | "personx absolutely loved ___"\|"absolutely loved" | "to share with others" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xAttr | at:enthused | "personx absolutely loved it"\|"absolutely loved it" | "enthused" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xAttr | at:appreciative | "personx absolutely loved it"\|"absolutely loved it" | "appreciative" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xAttr | at:satisfied | "personx absolutely loved it"\|"absolutely loved it" | "satisfied" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xAttr | at:contented | "personx absolutely loved it"\|"absolutely loved it" | "contented" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xAttr | at:delighted | "personx absolutely loved it"\|"absolutely loved it" | "delighted" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xAttr | at:amazed | "personx absolutely loved it"\|"absolutely loved it" | "amazed" | "person x has attribute" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xEffect | at:stomped_feet | "personx absolutely loved it"\|"absolutely loved it" | "stomped feet" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xEffect | at:laughed | "personx absolutely loved it"\|"absolutely loved it" | "laughed" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xEffect | at:takes_it_home | "personx absolutely loved it"\|"absolutely loved it" | "takes it home" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xEffect | at:buys_it | "personx absolutely loved it"\|"absolutely loved it" | "buys it" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xEffect | at:found_a_new_interest | "personx absolutely loved it"\|"absolutely loved it" | "found a new interest" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xEffect | at:gained_knowledge | "personx absolutely loved it"\|"absolutely loved it" | "gained knowledge" | "effect on person x" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xReact | at:ecstatic_over_his_gift | "personx absolutely loved it"\|"absolutely loved it" | "ecstatic over his gift" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xReact | at:happy | "personx absolutely loved it"\|"absolutely loved it" | "happy" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xReact | at:joyful | "personx absolutely loved it"\|"absolutely loved it" | "joyful" | "person x feels" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_buy_more | "personx absolutely loved it"\|"absolutely loved it" | "to buy more" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_eat_more | "personx absolutely loved it"\|"absolutely loved it" | "to eat more" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_take_pictures | "personx absolutely loved it"\|"absolutely loved it" | "to take pictures" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_buy_more | "personx absolutely loved it"\|"absolutely loved it" | "to buy more" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_use_it | "personx absolutely loved it"\|"absolutely loved it" | "to use it" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_show_it_to_everyone | "personx absolutely loved it"\|"absolutely loved it" | "to show it to everyone" | "person x wants" |  | "AT" |  |
| at:personx_absolutely_loved_it | at:xWant | at:to_thank_the_person_who_gave_it_to_them | "personx absolutely loved it"\|"absolutely loved it" | "to thank the person who gave it to them" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xAttr | at:conscious | "personx absorbs every ___"\|"absorbs every" | "conscious" | "person x has attribute" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xAttr | at:aware | "personx absorbs every ___"\|"absorbs every" | "aware" | "person x has attribute" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xAttr | at:unwasteful | "personx absorbs every ___"\|"absorbs every" | "unwasteful" | "person x has attribute" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xAttr | at:smart | "personx absorbs every ___"\|"absorbs every" | "smart" | "person x has attribute" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xIntent | at:moment | "personx absorbs every ___"\|"absorbs every" | "moment" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xIntent | at:to_completely_understand_his_position_and_the_alternatives | "personx absorbs every ___"\|"absorbs every" | "to completely understand his position and the alternatives" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xNeed | at:to_walk_around_and_take_notes | "personx absorbs every ___"\|"absorbs every" | "to walk around and take notes" | "person x needs" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xNeed | at:to_relax_in_the_spa | "personx absorbs every ___"\|"absorbs every" | "to relax in the spa" | "person x needs" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xNeed | at:to_be_a_quick_learner | "personx absorbs every ___"\|"absorbs every" | "to be a quick learner" | "person x needs" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xNeed | at:to_be_a_good_listener | "personx absorbs every ___"\|"absorbs every" | "to be a good listener" | "person x needs" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xNeed | at:to_be_at_a_conference | "personx absorbs every ___"\|"absorbs every" | "to be at a conference" | "person x needs" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xNeed | at:to_be_in_class | "personx absorbs every ___"\|"absorbs every" | "to be in class" | "person x needs" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xReact | at:very_nice | "personx absorbs every ___"\|"absorbs every" | "very nice" | "person x feels" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xReact | at:well_educated_on_the_pros_and_cons_of_the_matter | "personx absorbs every ___"\|"absorbs every" | "well educated on the pros and cons of the matter" | "person x feels" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:not_to_waste_any_detail | "personx absorbs every ___"\|"absorbs every" | "not to waste any detail" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:to_make_good_use_of_that_knowledge | "personx absorbs every ___"\|"absorbs every" | "to make good use of that knowledge" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:to_know_all_the_information | "personx absorbs every ___"\|"absorbs every" | "to know all the information" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:to_be_aware_of_their_surroundings | "personx absorbs every ___"\|"absorbs every" | "to be aware of their surroundings" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:to_write_notes | "personx absorbs every ___"\|"absorbs every" | "to write notes" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:to_remember_every_detail | "personx absorbs every ___"\|"absorbs every" | "to remember every detail" | "person x wants" |  | "AT" |  |
| at:personx_absorbs_every____ | at:xWant | at:to_teach_others | "personx absorbs every ___"\|"absorbs every" | "to teach others" | "person x wants" |  | "AT" |  |

