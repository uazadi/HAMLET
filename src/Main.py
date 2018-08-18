import TweetDownloader
import HMMTrainer
import TrainingFileCreator
import TweetChecker
import numpy
import os

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

def train(training_set, max_identity_value):
    model = HMMTrainer.train_hmm(file_name, training_set, voc_name, max_identity_value)
    return model

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
        corrected_tweet = TweetChecker.dull_check(mispelled_line, model)

        print "Calulating allignment ccci..."
        cc_char_identity = align_char(corrected_tweet, correct_line)
        print "Calulating allignment ccwi..."
        cc_word_identity = count_correct_words(corrected_tweet, correct_line)
        print "Calulating allignment mcci..."
        mc_char_identity = align_char(mispelled_line, correct_line)
        print "Calulating allignment mcwi..."
        mc_word_identity = count_correct_words(mispelled_line, correct_line)

        list_ccci.append(cc_char_identity)
        list_ccwi.append(cc_word_identity)
        list_mcci.append(mc_char_identity)
        list_mcwi.append(mc_word_identity)

    mean_ccci = numpy.mean(list_ccci)
    mean_ccwi = numpy.mean(list_ccwi)
    mean_mcci = numpy.mean(list_mcci)
    mean_mcwi = numpy.mean(list_mcwi)

    first_not_account_index = 5

    accounts_mean_ccci = numpy.mean(list_ccci[:first_not_account_index])
    accounts_mean_ccwi = numpy.mean(list_ccwi[:first_not_account_index])
    accounts_mean_mcci = numpy.mean(list_mcci[:first_not_account_index])
    accounts_mean_mcwi = numpy.mean(list_mcwi[:first_not_account_index])

    others_mean_ccci = numpy.mean(list_ccci[first_not_account_index:])
    others_mean_ccwi = numpy.mean(list_ccwi[first_not_account_index:])
    others_mean_mcci = numpy.mean(list_mcci[first_not_account_index:])
    others_mean_mcwi = numpy.mean(list_mcwi[first_not_account_index:])

    std_ccci = numpy.std(list_ccci)
    std_ccwi = numpy.std(list_ccwi)
    std_mcci = numpy.std(list_mcci)
    std_mcwi = numpy.std(list_mcwi)

    results_string = ""

    results_string += "<CORRECTED TWEET, CORRECT TWEET> CHARS IDENTITY:\n"
    results_string += str(list_ccci) + "\n"
    results_string += "\nMEAN: " + str(mean_ccci)
    results_string += "\nSTD: " + str(std_ccci)
    results_string += "\nSAME ACCOUNTS MEAN: " + str(accounts_mean_ccci)
    results_string += "\nOTHER ACCOUNTS MEAN: " + str(others_mean_ccci)
    results_string += "\n\n"

    results_string += "<CORRECTED TWEET, CORRECT TWEET> CORRECT WORDS:\n"
    results_string += str(list_ccwi) + "\n"
    results_string += "\nMEAN: " + str(mean_ccwi)
    results_string += "\nSTD: " + str(std_ccwi)
    results_string += "\nSAME ACCOUNTS MEAN: " + str(accounts_mean_ccwi)
    results_string += "\nOTHER ACCOUNTS MEAN: " + str(others_mean_ccwi)
    results_string += "\n\n"

    results_string += "<MISPELLED TWEET, CORRECT TWEET> CHARS IDENTITY:\n"
    results_string += str(list_mcci) + "\n"
    results_string += "\nMEAN: " + str(mean_mcci)
    results_string += "\nSTD: " + str(std_mcci)
    results_string += "\nSAME ACCOUNTS MEAN: " + str(accounts_mean_mcci)
    results_string += "\nOTHER ACCOUNTS MEAN: " + str(others_mean_mcci)
    results_string += "\n\n"

    results_string += "<MISPELLED TWEET, CORRECT TWEET> CORRECT WORDS:\n"
    results_string += str(list_mcwi) + "\n"
    results_string += "\nMEAN: " + str(mean_mcwi)
    results_string += "\nSTD: " + str(std_mcwi)
    results_string += "\nSAME ACCOUNTS MEAN: " + str(accounts_mean_mcwi)
    results_string += "\nOTHER ACCOUNTS MEAN: " + str(others_mean_mcwi)
    results_string += "\n\n"

    results_string += ("GAIN:\n")
    results_string += "\nWORD MEAN: " + str(mean_ccwi) + " - " + str(mean_mcwi) + " = " + str(mean_ccwi - mean_mcwi)
    results_string += "\nWORD STD: " + str(std_ccwi) + " - " + str(std_mcwi) + " = " + str(std_ccwi - std_mcwi)
    results_string += "\nCHARS MEAN: " + str(mean_ccci) + " - " + str(mean_mcci) + " = " + str(mean_ccci - mean_mcci)
    results_string += "\nCHARS STD: " + str(std_ccci) + " - " + str(std_mcci) + " = " + str(std_ccci - std_mcci)
    results_string += "\n\n"

    return results_string


