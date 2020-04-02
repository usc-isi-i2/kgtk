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
* -l : Used to limit how many lines of the ntriple file to run on. If not provided, the script will run on the entire input file

### assumptions
* The input ntriple file contains lines of the format :
  
  \<http://one.example/subject1> \<http://one.example/predicate1> \<http://one.example/object1> .
