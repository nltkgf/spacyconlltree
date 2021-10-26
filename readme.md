Instructions:

Follow steps 1 and 2 as below. You will now have an input file.

run:

python make_abstract.py input Name_Of_Abstract

eg. if you want to get an gf abstract file called Abstract.gf and a labels file called Abstract.label, do:

python make_abstract.py input Abstract

this should generate an Abstract file, and a labels file for you.

---

AIM: Getting predicates into Abstract Syntax Trees (AST)

1. To activate the virtual environment, do `source pdpaenv/bin/activate`. Ensure you have the necessary libraries
   1. `pip install pandas`
   2. `pip install spacy`
   3. `pip install spacy_udpipe`
   4. download the necessary spacy model `python -m spacy download en_core_web_sm`
   5. `pip install spacy_conll`
2. Part 1: Read the predicates into a file for subsequent feeding
   1. PDPA predicates are in pdpa_predicates.csv
   2. To output all the predicates into a file "input", do `python pdpa_read_predicates.py > input`
3. Part 2: Feed the contents of the input files (which contains the predicates) and transform them into a conllu format
   1. `python sentence.py input` will output the predicates in "input" into a conllu format at spacy.conllu

4. Part 3: Use the GF-UD to make show the UD for all the predicates, presenting them in GF labels
   1. Make a copy of the repo from https://github.com/GrammaticalFramework/gf-ud locally
   2. Go the the repo directory, pipe the conllu format output file created that is residing into its directory into the gf-ud directory using ud2gf with the appropriate grammars using `cat /Code/spacyconlltree/spacy.conllu | stack run gf-ud ud2gf grammars/MiniLang Eng Utt ut > spacyOP` . [ Utt is arbitrary; It could have been VP or other RGL phrase]
   3. `Ctrl C` to terminate. But it is a horribly long process
   4. spacyOP will contain the relationship of parent-children-grandchildren relationships of all the predicates.

5. Part 4: Extract the parent(root) indicated by the first column; and children (where there is a "6" in line) indicated by the second column into a bag with their gf and ud labels.
   1. Extact ....
   2. Draw the AST of these individual predicates with .. .



Files required:
1. readme.md
2. pdpa_predicates.csv
3. pdpa_read_predicates.py
4. sentence.py
5. make_abstract.py
6. treefrom.py
7. ud_relations