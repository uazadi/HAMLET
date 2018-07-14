import tweepy  # https://github.com/tweepy/tweepy
import csv

# Twitter API credentials
consumer_key = "wqTk5HoL0nlLQpXcSxzxTvyGm"
consumer_secret = "REybzEJC1bj5ceAX1RbmOveOQrtbxX2bXligErwhwZ0WcfzGCG"
access_key = "2816330308-kpkwWHhw4ARGPh9olP21hRtvXraEzzivDPp1qVs"
access_secret = "nEgSSbrodGMFwF2feHXRGrvwq5beStPVfCgBqsvUKD6R1"


def get_all_tweets(screen_name):

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
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
        api.user_timeline()

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv	| you can comment out data you don't need
    outtweets = []
    for tweet in alltweets:
        text = str(tweet.full_text.encode("ascii")).replace("\n", "[newline]")
        if not tweet.retweeted:
            if not ((text[0] == 'R') and (text[1] == 'T')):
                outtweets.append([text])

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(outtweets)


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("NASA")