#!/usr/bin/python
from geopy import geocoders, distance
import subprocess
import googlemaps
from GeoBases import GeoBase
import MySQLdb
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GMAPS_KEY = 'AIzaSyCC7J4WeMBCJiwoEPUhm9-mOZlc8NDR7Kc'
MILE_RADIUS = 160
AVG_GAS = 2.60
AVG_MPG = 22
def connect():
    db = MySQLdb.connect(host="10.16.0.3",          # your host, usually localhost
                         user="root",               # your username
                         passwd="flight-cost18",    # your password
                         db="FlightData")           # name of the data base

    return db

def airportsNearCoords(location, radius):
    g = geocoders.GoogleV3(api_key=GMAPS_KEY)
    geo_a = GeoBase(data='airports', verbose=False)

    # Build list of primary airports for filtering IATA coded airports
    f = open('airports.txt', 'r')
    IATA = [line.strip() for line in f.readlines()]
    f.close()

    # Lookup airports near a destination
    address0, (lat0, long0) = g.geocode(location, exactly_one=False)[0]
    latlong = (lat0, long0)
    near = sorted(geo_a.findNearPoint((lat0, long0), radius))
    airports = [k for _, k in near if k in IATA]
    return airports

def drivingDistance(start, end):
    gmaps = googlemaps.Client(key=GMAPS_KEY)
    g = geocoders.GoogleV3(api_key=GMAPS_KEY)
    dist = 0

    startAddress, (latitude, longitude) = g.geocode(start, exactly_one=True)
    startCoords = (latitude, longitude)

    endAddress, (latitude, longitude) = g.geocode(end, exactly_one=True)
    endCoords = (latitude, longitude)
    
    print "Start address " + startAddress + "\n"
    print "End address " + endAddress + "\n"

    estDistance = distance.distance(startCoords, endCoords).miles
    print "\t Est Distance: " + str(estDistance) + " miles\n"

    try:
        directions = gmaps.directions(startCoords, endCoords)
        driving = directions[0]['legs'][0]['distance']['value']/1609.34
        dist = driving
        print "\t Driving distance: %.2f miles." % driving
    except:
        dist = estDistance

    return dist

def extractDataODQ():
    db = connect()
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
    db = connect()
    cur = db.cursor()

    origin = org
    dest = des
    quarter = quart

    command = 'Select mktFare FROM HistoricalData WHERE Origin = "' + origin + '" AND Dest = "' + dest + '" AND Quarter = "' + str(quarter) + '" AND Passengers = "1"'

    cur.execute(command)
    result1 = cur.fetchall()

    db.close()
    return result1

def extractDataOD():
    db = connect()
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


def yearlyTrendAuto():

    start = raw_input('Enter your location: ')
    radius = float(raw_input('Search for airports within how many miles of your location?: '))*1.609
    dest = raw_input('Input destination airport (IATA code - i.e. JFK, LAX, CHA): ')[:3]
    gasYN = raw_input('Include driving (gas) to airport costs in calculation? [Y/N] ')
    gasYN = gasYN.lower()[:1]

    originAirports = airportsNearCoords(start, radius)
    print "Got airports " + str(originAirports)

    
    plt.style.use('ggplot')
    if gasYN == 'y':
        plt.suptitle("Yearly Trend of Flight Cost Per Passenger (including gas costs)")
    else:
        plt.suptitle("Yearly Trend of Flight Cost Per Passenger")
    plt.title(start + ' to ' + dest)
    plt.ylabel("Cost in USD ($)")
    plt.xlabel("Fiscal Quarter")
    plt.xticks(range(1,5), ('Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'))
    start = start.replace(" ", "")
    fname = "yearlyTrendAuto_" + start + "_" + dest + ".pdf"

    airportAvgs=[]
    for origin in originAirports:
        cost=[]
        for i in range(1,5):
            if gasYN == 'y':
                drivingCost = float((drivingDistance(start, origin + " airport")/AVG_MPG) * AVG_GAS)
                cost.append(float(avgCostperQinternal(origin, dest, i)) + drivingCost)
            else:
                cost.append(avgCostperQinternal(origin, dest, i))
        plt.plot(range(1, 5), cost, label=origin, marker="o")
        airportAvgs.append(np.mean(cost))
    print(airportAvgs)
    plt.legend()
    plt.savefig(fname)
    plt.close()

    fname2 = "airportAvgs_" + start+ ".pdf"
    # Make second cost plot
    plt.style.use('ggplot')
    plt.suptitle("Average Cost to Destination per Airport")
    plt.title('Your Area to ' + dest)
    plt.bar(range(1, len(originAirports)+1), airportAvgs, color='#4885ed')
    plt.ylabel("Avg. Cost in USD ($)")
    plt.xlabel("Airport")
    plt.xticks(range(1, len(originAirports)+1),[x for x in originAirports])
    plt.savefig(fname2)

    print "Attempting to move the file into Google Storage Bucket\n"
    command = "gsutil cp " + fname + " gs://graph_data"
    command = command.split()
    move_file = subprocess.call(command)

    
    print "Attempting to move the file into Google Storage Bucket\n"
    command = "gsutil cp " + fname2 + " gs://graph_data"
    command = command.split()
    move_file = subprocess.call(command)

