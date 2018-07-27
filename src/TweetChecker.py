import VocabularyExtractor
import GlobalVar
from ghmm import *

printable = GlobalVar.observable
alphabet = list(GlobalVar.alphabet)


def one_try_check(tweet, model, obs_states, voc):
    new_tweet = ""
    for word in str(tweet).split(" "):
        word = word + " "
        if not(word in voc):
            chars = list(word)
            obs = [printable.index(c)+1 for c in chars]
            obs_seq = EmissionSequence(obs_states, obs)
            [states, prob] = model.viterbi(obs_seq)
            new_chars = [alphabet[o] for o in states]
            new_word = ''.join(new_chars)
            new_tweet = new_tweet + " " + new_word

            print word + " " + str(obs) + " -> " \
                  + new_word + " " + str(states) \
                  + " | with prob: " + str(math.exp(prob))
        else:
            new_tweet = new_tweet + " " + word
    return new_tweet


def dull_check(tweet, model, obs_states, voc):
    new_tweet = ""
    for word in str(tweet).split(" "):
        word = word + " "
        count = 0
        while not(word in voc) and count < 1:

            old_word = word

            chars = list(word)
            obs = [printable.index(c)+1 for c in chars]
            obs_seq = EmissionSequence(obs_states, obs)
            [states, prob] = model.viterbi(obs_seq)
            new_chars = [alphabet[o] for o in states]
            word = ''.join(new_chars)

            if(word == old_word):
                count = count + 1
            else:
                count = 0

            print old_word + " " + str(obs) + " -> " \
                  + word + " " + str(states) \
                  + " | with prob: " + str(math.exp(prob))

        new_tweet = new_tweet + word

    return new_tweet
