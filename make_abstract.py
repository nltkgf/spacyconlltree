import spacy_udpipe
import sys
import treefrom

#nlp = spacy.load("en_core_web_sm")
#nlp = spacy_udpipe.load("en")

filename = sys.argv[-2]
print('load ', filename)
abstractGrammar = sys.argv[-1]
print('load abstract ', abstractGrammar)

#save unique type names as a variable
def getUsedCats():
  #uniqTypeNames = open("uniqTypeNames", "+w")
  # print('get unique ', treefrom.uniqueFuns())
  for types in treefrom.uniqueFuns():
    typeName = (types[0].split(":",1)[0]).split('_')
    #typeNames = typeName + "; "
    # print(len(typeNames))
    # add everything from typeName to list of uniqTypeNames
    uniqTypeNames.append(typeName)
  return uniqTypeNames

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
  if label == 'case':
    label = 'case_'
  newLabel = treefrom.replaceColon(label)
  return(newLabel)

def getCats():
#def writeUDfile():
  # udLabels = open("udLabels", "w")
  # udLabels.truncate(0)
  # udLabels.seek(0)
  udLabels = []
  for line in open("ud_relations", "r"):
    labels = extractUDLabels(line)
    # labels = labels + " ;"
    udLabels.append(labels)
  return udLabels
    # udLabels.write("\n" +labels)
  # udLabels.close()

def coerceFuns(cat):
  return [(cat + "_"), ":", "X", "->", cat, ";"]

def writeLabels():
  with open(abstractGrammar + '.label', 'w+') as labelFile:
    for eachFun in treefrom.uniqueFuns():
      eachLabel = "#fun " + eachFun[0].replace(': root ', 'head')
      labelFile.write(eachLabel + "\n")

writeLabels()

# create and abstract GF file with user input name and carry the unique functions from uniqTypesFile for Fun and labels from udLabels to the cat to this abstract GF file
def makeAbstractGF(userGrammar):
  abstractGF = open (abstractGrammar + ".gf", "w+")
  abstractGF.truncate(0)
  abstractGF.seek(0)

 # writeUDfile()

  abstractGF.write(
            "abstract "
          + abstractGrammar
          + " = {"
          + "\n\n\tflags"
          + "\n\t\tstartcat = UDS ;"
          + "\n\n\tcat"
          )

  for line in getCats():
    abstractGF.write("\n\t\t" + line)
    abstractGF.write(";")

  abstractGF.write(
    "\n\n\t -- coercion funs"
    + "\n\n\tfun"
  )

  # get coercedFuns
  for line in getCats():
    abstractGF.write("\n\t\t" + " ".join(coerceFuns(line)))

  abstractGF.write( "\n\n\tfun\n" )
  print('length of unique funs ', len(treefrom.uniqueFuns()))
  for line in treefrom.uniqueFuns():
      # lineEnd = ["UDS;" if i == "UDS" else i for i in line]
      # line = line.replace("UDS", "UDS ;" )
    abstractGF.write("\t--" + line[1] + " ;\n")
    abstractGF.write( "\t\t" + line[0] + " ;\n")
  abstractGF.write("}")
  abstractGF.close()

# writeUDfile()
makeAbstractGF(abstractGrammar)
