from . import config,db
from . import models
import tweepy
import os
import webbrowser


class RegisterUser(object):

    def __init__(self):
        self.auth_key = None
        self.auth_secret = None
        self.consumer_key = config.CONSUMER_KEY
        self.consumer_secret = config.CONSUMER_SECRET


    def __authenticate(self): 

        print "Authenticating...."

        auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            print 'Error! Failed to get request token.'
        
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open_new(redirect_url)
        finally:
            os.dup2(savout, 1)

        verifier = raw_input("Verifier: ")

        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
        
        auth_key = auth.access_token
        auth_secret = auth.access_token_secret
        
        return auth_key,auth_secret

    def register(self):
        author= raw_input("enter your name: ")
        self.auth_key,self.auth_secret = self.__authenticate()
        obj = models.User(user=author,auth_key=self.auth_key,auth_secret=self.auth_secret,tweet_count=0)
        db.add(obj)
        db.commit()