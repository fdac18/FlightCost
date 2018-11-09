#!/usr/bin/python
import MySQLdb
from flightInfo import yearlyTrend, extractDataODQ, extractDataOD, avgCostperQ
'''
data1 = extractDataODQ()
for row in data1:
    print row
    print '\n'
data2 = extractDataOD()
for row in data2:
    print row
    print '\n'
'''
# Test avgCost func

yearlyTrend()

