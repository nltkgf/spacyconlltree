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
  print(oldGrammar)
  gr = pgf.readPGF(oldGrammar)
  R = gr.embed(oldGrammar)
  print(gr)
  # print(R)

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
  for line in treefrom.uniqueFuns():
    abstractGF.write("\t\t" + line[0] + " -> UDS ;\n")
    abstractGF.write("\t--" + line[1] + " ;\n\n")
  abstractGF.write("}")
  abstractGF.close()



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

makeBak()
removeAllPrevFiles()
writeLabels()
makeAbstractGF(abstractGrammar)
makeConcreteGF(abstractGrammar)
getPGF(oldGrammar)

