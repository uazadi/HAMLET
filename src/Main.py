import TweetDownloader
import HMMTrainer
import TrainingFileCreator
import TweetChecker
import numpy
import random
import os
from alignment.sequence import Sequence
from alignment.vocabulary import Vocabulary
from alignment.sequencealigner import SimpleScoring, GlobalSequenceAligner

path = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/"
file_name = path + "TrainingTweet.txt"
voc_name ="/home/umberto/Documents/HMMTweetChecker/src/vocabularies/Vocabulary.txt"


def download_tweet(training_tweet, testing_tweet):
    lines = read_tweets(training_tweet, 5000)
    shortest_source = min(lines, key=len)
    select_trainig_tweet(lines, shortest_source, 51)
    select_testing_tweet(lines, shortest_source, 51, testing_tweet)


def select_testing_tweet(lines, shortest_source, num_for_testing, testing_tweet):
    testing_only_lines = read_tweets(testing_tweet, 200)
    testing_shortest_source = min(testing_only_lines, key=len)
    with open('training_sets/TestingTweet.txt', 'wb') as outfile:
        for i in range(len(shortest_source) - num_for_testing, len(shortest_source)):
            for j in range(0, len(lines)):
                outfile.write(lines[j][i] + "\n")
        for i in range(0, len(testing_shortest_source)):
            for j in range(0, len(testing_only_lines)):
                outfile.write(testing_only_lines[j][i] + "\n")


def read_tweets(training_tweet, num_of_tweets):
    filenames = []
    for name in training_tweet:
        print "Downloading " + name + " tweets.."
        file = TweetDownloader.get_tweets(name, num_of_tweets)
        filenames.insert(len(filenames), file)
    lines = []
    for fname in filenames:
        with open(fname) as infile:
            lines.insert(len(lines), infile.read().split("\n"))
    return lines


def select_trainig_tweet(lines, shortest_source, num_for_testing):
    with open('training_sets/TrainingTweet.txt', 'wb') as outfile:
        for i in range(0, len(shortest_source) - num_for_testing):
            for j in range(0, len(lines)):
                outfile.write(lines[j][i] + "\n")


def create_mispell_file(file_name, perc_of_error, misp_file_name, testing):
    tweet_file = open(file_name, 'r')
    return TrainingFileCreator.createTrainingFile(tweet_file, perc_of_error, misp_file_name, testing)


def divide_testing_and_verify(file_name):
    file_name = open(file_name, 'r')

def train(training_set):
    model = HMMTrainer.train_hmm(file_name, training_set, voc_name)
    return model

def test(model, testing_set_name, verify_test_file_name):

    corrected_tweets = []
    with open(testing_set_name, 'r') as test:
        i = 1
        wrong = test.read().splitlines()
        for line in wrong:
            line = line.replace("\n", "")

            print "[" + str(i) + "/" + str(len(wrong)) + "] Checking:\n\t " + line
            i = i + 1

            corrected_tweet = TweetChecker.dull_check(line, model, model.obs_states, model.vocabulary)
            corrected_tweets.insert(len(corrected_tweets), corrected_tweet)

    i=1
    letters_similarity = [] # type: List[float]
    word_sim = [] # type: List[float]
    wrong_letters_similarity = [] # type: List[float]
    wrong_sim = []  # type: List[float]

    with open(verify_test_file_name, 'r') as verify:
        lines = verify.read().splitlines()
        print zip(lines, corrected_tweets)
        for line, ctweet in zip(lines, corrected_tweets):
            line = line.replace("\n", "")

            while (ctweet[len(ctweet) - 1] == " "):
                ctweet = ctweet[0: len(ctweet) - 1]

            print "\n\n[" + str(i) + "/" + str(len(lines)) \
                  + "] Verifying:" \
                  + "\nwrong:\t\t " + wrong[i-1]
            i = i + 1

            # Allignment between corrected tweet and the correct word
            letters_similarity.insert(len(letters_similarity), align_char(ctweet, line))
            word_sim.insert(len(word_sim), align_word(ctweet, line))


            # Allignment between wrong tweet and the correct word
            wrong_sim.insert(len(wrong_sim), align_word(wrong[i-1], line))
            wrong_letters_similarity.insert(len(wrong_letters_similarity), align_char(wrong[i-1], line))


    mean_letters_similarity = sum(letters_similarity)/len(letters_similarity)
    mean_word_sim = sum(word_sim)/len(word_sim)
    mean_wrong_letters_similarity = sum(wrong_letters_similarity)/len(wrong_letters_similarity)
    mean_wrong_sim = sum(wrong_sim)/len(wrong_sim)

    return letters_similarity, \
           word_sim, \
           mean_letters_similarity, \
           mean_word_sim, \
           wrong_letters_similarity, \
           wrong_sim, \
           mean_wrong_letters_similarity, \
           mean_wrong_sim

