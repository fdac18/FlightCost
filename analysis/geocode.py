from geopy import geocoders, distance
import googlemaps
from GeoBases import GeoBase

GMAPS_KEY = 'AIzaSyCC7J4WeMBCJiwoEPUhm9-mOZlc8NDR7Kc'

# geopy geocoder
g = geocoders.GoogleV3(api_key=GMAPS_KEY)
# GoogleMaps for driving directions
gmaps = googlemaps.Client(key=GMAPS_KEY)
# GeoBase for geocoding data for all IATA-coded airports
geo_a = GeoBase(data='airports', verbose=False)

# Build list of primary airports (as defined by the FAA)
# for filtering IATA-coded airports
f = open('airports.txt','r')
IATA = [line.strip() for line in f.readlines()]
f.close()

# Lookup airports near a destination
destination = "Chattanooga, TN"
address0, (lat0, long0) = g.geocode(destination, exactly_one=False)[0]
latlong0 = (lat0, long0)
near = sorted(geo_a.findNearPoint((lat0, long0), 160))
#print(near);
airports = [k for _, k in sorted(geo_a.findNearPoint((lat0,long0), 160)) if k in IATA]
print(airports);
