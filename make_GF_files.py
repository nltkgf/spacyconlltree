from abc import abstractclassmethod
from typing import AbstractSet
import spacy_udpipe
import sys
import treefrom
import time
import os
import shutil
import pgf
import itertools

from pathlib import Path

filename = sys.argv[-3]
print('load ', filename)
abstractGrammar = sys.argv[-2]
print('load abstract ', abstractGrammar)
oldGrammar = sys.argv[-1]
print('load old grammar ', oldGrammar)

def getPGF(oldGrammar):
  # print(oldGrammar)
  gr = pgf.readPGF(oldGrammar)
  # R = gr.embed(oldGrammar)
  pgfAsStr = str(gr)
  listOldGram = []
  for line in pgfAsStr.splitlines():
    listOldGram.append(line)
  indexStart =  [idx for idx, s in enumerate(listOldGram) if "fun root__ : root -> UDS" in s][0]
  # print("index", indexStart)
  # print (listOldGram)
  # print (listOldGram[indexStart:])
  wantedList = listOldGram[indexStart:]
  # print("a list of funs with UDS",wantedList)
  list_old_Funs = []
  for phrase in wantedList:
    wantedPhrase = phrase.partition(";")[0]
    wantedFun = wantedPhrase [6:-8] if "UDS" in wantedPhrase else wantedPhrase [6:-1]
    list_old_Funs.append(wantedFun)
    # print (wantedFun)
  print ("list without UDS", list_old_Funs)
  return (list_old_Funs)



# def extractFunsOldGram (oldGrammar):
#     wantedFuns = oldGrammar.partition("\n\n\tfun\n")


def compareFunsLists(oldGrammar):
    list_Uniq_Funs = []
    # list_Uniq_Funs_Corpus= treefrom.uniqueFuns()
    # for element in list_Uniq_Funs_Corpus:
    #   uniq_Funs = element [0]
    #   list_Uniq_Funs.append(uniq_Funs)
    # # print (list_Uniq_Funs)
    # for line in open(abstractGrammar + "Unique_Funs.gf", "r"):
    #   list_Uniq_Funs.append(line)

    list_Uniq_Funs = makeAbstractGF(abstractGrammar)
    list_OldGram_Funs = getPGF(oldGrammar) # equal "list without UDS"
    # list_Old_Gram = getPGF (oldGrammar)
    # str_gr = getPGF(orignAbstract)
    li_dif = [i for i in list_Uniq_Funs  + list_OldGram_Funs if i not in list_Uniq_Funs  or i not in list_OldGram_Funs]
    print("list of difference", li_dif)

    # return li_dif


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

def coerceFunsAbs(cat):
  return [(cat + "_"), ":", "X", "->", cat, ";"]

def coerceFunsConcrete(cat):
  return [(cat + "_"), "x", "= TODO ;"]

def makeNewGrammars():
  oldPGF = getPGF(oldGrammar)
  # print(oldPGF)
  newGrammar = open ("newGrammar" + ".gf", "w+")
  newGrammar.truncate(0)
  newGrammar.seek(0)
  newGrammar.write(
            "abstract New"
          + abstractGrammar
          + " = Old"
          + abstractGrammar
          + " ** { \n\t\t +}"
  )

def writeLabels():
  with open(abstractGrammar + '.labels', 'w+') as labelFile:
    for eachFun in treefrom.uniqueFuns():
      eachLabel = "#fun " + eachFun[0].replace(': root ', 'head').replace("->", "") # TODO: return type should not be in the labels
      start = eachLabel.partition("head")[0] + eachLabel.partition("head")[1]
      trail = eachLabel.partition("head")[2]
      trailNew = treefrom.toUDelement(trail)
      labelFile.write(start+ trailNew +"\n")

# create an abstract GF file with user entered name
def makeAbstractGF(userGrammar):
  abstractGF = open (abstractGrammar + ".gf", "w+")
  abstractGFUniq_Funs = open (abstractGrammar + "Unique_Funs.gf", "w+")
  abstractGF.truncate(0)
  abstractGF.seek(0)
  abstractGF.write(
            "abstract "
          + abstractGrammar
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

  # get coercedFuns
  for line in getCats():
    abstractGF.write("\n\t\t" + " ".join(coerceFunsAbs(line)))

  abstractGF.write( "\n\n\tfun\n" )
  print('length of unique funs ', len(treefrom.uniqueFuns()))
  list_Corpus_Unique_Funs = []
  for line in treefrom.uniqueFuns():
    abstractGF.write("\t\t" + line[0] + " -> UDS ;\n")
    abstractGF.write("\t--" + line[1] + " ;\n\n")
    list_Corpus_Unique_Funs.append(line[0])
    abstractGFUniq_Funs.write(line[0] +"\n")
  abstractGF.write("}")
  abstractGF.close()
  abstractGFUniq_Funs.close()
  print("list_Corpus_Unique_Funs",list_Corpus_Unique_Funs)
  return (list_Corpus_Unique_Funs)

def makeConcreteGF(userGrammar):
  concreteGF = open (abstractGrammar+ "Eng.gf", "w+")
  concreteGF.truncate(0)
  concreteGF.seek(0)
  concreteGF.write(
          "concrete "
        + abstractGrammar
        + "Eng of "
        + abstractGrammar
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
      if filename.startswith(abstractGrammar+".gf"):
          source = os.path.join(currDirectory,filename)
          destination = os.path.join(backupDirectoryAbstract, filename+"_"+timestr)
          dest = shutil.copyfile(source, destination)
  for filename in os.listdir(currDirectory):
      if filename.startswith(abstractGrammar+"Eng"):
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

# makeBak()
# removeAllPrevFiles()
# writeLabels()
makeAbstractGF(abstractGrammar)
# makeConcreteGF(abstractGrammar)
getPGF(oldGrammar)
# makeNewGrammars()
compareFunsLists(oldGrammar)
# print(pgf.readPGF("Abstract.pgf"))
