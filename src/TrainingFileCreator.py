#!/usr/bin/python
import random
import string
import re

def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in set(string.printable), line)
    return line


def introduceError(line, percentageOfError):
    new_line = ""
    num_of_char = int(len(line) * percentageOfError)
    highest_index = len(line) - 1
    index_to_change = random.sample(range(0, highest_index), num_of_char)

    for i in range(0, len(line)-1):
        if i in index_to_change:
            new_char = random.choice(string.ascii_letters + string.digits)
            new_line = new_line + new_char
        else:
            new_line = new_line + line[i]

    return new_line


def getTrainingFile(tweetsFile, percentageOfError):
    with open('training_sets/TrainingFile.txt', 'wb') as f:
        for line in tweetsFile:
            line = parse(line)
            f.write(line.replace("\n", "") + "\n")
            wrongLine = introduceError(line.replace("\n", ""), percentageOfError)
            f.write(wrongLine + "\n")


fileName = "training_sets/small_NASA.txt"
tweet_file = open(fileName, 'r')
getTrainingFile(tweet_file, 0.1)
tweet_file.close()
