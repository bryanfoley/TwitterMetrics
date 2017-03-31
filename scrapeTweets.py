import sys
import getopt
import tweepy
from tweepy import OAuthHandler
from secret import *
import datetime
import string
import json
import jsonlines
import pandas
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
from plotter import plotter

api = tweepy.API(auth)

def print_tweet(tweet):
    print(json.dumps(tweet))

def get_tweets(outputfile):
    #Scrape the designated twitter feed for all tweets
    #This data is ALWAYS written to a file on disk because of rate restrictions
    #The data can be analysed later from the outputfile
    try:
        jsonlines.open(outputfile,mode='w')
    except FileNotFoundError:
        print("Could not open %s",inputfile," to write the data")
        sys.exit(1)
    with jsonlines.open(outputfile,mode='w') as f:
        for tweet in tweepy.Cursor(api.user_timeline).items():
            f.write(tweet._json)

def load_tweets(inputfile):
    #Load the tweet data from an input file on disk
    tweets = []
    container = []
    try:
        jsonlines.open(inputfile,mode='r')
    except FileNotFoundError:
        print("Could not locate",inputfile,"to read the data")
        sys.exit(1)
    with jsonlines.open(inputfile) as f:
        for line in f:
            tweets.append(line)
        container = get_date_time_data(tweets,container)
    return container

def get_date_time_data(tweets,container):
    #Back compatible with the old way of logging tweets
    for tweet in tweets:
        dt = datetime.datetime.strptime(tweet['created_at'],"%a %b %d %H:%M:%S %z %Y")
        dt2 = dt + datetime.timedelta(seconds=7200)#Convert UTC to Amsterdam time
        date = dt2.date()
        time = dt2.time()
        data = tweet['text'].split()#Backwards compatible
        if len(data) > 1:
            data = data[1]
        else:
            data = ", ".join(data)
        container.append([data,(date,time)])
    return container

def bucket_data(data):
    #For now, this is using hardcoded values
    #Make this more general
    bucketA = [] #This will hold the datetime object for Coffee (datetime.date,datetime.time)
    bucketB = [] #This will hold the same for Fruit
    for item in data:
        if item[0] == '30908':#Coffee
            bucketA.append(item[1])
        elif item[0] == '2344F3':#Fruit
            bucketB.append(item[1])
        else:
            pass #Discard terms which we are not looking for
    return bucketA,bucketB

def get_plot_data(data):
    xA = [d[0] for d in data[0]]
    yA = [d[1] for d in data[0]]

    xB = [d[0] for d in data[1]]
    yB = [d[1] for d in data[1]]

    xC = [d[1].hour for d in data[0]]
    xD = [d[1].hour for d in data[1]]

    return xA,yA,xB,yB,xC,xD


def do_processing(data):
    data = bucket_data(data)
    data = get_plot_data(data)
    plots = plotter(data)
    plots.generate_plots()

def main(argv):
    #Default inputfile that the script searches for
    inputfile = 'timeline_data.jsonl'
    try:
       opts, args = getopt.getopt(argv,"hui:",["ifile="])
    except getopt.GetoptError:
       print( 'scrapeTweets.py -u (refresh data) -i <custom inputfile name>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('scrapeTweets.py -u (refresh data) -i <custom inputfile name>')
          print('options -u and -i are mutually exclusive!')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
          print("Reading data from custom file",inputfile)
       elif opt == '-u':
          print("Scraping feed data...")
          get_tweets(inputfile)
          print("Data written to",inputfile)
    if(len(opts)==0):
        print("Reading data from",inputfile)

    data = load_tweets(inputfile)
    do_processing(data)

if __name__=='__main__':
    main(sys.argv[1:])

