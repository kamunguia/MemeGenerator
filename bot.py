import tweepy, time
from credentials import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id)
        print(status.text)
        print(status.user.screen_name)

        new_status = "hello, @{0}".format(status.user.screen_name)
        try:
            api.update_status(new_status, status.id)
            print("Tweeting!")
        except err:
            print(err)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@comp440cdk'])
