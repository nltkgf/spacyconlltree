import spacy_udpipe
import sys
import treefrom
import time
import os
import shutil
import pgf
import itertools
import glob

from pathlib import Path

filename = sys.argv[-3]
print('load ', filename)
newGrammar = sys.argv[-2]
print('load new grammar ', newGrammar)
oldGrammar = sys.argv[-1]
print('load old grammar ', oldGrammar)

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
def getNewGrammarFuns():
  list_Corpus_Unique_Funs = []
  for line in treefrom.uniqueFuns():
    list_Corpus_Unique_Funs.append("fun " + line[0] + " -> UDS ;")
  return list_Corpus_Unique_Funs

# compare old and new grammar
def compareFunsLists(oldGrammar):
    newGrammar = getNewGrammarFuns()
    oldGrammar = getPGF(oldGrammar)
    li_dif = [i for i in newGrammar + oldGrammar if i not in newGrammar  or i not in oldGrammar]
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

def makeNewGrammar(oldGrammar):
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
  for line in compareFunsLists(oldGrammar):
    newGrammarFile.write("\n\t\t" + line)

  newGrammarFile.write("\n}")

# write label file from scratch

def writeLabels():

    # check if label file already exists
    currentLabels = []
    os.chdir(os.getcwd())
    for label in glob.glob("*.labels"):
      currentLabels.append(label)

    if bool(currentLabels) == True:
      newLabels(currentLabels, oldGrammar)
    else:
      with open(newGrammar + '.labels', 'w+') as labelFile:
        for eachFun in treefrom.uniqueFuns():
          eachLabel = "#fun " + eachFun[0].replace(': root ', 'head').replace("->", "") # TODO: return type should not be in the labels
          start = eachLabel.partition("head")[0] + eachLabel.partition("head")[1]
          trail = eachLabel.partition("head")[2]
          trailNew = treefrom.toUDelement(trail)
          labelFile.write(start+ trailNew +"\n")

# append new labels

def newLabels(currentLabels, oldGrammar):
  with open(newGrammar + '.labels', 'a+') as labelFile:

    # get most recent label
    latestLabel = max(currentLabels, key=os.path.getmtime)

    # copy content from most recent label
    source = str(latestLabel)
    destination = str(newGrammar + '.labels')
    shutil.copyfile(source, destination)

    for line in compareFunsLists(oldGrammar):
      eachLabel = "#" + line.replace(': root ', 'head').replace("->", "").replace("UDS", "").replace(";", "")
      labelFile.write(eachLabel)

# create an abstract GF file with user entered name
def makeAbstractGF(userGrammar):
  abstractGF = open (newGrammar + ".gf", "w+")
  abstractGF.truncate(0)
  abstractGF.seek(0)
  abstractGF.write(
            "abstract "
          + newGrammar
          + " = {"
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
  print('length of unique funs ', len(treefrom.uniqueFuns()))
  for line in treefrom.uniqueFuns():
    funLine = "\t\t" + line[0] + " -> UDS ;\n\t--" + line[1] + " ;\n\n"
    abstractGF.write(funLine)
  abstractGF.write("}")
  abstractGF.close()

# make concrete grammar

def makeConcreteGF(userGrammar):
  concreteGF = open (newGrammar + "Eng.gf", "w+")
  concreteGF.truncate(0)
  concreteGF.seek(0)
  concreteGF.write(
          "concrete "
        + newGrammar
        + "Eng of "
        + newGrammar
        + " = {"
        + "\n\n\tlincat"
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

  for line in treefrom.uniqueFuns():
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

makeBak()
# removeAllPrevFiles()
writeLabels()

makeAbstractGF(newGrammar)
makeConcreteGF(newGrammar)

makeNewGrammar(oldGrammar)
