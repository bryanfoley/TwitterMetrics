import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas

class dataPlotter():
    #This class will contain specific plot arguments
    #and functions for the desired plots
    def __init__(self,data):
        self.data = data
        self.f1 = plt.figure()
        self.f2 = plt.figure()
        self.xA=[]
        self.yA=[]
        self.xB=[]
        self.yB=[]
        self.xC=[]
        self.xD=[]

    def plot(self):
        self.get_plot_data()
        self.plot_scatter()
        self.plot_histogram()
        self.f1.show()
        self.f2.show()
        input()

    def get_plot_data(self):
        self.xA = [d[0] for d in self.data[0]]
        self.yA = [d[1] for d in self.data[0]]

        self.xB = [d[0] for d in self.data[1]]
        self.yB = [d[1] for d in self.data[1]]

        self.xC = [d[1].hour for d in self.data[0]]
        self.xD = [d[1].hour for d in self.data[1]]

    def plot_scatter(self):
        #Scatter plot
        self.f1 = plt.figure(1)
        plt.subplot(211)
        plt.xlabel('Day of year')
        plt.ylabel('Time of day')
        plt.title('Coffee')
        plt.grid(True)
        plt.plot(self.xA,self.yA,'ro')
        plt.axis(['May 20 2016','April 2017','23:59:59','00:00:00'])
        plt.subplot(212)
        plt.xlabel('Day of year')
        plt.ylabel('Time of day')
        plt.title('Fruit')
        plt.grid(True)
        plt.plot(self.xB,self.yB,'g^')
        plt.axis(['May 20 2016','April 2017','23:59:59','00:00:00'])

    def plot_histogram(self):
        #Histogram plot
        self.f2 = plt.figure(2)
        plt.subplot(211)
        plt.xlabel('Hour of day')
        plt.ylabel('Probability')
        plt.title('Coffee drinking')
        plt.grid(True)
        plt.hist(self.xC,24,normed=1,facecolor='r')
        plt.axis([0,24,0,0.3])
        plt.subplot(212)
        plt.xlabel('Hour of day')
        plt.ylabel('Probability')
        plt.title('Fruit eating')
        plt.grid(True)
        plt.hist(self.xD,24,normed=1,facecolor='g')
        plt.axis([0,24,0,0.3])
