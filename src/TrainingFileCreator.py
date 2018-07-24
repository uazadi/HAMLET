#!/usr/bin/python
import random
import string
import re
import os.path
import VocabularyExtractor

file_name = '/home/umberto/Documents/HMMTweetChecker/' \
           'src/training_sets/TrainingFile.txt'

def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in set(VocabularyExtractor.alphabet), line)
    return line


def introduceError(line, percentageOfError):
    new_line = ""
    num_of_char = int(len(line) * percentageOfError)
    index_to_change = random.sample(range(0, len(line)), num_of_char)

    for i in range(0, len(line)):
        if i in index_to_change:
            new_char = random.choice(string.ascii_letters + string.digits)
            new_line = new_line + new_char
        else:
            new_line = new_line + line[i]

    return new_line

def getTrainingFile():
    if os.path.isfile(file_name):
        return file_name
    return None

def createTrainingFile(tweetsFile, percentageOfError):

    with open(file_name, 'wb') as f:
        for line in tweetsFile:
            line = parse(line)
            f.write(line.replace("\n", "") + "\n")
            wrongLine = introduceError(line.replace("\n", ""), percentageOfError)
            f.write(wrongLine + "\n")

    return file_name


if __name__ == '__main__':
    fileName = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/small_NASA.txt"
    tweet_file = open(fileName, 'r')
    createTrainingFile(tweet_file, 0.1)
    tweet_file.close()
