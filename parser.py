import datetime
import string

variables = {'Coffee':'30908','Fruit':'2344F3','Offset':7200}

class dataParser():
    #This class will contain the functions that parse
    #the data and teh items to be searched for

    def __init__(self,tweets):
        self.tweets = tweets
        self.container = []
        self.bucketA = [] #This will hold the datetime object for Coffee (datetime.date,datetime.time)
        self.bucketB = [] #This will hold the same for Fruit
    
    def parse(self):
        self.get_date_time_data()
        self.bucket_data()
        return self.bucketA,self.bucketB

    def get_date_time_data(self):
        #Back compatible with the old way of logging tweets
        for tweet in self.tweets:
            dt = datetime.datetime.strptime(tweet['created_at'],"%a %b %d %H:%M:%S %z %Y")
            dt2 = dt + datetime.timedelta(seconds=variables['Offset'])#Convert UTC to Amsterdam time
            date = dt2.date()
            time = dt2.time()
            data = tweet['text'].split()#Backwards compatible
            if len(data) > 1:
                data = data[1]
            else:
                data = ", ".join(data)
            self.container.append([data,(date,time)])

    def bucket_data(self):
        #For now, this is using hardcoded values
        #Make this more general
        for item in self.container:
            if item[0] == variables['Coffee']:#Coffee
                self.bucketA.append(item[1])
            elif item[0] == variables['Fruit']:#Fruit
                self.bucketB.append(item[1])
            else:
                pass #Discard terms which we are not looking for
