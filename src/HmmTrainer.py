#/usr/bin/python
import string
import math
from ghmm import *

# ASCII character
chars = list(string.printable)
# Create the HMM Matrix
PossibleObservation = IntegerRange(1, len(chars))

def createMatrix(numRows, numColumn):
    value =  1 / float(numRows)
    matrix = [value] * numRows
    if numColumn > 1:
        for i in range(numRows):
            matrix[i] = [value] * numColumn
    return matrix

def initializeHMM():
    TransitionMatrix = createMatrix(len(chars)-1, len(chars)-1)
    EmissionMatrix = createMatrix(len(chars)-1, len(chars)-1)
    InitialProbabilities = createMatrix(len(chars)-1, 1)

    m = HMMFromMatrices(PossibleObservation,
                        DiscreteDistribution(PossibleObservation),
                        TransitionMatrix,
                        EmissionMatrix,
                        InitialProbabilities)

    return m

def textToObs(tweet):
    obs = list(filter(lambda x: x in chars, tweet))
    for i in range(0, len(obs)):
        obs[i] = chars.index(obs[i])
    return obs

def trainHMM(hmm, trainingSet):
    for line in trainingSet:
        obs = EmissionSequence(PossibleObservation, textToObs(line))
        #ghmmwrapper.EPS_ITER_BW = 0
        hmm.baumWelch(obs)
    return hmm


hmm = initializeHMM()
print(hmm)
trainingSet = open("NASA_tweets.csv", 'r')
trainHMM(hmm, trainingSet)
print(hmm)
