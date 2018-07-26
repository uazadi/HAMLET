#!/usr/bin/python
import random
import math
import string
import re
import os.path
import VocabularyExtractor

file_name = '/home/umberto/Documents/HMMTweetChecker/' \
            'src/training_sets/TrainingFile.txt'

#printable_matrix = [
#                    list('!"*$%&/()=?^'),
#                    list("1234567890'|"),
#                    list('qwertyuiop[]'),
#                    list('QWERTYUIOP{}'),
#                    list('asdfghjkl@#+'),
#                    list('ASDFGHJKL;:*'),
#                    list('<zxcvbnm,.-@'),
#                    list('>ZXCVBNM;:_#'),
#                    list('            ')]

keyboard= {
    '1': {'y': 1, 'x': 1},
    '2': {'y': 1, 'x': 2},
    '3': {'y': 1, 'x': 3},
    '4': {'y': 1, 'x': 4},
    '5': {'y': 1, 'x': 5},
    '6': {'y': 1, 'x': 6},
    '7': {'y': 1, 'x': 7},
    '8': {'y': 1, 'x': 8},
    '9': {'y': 1, 'x': 9},
    '0': {'y': 1, 'x': 10},
    "'": {'y': 1, 'x': 11},
    'q': {'y': 2, 'x': 1},
    'w': {'y': 2, 'x': 2},
    'e': {'y': 2, 'x': 3},
    'r': {'y': 2, 'x': 4},
    't': {'y': 2, 'x': 5},
    'y': {'y': 2, 'x': 6},
    'u': {'y': 2, 'x': 7},
    'i': {'y': 2, 'x': 8},
    'o': {'y': 2, 'x': 9},
    'p': {'y': 2, 'x': 10},
    'a': {'y': 3, 'x': 1},
    's': {'y': 3, 'x': 2},
    'd': {'y': 3, 'x': 3},
    'f': {'y': 3, 'x': 4},
    'g': {'y': 3, 'x': 5},
    'h': {'y': 3, 'x': 6},
    'j': {'y': 3, 'x': 7},
    'k': {'y': 3, 'x': 8},
    'l': {'y': 3, 'x': 9},
    '@': {'y': 4, 'x': 10.5},
    '#': {'y': 3, 'x': 11.5},
    'z': {'y': 4, 'x': 1},
    'x': {'y': 4, 'x': 2},
    'c': {'y': 4, 'x': 3},
    'v': {'y': 4, 'x': 4},
    'b': {'y': 4, 'x': 5},
    'n': {'y': 4, 'x': 6},
    'm': {'y': 4, 'x': 7},
    'Q': {'y': 2.5, 'x': 1.5},
    'W': {'y': 2.5, 'x': 2.5},
    'E': {'y': 2.5, 'x': 3.5},
    'R': {'y': 2.5, 'x': 4.5},
    'T': {'y': 2.5, 'x': 5.5},
    'Y': {'y': 2.5, 'x': 6.5},
    'U': {'y': 2.5, 'x': 7.5},
    'I': {'y': 2.5, 'x': 8.5},
    'O': {'y': 2.5, 'x': 9.5},
    'P': {'y': 2.5, 'x': 10.5},
    'A': {'y': 3.5, 'x': 1.5},
    'S': {'y': 3.5, 'x': 2.5},
    'D': {'y': 3.5, 'x': 3.5},
    'F': {'y': 3.5, 'x': 4.5},
    'G': {'y': 3.5, 'x': 5.5},
    'H': {'y': 3.5, 'x': 6.5},
    'J': {'y': 3.5, 'x': 7.5},
    'K': {'y': 3.5, 'x': 8.5},
    'L': {'y': 3.5, 'x': 9.5},
    'Z': {'y': 4.5, 'x': 1.5},
    'X': {'y': 4.5, 'x': 2.5},
    'C': {'y': 4.5, 'x': 3.5},
    'V': {'y': 4.5, 'x': 4.5},
    'B': {'y': 4.5, 'x': 5.5},
    'N': {'y': 4.5, 'x': 6.5},
    'M': {'y': 4.5, 'x': 7.5},
    ' ': {'y': 5, 'x': 5}
}


def parse(line):
    line = re.sub('https?:[A-Za-z0-9/\.]+', '', line)
    line = filter(lambda x: x in set(VocabularyExtractor.alphabet), line)
    return line

def sampleChar():
    return random.choice(string.ascii_letters + string.digits)



def sampleQWERTY(char):
    num = 1
    prob = 0
    new_char = ''
    while(num > prob):
        new_char = random.choice(string.ascii_letters + string.digits)
        x1 = keyboard[char]['x']
        y1 = keyboard[char]['y']
        x2 = keyboard[new_char]['x']
        y2 = keyboard[new_char]['y']
        dist = ((x1-x2)**2) + ((y1 - y2)**2)
        print dist
        if(dist <= 1):
            break
        prob = 1/dist if dist != 0 else 1
        num = random.random()
    return new_char



def introduceError(line, percentageOfError):
    new_line = ""
    num_of_char = int(len(line) * percentageOfError)
    index_to_change = random.sample(range(0, len(line)), num_of_char)

    for i in range(0, len(line)):
        if i in index_to_change:
            new_char = sampleQWERTY(line[i])
            #new_char = sampleChar()
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
    pass
    #fileName = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/small_NASA.txt"
    #tweet_file = open(fileName, 'r')
    #createTrainingFile(tweet_file, 0.1)
    #tweet_file.close()
    #print sampleQWERTY('l')
