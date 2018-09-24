#!/usr/bin/python
import random
import string
import TweetChecker
import GlobalVar
import math

keyboard = GlobalVar.keyboard




def sampleChar():
    return random.choice(string.ascii_letters + string.digits)



def sampleQWERTY(char):
    num = 1
    prob = 0
    new_char = ''
    while(num > prob):
        new_char = random.choice(string.ascii_letters + string.digits + " " + "_")
        x1 = keyboard[char]['x']
        y1 = keyboard[char]['y']
        x2 = keyboard[new_char]['x']
        y2 = keyboard[new_char]['y']
        dist = math.sqrt(((x1-x2)**2) + ((y1 - y2)**2))
        #print dist
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


def createTrainingFile(tweetsFile, percentageOfError, file_name, without_underscore):

    with open(file_name, 'w+') as f:
        for line in tweetsFile:
            line = TweetChecker.parse(line)
            f.write(line.replace("\n", "") + "\n")
            wrongLine = introduceError(line.replace("\n", ""), percentageOfError)
            if without_underscore:
                wrongLine = wrongLine.replace("_", "")
            f.write(wrongLine + "\n")

    return file_name


if __name__ == '__main__':
    pass
    #fileName = "/home/umberto/Documents/HMMTweetChecker/src/training_sets/small_NASA.txt"
    #tweet_file = open(fileName, 'r')
    #createTrainingFile(tweet_file, 0.1)
    #tweet_file.close()
    #print sampleQWERTY('l')
