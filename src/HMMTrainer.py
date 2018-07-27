import TrainingFileCreator
import VocabularyExtractor
import TweetChecker
import CustomHMM as HMMFile
from CustomHMM import CustomHMM
import GlobalVar
import string
from ghmm import *

alphabet = list(GlobalVar.alphabet)
observable = GlobalVar.observable

class HMMTrainer:

    def __init__(self, tweets_file_name, voc_file_name):
        self.hmm = self.train_hmm(tweets_file_name, voc_file_name)

    def get_initial_probabilities(self, voc):
        vector = [1] * len(alphabet)

        for word in voc:
            index = alphabet.index(word[0])
            vector[index] = vector[index] + 1
        vector = [float(i) / sum(vector) for i in vector]
        return vector

    def get_transition_matrix(self, voc):
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

    def parseObservation(self, line):
        line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
        line = filter(lambda x: x in set(string.printable), line)
        return line


    def get_emission_matrix(self, training_file_name):

        matrix = [1] * len(alphabet)
        for i in range(0, len(alphabet)):
            matrix[i] = [1] * len(observable)

        training = open(training_file_name)
        for correct_tweet in training:
            correct_tweet = TrainingFileCreator.parse(correct_tweet)
            misspelled_tweet = self.parseObservation(training.next())

            for i in range(0, len(correct_tweet)):
                raw = alphabet.index(correct_tweet[i])
                col = observable.index(misspelled_tweet[i])
                matrix[raw][col] = matrix[raw][col] + 1

        training.close()

        for i in range(0, len(matrix)):
            den = sum(matrix[i])
            #if matrix[i][i] > den*0.5:
                #matrix[i][i] = den*0.5
            matrix[i] = [float(j) / den for j in matrix[i]]

        return matrix

    def train_hmm(self, tweets_file_name, voc_file_name):
        tweet_file = open(tweets_file_name, 'r')
        trainingFileName = TrainingFileCreator.createTrainingFile(tweet_file, 0.2)

        tweet_file = open(tweets_file_name, 'r')
        voc_file = open(voc_file_name, 'r')
        vocabulary = VocabularyExtractor.getVocabulary(tweet_file, voc_file)

        obs_states = IntegerRange(1, len(observable) + 1)
        transition_matrix = self.get_transition_matrix(vocabulary)
        emission_matrix = self.get_emission_matrix(trainingFileName)
        initial_probabilities = self.get_initial_probabilities(vocabulary)
        model = HMMFromMatrices(obs_states,
                                DiscreteDistribution(obs_states),
                                transition_matrix,
                                emission_matrix,
                                initial_probabilities)


        chmm = CustomHMM(
            model,
            transition_matrix,
            emission_matrix,
            initial_probabilities,
            obs_states,
            vocabulary)

        chmm.save_hmm(None)

        return chmm


if __name__ == '__main__':

    file_name = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/DownloadedTweet.txt"
    voc_name ="/home/umberto/Documents/HMMTweetChecker/src/vocabularies/Vocabulary.txt"

    print HMMTrainer(file_name, voc_name).hmm

    print HMMFile.load("/home/umberto/Documents/HMMTweetChecker/src/HMM/")



    # Test for completly random extraction
    test = "Authurities aoe inveNtmgating afteroan kCEzdetaVnee facing pos7ible deportation apparentky kBlledFhimself "

    # Test for qwerty sample
    test = "Hap0y ValDntGnes DaY @MiXhelKeObama You jAkeBSv3ryDdaY and eveGy place bet5er"

    #print TweetChecker.dull_check(test, m, obs_states, vocabulary)



