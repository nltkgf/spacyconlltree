import spacy_udpipe
spacy_udpipe.download("en")
nlp = spacy_udpipe.load("en")
text = "the cat is black"
doc = nlp(text)
for i, token in zip(range(len(doc)), doc):
  print(i+1, token.text, token.lemma_, token.pos_, token.dep_)
