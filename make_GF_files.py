import spacy_udpipe
import sys
import treefrom
import time
import os
import os.path
import shutil
import pgf
import itertools
import glob

from pathlib import Path


# get old grammar from pgf
def getPGF(oldGrammar):
  gr = pgf.readPGF(oldGrammar + ".pgf")
  pgfAsStr = str(gr)
  listOldGram = []
  for line in pgfAsStr.splitlines():
    listOldGram.append(line.strip().partition("   --")[0])
  # remove until fun and last }
  indexStart =  [idx for idx, s in enumerate(listOldGram) if "fun" in s][0]
  onlyFuns = listOldGram[indexStart:-1]
  # remove straggling coerce funs
  coerceIdx = [idx for idx, s in enumerate(onlyFuns) if " : X -> " in s]
  for index in sorted(coerceIdx, reverse=True):
    del onlyFuns[index]
  return onlyFuns

# get corpus funs only for new grammar
def getNewGrammarFuns(inputFile):
  list_Corpus_Unique_Funs = []
  for line in treefrom.uniqueFuns(inputFile):
    list_Corpus_Unique_Funs.append("fun " + line[0] + " -> UDS ;")
  return list_Corpus_Unique_Funs

# compare old and new grammar
def compareFunsLists(inputFile, oldGrammar, newGrammar):
    newGrammar = getNewGrammarFuns(inputFile)
    oldGrammar = getPGF(oldGrammar)
    li_dif = [i for i in newGrammar if i not in oldGrammar]
    print("diffs")
    print(*li_dif, sep="\n")
    return li_dif

# massage the ud_relations to only have the labels
def extractUDLabels(line):
  words = line.partition( ": ")
  label = words[0]
  if label == 'case':
    label = 'case_'
  newLabel = treefrom.replaceColon(label)
  return(newLabel)

# get categories from ud_relations
def getCats():
  udLabels = []
  for line in open("ud_relations", "r"):
    labels = extractUDLabels(line)
    udLabels.append(labels)
  return udLabels

# massage the ud_relations to only have the labels
def extractUDLabels(line):
  words = line.partition( ": ")
  label = words[0]
  if label == 'case':
    label = 'case_'
  newLabel = treefrom.replaceColon(label)
  return(newLabel)

# get categories from ud_relations
def getCats():
  udLabels = []
  for line in open("ud_relations", "r"):
    labels = extractUDLabels(line)
    udLabels.append(labels)
  return udLabels

#get coerce funs

def coerceFunsAbs(cat):
  return [(cat + "_"), ":", "X", "->", cat, ";"]

def coerceFunsConcrete(cat):
  return [(cat + "_"), "x", "= TODO ;"]

# write new grammar

def makeNewGrammar(inputFile, oldGrammar, newGrammar):
  newGrammarFile = open (newGrammar + ".gf", "w+")
  newGrammarFile.truncate(0)
  newGrammarFile.seek(0)
  newGrammarFile.write(
            "abstract "
          + newGrammar
          + " = "
          + oldGrammar
          + " ** {"
  )

  newGrammarFile.write(
    "\n\n\t -- additional corpus funs"
  )

  # write additional corpus funs
  for line in compareFunsLists(inputFile, oldGrammar, newGrammar):
    newGrammarFile.write("\n\t\t" + line)

  newGrammarFile.write("\n}")

# write label file from scratch

def writeLabels(inputFile, oldGrammar, newGrammar):
    os.chdir(os.getcwd())
    oldLabelsFile = oldGrammar + ".labels"
    newLabelsFile = newGrammar + ".labels"

    # Kickstart the new labels file by copying the old labels
    if os.path.isfile(oldLabelsFile):
      shutil.copyfile(oldLabelsFile, newLabelsFile)

    # Print in stdout + write to file as well
    print("labels")
    with open(newGrammar + '.labels', 'w+') as labelFile:
        for eachFun in treefrom.uniqueFuns(inputFile):
            labelFile.write(funToLabel(eachFun[0]) +"\n")
            print(funToLabel(eachFun[0]))


def funToLabel(fun):
    label = "#fun " + fun.replace(': root ', 'head').replace("->", "") # replacing "root" with "head"
    start = label.partition("head")[0] + label.partition("head")[1]
    trail = label.partition("head")[2]
    trailNew = treefrom.toUDelement(trail) # removing return type from the labels
    return start+trailNew


