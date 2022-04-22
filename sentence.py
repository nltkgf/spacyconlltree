import spacy
import spacy_udpipe
import sys
import treefrom

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")
from spacy import displacy

from spacy_conll import init_parser

con = init_parser(
     "en", "udpipe", include_headers=True
)

filename = sys.argv[-1]

allConll = []

with open(filename) as input:
  texts = input.readlines()
  for text in texts: #[:-1]:
    text = text.rstrip()
    doc = nlp(text)
    doc_con = con(text)

    def sub_fun(x):
      conll = x._.conll_str
      conllArr = []

      for line in conll.splitlines()[2:]:
        # if not empty \n

        line_list = line.split()
        if not line_list:
          break
        else:
          if (not conllArr) and (int(line_list[0]) == 1):
            conllArr.append('\n')
          if (line_list[3] == 'NOUN'):
            make_fun = "FUN=" + line_list[2] + "_N"
          elif (line_list[3] == 'ADJ'):
            make_fun = "FUN=" + line_list[2] + "_A"
          elif (line_list[3] == 'DET'):
            if (line_list[2] == 'the'):
              make_fun = "FUN=DefArt"
            else:
              make_fun = "FUN=" + line_list[2] + "_Det"
          elif (line_list[3] == 'VERB'):
            make_fun = "FUN=" + line_list[2] + line_list[4]
          elif (line_list[3] == 'PRON'):
            make_fun = "FUN=" + line_list[3] + line_list[4]
          elif (line_list[3] == 'CCONJ'):
            make_fun = "FUN=" + line_list[2] + "_Conj"
          elif (line_list[3] == 'AUX' and line_list[2] == 'be'):
            make_fun = "FUN=UseComp"
          else:
            make_fun = "_"
          line_list[-1] = make_fun + "\n"
          morpho(line_list)
          lowerroot(line_list)
          list_to_line = "\t".join(line_list)

        conllArr.append(list_to_line)
      return conllArr

    def morpho(line_list):
      if (line_list[1] == 'the'):
        line_list[4] = "Quant"
        line_list[5] = "FORM=0"

    def lowerroot(line_list):
      line_list[7] = line_list[7].lower()

    allConll.append(sub_fun(doc_con))

def extractUDLabels(line):
  words = line.partition( ": ")
  label = words[0]
  if label == 'case':
    label = 'case_'
  newLabel = treefrom.replaceColon(label)
  return(newLabel)

def getCats(funs):
  udLabels = []
  for line in funs:
    labels = extractUDLabels(line)
    print(labels)

for eachConll in allConll:
  getCats(eachConll)
