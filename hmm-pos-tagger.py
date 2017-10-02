# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 09:35:55 2017

@author: noah
"""
## FOR NICO
## To change feature, see line 98

# Load Dataset

from conllu.parser import parse 

f = open('id-ud-train.conllu','r', encoding='utf-8')
data = f.read()
tagged = parse(data)

percentage = int(.8 * len(tagged))

training_sentences = tagged[:percentage]
test_sentences = tagged[percentage:]

# Making transition probability

WORD_TYPES = ['START', 'ADV', 'ADJ', 'ADP', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 
               'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'VERB', 'X', 'PART', 'SYM']

contextDictionary = {}
transitionDictionary = {}
emitDictionary = {}
for wordTypeKey in WORD_TYPES:
    transitionDictionary[wordTypeKey] = {}
    for wordTypeValue in WORD_TYPES:
        transitionDictionary[wordTypeKey][wordTypeValue] = 0
for wordType in WORD_TYPES:
    contextDictionary[wordType] = 0


def createEmptyWordTypeDictionary():
    global WORD_TYPES
    emptyWordTypeDictionary = {}
    for wordType in WORD_TYPES:
        emptyWordTypeDictionary[wordType] = 0
    return emptyWordTypeDictionary

for sentence in training_sentences:
    global contextDictionary
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

len(transitionDictionary['VERB'])

def searchProbability(dictionary, exception): 
    probList = []
    sum = 0
    for key, value in dictionary.items():
        if key == exception:
            pass
        else:
            probList.append(value)
            sum += value
    
    for idxValue in range(0,len(probList)):
        try:
            probList[idxValue] /= sum
        except ZeroDivisionError:
            probList[idxValue] = 0
    
    return probList
    
    

startProb = searchProbability(transitionDictionary['START'], 'START')


listProb = []

for key, value in transitionDictionary.items():
    print(key)
    listTemp = searchProbability(transitionDictionary[key], 'START')
    listProb.append(listTemp)



# feature 1

import numpy as np
from hmmlearn import hmm

lr = hmm.GaussianHMM(n_components=(17), covariance_type="diag",
                     init_params="cm", params="cmt")
lr.startprob_ = np.array(startProb)
lr.transmat_ = np.array(listProb)
lr.monitor_.converged

lr.predict([1,2,3,4],4)

