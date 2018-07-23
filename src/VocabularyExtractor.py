#!/usr/bin/python
import re
import string

def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in set(string.ascii_letters + string.digits + ' '), line)
    return line


def getVocabulary(file):
    voc = []
    for line in file:
        line = parse(line)
        voc.extend(str(line).split(" "))
    voc = list(set(voc))
    print [(i, voc[i]) for i in range(0, len(voc))]
    return voc


fileName = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/small_NASA.txt"
tweet_file = open(fileName, 'r')
getVocabulary(tweet_file)
