#!/usr/bin/python
import re
import string

alphabet = set(string.ascii_letters + string.digits + ' ' + '#' + '@')

def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in alphabet, line)
    return line

def getVocabulary(file):
    voc = []
    for line in file:
        line = parse(line)
        words = [word + " " for word in str(line).split(" ")]
        voc.extend(words)
    voc = list(set(voc))

    try:
        voc.remove('')
    except ValueError:
        pass

    return voc

if __name__ == '__main__':
    fileName = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/small_NASA.txt"
    tweet_file = open(fileName, 'r')
    getVocabulary(tweet_file)
