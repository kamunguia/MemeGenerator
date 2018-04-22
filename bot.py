import tweepy, time
from credentials import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
        elif ss['compound'] < 0.3:
            new_status = "@{0} neutral, sentiment rating: {1}".format(status.user.screen_name, ss['compound'])
        else:
            new_status = "@{0} happy, sentiment rating: {1}".format(status.user.screen_name, ss['compound'])

        try:
            api.update_status(new_status, status.id)
            print("Tweeting!")
        except err:
            print(err)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@comp440cdk'])
