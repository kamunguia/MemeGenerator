import tweepy, time
from credentials import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from os import listdir
from os.path import isfile, join
import random

positive_folder='images/positive/'
neutral_folder='images/neutral/'
negative_folder='images/negative/'

positive_images = ['images/positive/' + f for f in listdir(positive_folder) if isfile(join(positive_folder, f))]
neutral_images = ['images/neutral/' + f for f in listdir(neutral_folder) if isfile(join(neutral_folder, f))]
negative_images = ['images/negative/' + f for f in listdir(negative_folder) if isfile(join(negative_folder, f))]

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

        if ss['compound'] < -0.3:
            new_status = "@{0} sad, sentiment rating: {1}".format(status.user.screen_name, ss['compound'])
            meme = random.choice(negative_images)
        elif ss['compound'] < 0.3:
            new_status = "@{0} neutral, sentiment rating: {1}".format(status.user.screen_name, ss['compound'])
            meme = random.choice(neutral_images)
        else:
            new_status = "@{0} happy, sentiment rating: {1}".format(status.user.screen_name, ss['compound'])
            meme = random.choice(positive_images)

        try:
            # api.update_status(new_status, status.id)
            api.update_with_media(meme, status=new_status, in_reply_to_status_id=status.id)
            print("Tweeting!")
        except err:
            print(err)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@comp440cdk'])
