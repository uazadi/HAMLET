import TweetDownloader
import HMMTrainer
import TrainingFileCreator
import TweetChecker
import random
import os
from alignment.sequence import Sequence
from alignment.vocabulary import Vocabulary
from alignment.sequencealigner import SimpleScoring, GlobalSequenceAligner

path = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/"
file_name = path + "DownloadedTweet.txt"
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


def create_mispell_file(file_name, perc_of_error, misp_file_name):
    tweet_file = open(file_name, 'r')
    return TrainingFileCreator.createTrainingFile(tweet_file, perc_of_error, misp_file_name)

def divide_testing_and_verify(file_name):
    file_name = open(file_name, 'r')



def create_train_and_test_file():
    tweet_file = open(file_name, 'r')
    trainandtest_file_name = TrainingFileCreator.createTrainingFile(tweet_file, 0.2)

    #size = 0
    with open(trainandtest_file_name) as f:
        size=len([0 for _ in f])

    perc_of_training = 0.8
    num_of_lines_for_training = int(size * perc_of_training)/2
    even_range = [x for x in range(0, size) if x % 2 != 0]
    indexes_for_training = random.sample(even_range, num_of_lines_for_training)

    training_file_name = path + "TrainingSet.txt"
    testing_file_name = path + "TestingSet.txt"
    verify_test_file_name = path + "VerifyTestSet.txt"

    trainandtest_file = open(trainandtest_file_name, 'r')
    training_file = open(training_file_name, 'wb')
    testing_file = open(testing_file_name, 'wb')
    verify_test_file = open(verify_test_file_name, 'wb')

    with open(trainandtest_file_name, 'r') as tandt:
        line_index = 0
        for line in tandt:
            next_line = tandt.next()
            if line_index in indexes_for_training:
                training_file.write(line)
                training_file.write(next_line)
            else:
                verify_test_file.write(line)
                testing_file.write(next_line)
            line_index = line_index + 1

    return training_file_name, testing_file_name, verify_test_file_name

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
    print "\n" + str(alignment)
    print 'Alignment score:', alignment.score
    if str(alignment).replace(" ", "")[-1] == "-":
        perc_of_identity = (alignment.percentIdentity() * len(alignment)) / (len(alignment) + 1)
        print 'Percent identity:', perc_of_identity
    else:
        perc_of_idetity = alignment.percentIdentity()
        print 'Percent identity:', alignment.percentIdentity()
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
    print alignment
    print 'Alignment score:', alignment.score
    print 'Percent identity:', alignment.percentIdentity()
    return alignment.percentIdentity()


if __name__ == '__main__':
    #download_tweet(["BarackObama", "NASA", "CNN"], ["BillGates", "nytimes"])

    mispell_perc = [0.1, 0.2, 0.3, 0.4]
    path_names = []
    for i in [0.1, 0.2, 0.3, 0.4]:
        mispell_path = path + "mispell_perc_" + str(int(i * 100)) + "/"
        path_names.insert(len(path_names), mispell_path)
        os.makedirs(mispell_path)
        create_mispell_file(path + "TrainingTweet.txt", i, mispell_path + "/MispelledTrainingTweet.txt")
        create_mispell_file(path + "TestingTweet.txt",  i, mispell_path + "/MispelledTestingTweet.txt")





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