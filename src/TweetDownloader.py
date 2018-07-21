import tweepy  # https://github.com/tweepy/tweepy
import csv

# Twitter API credentials
consumer_key = "wqTk5HoL0nlLQpXcSxzxTvyGm"
consumer_secret = "REybzEJC1bj5ceAX1RbmOveOQrtbxX2bXligErwhwZ0WcfzGCG"
access_key = "2816330308-kpkwWHhw4ARGPh9olP21hRtvXraEzzivDPp1qVs"
access_secret = "nEgSSbrodGMFwF2feHXRGrvwq5beStPVfCgBqsvUKD6R1"


def get_tweets(screen_name, num_of_tweet):

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(alltweets) < num_of_tweet and len(new_tweets) > 0:
        #print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
        api.user_timeline()

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "\t %s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv	| you can comment out data you don't need
    outtweets = []
    for tweet in alltweets:
        text = str(tweet.full_text.encode("UTF-8"))
        if not tweet.retweeted:
            if not ((text[0] == 'R') and (text[1] == 'T')):
                text = text.replace('"', '')
                text = text.replace('\n', '')
                outtweets.insert(len(outtweets), text)

    # write the csv
    with open('training_sets/%s_tweets.txt' % screen_name, 'wb') as f:
        for string in outtweets:
            f.write(string + "\n")

    return "training_sets/" + screen_name + "_tweets.txt"


if __name__ == '__main__':

    print "Downloading BarackObama tweet...."
    file1 = get_tweets("BarackObama", 2000)

    print "Downloading NASA tweet...."
    file2 = get_tweets("NASA", 2000)

    print "Downloading CNN tweet...."
    file3 = get_tweets("CNN", 2000)

    filenames = [file1, file2, file3]
    with open('training_sets/TrainingSet.txt', 'wb') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())
