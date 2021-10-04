import spacy
import spacy_udpipe

nlp = spacy.load("en_core_web_sm")
text = "the cat sings"
print("just spacy")
for token in nlp(text):
  print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text)

print("spacy_udpipe")
nlp_pipe = spacy_udpipe.load("en")
for token in nlp_pipe(text):
    print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text)
