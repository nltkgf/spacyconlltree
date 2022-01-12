import spacy_udpipe
import sys
import fnmatch

spacy_udpipe.download("en")
# nlp = spacy_udpipe.load("en")

model = sys.argv[-1]


nlp = spacy_udpipe.load_from_path(lang="en",
                                  path=model)

filename = "./input"

with open(filename) as input:
  texts = input.readlines()
  for text in texts:
    doc = nlp(text)
    for token in doc:
      print(token.text, token.lemma_, token.pos_, token.dep_)