# create an abstract GF file with user entered name
def makeAbstractGF(inputFile, oldGrammar, newGrammar):
  abstractGF = open (newGrammar + ".gf", "w+")
  abstractGF.truncate(0)
  abstractGF.seek(0)
  abstractGF.write(
            "abstract "
          + newGrammar
          + " = ** "
          + oldGrammar
          + " {"
          + "\n\n\tflags"
          + "\n\t\tstartcat = UDS ;"
          + "\n\n\tcat"
          + "\n\t\tUDS ;"
          + "\n\t\tX ;"
          )

  for line in getCats():
    abstractGF.write("\n\t\t" + line)
    abstractGF.write(" ;")

  abstractGF.write(
    "\n\n\t -- coercion funs"
    + "\n\n\tfun"
  )

  # write coercedFuns
  for line in getCats():
    abstractGF.write("\n\t\t" + " ".join(coerceFunsAbs(line)))

  # write corpus funs
  abstractGF.write( "\n\n\tfun\n" )
  print('length of unique funs ', len(treefrom.uniqueFuns(inputFile)))
  for line in treefrom.uniqueFuns(inputFile):
    funLine = "\t\t" + line[0] + " -> UDS ;\n\t--" + line[1] + " ;\n\n"
    abstractGF.write(funLine)
  abstractGF.write("}")
  abstractGF.close()

# make concrete grammar

def makeConcreteGF(inputFile, oldGrammar, newGrammar):
  concreteGF = open (newGrammar + "Eng.gf", "w+")
  concreteGF.truncate(0)
  concreteGF.seek(0)
  concreteGF.write(
          "concrete "
        + newGrammar
        + "Eng of "
        + newGrammar
        + " = ** "
        + oldGrammar + "Eng"
        + " {"        + "\n\n\tlincat"
        + "\n\n\t\tUDS = TODO;"
        + "\n\t\tX = TODO;"
        )
  for line in getCats():
    concreteGF.write("\n\t\t"
                    + line
                    + " = TODO ;"
                    )
  concreteGF.write(
         "\n\n\tlin"
        + "\n\t\t-- the coercion funs"
        )
  for line in getCats():
    concreteGF.write("\n\t\t" + " ".join(coerceFunsConcrete(line)))

  concreteGF.write("\n\n\t\t-- the actual funs")

  for line in treefrom.uniqueFuns(inputFile):
      function  = line[0].partition( ": ")
      fun = function[2]
      concreteGF.write("\n\t\t-- : " + fun)
      funName = function[0]
      simpleFuns = fun.replace("-> ", "")
      argFuns = simpleFuns.replace("UDS", "")
      concreteGF.write("\n\t\t"
                      + funName
                      + argFuns
                      + " = TODO ;"
                      )
  concreteGF.write("\n}")
  concreteGF.close()

# Create datetime for backup files (abstract, concrete, labels)
timestr = time.strftime("%Y%m%d-%H%M%S")

def makeDir(ls):
  for l in ls:
    Path(l).mkdir(parents=True, exist_ok=True)

def makeBak():
  currDirectory = "./"
  backupDirectoryAbstract = "./backupFiles/Abstracts/"
  backupDirectoryConcrete = "./backupFiles/Concretes/"
  backupDirectoryLabels = "./backupFiles/Labels/"
  makeDir([backupDirectoryAbstract, backupDirectoryConcrete, backupDirectoryLabels])
  for filename in os.listdir(currDirectory):
      if filename.startswith(newGrammar+".gf"):
          source = os.path.join(currDirectory,filename)
          destination = os.path.join(backupDirectoryAbstract, filename+"_"+timestr)
          dest = shutil.copyfile(source, destination)
  for filename in os.listdir(currDirectory):
      if filename.startswith(newGrammar+"Eng"):
          source = os.path.join(currDirectory,filename)
          destination = os.path.join(backupDirectoryConcrete, filename+"_"+timestr)
          dest = shutil.copyfile(source, destination)
  for filename in os.listdir(currDirectory):
      if filename.endswith(".labels"):
          source = os.path.join(currDirectory,filename)
          destination = os.path.join(backupDirectoryLabels, filename+"_"+timestr)
          dest = shutil.copyfile(source, destination)

def removePrevLabelFiles():
  currDirectory = "./"
  for filename in os.listdir(currDirectory):
    if filename.endswith(".labels"):
      os.remove(filename)
def removePrevGFFiles():
  currDirectory = "./"
  for filename in os.listdir(currDirectory):
    if filename.endswith(".gf"):
      os.remove(filename)

def removeAllPrevFiles():
  removePrevLabelFiles()
  removePrevGFFiles()

if __name__ == "__main__":

  inputFile = sys.argv[-3]
  print('load ', inputFile)
  newGrammar = sys.argv[-2]
  print('load new grammar ', newGrammar)
  oldGrammar = sys.argv[-1]
  print('load old grammar ', oldGrammar)

  makeBak()
  # removeAllPrevFiles()
  writeLabels(inputFile, oldGrammar, newGrammar)

  makeAbstractGF(inputFile, oldGrammar, newGrammar)
  makeConcreteGF(inputFile, oldGrammar, newGrammar)

  makeNewGrammar(inputFile, oldGrammar, newGrammar)
