import spacy_udpipe
import sys

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")

filename = sys.argv[-2]

def removePunct(ls):
  return [l for l in ls if l[2] != 'punct']

def getTree(text):
  for token in nlp(text):
    trees = []
    Tree = {}
    # print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text)
    if token.dep_.lower() == 'root':
      Tree['root'] = [token.text, token.lemma_, token.dep_.lower(), token]
      unfiltered = [[child.text, child.lemma_, child.dep_, child] for child in token.children]
      Tree['children'] = unfiltered
      Tree['children'] = removePunct(unfiltered)
      #print(Tree)
      trees.append(Tree)
      return trees
      #print(trees)

# get different elements from token [text, lemma, dep, whole token]
def getElements(trees, el):
  fun_elements = []
  for tree in trees:
    fun_elements.append(tree['root'][el])
    children = tree['children']
    # print(children)
    for child in children:
      fun_elements.append(replaceColon(child[el]))
  return(fun_elements)

def replaceColon(el):
  if el.find(':') != -1:
    ind = el.index(':')
    cap = el[ind+1].upper()
    newStr = el[:ind] + cap + el[ind + 2:]
    return newStr
  return el

def writeFun(trees):
  fun_elements = getElements(trees, 2)
  # rep_nsubj_pass = ["nsubj_pass" if i == "nsubj:pass" else i for i in fun_elements]
  # fun_name = '_'.join(rep_nsubj_pass)
  fun_name = '_'.join(fun_elements)
  fun_elements = [e.replace('case', 'case_') for e in fun_elements]
  fun = fun_name + " : " + ' -> '.join(fun_elements) + ' -> UDS'
  return(fun)

# def writeCat(trees):
def getFuns():
  allFuns = []

  with open(filename) as input:
    for _ in range(4):
      next(input)
    texts = input.readlines()
    for text in texts[:-1]:
      text = text.rstrip()

      allTrees = getTree(text)

      allFuns.append(writeFun(allTrees))
  return allFuns

def uniqueFuns():
  outfile = getFuns()

  # remove duplicate funs
  outfile = list(dict.fromkeys(outfile))
  return sorted(outfile)