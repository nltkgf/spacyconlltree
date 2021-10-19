import spacy_udpipe
import sys

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")

filename = sys.argv[-1]

def getTree(text):
  for token in nlp(text):
    trees = []
    Tree = {}
    # print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text)
    if token.dep_.lower() == 'root':
      Tree['root'] = token.text
      Tree['children'] = [child.text for child in token.children]
      #print(Tree)
      trees.append(Tree)
      return trees
      #print(trees)

with open(filename) as input:
  for _ in range(4):
    next(input)
  texts = input.readlines()
  for text in texts[:-1]:
    text = text.rstrip()
    # doc = nlp(text)

    allTrees = getTree(text)
    print(allTrees)
