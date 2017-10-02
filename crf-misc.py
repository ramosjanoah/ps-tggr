# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 21:58:00 2017

@author: Fina
"""

# CRF

import sklearn_crfsuite
from sklearn_crfsuite import metrics

def sentences_feature(sentence):
    return [features3(sentence, i) for i in range(len(sentence))]
            
def sentences_label(sentence):
    return [tagFromWord(sentence, i) for i in range(len(sentence))]

dataset_train = [sentences_feature(s) for s in training_sentences]
label_train = [sentences_label(s) for s in training_sentences]
               
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)               
               
crf.fit(dataset_train[:1000], label_train[:1000])

dataset_test = [sentences_feature(s) for s in test_sentences]
label_test = [sentences_label(s) for s in test_sentences]
              
label_predict = crf.predict(dataset_test)

labels = list(crf.classes_)
              
metrics.flat_f1_score(label_test, label_predict,
                      average='weighted', labels=labels)