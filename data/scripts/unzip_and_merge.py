#!/usr/bin/python3
import sys
import os
import shutil
import zipfile
import pandas as pd

def renameFile(file_tmp, file_dest):
    files = os.listdir(file_tmp)
    for f in files:
        if (f.endswith("csv")):
            os.rename(file_tmp + f, file_dest)
            print("Successfully unzipped file into {}".format(file_dest))

def readIn(market_name, ticket_name):
    market_tmp = 'market_temp/'
    ticket_tmp = 'ticket_temp/'
    market_dest = market_tmp + market_name[-18:-3] + 'csv'
    ticket_dest = ticket_tmp + ticket_name[-18:-3] + 'csv'

    with zipfile.ZipFile(market_name, 'r') as f:
        f.extractall(market_tmp)
    with zipfile.ZipFile(ticket_name, 'r') as f:
        f.extractall(ticket_tmp)

    renameFile(market_tmp, market_dest)
    renameFile(ticket_tmp, ticket_dest)

    return market_dest, ticket_dest

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USAGE: ./unzip_and_merge.py QX_YEAR_Market.zip QX_YEAR_Ticket.zip")
        sys.exit()
    else:
        market_name = sys.argv[1]
        ticket_name = sys.argv[2]
        if 'market' not in market_name.lower() or 'ticket' not in ticket_name.lower():
            print("ERROR: Market or Ticket ZIP file provided in wrong position!")
            print("USAGE: ./unzip_and_merge.py QX_YEAR_Market.zip QX_YEAR_Ticket.zip")
            sys.exit()
        if market_name[-18:-16] != ticket_name[-18:-16]:
            print("ERROR: Attempting to merge two DIFFERENT quarters!")
            print("USAGE: ./unzip_and_merge.py QX_YEAR_Market.zip QX_YEAR_Ticket.zip")
            sys.exit()
        if market_name[-14:-11] != ticket_name[-14:-11]:
            print("ERROR: Attempting to merge two DIFFERENT years!")
            print("USAGE: ./unzip_and_merge.py QX_YEAR_Market.zip QX_YEAR_Ticket.zip")
            sys.exit()

    output_name = market_name[-18:-10] + 'Merged.csv'

    try:
        market_dest, ticket_dest = readIn(market_name, ticket_name)
    except Exception as e:
        print("RUNTIME ERROR: ", e)

    t_cols = ['ItinID', 'OnLine', 'FarePerMile', 'ItinFare', 'MilesFlown', 'RoundTrip']
    m_cols = ['ItinID', 'MktID', 'Year', 'Quarter', 'Origin', 'OriginState', 'Dest', 'DestState', 'AirportGroup', 'TkCarrier', 'OpCarrier', 'MktFare', 'MktMilesFlown', 'RPCarrier', 'BulkFare', 'Passengers']

    market = pd.read_csv('market_temp/Q1_2015_Market.csv', usecols=m_cols)
    ticket = pd.read_csv('ticket_temp/Q1_2015_Ticket.csv', usecols=t_cols)
    print("Successfully read in both files into dataframe. Begin processing...")

    merged = market.merge(ticket, left_on='ItinID', right_on='ItinID', how='outer')
    if (len(merged) != len(market)):
        print("The result of the merge produced a file with a different row count than expected (it should match the row count of the Market csv). Double check to see if the resulting file looks correct!")
    merged.to_csv(output_name, index=False)
    print("Successfully merged {} and {} into {}!".format(sys.argv[1], sys.argv[2], output_name))

    print("Attempting to clean up temporary directories....")
    shutil.rmtree('market_temp/')
    shutil.rmtree('ticket_temp/')
    print("Successfully cleaned up the temporary directories!")
