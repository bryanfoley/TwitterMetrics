import sys
import getopt
from scraper import dataScraper
from parser import dataParser
from plotter import dataPlotter

def main(argv):
    #Default inputfile that the script searches for
    inputfile = 'timeline_data.jsonl'
    update = 'False'
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
          update=True
          print("Data written to",inputfile)
    if(len(opts)==0):
        print("Reading data from",inputfile)

    scraper = dataScraper(inputfile,update)
    scrapedData = scraper.scrape()
    parser = dataParser(scrapedData)
    parsedData = parser.parse()
    plotter = dataPlotter(parsedData)
    plotter.plot()

if __name__=='__main__':
    main(sys.argv[1:])

