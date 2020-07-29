#https://www.billboard.com/charts/hot-100/YYYY-MM-DD
#scrape 
from datetime import datetime, date
from datetime import timedelta

from scrapy.crawler import CrawlerProcess
import scrapy

#list of top 100s songs
list100 = []

#starts scrapy crawl, simulates "scrapy crawl top100s"
class scrape_main():
    def scrape(dates):
        global listofDates
        listofDates = dates
        
        for dat in dates:
            print('DATE: ' + str(dat))

        # start scrapy
        process = CrawlerProcess()
        
        process.crawl(top100Spider)
        process.start() # the script will block here until the crawling is finished
    
class top100Spider(scrapy.Spider):
    #call > scrapy crawl top100s
    name = "top100s"
    def start_requests(self):
        urls = []
        #get dates based on main function from main.py
        
        for week in listofDates:
            urls.append('https://www.billboard.com/charts/hot-100/' + datetime.strftime(week,'%Y-%m-%d'))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #personal, set up terminal to run from a few folders up
        filename = 'python/billboard/scrapes/top_100s.txt'
        #filename = 'billboard/scrapes/top_100s-3.txt'

        #saves info to txt file and adds song to list
        with open(filename, 'w') as f:
            i = 0
            for quote in response.css("span.chart-element__information"):
                i = i + 1
                songName = str(quote.css("span.chart-element__information__song::text").extract_first())
                artistName = str(quote.css("span.chart-element__information__artist::text").extract_first())
                
                f.write('Rank: ' + str(i) + '\n')
                f.write('Song: ' + songName+ '\n')
                f.write('Artist: ' + artistName + '\n')
                f.write('\n')

                #adds song to list
                billboards(artistName,songName,str(i))
        
            self.log('Saved file %s' % filename)

#organize list of songs along with ranks, creates object 'song'
class billboards():
    def __init__(song, artist, name, rank):
        #check if song is already in list, if so, add its rank
        matching = [s for s in list100 if (name in s.name and artist in s.artist)]
        if len(matching)>0:
            numMatch = matching[0].numID
            list100[numMatch].rank.append(rank)

        #if song is not in list, add it to list and initialize rank list
        else:
            song.numID = len(list100)
            song.artist = artist 
            song.name = name 
            song.rank = []
            (song.rank).append(rank)
            #add new song
            list100.append(song)

    def getList():
        return list100
        