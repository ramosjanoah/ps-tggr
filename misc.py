#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 15:00:19 2017

@author: ramosjanoah
"""
def initProbability(word):
    global WORD_TYPES
    ProbabilityDictionaryOfWord = {}
    for wordType in WORD_TYPES:
        ProbabilityDictionaryOfWord = 1
    return ProbabilityDictionaryOfWord

for WordType in WORD_TYPES:
    f = open(WordType + '.txt','r')
    words = f.readline()
    words = words.lower()
    words = words.replace('\n', '')

    if WordType == 'PUNCT':
        word = words.split("0")
    else:
        word = words.split(", ")
    DICTIONARY_OF_WORD[WordType] = word