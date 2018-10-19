#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="10.16.0.3",    # your host, usually localhost
        user="root",         # your username
        passwd="flight-cost18",  # your password
        db="FlightData")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
#cur.execute("Show Tables")
cur.execute("SELECT * from HistoricalData")
# print all the first cell of all the rows
for row in cur.fetchall():
    print row

db.close()
