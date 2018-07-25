import TrainingFileCreator
import VocabularyExtractor
import TweetChecker
import string
from ghmm import *

alphabet = list(VocabularyExtractor.alphabet)
printable = list(string.printable)


def get_initial_probabilities(voc):
    vector = [1] * len(alphabet)

    for word in voc:
        index = alphabet.index(word[0])
        vector[index] = vector[index] + 1
    vector = [float(i) / sum(vector) for i in vector]
    return vector

def get_transition_matrix(voc):
    matrix = [1] * len(alphabet)
    for i in range(0, len(alphabet)):
        matrix[i] = [1] * len(alphabet)

    for word in voc:
        for i in range(1, len(word)):
            raw = alphabet.index(word[i - 1])
            col = alphabet.index(word[i])
            matrix[raw][col] = matrix[raw][col] + 1

    for i in range(0, len(matrix)):
        matrix[i] = [float(j) / sum(matrix[i]) for j in matrix[i]]
    return matrix

def parseObservation(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in set(string.printable), line)
    return line

def get_emission_matrix(training_file_name):

    matrix = [1] * len(alphabet)
    for i in range(0, len(alphabet)):
        matrix[i] = [1] * len(printable)

    training = open(training_file_name)
    for correct_tweet in training:
        correct_tweet = TrainingFileCreator.parse(correct_tweet)
        misspelled_tweet = parseObservation(training.next())

        for i in range(0, len(correct_tweet)):
            raw = alphabet.index(correct_tweet[i])
            col = printable.index(misspelled_tweet[i])
            matrix[raw][col] = matrix[raw][col] + 1

    training.close()

    for i in range(0, len(matrix)):
        matrix[i] = [float(j) / sum(matrix[i]) for j in matrix[i]]
    return matrix


def print_stuff():
    print(vocabulary)
    t = get_transition_matrix(vocabulary)
    print "lenght transition: " + str(len(t))
    for i in range(0, len(t[0])):
        print str(alphabet[i]) + " -> " + str(t[i])
    print("\n\n\n\n")
    o = get_emission_matrix(trainingFileName)
    print "lenght emission: " + str(len(o[0]))
    for i in range(0, len(o)):
        print str(alphabet[i]) + " -> " + str(o[i])
    print("\n\n\n\n")
    print get_initial_probabilities(vocabulary)


if __name__ == '__main__':
    file_name = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/DownloadedTweet.txt"
    tweet_file = open(file_name, 'r')
    trainingFileName = TrainingFileCreator.createTrainingFile(tweet_file, 0.05)
    tweet_file = open(file_name, 'r')
    vocabulary = VocabularyExtractor.getVocabulary(tweet_file)

    #print_stuff()
    print alphabet
    print [(i, alphabet[i]) for i in range(0, len(alphabet))]

    obs_states = IntegerRange(1, len(printable)+1)  # Range of the observation.
    # N.B. the upper limit is not part of a range.
    A = get_transition_matrix(vocabulary)
    B = get_emission_matrix(trainingFileName)
    pi = get_initial_probabilities(vocabulary)
    m = HMMFromMatrices(obs_states, DiscreteDistribution(obs_states), A, B, pi)


    #test = "The Justice 0epartment is apEe4liYg the approval"
    test = "ment"

    print TweetChecker.check(test, m, obs_states, vocabulary)



