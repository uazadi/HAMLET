#!/usr/bin/python
import re
import GlobalVar

alphabet = GlobalVar.alphabet

def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in alphabet, line)
    return line

def getVocabulary(tr_file, word_file):
    voc = []
    for line in tr_file:
        line = parse(line)
        words = [word + " " for word in str(line).split(" ")]
        voc.extend(words)
    voc = list(set(voc))

    for line in word_file:
        voc.insert(len(voc), line.replace("\n", " "))

    try:
        voc.remove('')
    except ValueError:
        pass


    return voc

if __name__ == '__main__':
    fileName = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/small_NASA.txt"
    voc_file_name = "/home/umberto/Documents/HMMTweetChecker/src/Vocabulary.txt"
    tweet_file = open(fileName, 'r')
    voc_file = open(voc_file_name, 'r')
    print getVocabulary(tweet_file, voc_file)
