#!/usr/bin/python3

from urllib import request

def download(year, quarters):
    year = str(year)
    for i in range(1, quarters+1):
        tick_url = 'https://transtats.bts.gov/PREZIP/Origin_and_Destination_Survey_DB1BTicket_{}_{}.zip'.format(year, str(i))
        mark_url = 'https://transtats.bts.gov/PREZIP/Origin_and_Destination_Survey_DB1BMarket_{}_{}.zip'.format(year, str(i))
        tick_file = '../downloads/Q{}_{}_Ticket.zip'.format(str(i), year)
        mark_file = '../downloads/Q{}_{}_Market.zip'.format(str(i), year)
        try:
            print("Downloading Ticket Table for Q{} {}".format(str(i), year))
            request.urlretrieve(tick_url, tick_file)
            print("Successfully downloaded {}!".format(tick_file))
        except Exception as e:
            print("Ticket Error: ", e)
        try:
            print("Downloading Market Table for Q{} {}".format(str(i), year))
            request.urlretrieve(mark_url, mark_file)
            print("Successfully downloaded {}!".format(mark_file))
        except Exception as e:
            print("Market Error: ", e)

if __name__ == '__main__':
    for i in range(2015, 2019):
        download(i, 4)
