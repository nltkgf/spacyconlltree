# https://www.machinelearningplus.com/spacy-tutorial-nlp/#docobject

import spacy

# import tweets
f = open('allQuotes.txt', 'r')
text = f.read()

# get language model
nlp = spacy.load("en_core_web_sm")

# the nlp function tokenises the text
doc = nlp(text)
type(doc)

# preprocessing remove stopwords and punctuation

just_words_doc = [token for token in doc if not token.is_punct]


# lemmatization converts to root form

for token in doc:
  print(token.text, '-', token.lemma_)

print('---')

for token in just_words_doc:
  print(token.text, '-', token.lemma_)

# pos tagging

print('---')

for token in doc:
  print(token.text, '-', token.pos_)

# print named entities

print ('---')

print(doc.ents)

for entity in doc.ents:
  print(entity.text,'--- ',entity.label_)
