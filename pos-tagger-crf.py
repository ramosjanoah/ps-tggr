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

# Feature Extraction

# feature 1, 
def features1(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index]['form'],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 2,
        'is_dot': index == len(sentence) - 1,
        'is_capitalized': sentence[index]['form'][0].upper() == sentence[index]['form'][0],
        'is_all_caps': sentence[index]['form'].upper() == sentence[index]['form'],
        'is_all_lower': sentence[index]['form'].lower() == sentence[index]['form'],
        'prefix2': sentence[index]['form'][:2],
        'suffix2': sentence[index]['form'][-2:],
        'prev_word': '' if index == 0 else sentence[index - 1]['form'],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1]['form'],
        'is_numeric': sentence[index]['form'].isdigit(),
}

def features2(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index]['form'],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 2,
        'is_dot': index == len(sentence) - 1,
        'is_capitalized': sentence[index]['form'][0].upper() == sentence[index]['form'][0],
        'is_all_caps': sentence[index]['form'].upper() == sentence[index]['form'],
        'is_all_lower': sentence[index]['form'].lower() == sentence[index]['form'],
        'prefix2': sentence[index]['form'][:2],
        'suffix2': sentence[index]['form'][-2:],
        'prev_word': '' if index == 0 else sentence[index - 1]['form'],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1]['form'],
        'prev2_word': '' if (index == 0 or index == 1) else sentence[index - 2]['form'],
        'is_numeric': sentence[index]['form'].isdigit(),

        'prev_tag': '' if index == 0 else tagFromWord(sentence, index-1),
        'next_tag': '' if index == len(sentence) - 1 else tagFromWord(sentence, index+1),
}

def features3(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index]['form'],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 2,
        'is_dot': index == len(sentence)- 1,
        'is_capitalized': sentence[index]['form'][0].upper() == sentence[index]['form'][0],
        'is_all_caps': sentence[index]['form'].upper() == sentence[index]['form'],
        'is_all_lower': sentence[index]['form'].lower() == sentence[index]['form'],
        'prefix2': sentence[index]['form'][:2],
        'suffix2': sentence[index]['form'][-2:],
        'prev_word': '' if index == 0 else sentence[index - 1]['form'],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1]['form'],
        'prev2_word': '' if (index == 0 or index == 1) else sentence[index - 2]['form'],
        'is_numeric': sentence[index]['form'].isdigit(),

        'prev_tag': '' if index == 0 else tagFromWord(sentence, index-1),
        'next_tag': '' if index == len(sentence) - 1 else tagFromWord(sentence, index+1),

        'prev_word2': '' if (index == 0 or index == 1) else sentence[index - 2]['form'],
        'next_word2': '' if (index == len(sentence) - 1 or index == len(sentence) - 2) else sentence[index + 2]['form'],
        'prev_tag2': '' if (index == 0 or index == 1) else tagFromWord(sentence, index-2),
        'next_tag2': '' if (index == len(sentence) - 1 or index == len(sentence) - 2) else tagFromWord(sentence, index+2),
}
   
def tagFromWord(sentence, index):
    if (sentence[index]['upostag']) != None:
        return sentence[index]['upostag']
    else:
        return sentence[index]['xpostag']

tagFromWord(tagged[0], 0)

percentage = int(.8 * len(tagged))

training_sentences = tagged[:percentage]
test_sentences = tagged[percentage:]


def transform_to_dataset(training_sentences):
    X, y = [], []    
    for sentence in training_sentences:
        for idxWord in range(len(sentence)):
            X.append(features2(sentence, idxWord))
            y.append(tagFromWord(sentence, idxWord))
 
    return X, y

dataset_training, tag_training = transform_to_dataset(training_sentences)

# Training

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

len(dataset_test)

labels = list(crf.classes_)
              
score = metrics.flat_f1_score(label_test, label_predict,
                      average='weighted', labels=labels)

print ("SCORE : ")
print (score)