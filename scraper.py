import sys
import tweepy
from tweepy import OAuthHandler
from secret import *
import json
import jsonlines
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class dataScraper():
    #This class will used to determine where the raw data
    #is gathered from and saved too.

    def __init__(self,inputfile=None,update=False):
        if inputfile:
            self.inputfile = inputfile
        else:
            self.inputfile = 'timeline_data.jsonl'
        self.update = update
        self.tweets = []

    def scrape(self):
        if self.update==True:
            self.update_data()
            self.load_data()
        else:
            self.load_data()
        return self.tweets

    def update_data(self):
        #Scrape the user twitter feed for all tweets
        #This data is ALWAYS written to a file on disk because of rate restrictions
        #The data can be analysed later from the outputfile
        try:
            jsonlines.open(self.inputfile,mode='w')
        except FileNotFoundError:
            print("Could not open %s",self.inputfile," to write the data")
            sys.exit(1)
        with jsonlines.open(self.inputfile,mode='w') as f:
            for tweet in tweepy.Cursor(api.user_timeline).items():
                f.write(tweet._json)

    def load_data(self):
        #Load the tweet data from an input file on disk
        try:
            jsonlines.open(self.inputfile,mode='r')
        except FileNotFoundError:
            print("Could not locate",self.inputfile,"to read the data")
            sys.exit(1)
        with jsonlines.open(self.inputfile) as f:
            for line in f:
                self.tweets.append(line)
        return self.tweets

    
