# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    unchanging_plurals=[]
    singulars=[]
    plurals=[]
    with open("sentences.1.txt", "r") as f:
        for line in f:
            for taggedWord in line.split(" "):
                word, tag = taggedWord.split("|")
                if tag== "NN":
                    singulars.append(word)
                elif tag =="NNS":
                    plurals.append(word)
                else:
                    continue
        for s_word in singulars:
            if s_word not in unchanging_plurals and s_word in plurals:
                unchanging_plurals.append(s_word)
        
    return unchanging_plurals


unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""  
    if s in unchanging_plurals_list:
        return s
    elif (s[-3:]== "men"):
        s=list(s)
        s[-2]="a"
        return "".join(s)
    elif re.match ("[a-z]*[^sxyzaeiou]s$", s) and s[-4:-2] not in ["ch", "sh"]:
        return s[:-1]
    elif re.match ("[a-z]*[aeiou]ys$", s):
        return s[:-1]
    elif re.match ("[a-z]+[^aeiou]ies$", s) and len(s) >= 5:
        return s[:-3] + "y"
    elif re.match ("[^aeiou]ies$", s):
        return s[:-1]
    elif re.match ("[a-z]*(o|x|ch|sh|ss|zz)es$", s):
        return s[:-2]
    elif (re.match ("[a-z]*(se|ze)s$", s) and s[-3:] != "sses" and s[-3:] != "zzes"):
        return s[:-1]
    elif re.match ("[a-z]*[^iosxz]es$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
        return  s[:-1]
    else:
        return ""

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    word_tags = []

    if wd in function_words:
        for pair in function_words_tags:
            if pair[0] == wd and pair[1] not in word_tags:
                word_tags.append(pair[1])
    for cat in ["I", "T"]:
        if wd in lx.getAll(cat):                  
            if verb_stem(wd) == "":
                word_tags.append(cat + "p")
            else:
                word_tags.append(cat + "s")
        if verb_stem(wd) in lx.getAll(cat):
            word_tags.append(cat + "s")
        for word in lx.getAll(cat):
            if verb_stem(word) == wd:
                word_tags.append(cat + "p")
                break

    for cat in ["P", "A"]:                             
        if wd in lx.getAll(cat):
                word_tags.append(cat)

    if wd in lx.getAll("N"):                      
        if wd in unchanging_plurals_list:
            word_tags += ["Ns", "Np"]
        elif noun_stem(wd) == "":
            word_tags.append("Ns")
        else:
            word_tags.append("Np")
    if noun_stem(wd) in lx.getAll("N"):
        word_tags.append("Np")
    for word in lx.getAll("N"):
        if noun_stem(word) == wd:
            word_tags.append("Ns")
            break

    return list(set(word_tags))

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.