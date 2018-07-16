#/usr/bin/python
import string
import numpy as np
from sklearn.preprocessing import LabelEncoder
from hmmlearn import hmm

# ASCII character
chars = list(string.printable)
chars.pop()
chars.pop()
chars.pop()
chars.pop()
print(chars)

def createMatrix(numRows, numColumn):
    value = (1 / float(numRows))
    matrix = [value] * numRows
    if numColumn > 1:
        for i in range(numRows):
            matrix[i] = [value] * numColumn
    return matrix

def textToObs(tweet):
    obs = list(filter(lambda x: x in chars, tweet))
    for i in range(0, len(obs)):
        obs[i] = [chars.index(obs[i])]
    return obs

def getTrainingSet(trainingSet):
    obss = []
    for line in trainingSet:
        obss.extend(textToObs(line))
    return obss

n_components = len(chars)
n_features = len(chars)
h = hmm.MultinomialHMM(n_components)
h.n_features = n_features
h.startprob_ = np.array(createMatrix(len(chars), 1))
h.transmat_ = np.array(createMatrix(len(chars), len(chars)))
h.emissionprob_ = np.array(createMatrix(len(chars), len(chars)))


print(h.startprob_)
print(h.transmat_)
print(h.emissionprob_)

trainingFile = open("train.txt", 'r')
trainingSet = getTrainingSet(trainingFile)
print(trainingSet)
h.fit(trainingSet)

print(h.startprob_)
print(h.transmat_)
print(h.emissionprob_)