# Import Scripts for Wikidata and ntriple files

## ntriples_import.py
This script can be run to import an ntriple file into the KGTK format. 

Input: Ntriple file

Output: TSV file in KGTK format

### usage
python3 ntriple_import.py -i input.nt -o output.tsv -l limit

### options
* -i : Used to specify the path to the input ntriple file
* -o : Used to specify the path to the output KGTK tsv file
* -l : (Optional) Used to limit how many lines of the ntriple file to run on. If not provided, the script will run on the entire input file

### assumptions
* The input ntriple file contains lines of the format :
  
  \<http://one.example/subject1> \<http://one.example/predicate1> \<http://one.example/object1> .

## wikidata_nodes.py
This script can be run to import the nodes from the bz2 compressed wikidata dump file into KGTK format. 

Input: Compressed Wikidata dump file (bz2 format)

Output: TSV file in KGTK format containing the wikidata nodes

### usage
python3 wikidata_nodes.py -i input.json.bz2 -o output.tsv -l limit -L lang -s doc_id

### options
* -i : Used to specify the path to the compressed wikidata file
* -o : Used to specify the path to the output KGTK file
* -l : (Optional) Used to limit how many lines of the dump file (number of nodes we extract) we import. If not provided, the script will run on the whole dump
* -L : (Optional) Used to specify the language tag to be used to extract information about nodes. It is 'en' by default.
* -s: Used to specify the source/version of the dump file. If not provided, the source will be output as 'Wikidata'

### assumptions
* The input file is compressed in the bz2 format.


## wikidata_edges.py
This script can be run to import the edges and qualifiers from the bz2 compressed wikidata dump file into KGTK format. 

Input: Compressed Wikidata dump file (bz2 format)

Output: Two TSV files in KGTK format, one containing the wikidata edges, and one containing wikidata qualifiers

### usage
python3 wikidata_edges.py -i input.json.bz2 -e edges_output.tsv -q qualifiers_output.tsv -l limit -L lang -s doc_id

### options
* -i : Used to specify the path to the compressed wikidata file
* -e : (Optional) Used to specify the path to the output KGTK edge file. If not specified, edges won't be written out. 
* -q : (Optional) Used to specify the path to the output KGTK qualifier file. If not specified, qualifiers won't be written out.
* -l : (Optional) Used to limit how many lines of the dump file (number of nodes we extract) we import. If not provided, the script will run on the whole dump
* -L : (Optional) Used to specify the language tag to be used to extract information about nodes. It is 'en' by default.
* -s: Used to specify the source/version of the dump file. If not provided, the source will be output as 'Wikidata'

### assumptions
* The input file is compressed in the bz2 format.
