import TweetDownloader
import HMMTrainer
import TrainingFileCreator
import random

print "Downloading BarackObama tweet...."
file1 = TweetDownloader.get_tweets("BarackObama", 5000)

print "Downloading NASA tweet...."
file2 = TweetDownloader.get_tweets("NASA", 5000)

print "Downloading CNN tweet...."
file3 = TweetDownloader.get_tweets("CNN", 5000)

filenames = [file1, file2, file3]
with open('training_sets/DownloadedTweet.txt', 'wb') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

file_name = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/DownloadedTweet.txt"
voc_name ="/home/umberto/Documents/HMMTweetChecker/src/vocabularies/Vocabulary.txt"

tweet_file = open(file_name, 'r')
trainandtest_file_name = TrainingFileCreator.createTrainingFile(tweet_file, 0.2)

size = 0
with open(trainandtest_file_name) as f:
    size=len([0 for _ in f])

perc_of_training = 0.8
num_of_lines_for_training = int(size * perc_of_training)
even_range = [x for x in range(0, size) if x % 2 != 0]
indexes_for_training = random.sample(even_range, num_of_lines_for_training)

trainandtest_file = open(trainandtest_file_name, 'r')
training_file = open("TrainingSet.txt", 'wb')
testing_file = open("TestingSet.txt", 'wb')

with open(trainandtest_file_name, 'r') as tandt:
    line_index = 0
    for line in tandt:
        next_line = tandt.next()
        if line_index in indexes_for_training:
            training_file.write(line)
            training_file.write(next_line)
        else:
            testing_file.write(line)
        line_index = line_index + 1




model = HMMTrainer.train_hmm(file_name, "TrainingSet.txt", voc_name)
model.save_hmm(None)

