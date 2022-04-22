import spacy
import spacy_udpipe
import sys

#nlp = spacy.load("en_core_web_sm")
nlp = spacy_udpipe.load("en")
from spacy import displacy

from spacy_conll import init_parser

con = init_parser(
     "en", "udpipe", include_headers=True
)

filename = sys.argv[-1]

def uniqueFuns(input):
  """
  input: a file (free text or conllu)
  output: a list of UDresult
  """
  fun_list = []
  results = getRelsText(input)
  for res in results:
    if res not in fun_list:
      fun_list.append(res.labels())
  return sorted(fun_list)


def getRelsText(input):
  """
  input: list of sentences (strings)
  output: generator of UDresults
  """
  with open(filename) as input:
    texts = input.readlines()
    for text in texts:
      doc = nlp(text)
      for token in doc:
        if token.dep_ == 'ROOT':
          rels = [child.dep_ for child in token.children
                  if child.dep_ != 'punct'] # e.g. ['nsubj', 'obl']
          yield UDresult(rels, text)

#########################################
## Class for UDresult
## This contains the list of relations,
## and methods to create different formats

class UDresult:
  def __init__(self, relations, example):
    """
    input: list of relations, e.g. ['nsubj:pass', 'aux:pass', 'obl']
    """
    relations.insert(0, "root")
    self.relations = relations
    self.fun_name = self.funName()
    self.example = example


  ## Methods to manipulate strings
  def funName(self):
    """
    returns a single string that is the name of the function,
    e.g. root_nsubjPass_auxPass_obl.
    This is the simplest representation, used to compare the funs.
    """
    return '_'.join([replaceColon(r) for r in self.relations])

  def gfAbs(self):
    """
    returns a line of GF abstract syntax:
    e.g. fun root_nsubjPass_auxPass_obl : root -> nsubjPass -> auxPass -> obl -> UDS ;
    """
    fun_and_sig = "fun %s : %s ;" % (self.fun_name, self.gfTypeSig())
    return fun_and_sig

  def gfTypeSig(self):
    args = [labelToGFcat(r) for r in self.relations]
    args.append('UDS') # add return type
    return ' -> '.join(args)

  def gfFunArgs(self):
    args = [labelToGFcat(r) for r in self.relations]
    return ' '.join(args)

  def labels(self):
    """
    returns a line of GF labels:
    e.g. #fun root_nsubjPass_auxPass_obl head nsubj:pass aux:pass obl
    """
    args = [r.replace('root', 'head') for r in self.relations]
    fun_and_body = "#fun %s %s" % (self.fun_name, ' '.join(args))
    return fun_and_body

  ## Python class plumbing
  def __repr__(self):
    """representative field of a UDresult, used for comparison """
    return self.fun_name

  def __lt__(self, other):
    # p1 < p2 calls p1.__lt__(p2)
    return self.__repr__() < other.__repr__()

  def __eq__(self, other):
    # p1 == p2 calls p1.__eq__(p2)
    return self.__repr__() == other.__repr__()

def labelToGFcat(label):
  """
  input: a UD label name as a string, e.g. 'case', 'acl:relcl'
  output: sanitized version that is a valid GF cat, 'case_', 'aclRelcl'
  """
  return replaceColon(label.replace('case', 'case_'))

def replaceColon(el):
  """
  input: UD label as a string, e.g. acl:relcl
  output: colon replaced with camelcase, aclRelcl
  """
  if el.find(':') != -1:
    ind = el.index(':')
    try:
      cap = el[ind+1].upper()
      newStr = el[:ind] + cap + el[ind + 2:]
      return newStr
    except IndexError:
      return el[:ind]
  return el

for fun in uniqueFuns(filename):
  print(fun)
