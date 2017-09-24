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

f = open('id-ud-train.conllu','r', encoding='utf-8')
data = f.read()
data = parse(data)

def tp(i,j):
    tes
def sol(o,j):
    tes

def viterbi(Obs,States):
    viterbi = {}
    backpointer = {}
    for state in States:
        viterbi[state][1] = tp(i,j) * sol(o,j)
        backpointer[state][1] = 0
    for i in range(2,T):
        for state in States:
            viterbi[state][i] = tp(i,j) * sol(o,j)
            backpointer[state][i] = tp(i,j)
    viterbi[state][i] = tp(i,j)
    backpointer[state][i] = tp(i,j)
	
## initiate model

def createEmptyWordTypeDictionary():
    global WORD_TYPES
    emptyWordTypeDictionary = {}
    for wordType in WORD_TYPES:
        emptyWordTypeDictionary[wordType] = 0
    return emptyWordTypeDictionary

emitDictionary = {}
transitionDictionary = {}
contextDictionary = {}

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
    stc = [""]
    labelv = [""]
    for word in sentence:
        stc.append(word['form'])
        if word['upostag'] != None:
            tag = word['upostag']
            labelv.append(word['upostag'])
        else:
            tag = word['xpostag']
            labelv.append(word['xpostag'])
        transitionDictionary[previous][tag] += 1
        contextDictionary[tag] += 1
        if emitDictionary.get(word['form'], None) == None:
            emitDictionary[word['form']] = createEmptyWordTypeDictionary()
        emitDictionary[word['form']][tag] += 1
        previous = tag
    transitionDictionary[previous]['START'] += 1
    try:
        stc.remove('')
    except:
        pass
    try:
        labelv.remove('')
    except:
        pass
    #print(stc)
    #print(labelv)
#for previous, tagDictionary in transitionDictionary.items():
#    for tag, value in tagDictionary.items   ():
#        print("PREVIOUS TAG: " + previous + "," + " TAG: " + tag + ". JUMLAH KEMUNCULAN : " + str(value))
        
#print(emitDictionary['jingga'])
#print(emptyWordTypeDictionary)
#print(emitDictionary[','])
#print(transitionDictionary)
#print(contextDictionary)
#print(data)