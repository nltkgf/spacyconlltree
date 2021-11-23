import spacy
import spacy_udpipe
import sys

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")
from spacy import displacy

from spacy_conll import init_parser

con = init_parser(
     "en", "udpipe", include_headers=True
)

filename = sys.argv[-1]

# empty output file
open('spacy.conllu', 'w').close()

with open(filename) as input:
  # for _ in range(4):
  #   next(input)
  texts = input.readlines()
  for text in texts: #[:-1]:
    text = text.rstrip()
    doc = nlp(text)
    doc_con = con(text)

    def sub_fun(x):
      conll = x._.conll_str

      for line in conll.splitlines()[2:]:
        output = open('spacy.conllu', 'a+')
        output.seek(0)
        checkEmpty = output.read(10)
        # if not empty \n

        line_list = line.split()
        if not line_list:
          break
        else:
          if ((len(checkEmpty) > 0) and (int(line_list[0]) == 1)):
            output.write('\n')
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

          output.writelines(list_to_line)
          output.close()

    def morpho(line_list):
      if (line_list[1] == 'the'):
        line_list[4] = "Quant"
        line_list[5] = "FORM=0"

    def lowerroot(line_list):
      line_list[7] = line_list[7].lower()

    sub_fun(doc_con)
    #sub_fun(conll, "spacy.conllu")
# morpho(conll)

nlp_pipe = spacy_udpipe.load("en")
with open("spacy_udpipe.txt", "w") as f:
    for token in nlp_pipe(text):
        f.writelines([token.text, " ", token.lemma_, " ", token.pos_, " ", token.dep_, " ", token.head.text, "\n"])
