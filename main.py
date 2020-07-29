#import libraries

from datetime import datetime, date
from datetime import timedelta

#import other files from python project
from billboard.spiders.billboard_spider import top100Spider, billboards, scrape_main
from spotify import spotify_main

def checkDate(date):
    now = datetime.now()
    day = date.split('-')
    if len(day) == 3:
        if len(day[0]) == 4 and day[0].isdigit():
            #year must fall between range of 1958 and now
            if int(day[0]) >= 1958 and int(day[0]) <= now.year:
                #year must fall between 1 to 12
                if int(day[1]) >= 1 and int(day[1]) <= 12 and day[1].isdigit():
                    #day must fall between 1 and 31
                    if (int(day[2]) >= 1 and int(day[2]) <= 31) and day[2].isdigit():
                        #exception, 1958 and current year
                        if int(day[0]) == 1958:
                            if int(day[1]) == 8:
                                if int(day[2]) >= 3:
                                    return True
                                else: 
                                    print('ERROR: too early of a date')
                                    return False
                        if int(day[0]) == now.year:
                            if int(day[1]) == now.month:
                                if int(day[2]) < now.day:
                                    return True
                                else: 
                                    print('ERROR: too far ahead')
                                    return False
                        return True
                    else: 
                        print('ERROR: date is less than 1 or greater than 31')
                        return False
                else: 
                    print('ERROR: date is less than 1 or greater than 12')
                    return False
            else: 
                print('ERROR: date is less than 1958 or greater than 2020')
                return False
        else:
            print('ERROR: year is 4 digits')
            return False
    else:
        print('ERROR: less than 3 args sent')
        return False
        #Update code to fix/update the date inputted
            #ignore 0 in singular digit days/months
            #add '-' between dates, etc
        '''
        elif len(day) = 2
        split twice, check for size = 3
        change to int
            check first val
            equal or greater than 1958
        change to int
            check second val
            between 01 - 12
        change to int
            check third val
            between 01 - 31
           return True
        '''


def main():
    #get username for spotify
    print('Please enter spotify username')
    username = input('>> ')
    print('\n')
    #get date from terminal window

    # get start date
    print('Enter start date (YYYY-MM-DD)')
    start = input(">> ")
    check = checkDate(start)
    while not check:
        print('Sorry, please input a valid start date')
        start = input(">> ")
        check = checkDate(start)
    print('Valid date detected: ' + start + '\n')
    start = datetime.strptime(start, "%Y-%m-%d")

    # get end date
    print('Enter end date (YYYY-MM-DD)')
    end = input(">> ")
    while not checkDate(end):
        print('Please input a valid date')
        end = input(">> ")
    end = datetime.strptime(end, "%Y-%m-%d")
    print('\n')

    #get range of dates
    if (end < start):
        print('Start date comes after end date, swapping order.')
        temp = end
        end = start
        start = temp

    #get list of dates separated by week
    dates = []
    dates.append(start)
    date = start
    while date < end:
        date = date + timedelta(days=7)
        dates.append(date)

    #scrape billboard top 100s
    scrape_main.scrape(dates)

    #get processed list of songs and artists  
    listOfSongs = billboards.getList()

    '''
    #testing, displays in terminal
    for song in listOfSongs:
        print('Song: ' + song.name)
        print('Artist: ' + song.artist + '\n')
    '''

    #get playlist from terminal
    spotify_main(listOfSongs, username)

    

main()