def count_correct_words(mtweet, ctweet):

    correct_word = 0

    mtweet = mtweet.split(" ")
    ctweet = ctweet.split(" ")

    for word in mtweet:
        if word in ctweet:
            correct_word += 1

    return correct_word / float(len(ctweet))

    #for i in ctweet.split(" "):
    #    for j in line.split(" "):
    #        if i == j:
    #            corrected_word

    #a = Sequence(ctweet.split())
    #b = Sequence(line.split())
    #v = Vocabulary()
    #aEncoded = v.encodeSequence(a)
    #bEncoded = v.encodeSequence(b)
    #scoring = SimpleScoring(2, -2)
    #aligner = GlobalSequenceAligner(scoring, -1)
    #score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)
    #alignment = v.decodeSequenceAlignment(encodeds[0])
    #print alignment
    #if str(alignment).replace(" ", "")[-1] == "-":
    #    perc_of_identity = (alignment.percentIdentity() * len(alignment)) / (len(alignment) + 1)
    #else:
    #    perc_of_identity = alignment.percentIdentity()
    #return corrected_word/float(len(line))


def align_char(mtweet, line):
    mtweet = mtweet.replace(" ", "")
    line = line.replace(" ", "")

    i = 0
    matched_chars = 0

    while i < len(mtweet) and i < len(line):
        if mtweet[i] == line[i]:
            matched_chars += 1
        i += 1

    return (matched_chars*2)/float(len(mtweet) + len(line))

    #a = Sequence(list(ctweet))
    #b = Sequence(list(line))
    #v = Vocabulary()
    #aEncoded = v.encodeSequence(a)
    #bEncoded = v.encodeSequence(b)
    #scoring = SimpleScoring(2, -10)
    #aligner = GlobalSequenceAligner(scoring, -2)
    #score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)
    #alignment = v.decodeSequenceAlignment(encodeds[0])
    #return alignment.percentIdentity()


if __name__ == '__main__':
    #download_tweet(["BarackObama", "NASA", "CNN"], ["BillGates", "nytimes"])

    misspell_perc = [0.1, 0.2, 0.3]
    max_values =  [0.5, 0.75, 0]
    path_names = []
    for i in misspell_perc:
        misspell_path = path + "misspell_perc_" + str(int(i * 100)) + "/"
        path_names.insert(len(path_names), misspell_path)
        if not os.path.exists(misspell_path):
            os.makedirs(misspell_path)
        create_mispell_file(path + "TrainingTweet.txt", i, misspell_path + "MisspelledTrainingTweet.txt", False)
        create_mispell_file(path + "TestingTweet.txt",  i, misspell_path + "MisspelledTestingTweet.txt", True)
    create_mispell_file(path + "TestingTweet.txt", 0.05, path + "MisspelledTestingTweet.txt", True)


    # circa 30 (codice sopra + primo for innestato del codice che segue)

    num_tweet = 2800

    models = []
    for misspell_path in path_names:
        complete_file = open(misspell_path + "MisspelledTrainingTweet.txt").readlines()
        # tweet + mispelled_tweet = instance -> 1400 lines = 700 tweet
        for i in range(num_tweet, 14001, num_tweet):
            for mv in max_values:
                name_training_set = misspell_path + "TrainingFile_" + str(i) + "_" + str(mv) + ".txt"
                sliced_file = open(name_training_set, 'w+')
                sliced_file.write(complete_file[0].replace("\n", ""))
                for line in complete_file[1:i]:
                    sliced_file.write("\n" + line.replace("\n", ""))
                sliced_file.close()
                models.append(train(name_training_set, mv))
                print "===============================" + str(len(models))

        with open(misspell_path + "Results.txt", 'w+') as results_file:
            i = num_tweet
            j = 0
            print ">>>>>>>>>>>>>>>>> " + str(len(models))
            for model in models:
                hmm_folder = misspell_path + "HMM_" + str(i) + "_" + str(max_values[j%3]) + "/"
                if not os.path.exists(hmm_folder):
                    os.makedirs(hmm_folder)
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(hmm_folder)
                model.save_hmm(hmm_folder)
                results_file.write("_____________RESULTS FOR MODEL TRAINED WITH " + str(i/2) + " TWEETS_____________\n\n")
                results_file.write(new_test(model, misspell_path + "/MisspelledTestingTweet.txt", 10))
                results_file.write("--------------------------------------------------------------------------------\n\n")
                results_file.write(new_test(model, path + "/MisspelledTestingTweet.txt", 10))
                results_file.write("________________________________________________________________________________\n\n")
                j = j + 1
                if j%3 == 2:
                    i = i + num_tweet






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