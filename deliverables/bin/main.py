# Read input

file = open('input.txt','r')

_input_sentence = file.readline()
_input = _input_sentence.split(' ')

from conllu.parser import parse 

# Load Dataset

f = open('id-ud-train.conllu','r', encoding='utf-8')
data = f.read()
tagged = parse(data)

# Feature Extraction

# feature 1, 
def features1(sentence, index):
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

def features1_input(sentence, index):
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 2,
        'is_dot': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix2': sentence[index][:2],
        'suffix2': sentence[index][-2:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'is_numeric': sentence[index].isdigit(),
}

def tagFromWord(sentence, index):
    if (sentence[index]['upostag']) != None:
        return sentence[index]['upostag']
    else:
        return sentence[index]['xpostag']

percentage = int(.8 * len(tagged))

training_sentences = tagged[:percentage]

def transform_to_dataset(training_sentences):
    X, y = [], []    
    for sentence in training_sentences:
        for idxWord in range(len(sentence)):
            X.append(features1(sentence, idxWord))
            y.append(tagFromWord(sentence, idxWord))
 
    return X, y

dataset_training, tag_training = transform_to_dataset(training_sentences)

# Training

import sklearn_crfsuite

def sentences_feature(sentence):
    return [features1(sentence, i) for i in range(len(sentence))]
            
def sentences_label(sentence):
    return [tagFromWord(sentence, i) for i in range(len(sentence))]
            
def sentences_feature_input(sentence):
    return [features1_input(sentence, i) for i in range(len(sentence))]

dataset_train = [sentences_feature(s) for s in training_sentences]
label_train = [sentences_label(s) for s in training_sentences]
               
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)               
               
crf.fit(dataset_train[:1500], label_train[:1500])

sentences_feature_input(_input) 

dataset_test = [sentences_feature_input(_input)]
              
label_predict = crf.predict(dataset_test)

print ("[RESULT] - " + _input_sentence)
for idx in range(len(_input)):
    print (_input[idx] + " : " + label_predict[0][idx
