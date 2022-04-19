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
def getPGFfuns(oldGrammar):
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


# compare old and new grammar
def compareFunsLists(newFuns, oldGrammar):
    oldFuns = getPGFfuns(oldGrammar)
    li_dif = [i for i in newFuns if i.gfAbs() not in oldFuns]
    print("diffs")
    print(*[i.gfAbs() for i in li_dif], sep="\n")
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


#get coerce funs

def coerceFunsAbs(cat):
  return [(cat + "_"), ":", "X", "->", cat, ";"]

def coerceFunsConcrete(cat):
  return [(cat + "_"), "x", "= TODO ;"]

# Write new grammar, which extends the old grammar

def makeNewGrammar(newFuns, oldGrammar, newGrammar):
  newGrammarFile = open (newGrammar + ".gf", "w+")
  newGrammarFile.truncate(0)
  newGrammarFile.seek(0)
  newGrammarFile.write(
            "abstract %s = %s ** {" % (newGrammar, oldGrammar)
  )

  newGrammarFile.write(
    "\n\n     -- additional corpus funs"
  )

  # write additional corpus funs
  for line in newFuns:
    newGrammarFile.write("    -- %s\n" % line.example)
    newGrammarFile.write("\n    " + line.gfAbs())

  newGrammarFile.write("\n}")

# write label file from scratch

def writeLabels(newFuns, oldGrammar, newGrammar):
    os.chdir(os.getcwd())
    oldLabelsFile = oldGrammar + ".labels"
    newLabelsFile = newGrammar + ".labels"

    # Kickstart the new labels file by copying the old labels
    if os.path.isfile(oldLabelsFile):
      shutil.copyfile(oldLabelsFile, newLabelsFile)

    # Print in stdout + write to file as well
    print("labels")
    with open(newGrammar + '.labels', 'w+') as labelFile:
        for res in newFuns:
          labelFile.write(res.labels() + "\n")
          print(res.labels())


# create an abstract GF file from scratch with user entered name
def makeAbstractGF(newFuns, newGrammar):
  abstractGF = open (newGrammar + ".gf", "w+")
  abstractGF.truncate(0)
  abstractGF.seek(0)
  abstractGF.write(
            "abstract %s = {" % newGrammar
          + "\n\n  flags"
          + "\n    startcat = UDS ;"
          + "\n\n  cat"
          + "\n    UDS ;"
          + "\n    X ;"
          )

  for line in getCats():
    abstractGF.write("\n    %s ;" % line)

  abstractGF.write(
    "\n\n  -- coercion funs"
  + "\n  fun"
  )

  # write coercedFuns
  for line in getCats():
    abstractGF.write("\n    " + " ".join(coerceFunsAbs(line)))

  # write corpus funs
  abstractGF.write( "\n\n  -- funs from corpus\n" )

  for line in newFuns:
    abstractGF.write("    -- %s\n" % line.example)
    abstractGF.write("    %s\n\n"    % line.gfAbs())
  abstractGF.write("}")
  abstractGF.close()

# make concrete grammar

def makeConcreteGF(newFuns, newGrammar):
  concreteGF = open (newGrammar + "Eng.gf", "w+")
  concreteGF.truncate(0)
  concreteGF.seek(0)
  concreteGF.write(
          "concrete "
        + "%s Eng of %s = {" % (newGrammar, newGrammar)
        + "\n\n  lincat"
        + "\n    UDS = TODO;"
        + "\n    X = TODO;"
        )
  for line in getCats():
    concreteGF.write("\n    %s = TODO ;" % line)
  concreteGF.write(
         "\n\n  -- the coercion funs"
        + "\n  lin"
        )
  for line in getCats():
    concreteGF.write("\n    " + " ".join(coerceFunsConcrete(line)))

  concreteGF.write("\n\n  -- the actual funs")

  for res in newFuns:
      concreteGF.write("\n    -- : %s" % res.gfTypeSig())
      concreteGF.write("\n    %s %s = TODO ;" % (res.funName(), res.gfFunArgs))

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

  inputFile = sys.argv[1]
  print('load ', inputFile)
  newGrammar = sys.argv[2]
  print('load new grammar ', newGrammar)
  oldGrammar = sys.argv[3]
  print('load old grammar ', oldGrammar)

  #makeBak()
  # removeAllPrevFiles()


  uniqFuns = treefrom.uniqueFuns(inputFile) # retrieve unique funs in input
  newUniqueFuns = compareFunsLists(uniqFuns, oldGrammar) # filter out funs already in old grammar

  print('length of unique funs ', len(newUniqueFuns))

  # Comment out only if you want to create a grammar from scratch
  #makeAbstractGF(newUniqueFuns, newGrammar)
  #makeConcreteGF(newUniqueFuns, newGrammar)

  # Augment the given old grammar
  writeLabels(newUniqueFuns, oldGrammar, newGrammar)
  makeNewGrammar(newUniqueFuns, oldGrammar, newGrammar)
