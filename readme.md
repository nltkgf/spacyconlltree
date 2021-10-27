Instructions:
AIM: Getting predicates into Abstract Syntax Trees (AST) **WIP**

1. Ensure you have the necessary libraries
   1. `pip install pandas`
   2. `pip install spacy`
   3. `pip install spacy_udpipe`
   4. download the necessary spacy model `python -m spacy download en_core_web_sm`
   5. `pip install spacy_conll`
2. To work in a virtual environment, do
   1. `pip install virtualenv`
   2. `virtualenv pdpaenv`
   3. `source pdpaenv/bin/activate`
3. *For predicates extraction* Extract the predicates from a csv into a file for subsequent processing
   1. Here, the PDPA predicates are in `pdpa_predicates.csv` under the field *Predicates*
   2. To pull all the predicates into a file "input", do `python pdpa_read_predicates.py > input`
   3. The first 4 lines contains some meta info of the contents.
4. *For making conllu* <Option> Feed the contents of the `input` file (which contains the predicates) and transform them into a conllu format
   1. `python sentence.py input` will output the predicates in `input` into a conllu format at `spacy.conllu`

~~4. Part 3: Use the GF-UD to make show the UD for all the predicates, presenting them in GF labels~~
   ~~1. Make a copy of the repo from https://github.com/GrammaticalFramework/gf-ud locally~~
   ~~2. Go the the repo directory, pipe the conllu format output file created that is residing into its directory into the gf-ud directory using ud2gf with the appropriate grammars using `cat /Code/spacyconlltree/spacy.conllu | stack run gf-ud ud2gf grammars/MiniLang Eng Utt ut > spacyOP` . [ Utt is arbitrary; It could have been VP or other RGL phrase]~~
   ~~3. `Ctrl C` to terminate. But it is a horribly long process~~
   ~~4. spacyOP will contain the relationship of parent-children-grandchildren relationships of all the predicates.~~

5. *For Create GF files and label file* Create an abstract gf, a concrete gf file and a labels file
   1. `python make_GF_files.py input Name_Of_Abstract` eg. run this command `python make_GF_files.py input Abstract` if you want to get
      1. an gf abstract file (Abstract.gf),
      2. a gf concrete file (AbstractEng.gf) and
      3. a labels file called (Abstract.label).
   
6. For info:
   1. Purpose of `treefrom` module
      1. Extract the parent(root) and children for the AST functions in all the predicates that was fed with `input` e.g `root_nsubj_obj head-> nsubj -> obj -> UDS`
      2. Compile all these to only retain the unique functions.
   2. Making the abstract gf, concrete gf file and labels file:
      1. With the labels from ud_relations and the generated unique functions, the contents are then processed to produce a pair of abstract gf and its corresponding concrete gf file.
      2. A labels file is also created for reference.
   3. backupFiles folder contains all the backup copies of gf abstract, gf concrete and labels files.

7. Overview for information:

|   	|  Required 	            | Section  	                           | Comments   	                              |
|---	|---	                     |---	                                 |---	                                       |
|  1 	| readme.md  	            |  - 	                                 | Instructions and information 	            |
|  2 	| make_GF_files.py 	      | For Create GF files and label file   | With the labels from ud_relations and the generated unique functions, the contents are then processed to produce a pair of abstract gf and its corresponding concrete gf file. A labels file is also created for reference. 	|
|  3 	| pdpa_predicates.csv  	   | For predicates extraction            | Predicates are in the field "Predicates  	|
|  4 	| pdpa_read_predicates.py  | For predicates extraction            | Extract the predicates from pdpa_predicates.csv to a specified file (input) 	|
|  5 	| sentence.py  	         | For making conllu   	               | Process the extracted predicates in input to a conllu format  	|
|  6 	| treefrom.py  	         | For Create GF files and label file   | Obtain the parent(root) and children tokens to make the functions underlying each predicates. Then narrow these down to unique functions for writing into the .label file.	|
|  7 	| ud_relations  	         | For Create GF files and label file   |  These are the [universal dependencies relations](https://universaldependencies.org/u/dep/#:~:text=alphabetical%20listing) 	|