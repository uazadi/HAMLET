import VocabularyExtractor
import GlobalVar
from ghmm import *


printable = GlobalVar.observable
alphabet = list(GlobalVar.alphabet)


def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in set(GlobalVar.alphabet), line)
    return line

def one_try_check(tweet, model):
    new_tweet = ""
    tweet = parse(tweet)
    for word in str(tweet).split(" "):
        word = word + " "
        if not(word in model.vocabulary):
            chars = list(word)
            #for c in chars:
            #    chars.insert(len(chars.index(c)+1), " ")
            obs = [printable.index(c)+1 for c in chars]
            obs_seq = EmissionSequence(model.obs_states, obs)
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


def __try_simple_scan(model, word):
    count = 0
    while not (word in model.vocabulary) and count < 1:

        old_word = word

        chars = list(word)
        obs = [printable.index(c) + 1 for c in chars]
        obs_seq = EmissionSequence(model.obs_states, obs)
        [states, prob] = model.hmm.viterbi(obs_seq)
        new_chars = [alphabet[o] for o in states]
        word = ''.join(new_chars)

        if word == old_word:
            count = count + 1
        else:
            count = 0

        #print old_word + " " + str(obs) + " -> " \
        #      + word + " " + str(states) \
        #      + " | with prob: " + str(math.exp(prob))

    return word


def __try_missing_letter(model, word):
    possible_words = []
    chars = list(word)
    count = 0
    i = 0

    #N.B not(<empty_set>) = true
    while not(set(possible_words).intersection(set(model.vocabulary))) and count < 1 and i < len(word)+1:

        spaced_chars = chars[:]
        #letter = alphabet.index(spaced_chars[i-1])
                        #Indice del meno probabile simbolo che segue spaced_chars[i-1]
        #char = alphabet[model.transition_matrix[letter].index(min(model.transition_matrix[letter]))]
        #spaced_chars.insert(i, char)
        spaced_chars.insert(i, "_")
        i = i + 1

        possible_words.insert(
            len(possible_words),
            __try_simple_scan(model, ''.join(spaced_chars))
        )

    if bool(set(possible_words).intersection(set(model.vocabulary))):
        possible_words = set(possible_words).intersection(set(model.vocabulary))

    possible_word = max(set(possible_words), key=list(possible_words).count)

    return possible_word


def dull_check(tweet, model):
    new_tweet = ""
    tweet = parse(tweet)
    list_word = str(tweet).split(" ")
    for word in list_word:
        word = word + " "

        first_correction = word
        if not(word in model.vocabulary):
            first_correction = __try_simple_scan(model, word)
            if first_correction[0:len(first_correction)-1].count(" ") > 0:
                words = first_correction[0:len(first_correction)-1]
                index = list_word.index(word[0:len(word)-1])
                #list_word.remove(word[0:len(word)-1])
                offset = 1
                for w in words.split(" "):
                    list_word.insert((index + offset), w)
                    offset = offset + 1
                continue



        second_correction = first_correction
        if not(first_correction in model.vocabulary):
            second_correction = __try_missing_letter(model, word)

        third_correction = second_correction
        if not (second_correction in model.vocabulary):
            third_correction = __try_missing_letter(model, first_correction)


        if not(third_correction in model.vocabulary):
            new_tweet = new_tweet + first_correction
        else:
            new_tweet = new_tweet + second_correction

    return new_tweet




def sentense_check(tweet, model):
    tweet = parse(tweet)
    #text = str(tweet).replace(" ", "")
    text = parse(tweet)

    obs = [printable.index(c) + 1 for c in text]
    obs_seq = EmissionSequence(model.obs_states, obs)
    [states, prob] = model.hmm.viterbi(obs_seq)
    new_chars = [alphabet[o] for o in states]
    new_tweet = ''.join(new_chars)


    return new_tweet