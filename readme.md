Instructions:
AIM: Getting predicates into Abstract Syntax Trees (AST) **WIP**
1. AIM:
   1. Create abstract GF file
   2. Create contrect GF file
   3. Create a labels file containing unique Funs from a file of predicates
   4. Extend a grammar from a existing pgf grammar file. (*For more on pgf, read [embedding-grammars](https://inariksit.github.io/gf/2019/12/12/embedding-grammars.html)*)

2. Ensure you have the necessary libraries
   1. `pip install pandas`
   2. `pip install spacy`
   3. `pip install spacy_udpipe`
   4. download the necessary spacy model `python -m spacy download en_core_web_sm`
   5. `pip install spacy_conll`
3. To work in a virtual environment, do
   1. `pip install virtualenv`
   2. `virtualenv pdpaenv`
   3. `source pdpaenv/bin/activate`
4. *Where required: For predicates extraction into an INPUT file* Extract the predicates from a csv into a file for subsequent processing
   1. Here, the PDPA predicates are in `pdpa_predicates.csv` under the field *Predicates*
   2. To pull all the predicates into a file "input", do `python pdpa_read_predicates.py > input`
   3. The first 4 lines contains some meta info of the contents.
5. *For making conllu* <Optional> Feed the contents of the `input` file (which contains the predicates) and transform them into a conllu format
   1. `python sentence.py input` will output the predicates in `input` into a conllu format at `spacy.conllu`

6. To create a pgf file so as to use the GF grammar from another program, first compile it into a PGF first by simply running this command after ensuring you have GF installed.
   1. To install GF : see [Grammatical Framework Download and Installation](https://www.grammaticalframework.org/download/index-3.11.html)
   2. Go into GF shell with the grammar that you have with `gf GrammarInDirectory.gf`
   3. Compile grammar into pgf with `gf -make GrammarInDirectory.gf`


7. *For Create GF extension grammar, concrete file, labels file* Create an extenstion abstract gf, a concrete gf file and a labels file
   1. `python make_GF_files.py input NewGrammar ExistingGrammar` eg. run this command `python make_GF_files.py input NewGrammar GrammarInDirectory` to get
      1. a gf concrete file (NewGrammarEng.gf)
      2. a labels file called (NewGrammar.labels) and
      3. an extension grammar file (NewGrammar.gf)
   2. If you encounter error message similar to below
      ```Traceback (most recent call last):
         File "/Users/regina/Code/spacyconlltree/make_GF_files.py", line 285, in <module>
            writeLabels()
         File "/Users/regina/Code/spacyconlltree/make_GF_files.py", line 129, in writeLabels
            newLabels(currentLabels, oldGrammar)
         File "/Users/regina/Code/spacyconlltree/make_GF_files.py", line 150, in newLabels
            shutil.copyfile(source, destination)
         File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/shutil.py", line 244, in copyfile
            raise SameFileError("{!r} and {!r} are the same file".format(src, dst))
         shutil.SameFileError: 'NewGrammar.labels' and 'NewGrammar.labels' are the same file
      ```
      The solution is remove the current labels file with the same name that you had put in for `NewGrammar`. Another solution could be just give a different name to your new grammar.

8. For info:
   1. Purpose of `treefrom` module
      1. Extract the parent(root) and children for the AST functions in all the predicates that was fed with `input` e.g `root_nsubj_obj head-> nsubj -> obj -> UDS`
      2. Compile all these to only retain the unique functions.
   2. Making the abstract gf, concrete gf file and labels file:
      1. With the labels from ud_relations and the generated unique functions, the contents are then processed. These are used to generate the concrete file. The unique functions are also compared to the ones in the existing pgf file to create an extension grammar.
      2. A labels file is also created for reference.
   3. backupFiles folder contains all the backup copies of gf abstract, gf concrete and labels files.

9. Overview for information:

|   	|  Required 	            | Section  	                           | Comments   	                              |
|---	|---	                     |---	                                 |---	                                       |
|  1 	| readme.md  	            |  - 	                                 | Instructions and information 	            |
|  2 	| make_GF_files.py 	      | For Create GF files and label file   | With the labels from ud_relations and the generated unique functions, the contents are then processed to produce a pair of abstract gf and its corresponding concrete gf file. A labels file is also created for reference. 	|
|  3 	| pdpa_predicates.csv  	   | For predicates extraction            | Predicates are in the field "Predicates  	|
|  4 	| pdpa_read_predicates.py  | For predicates extraction            | Extract the predicates from pdpa_predicates.csv to a specified file (input) 	|
|  5 	| sentence.py  	         | For making conllu   	               | Process the extracted predicates in input to a conllu format  	|
|  6 	| treefrom.py  	         | For Create GF files and label file   | Obtain the parent(root) and children tokens to make the functions underlying each predicates. Then narrow these down to unique functions for writing into the .label file.	|
|  7 	| ud_relations  	         | For Create GF files and label file   |  These are the [universal dependencies relations](https://universaldependencies.org/u/dep/#:~:text=alphabetical%20listing) 	|