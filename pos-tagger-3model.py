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

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', DecisionTreeClassifier())
    #('classifier', KNeighborsClassifier())
    #('classifier', GaussianNB())
])

clf.fit(dataset_training[:5000], tag_training[:5000])

X_test, y_test = transform_to_dataset(test_sentences)

print ("SCORE : " + str(clf.score(X_test[:1000], y_test[:1000])*100))