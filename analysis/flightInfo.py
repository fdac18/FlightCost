#!/usr/bin/python
import MySQLdb
import numpy as np
import matplotlib.pylot as plt

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

    cur.execute(command)
    result2 = cur.fetchall()

    db.close()
    return result2

# Returns average cost per flight
def avgCostperQ():

    origin = raw_input('Input origin airport: ')
    dest = raw_input('Input destination airport: ')
    quarter= raw_input('Input quarter: ')

    prices= extractPassPriceODQ(origin, dest, quarter)

    avgCost= np.mean(prices)

    return avgCost

# Internal function for passing arguments within 
## another function
def avgCostperQinternal(origin, dest, quart):
    prices=extractPassPriceODQ(origin, dest, quart)

    avgCost= np.mean(prices)
    return avgCost

# Create plot of yearly trend
def yearlyTrend():

    origin = raw_input('Input origin airport: ')
    dest = raw_input('Input destination airport: ')

    cost=[]
    for i in range(1,5):
        cost.append(avgCostperQinternal(origin, dest, i))

    plt.style.use('ggplot')
    plt.suptitle("Yearly Trend of Flight Cost Per Passenger")
    plt.title(origin + ' to ' + dest)
    plt.plot(range(1, 5), cost, c="b")
    plt.ylabel("Cost in USD ($)")
    plt.xlabel("Fiscal Quarter")
    plt.xticks(range(1,5), ('Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'))
    plt.savefig("./yearlyTrend_"+origin+"_"+dest+".pdf")


