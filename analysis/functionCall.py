#!/usr/bin/python
import MySQLdb
from flightInfo import (
        extractDataODQ,
        extractDataOD,
        avgCostperQ,
        yearlyTrend,
        yearlyTrendAuto,
        airportsNearCoords)
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
# price= avgCostperQ()
# print price
yearlyTrendAuto()
