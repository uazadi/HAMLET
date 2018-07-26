#/usr/bin/python
import string
from hmmlearn import hmm
import numpy as np
from sklearn.externals import joblib


model = joblib.load("Saved_HMM.pkl")

def obs_to_text(obs, voc):
    #text = list(filter(lambda x: x in voc, tweet))
    text = ""
    for i in obs:
        text = text + " " + voc[i]
    return text

def text_to_obs(tweet, voc):
    obs = list(filter(lambda x: x in voc, tweet))
    print obs
    #obs = tweet.split(" ")
    for i in range(0, len(obs)):
        obs[i] = [voc.index(obs[i])]
    return obs


def getVocabulary(file):
    text = ""
    for line in file:
        text = text + line
    voc = [char for char in text]
    voc = list(set(voc))

    print [(i, voc[i]) for i in range(0, len(voc))]

    return voc

def getVocabulary2(file):
    voc = []
    for line in file:
        voc.extend(str(line).split(" "))

    voc = list(set(voc))

    print [(i, voc[i]) for i in range(0, len(voc))]

    return voc


# Load the training file and extract the vocubulary
fileName = "training_sets/small_NASA.txt"
trainingFile = open(fileName, 'r')

print("Creating the vocabulary...")
#chars = list(string.ascii_lowercase + string.ascii_uppercase + " " + "0123456789")
chars = getVocabulary(trainingFile)
#chars = list(string.ascii_lowercase + string.ascii_uppercase)
X = text_to_obs("when the very first humans stepped foot on the Moon", chars)
print X

logprob, state_sequence = model.decode(X, algorithm="viterbi")
logprob = round(np.exp(logprob), 5)
print(logprob)
print(state_sequence)
print(obs_to_text(state_sequence, chars))
