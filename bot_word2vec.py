import gensim
import logging
import os.path
import csv
import tweepy, time
from credentials import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

def load_memetags(fname):
    # Returns a dictionary of filename: [tags]
    memetags = {}
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name = row[0]
            tags = [t for t in row[1:] if t in model.wv.vocab]
            memetags[name] = tags
    return memetags

def get_distance(sentence, tags, mode='max'):
    # Returns distance between a sentence and a list of tags
    if mode == 'max':
        max_dist = -1
        for word in sentence:
            if word in model.wv.vocab:
                for tag in tags:
                    dist = model.wv.similarity(word, tag)
                    if dist > max_dist:
                        max_dist = dist
        return max_dist
    elif mode == 'avg':
        avg_dist = 0
        for word in sentence:
            if word in model.wv.vocab:
                for tag in tags:
                    avg_dist += model.wv.similarity(word, tag)
        return avg_dist/(len(sentence)*len(tags))

def get_closest_meme(sentence, memes):
    # Returns the name of the meme whose tags have closest distance to the sentence
    max_meme = ''
    max_dist = -1
    for meme in memes.keys():
        dist = get_distance(sentence, memes[meme])
        if dist > max_dist:
            max_dist = dist
            max_meme = meme
    return max_meme

def get_tokens(tweet):
    # Removes punctation, lowers, and splits tweet
    text = re.sub(r'[^\w\s]','',tweet)
    return text.lower().split()

model = gensim.models.Word2Vec.load('data/funny.model')

memetags_positive = load_memetags('images/positive/postive.csv')
memetags_neutral = load_memetags('images/neutral/neutral.csv')
memetags_negative = load_memetags('images/negative/sad.csv')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
sid = SentimentIntensityAnalyzer()

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id)
        print(status.text)
        print(status.user.screen_name)

        ss = sid.polarity_scores(status.text)
        tokens = get_tokens(status.text)

        if ss['compound'] < -0.1:
            meme = 'images/negative/' + get_closest_meme(tokens, memetags_negative)
            new_status = "@{0} I am sorry you're sad :( Here's a meme to cheer you up, hopefully".format(status.user.screen_name, ss['compound'])
        elif ss['compound'] < 0.1:
            meme = 'images/neutral/' + get_closest_meme(tokens, memetags_neutral)
            new_status = "@{0} You seem to be chilling, here's a meme! ".format(status.user.screen_name, ss['compound'])
        else:
            meme = 'images/positive/' + get_closest_meme(tokens, memetags_positive)
            new_status = "@{0} Glad you're happy, enjoy this meme :D".format(status.user.screen_name, ss['compound'])

        try:
            api.update_with_media(meme, status=new_status, in_reply_to_status_id=status.id)
            print("Tweeting!")
        except err:
            print(err)

# Create stream listener and track name of memebot 
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@comp440cdk'])
