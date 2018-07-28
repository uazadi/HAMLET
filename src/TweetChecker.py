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
            for c in chars:
                chars.insert(len(chars.index(c)+1), " ")
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


def __try_simple_scan(model, obs_states, word, voc):
    count = 0
    while not (word in voc) and count < 1:

        old_word = word

        chars = list(word)
        obs = [printable.index(c) + 1 for c in chars]
        obs_seq = EmissionSequence(obs_states, obs)
        [states, prob] = model.hmm.viterbi(obs_seq)
        new_chars = [alphabet[o] for o in states]
        word = ''.join(new_chars)

        if word == old_word:
            count = count + 1
        else:
            count = 0

        print old_word + " " + str(obs) + " -> " \
              + word + " " + str(states) \
              + " | with prob: " + str(math.exp(prob))

    return word


def __try_missing_letter(model, obs_states, word, voc):
    possible_words = []
    chars = list(word)
    count = 0
    i = 0

    #N.B not(<empty_set>) = true
    while not(set(possible_words).intersection(set(voc))) and count < 1 and i < len(word)+1:

        spaced_chars = chars[:]
        #letter = alphabet.index(spaced_chars[i-1])
                        #Indice del meno probabile simbolo che segue spaced_chars[i-1]
        #char = alphabet[model.transition_matrix[letter].index(min(model.transition_matrix[letter]))]
        #spaced_chars.insert(i, char)
        spaced_chars.insert(i, "_")
        i = i + 1

        possible_words.insert(
            len(possible_words),
            __try_simple_scan(model, obs_states, ''.join(spaced_chars), voc)
        )

    if bool(set(possible_words).intersection(set(voc))):
        possible_words = set(possible_words).intersection(set(voc))

    return list(possible_words)


def dull_check(tweet, model, obs_states, voc):
    new_tweet = ""

    list_word = str(tweet).split(" ")

    for word in list_word:
        word = word + " "

        first_correction = word
        if(not(word in voc)):
            first_correction = __try_simple_scan(model, obs_states, word, voc)

        second_correction = first_correction
        if (not(first_correction in voc)):
            second_correction = __try_missing_letter(model, obs_states, word, voc)
            second_correction = second_correction + __try_missing_letter(model, obs_states, first_correction, voc)
            second_correction.insert(0, first_correction)

        new_tweet = new_tweet + str(second_correction)

    return new_tweet




def sentense_check(tweet, model, obs_states):
    text = str(tweet).replace(" ", "")

    obs = [printable.index(c) + 1 for c in text]
    obs_seq = EmissionSequence(obs_states, obs)
    [states, prob] = model.hmm.viterbi(obs_seq)
    new_chars = [alphabet[o] for o in states]
    new_tweet = ''.join(new_chars)


    return new_tweet