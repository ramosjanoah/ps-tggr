#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 20:25:25 2017

@author: ramosjanoah
"""

from conllu.parser import parse, parse_tree

WORD_TYPES = ['ADV', 'ADJ', 'ADP', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 
               'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'VERB', 'X']
DICTIONARY_OF_WORD = {}

f = open('id-ud-train.conllu','r')
data = f.read()

parse(data)