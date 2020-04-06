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
  
## wikidata_import_parallel.py
This script can be used to import nodes, edges and qualifiers from the bz2 compressed wikidata dump file into KGTK format. 

Input: Compressed Wikidata dump file (bz2 format)

Output: TSV files in KGTK format. 

### usage
python3 wikidata_import_parallel -i input.json.bz2 -n node_file.tsv -e edge_file.tsv -q qual_file.tsv -p num_procs -l limit -L lang -s doc_id

cat node_file.tsv_* >> node_file.tsv && rm node_file.tsv_*

cat edge_file.tsv_* >> edge_file.tsv && rm edge_file.tsv_*

cat qual_file.tsv_* >> qual_file.tsv && rm qual_file.tsv_*

### options 
* -i : Used to specify the path to the compressed wikidata file
* -p : (Optional) Number of proccesses to be run in parallel. Default and recommended is 2.
* -n : (Optional) Used to specify the path to the output KGTK node file. If not specified, nodes won't be written out.
* -e : (Optional) Used to specify the path to the output KGTK edge file. If not specified, edges won't be written out. 
* -q : (Optional) Used to specify the path to the output KGTK qualifier file. If not specified, qualifiers won't be written out.
* -l : (Optional) Used to limit how many lines of the dump file (number of nodes we extract) we import. If not provided, the script will run on the whole dump
* -L : (Optional) Used to specify the language tag to be used to extract information about nodes. It is 'en' by default.
* -s: Used to specify the source/version of the dump file. If not provided, the source will be output as 'Wikidata'

### assumptions
* The input file is compressed in the bz2 format.