def new_test(model, test_file_name, test_file_length):
    test_file = open(test_file_name)
    i = 0
    list_ccci = []
    list_ccwi = []
    list_mcci = []
    list_mcwi = []

    for line in test_file:
        correct_line = line.replace("\n", "")
        mispelled_line = test_file.next().replace("\n", "")
        i = i + 1
        print "[" + str(i) + "/" + str(test_file_length) + "] Checking:\n\t " + mispelled_line
        corrected_tweet = TweetChecker.dull_check(mispelled_line, model, model.obs_states, model.vocabulary)

        #print "Calulating allignment ccci..."
        #cc_char_identity = align_char(corrected_tweet, correct_line)
        print "Calulating allignment ccwi..."
        cc_word_identity = align_word(corrected_tweet, correct_line)
        #print "Calulating allignment mcci..."
        #mc_char_identity = align_char(mispelled_line, correct_line)
        print "Calulating allignment mcwi..."
        mc_word_identity = align_word(mispelled_line, correct_line)

        #list_ccci.append(cc_char_identity)
        list_ccwi.append(cc_word_identity)
        #list_mcci.append(mc_char_identity)
        list_mcwi.append(mc_word_identity)

    #arr_ccci = numpy.array(list_ccci)
    #arr_ccwi = numpy.array(list_ccwi)
    #arr_mcci = numpy.array(list_mcci)
    #arr_mcwi = numpy.array(list_mcwi)

    #mean_ccci = numpy.mean(list_ccci)
    mean_ccwi = numpy.mean(list_ccwi)
    #mean_mcci = numpy.mean(list_mcci)
    mean_mcwi = numpy.mean(list_mcwi)

    #std_ccci = numpy.std(list_ccci)
    std_ccwi = numpy.std(list_ccwi)
    #std_mcci = numpy.std(list_mcci)
    std_mcwi = numpy.std(list_mcwi)

    results_string = ""

    #results_string += ("<CORRECTED TWEET, CORRECT TWEET> CHARS IDENTITY:\n")
    #results_string += str( list_ccci + "\n")
    #results_string += str("\n\MEAN: " + mean_ccci)
    #results_string += str("\n\STD: " + std_ccci)
    #results_string += "\n\n"

    results_string += ("<CORRECTED TWEET, CORRECT TWEET> WORDS IDENTITY:\n")
    results_string += str(list_ccwi) + "\n"
    results_string += "\nMEAN: " + str(mean_ccwi)
    results_string += "\nSTD: " + str(std_ccwi)
    results_string += "\n\n"

    #results_string += ("<MISPELLED TWEET, CORRECT TWEET> CHARS IDENTITY:\n")
    #results_string += str(list_mcci + "\n")
    #results_string += str("\n\MEAN: " + mean_mcci)
    #results_string += str("\n\STD: " + std_mcci)
    #results_string += "\n\n"

    results_string += ("<MISPELLED TWEET, CORRECT TWEET> WORDS IDENTITY:\n")
    results_string += str(list_mcwi) + "\n"
    results_string += "\nMEAN: " + str(mean_mcwi)
    results_string += "\nSTD: " + str(std_mcwi)
    results_string += "\n\n"

    return results_string

