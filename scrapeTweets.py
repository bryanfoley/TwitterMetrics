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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
        print("Could not open %s",outputfile," to write the data")
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
    bucketA = []
    bucketB = []
    for item in data:
        if item[0] == '30908':#Coffee
            bucketA.append(item[1])
        elif item[0] == '2344F3':#Fruit
            bucketB.append(item[1])
        else:
            pass
    return bucketA,bucketB

def get_plot_data(data):
    xA = [d[0] for d in data[0]]
    yA = [d[1] for d in data[0]]

    xB = [d[0] for d in data[1]]
    yB = [d[1] for d in data[1]]

    xC = [d[1].hour for d in data[0]]
    xD = [d[1].hour for d in data[1]]

    return xA,yA,xB,yB,xC,xD


def plot_data(data):
    f1 = plt.figure(1)
    plt.subplot(211)
    plt.xlabel('Day of year')
    plt.ylabel('Time of day')
    plt.title('Coffee')
    plt.grid(True)
    plt.plot(data[0],data[1],'ro')
    plt.axis(['May 20 2016','April 2017','23:59:59','00:00:00'])
    plt.subplot(212)
    plt.xlabel('Day of year')
    plt.ylabel('Time of day')
    plt.title('Fruit')
    plt.grid(True)
    plt.plot(data[2],data[3],'g^')
    plt.axis(['May 20 2016','April 2017','23:59:59','00:00:00'])
    f1.show()

    f2 = plt.figure(2)
    plt.subplot(211)
    plt.xlabel('Hour of day')
    plt.ylabel('Probability')
    plt.title('Coffee drinking')
    plt.grid(True)
    plt.hist(data[4],24,normed=1,facecolor='r')
    plt.axis([0,24,0,0.3])
    plt.subplot(212)
    plt.xlabel('Hour of day')
    plt.ylabel('Probability')
    plt.title('Fruit eating')
    plt.grid(True)
    plt.hist(data[5],24,normed=1,facecolor='g')
    plt.axis([0,24,0,0.3])
    f2.show()

    input()

def do_processing(data):
    #bucketA,bucketB = bucket_data(data)
    data = bucket_data(data)
    data = get_plot_data(data)
    plot_data(data)

def main(argv):
    inputfile = 'timeline_prototype.jsonl'
    outputfile = 'timeline_prototype.jsonl'
    try:
       opts, args = getopt.getopt(argv,"hui:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print( 'test.py -i <inputfile> -o <outputfile>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print ('scrapeTweets.py -u (refresh data) -i <inputfile> -o <outputfile>')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
       elif opt == '-u':
          print("Scraping feed data...")
          get_tweets(outputfile)
    print('Input file is ', inputfile)
    print('Output file is ', outputfile)
  
    data = load_tweets(inputfile)
    do_processing(data)

if __name__=='__main__':
    main(sys.argv[1:])

