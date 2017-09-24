#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 20:25:25 2017

@author: ramosjanoah
"""

from conllu.parser import parse,
import math

WORD_TYPES = ['ADV', 'ADJ', 'ADP', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 
               'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'VERB', 'X', 'PART', 'SYM']
DICTIONARY_OF_WORD = {}

# read Data

f = open('id-ud-train.conllu','r', encoding='utf-8')
data = f.read()
data = parse(data)

def viterbi(N,T):
	viterbi = {}



    
	
def viterbi_segment(text, P):
    """Find the best segmentation of the string of characters, given the
    UnigramTextModel P."""
    # best[i] = best probability for text[0:i]
    # words[i] = best word ending at position i
    n = len(text)
    words = [''] + list(text)
    best = [1.0] + [0.0] * n
    ## Fill in the vectors best, words via dynamic programming
    for i in range(n+1):
        for j in range(0, i):
            w = text[j:i]
            if P[w] * best[i - len(w)] >= best[i]:
                best[i] = P[w] * best[i - len(w)]
                words[i] = w
    ## Now recover the sequence of best words
    sequence = []; i = len(words)-1
    while i > 0:
        sequence[0:0] = [words[i]]
        i = i - len(words[i])
    ## Return sequence of best words and overall probability
    return sequence, best[-1]

## initiate model

def createEmptyWordTypeDictionary():
    global WORD_TYPES
    emptyWordTypeDictionary = {}
    for wordType in WORD_TYPES:
        emptyWordTypeDictionary[wordType] = 0
    return emptyWordTypeDictionary
    
def createWordTagDictionary_none():
    global WORD_TYPES
    emptyWordTypeDictionary = {}
    for wordType in WORD_TYPES:
        emptyWordTypeDictionary[wordType] = None
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
    for word in sentence:
        stc.append(word['form'])
        if word['upostag'] != None:
            tag = word['upostag']
        else:
            tag = word['xpostag']
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
    print(stc)
    

#for previous, tagDictionary in transitionDictionary.items():
#    for tag, value in tagDictionary.items   ():
#        print("PREVIOUS TAG: " + previous + "," + " TAG: " + tag + ". JUMLAH KEMUNCULAN : " + str(value))
        
#print(emitDictionary['jingga'])
#print(emptyWordTypeDictionary)
#print(emitDictionary[','])
#print(transitionDictionary)
#print(contextDictionary)
#print(data)







# --- ramos part ----


sentence = ['Jadi', 'dicoba', 'untuk', 'menjawab', 'pertanyaan-pertanyaan', 'seperti', 'kebutuhan', 'apa', 'yang', 'dicoba', 'dipuaskan', 'oleh', 'seseorang', '?']

transitionDictionary

def probabilityT(_next, prev):
    sumValue = 0
    for tag in WORD_TYPES:
        sumValue += transitionDictionary[tag][_next]
    return transitionDictionary[prev][_next]/sumValue

def probabilityE(word, tag):
    global emitDictionary
    if emitDictionary.get(word, None) != None:
        sumValue = 0
        for key, value in emitDictionary[word].items():
            sumValue += value            
        return emitDictionary[word][tag]/sumValue
    else:
        return 1
        

def Classify(arrayOfWord):
    global WORD_TYPES
    bestScore = {}
    bestEdge = {}
    for i in range(0, len(arrayOfWord)):        
        bestScore[i] = {}
        for tag in WORD_TYPES:
            bestScore[i][tag] = 99
    for i in range(0, len(arrayOfWord)):            
        bestEdge[i] = createWordTagDictionary_none()
        
    for i in range(0, len(arrayOfWord)):
        print(arrayOfWord[i])
        for prev in WORD_TYPES:
            for _next in WORD_TYPES:
                if bestScore[i][prev] and transitionDictionary[prev][_next] :
                    try:
                        score = bestScore[i][prev] - math.log10(probabilityT(_next,prev)) - math.log10(probabilityE(arrayOfWord[i],_next))
                    except ValueError:
                        score = bestScore[i][prev]
                    if i+1 < len(arrayOfWord):
                        print("---")
                        print(str(score) + " " + str(bestScore[i+1][_next]))
                        print("---")
                        if bestScore[i+1][_next] > score:

                            bestScore[i+1][_next] = score
                            bestEdge[i+1][_next] = (i, prev)
    return bestEdge

a = Classify(sentence)