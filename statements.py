# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.words=[]
    def add(self, stem, cat):
        try:
            if (cat in ["P","N","A","I","T"]):
                add(self.words, (stem, cat))
            else: 
                raise Exception ("The category tag: "+ cat + " is not supported")
        except Exception as error:
            print error

    def getAll(self, cat):
        categirizedWords=[]
        for w in self.words:
            if(w[1]==cat and w[0] not in categirizedWords): # make sure not duplicates
                categirizedWords.append(w[0])
        return categirizedWords



class FactBase:
    """stores unary and binary relational facts"""
    # add code here
    def __init__(self):
        self.unaryFacts=[]
        self.binaryFacts=[]
    def addUnary(self, pred,e1):
        self.unaryFacts.append((pred, e1))
    
    def addBinary(self, pred,e1,e2):
        self.binaryFacts.append((pred,e1, e2))
    
    def queryUnary(self, pred,e1):
        return (pred,e1) in self.unaryFacts
    def queryBinary(self, pred,e1,e2):
        return (pred, e1, e2) in self.binaryFacts

import re
from nltk.corpus import brown 
BrownTaggedWords=brown.tagged_words()
def verb_stem(s):
    stem = ""
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    if re.match ("[a-z]*[^sxyzaeiou]s$", s) and s[-4:-2] not in ["ch", "sh"]:
        stem = s[:-1]
    elif re.match ("[a-z]*[aeiou]ys$", s):
        stem = s[:-1]
    elif re.match ("[a-z][a-z]*[^aeiou]ies$", s):
        stem = s[:-3] + "y"
    elif re.match ("[^aeiou]ies$", s):
        stem = s[:-1]
    elif re.match ("[a-z]*(o|x|ch|sh|ss|zz)es$", s):
        stem = s[:-2]
    elif (re.match ("[a-z]*(se|ze)s$", s) and s[-3:] != "sses" and s[-3:] != "zzes"):
        stem = s[:-1]
    elif s == "has":
        stem = "have"
    elif re.match ("[a-z]*[^iosxz]es$", s) and s[-4:-2] != 'sh' and s[-4:-2] != 'ch':
        stem =  s[:-1]
    else:
        return "" # return directly avoid the need to search through the dictionary
    if(isVBorZ(s, stem)):
        return stem
    else:
        return ""
    
def isVBorZ(s, stem):
    for word,tag in BrownTaggedWords:
        if tag =="VB" and stem == word:
            return True
        elif tag =="VBZ" and s == word:
            return True
    return False
                

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

