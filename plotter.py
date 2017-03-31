import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class plotter():
    #This class will contain specific plot arguments
    #and functions for the desired plots
    def __init__(self,data):
        self.data = data
        self.f1 = plt.figure()
        self.f2 = plt.figure()

    def show_plots(self):
        self.f1.show()
        self.f2.show()
        input()

    def generate_plots(self):
        #Scatter plot
        self.f1 = plt.figure(1)
        plt.subplot(211)
        plt.xlabel('Day of year')
        plt.ylabel('Time of day')
        plt.title('Coffee')
        plt.grid(True)
        plt.plot(self.data[0],self.data[1],'ro')
        plt.axis(['May 20 2016','April 2017','23:59:59','00:00:00'])
        plt.subplot(212)
        plt.xlabel('Day of year')
        plt.ylabel('Time of day')
        plt.title('Fruit')
        plt.grid(True)
        plt.plot(self.data[2],self.data[3],'g^')
        plt.axis(['May 20 2016','April 2017','23:59:59','00:00:00'])

        #Histogram plot
        self.f2 = plt.figure(2)
        plt.subplot(211)
        plt.xlabel('Hour of day')
        plt.ylabel('Probability')
        plt.title('Coffee drinking')
        plt.grid(True)
        plt.hist(self.data[4],24,normed=1,facecolor='r')
        plt.axis([0,24,0,0.3])
        plt.subplot(212)
        plt.xlabel('Hour of day')
        plt.ylabel('Probability')
        plt.title('Fruit eating')
        plt.grid(True)
        plt.hist(self.data[5],24,normed=1,facecolor='g')
        plt.axis([0,24,0,0.3])
        self.show_plots()
