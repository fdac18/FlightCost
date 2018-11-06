#!/usr/bin/python
import MySQLdb
import numpy as np

def extractDataODQ():
    db = MySQLdb.connect(host="10.16.0.3",    # your host, usually localhost
            user="root",         # your username
            passwd="flight-cost18",  # your password
            db="FlightData")        # name of the data base

    cur = db.cursor()

    origin = raw_input('input origin airport: ')
    dest = raw_input('input destination airport: ')
    quarter = raw_input('input quarter of flight: ')

    command = 'Select * FROM HistoricalData WHERE Origin = "' + origin + '" AND Dest = "' + dest + '" AND Quarter = "' + quarter + '"'
    #for troubleshooting
    #print(command)

    cur.execute(command)
    result1 = cur.fetchall()

    db.close()
    return result1

#I am keeping this here just to show a possible average Query 
#cur.execute('SELECT AVG(mktFare) FROM HistoricalData WHERE Origin = "ATL" AND Dest = "LAX" AND Quarter = "1" AND Passengers = "1"')

# Second function with arguments passed
def extractPassPriceODQ(org, des, quart):
    db = MySQLdb.connect(host="10.16.0.3",    # your host, usually localhost
            user="root",         # your username
            passwd="flight-cost18",  # your password
            db="FlightData")        # name of the data base

    cur = db.cursor()

    origin = org
    dest = des
    quarter = quart

    command = 'Select mktFare FROM HistoricalData WHERE Origin = "' + origin + '" AND Dest = "' + dest + '" AND Quarter = "' + quarter + '" AND Passengers = "1"'

    cur.execute(command)
    result1 = cur.fetchall()

    db.close()
    return result1

def extractDataOD():
    db = MySQLdb.connect(host="10.16.0.3",    # your host, usually localhost
            user="root",         # your username
            passwd="flight-cost18",  # your password
            db="FlightData")        # name of the data base

    cur = db.cursor()

    origin = raw_input('Input origin airport: ')
    dest = raw_input('Input destination airport: ')

    command = 'Select * FROM HistoricalData WHERE Origin = "' + origin + '" AND Dest = "' + dest + '"'
    #for troubleshooting
    #print(command)

    cur.execute(command)
    result2 = cur.fetchall()

    db.close()
    return result2


def avgCostperQ():

    origin = raw_input('Input origin airport: ')
    dest = raw_input('Input destination airport: ')
    quarter= raw_input('Input quarter: ')

    prices= extractPassPriceODQ(origin, dest, quarter)

    avgCost= np.mean(prices)

    return avgCost


#for troubleshooting
#data1 = extractDataODQ()
#for row in data1:
#    print "info:"
#    print row
#    print '\n'

#data2 = extractDataOD()

#for row in data2:
#    print "info:"
#    print row
#    print '\n'
