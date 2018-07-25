import string
import VocabularyExtractor
import math
from ghmm import *

printable = list(string.printable)
alphabet = list(VocabularyExtractor.alphabet)

def check(tweet, hmm, obs_states, voc):
    new_tweet = ""
    for word in str(tweet).split(" "):
        word = word + " "
        if not(word in voc):
            chars = list(word)
            obs = [printable.index(c)+1 for c in chars]
            obs_seq = EmissionSequence(obs_states, obs)
            [states, prob] = hmm.viterbi(obs_seq)
            new_chars = [alphabet[o-1] for o in states]
            new_word = ''.join(new_chars)
            new_tweet = new_tweet + " " + new_word

            print word + " -> " + new_word + " with prob: " + str(math.exp(prob)) + "  states: " + str(states)
        else:
            new_tweet = new_tweet + " " + word
    return new_tweet