def align_word(ctweet, line):
    a = Sequence(ctweet.split())
    b = Sequence(line.split())
    v = Vocabulary()
    aEncoded = v.encodeSequence(a)
    bEncoded = v.encodeSequence(b)
    scoring = SimpleScoring(2, -10)
    aligner = GlobalSequenceAligner(scoring, -2)
    score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)
    alignment = v.decodeSequenceAlignment(encodeds[0])
    if str(alignment).replace(" ", "")[-1] == "-":
        perc_of_identity = (alignment.percentIdentity() * len(alignment)) / (len(alignment) + 1)
    else:
        perc_of_identity = alignment.percentIdentity()
    return perc_of_identity


def align_char(ctweet, line):
    a = Sequence(list(ctweet))
    b = Sequence(list(line))
    v = Vocabulary()
    aEncoded = v.encodeSequence(a)
    bEncoded = v.encodeSequence(b)
    scoring = SimpleScoring(2, -10)
    aligner = GlobalSequenceAligner(scoring, -2)
    score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)
    alignment = v.decodeSequenceAlignment(encodeds[0])
    return alignment.percentIdentity()


if __name__ == '__main__':
    #download_tweet(["BarackObama", "NASA", "CNN"], ["BillGates", "nytimes"])

    mispell_perc = [0.1, 0.2, 0.3, 0.4]
    path_names = []
    for i in [0.1, 0.2, 0.3, 0.4]:
        mispell_path = path + "misspell_perc_" + str(int(i * 100)) + "/"
        path_names.insert(len(path_names), mispell_path)
        if not os.path.exists(mispell_path):
            os.makedirs(mispell_path)
        create_mispell_file(path + "TrainingTweet.txt", i, mispell_path + "MisspelledTrainingTweet.txt", False)
        create_mispell_file(path + "TestingTweet.txt",  i, mispell_path + "MisspelledTestingTweet.txt", True)

    for path in path_names:
        models = []
        complete_file = open(path + "MisspelledTrainingTweet.txt").readlines()
        # tweet + mispelled_tweet = instance -> 1400 lines = 700 tweet
        for i in range(1400, 14001, 1400):
            name_training_set = path + "TrainingFile_" + str(i) + ".txt"
            sliced_file = open(name_training_set, 'w+')
            sliced_file.write(complete_file[0].replace("\n", ""))
            for line in complete_file[1:i]:
                sliced_file.write("\n" + line.replace("\n", ""))
            sliced_file.close()
            models.append(train(name_training_set))

        results_file = open(path + "Results.txt", 'w+')
        i = 1400
        for model in models:
            model.save_hmm(path)
            results_file.write("_____________RESULTS FOR MODEL TRAINED WITH " + str(i/2) + " TWEETS_____________\n\n")
            results_file.write(new_test(model, path + "/MisspelledTestingTweet.txt", 495))
            results_file.write("________________________________________________________________________________\n\n")




    #create_testing_file()
    #(training_file_name, testing_file_name, verify_test_file_name) = create_train_and_test_file()
    #model = train(training_file_name)

    #s_testing = path + "small_testing_set.txt"
    #s_verify = path + "small_verify_testset.txt"

    #letters_similarity, \
    #word_sim, \
    #mean_letters_similarity, \
    #mean_word_sim, \
    #wrong_letters_similarity, \
    #wrong_word_sim, \
    #mean_wrong_letters_similarity, \
    #mean_wrong_word_sim= test(model, s_testing, s_verify)

    #print "\n\nResults: "
    #print letters_similarity
    #print mean_letters_similarity
    #print "\n"
    #print wrong_letters_similarity
    #print mean_wrong_letters_similarity
    #print "\n"
    #print word_sim
    #print mean_word_sim
    #print "\n"
    #print wrong_word_sim
    #print mean_wrong_word_sim