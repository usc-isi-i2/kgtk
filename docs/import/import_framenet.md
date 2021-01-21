Import [FrameNet](https://framenet.icsi.berkeley.edu/fndrupal/) v1.7 into KGTK format. The resulting KGTK file consists of 9 columns.

## Usage
```
usage: kgtk import-framenet [-h] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
```

## Examples

Importing FrameNet can be done as follows (no inputs should be provided, as FrameNet is read through the NLTK package):

```
kgtk import-framenet
```

Example output (first and last 10 lines):

| node1                   | relation           | node2                         | node1;label            | node2;label            | relation;label      | relation;dimension | source | sentence |
| ----------------------- | ------------------ | ----------------------------- | ---------------------- | ---------------------- | ------------------- | ------------------ | ------ | -------- |
| fn:intentionally_affect | fn:IsInheritedBy   | fn:abandonment                | "intentionally affect" | "abandonment"          | "Is Inherited By"   |                    | "FN"   |          |
| fn:abandonment          | fn:InheritsFrom    | fn:intentionally_affect       | "abandonment"          | "intentionally affect" | "Inherits From"     |                    | "FN"   |          |
| fn:abandonment          | fn:HasLexicalUnit  | fn:lu:abandonment:abandon     | "abandonment"          | "abandon"              | "Has Lexical Unit"  |                    | "FN"   |          |
| fn:abandonment          | fn:HasLexicalUnit  | fn:lu:abandonment:leave       | "abandonment"          | "leave"                | "Has Lexical Unit"  |                    | "FN"   |          |
| fn:abandonment          | fn:HasLexicalUnit  | fn:lu:abandonment:abandonment | "abandonment"          | "abandonment"          | "Has Lexical Unit"  |                    | "FN"   |          |
| fn:abandonment          | fn:HasLexicalUnit  | fn:lu:abandonment:abandoned   | "abandonment"          | "abandoned"            | "Has Lexical Unit"  |                    | "FN"   |          |
| fn:abandonment          | fn:HasLexicalUnit  | fn:lu:abandonment:forget      | "abandonment"          | "forget"               | "Has Lexical Unit"  |                    | "FN"   |          |
| fn:abandonment          | fn:HasFrameElement | fn:fe:agent                   | "abandonment"          | "agent"                | "Has Frame Element" |                    | "FN"   |          |
| fn:abandonment          | fn:HasFrameElement | fn:fe:theme                   | "abandonment"          | "theme"                | "Has Frame Element" |                    | "FN"   |          |
| ...                     |                    |                               |                        |                        |                     |                    |        |          |
| fn:st:manner            | fn:st:SuperType    | fn:st:attribute               | "manner"               | "attribute"            | "Super Type"        |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:manner                  | "working a post"       | "manner"               | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:frequency               | "working a post"       | "frequency"            | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:period_of_iterations    | "working a post"       | "period of iterations" | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:result                  | "working a post"       | "result"               | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:particular_iteration    | "working a post"       | "particular iteration" | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:explanation             | "working a post"       | "explanation"          | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:event_description       | "working a post"       | "event description"    | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:post                    | "working a post"       | "post"                 | "Has Frame Element" |                    | "FN"   |          |
| fn:working_a_post       | fn:HasFrameElement | fn:fe:salient_entity          | "working a post"       | "salient entity"       | "Has Frame Element" |                    | "FN"   |          |

