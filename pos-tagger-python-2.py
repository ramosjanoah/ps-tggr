#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 20:25:25 2017

@author: ramosjanoah
"""

from conllu.parser import parse, parse_tree

WORD_TYPES = ['ADV', 'ADJ', 'ADP', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 
               'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'VERB', 'X', 'PART', 'SYM']
DICTIONARY_OF_WORD = {}

# read Data

f = open('id-ud-train.conllu','r')
data = f.read()
data = parse(data)

## initiate model

emptyWordTypeDictionary = {}
emitDictionary = {}
transitionDictionary = {}
contextDictionary = {}

for wordType in WORD_TYPES:
    emptyWordTypeDictionary[wordType] = 0

WORD_TYPES.append('START')
for wordTypeKey in WORD_TYPES:
    transitionDictionary[wordTypeKey] = {}
    for wordTypeValue in WORD_TYPES:
        transitionDictionary[wordTypeKey][wordTypeValue] = 0

for wordType in WORD_TYPES:
    contextDictionary[wordType] = 0


# for transitionDictionary, first key of dictionary is previous, the second key is the tag, 
# value is the number

for sentence in data:
    previous = 'START'
    contextDictionary[previous] += 1
    for word in sentence:
        if word['upostag'] != None:
            tag = word['upostag']
        else:
            tag = word['xpostag']
        transitionDictionary[previous][tag] += 1
        contextDictionary[tag] += 1
        if emitDictionary.get(word['form'], None) == None:
            emitDictionary[word['form']] = emptyWordTypeDictionary
        previous = tag
    transitionDictionary[previous]['START'] += 1

for previous, tagDictionary in transitionDictionary.iteritems():
    for tag, value in tagDictionary.iteritems():
        print "PREVIOUS TAG: " + previous + "," + " TAG: " + tag + ". JUMLAH KEMUNCULAN : " + str(value)
        