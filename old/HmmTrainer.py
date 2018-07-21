#/usr/bin/python
import string
import numpy as np
from ghmm import *

# ASCII character
chars = list(string.printable)
# Create the HMM Matrix
PossibleObservation = IntegerRange(0, len(chars))
print(PossibleObservation)


def createMatrix(numRows, numColumn):
    value = (1 / float(numRows))
    matrix = [value] * numRows
    if numColumn > 1:
        for i in range(numRows):
            matrix[i] = [value] * numColumn
    return matrix

def initializeHMM():
    TransitionMatrix = createMatrix(len(chars), len(chars))
    EmissionMatrix = createMatrix(len(chars), len(chars))
    InitialProbabilities = createMatrix(len(chars), 1)
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
    count = 0
    obss = []
    for line in trainingSet:
        print(line)
        print(textToObs(line))
        obss.extend(textToObs(line))

    obs = EmissionSequence(PossibleObservation, obss)
    #ghmmwrapper.EPS_ITER_BW = 0
    hmm.baumWelch(obs)
    #if count >= 0:
        #break
    count = count + 1
    return hmm


hmm = initializeHMM()
print(hmm)
trainingSet = open("NASA_tweets.csv", 'r')
trainHMM(hmm, trainingSet)
print(hmm.write("/home/umberto/Desktop/output.txt"))
