import spacy_udpipe
import sys

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")

filename = sys.argv[-2]
abstractGrammar = sys.argv[-1]

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
    ind = el.index(':')
    cap = el[ind+1].upper()
    newStr = el[:ind] + cap + el[ind + 2:]
    return newStr
  return el

def writeFun(trees):
  fun_elements = getElements(trees)
  # rep_nsubj_pass = ["nsubj_pass" if i == "nsubj:pass" else i for i in fun_elements]
  # fun_name = '_'.join(rep_nsubj_pass)
  fun_name = '_'.join(fun_elements)
  fun = fun_name + " : " + ' -> '.join(fun_elements) + ' -> UDS'
  return(fun)

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

# take all the funs in myOutFile and remove duplicates, then put the unique funs into uniTypesFile
line_seen = set()
outfile = open("uniqTypesFile", "w")
outfile.truncate(0)
outfile.seek(0)
for line in open("myOutFile", "r"):
  if line not in line_seen:
    outfile.write(line)
    line_seen.add(line)
outfile.close()
# collect the names of the unitque types from uniqTypesFile into a file "uniqTypeNames"
uniqTypeNames = open("uniqTypeNames", "w")
uniqTypeNames.truncate(0)
uniqTypeNames.seek(0)
for types in open("uniqTypesFile", "r"):
  typeName = types.split(":",1)[0]
  typeNames = typeName + "; "
  print(len(typeNames))
  uniqTypeNames.write(typeNames)
uniqTypeNames.close()

# massage the ud_relations to only have the labels
def extractUDLabels(line):
  words = line.partition( ": ")
  label = words[0]
  # print(label)
  # if label.find(':') != -1:
  #   ind = label.index(":")
  #   cap = label[ind + 1].upper()
  #   newLabel = line[:ind] + cap + line [ind + 2:]
  #   print(newLabel)
  # return label
  newLabel = replaceColon(label)
  return(newLabel)

def writeUDfile():
  udLabels = open("udLabels", "w")
  udLabels.truncate(0)
  udLabels.seek(0)
  for line in open("ud_relations", "r"):
    labels = extractUDLabels(line)
    labels = labels + ";"
    udLabels.write("\n" +labels)
  udLabels.close()


  # create and abstract GF file with user input name and carry the unique functions from uniqTypesFile for Fun and labels from ukLabels to the cat to this abstract GF file
def makeAbstractGF(userGrammar):
  abstractGF = open (abstractGrammar + ".gf", "w")
  abstractGF.truncate(0)
  abstractGF.seek(0)

  # abstractGF.seek(1)
  # abstractGF.write("\n\n")
  # abstractGF.seek(0)
  abstractGF.write(
            "abstract "
          + abstractGrammar
          + " = {"
          + "\n\tcat"
          )
  # abstractGF.write("hello;")
  for line in open("udLabels", "r"):
    line = line
    abstractGF.write("\t\t" + line)
    # abstractGF.write(";")
  abstractGF.write( "\n\tfun\n\t\t" )
  for line in open("uniqTypesFile", "r"):
      # lineEnd = ["UDS;" if i == "UDS" else i for i in line]
      line = line.replace("UDS", "UDS;" )
      abstractGF.write( "\t\t" + line)
  abstractGF.write("}")
  abstractGF.close()


writeUDfile()
makeAbstractGF(abstractGrammar)
