import spacy_udpipe
import sys

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")

filename = sys.argv[-1]

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

def getElements(trees):
  fun_elements = []
  for tree in trees:
    fun_elements.append(tree['root'][2])
    children = tree['children']
    # print(children)
    for child in children:
      fun_elements.append(replaceColon(child[2]))
  return(fun_elements)

def replaceColon(el):
  if el.find(':') != -1:
    return el.replace(':','_')
  return el

def writeFun(trees):
  fun_elements = getElements(trees)
  # rep_nsubj_pass = ["nsubj_pass" if i == "nsubj:pass" else i for i in fun_elements]
  # fun_name = '_'.join(rep_nsubj_pass)
  fun_name = '_'.join(fun_elements)
  fun = fun_name + " : " + ' -> '.join(fun_elements) + ' -> UDS'
  return(fun)

# def writeCat(trees):

# write all fun to file
outAllFun = open("myOutFile", "a")
outAllFun.truncate(0)
outAllFun.seek(0)
with open(filename) as input:
  for _ in range(4):
    next(input)
  texts = input.readlines()
  for text in texts[:-1]:
    text = text.rstrip()
    # doc = nlp(text)

    allTrees = getTree(text)
    outAllFun.write(writeFun(allTrees))
    outAllFun.write("\n")
  outAllFun.close()
  # take all the funs in myOutFile and remove duplicates, then put the unique funs into uniTypeFile
  line_seen = set()
  outfile = open("uniqTypesFile", "w")
  outfile.truncate(0)
  outfile.seek(0)
  for line in open("myOutFile", "r"):
    if line not in line_seen:
      outfile.write(line)
      line_seen.add(line)
  outfile.close()
