import tweepy
#from ipdb import set_trace
import sys
import os
import datetime
import time
from . import config,db
from models import User,TweetStore
import sqlalchemy

class TweepyHandler(object):

    def __init__(self,kwargs):
        self.consumer_key = config.CONSUMER_KEY
        self.consumer_secret = config.CONSUMER_SECRET
        self.auth_key = kwargs.get('AUTH_KEY')
        self.auth_secret = kwargs.get('AUTH_SECRET')

    def login(self):
        Oauth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        Oauth.set_access_token(self.auth_key,self.auth_secret)
        self.api=tweepy.API(Oauth)
        #print "Authenticated!!"

    def post(self,update):
        self.api.update_status(status=update)
        #sys.stderr.write("status = "+update)
        print("Tweet Posted Successfully")



class DbHandler(object):

    def __init__(self):
        self.db = db


def get_cred(self):
        try:
            user = self.db.query(User).first()
            return {'AUTH_KEY': user.auth_key, 'AUTH_SECRET' : user.auth_secret}
        except AttributeError:
            print "No user found,register first"
            sys.exit(1)

    def store_tweet(self):
        print "Press Enter to stop Storing tweets!"
        tweet_obj = []
        while True:
            tweet = raw_input("enter your tweet: ")
            if tweet is not "":
                tweet_obj.append(TweetStore(
                tweet=tweet))
            else:
                break
        self.db.add_all(tweet_obj)
        self.db.commit()


    def del_post(self,**kwargs):
        if kwargs.get('id'):
            self.db.query(TweetStore).filter(TweetStore.id == kwargs.get('id')).delete()
        elif kwargs.get('tweet'):
            self.db.query(TweetStore).filter(TweetStore.tweet == kwargs.get('tweet')).delete()
        self.db.commit()

    def post(self):
        try:
            tweet = self.db.query(TweetStore).first()
            return tweet
        except Exception as e:
            print e
            print "No tweet found,add tweets first"
            sys.exit(1)

    def buff_disp(self):
        tweet_list = self.db.query(TweetStore).all()
        if tweet_list:
            print "id \t\t tweets \t\t created"
            print "== \t\t ====== \t\t =======\n"
        else:
            print "No tweets saved, add new tweets"
        for tweet in tweet_list:
            print "{id}) \t\t {tweet} \t\t {created}".format(id=tweet.id,tweet=tweet.tweet,created=tweet.created)

class Tweetdaemon(object):

    def __init__(self,time=1):
        self.t=time
        self.name="bufftweet"
        self.pidfile_path='/var/tmp/%s.pid' % self.name
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/tmp/%s.log' % self.name
        self.stderr_path = '/var/tmp/%s.log' % self.name
        self.pidfile_timeout = 5

    def initialize(self):
        self.DB = DbHandler()
        self.API= TweepyHandler(self.DB.get_cred())

    def safe_close_db(self):
        self.DB.db.close()

    def run(self):
        self.API.login()
        while True:
            status = self.DB.post()
            #sys.stderr.write("status = running")
            if status is not None:
                self.API.post(status.tweet)
                self.DB.del_post(tweet=status.tweet)
            time.sleep(self.t*60)


