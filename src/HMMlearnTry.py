#/usr/bin/python
import string
import numpy as np
from hmmlearn import hmm
from sklearn.externals import joblib


def getVocabulary(file):
    text = ""
    for line in file:
        text = text + line
    voc = [char for char in text]
    voc = list(set(voc))

    print [(i, voc[i]) for i in range(0, len(voc))]

    return voc


def createMatrix(numRows, numColumn):
    value = (1 / float(numRows))
    matrix = [value] * numRows
    if numColumn > 1:
        for i in range(numRows):
            matrix[i] = [value] * numColumn
    return matrix


def textToObs(tweet, voc):
    obs = list(filter(lambda x: x in voc, tweet))
    for i in range(0, len(obs)):
        obs[i] = [voc.index(obs[i])]
    return obs


def getTrainingSet(trainingSet, voc):
    obss = []
    tmpvoc = voc[:]
    tmp_tweet = []
    for line in trainingSet:
        linevoc = [char for char in line]
        linevoc = list(set(linevoc))
        tmpvoc = [x for x in tmpvoc if x not in linevoc]

        #print(tmp_tweet)

        if len(tmpvoc) == 0:
            tmp_tweet.extend(textToObs(line, voc))
            obss.insert(len(obss), tmp_tweet)
            tmp_tweet = []
            tmpvoc = voc[:]
        else:
            tmp_tweet.extend(textToObs(line, voc))
    return obss


def setUpHMM(numOfChars):
    n_components = numOfChars
    n_features = numOfChars
    model = hmm.MultinomialHMM(n_components)
    model.n_features = n_features
    model.startprob_ = np.array(createMatrix(numOfChars, 1))
    model.transmat_ = np.array(createMatrix(numOfChars, numOfChars))
    model.emissionprob_ = np.array(createMatrix(numOfChars, numOfChars))
    return model

# Load the training file and extract the vocubulary
fileName = "small_NASA.txt"
trainingFile = open(fileName, 'r')
#chars = getVocabulary(trainingFile)
chars = list(string.ascii_lowercase + string.ascii_uppercase)
trainingFile = open(fileName, 'r')
trainingSet = getTrainingSet(trainingFile, chars)

model = setUpHMM(len(chars))

output = open('./HMM_description.txt', 'w+')

#print("Printing untrained HMM...")
#output.write('Untrained HMM:\n\n')
#printHMM(model, output)

print(trainingSet)

print("Training HMM...")
for tweet in trainingSet:
    print(tweet)
    model.fit(tweet)

#print("Printing trained HMM...")
#output.write('\n\nTrained HMM:\n\n')
#printHMM(model, output)

print("Saving HMM...")
joblib.dump(model, "Saved_HMM.pkl")

output.close()