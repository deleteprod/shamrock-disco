#!/usr/bin/env python

# import the necessary modules
import json
import urllib2
import datetime
import argparse
from decimal import Decimal


parser = argparse.ArgumentParser(description='Ryanair Per-day Detailed Fare Finder')
parser.add_argument('-o','--origin', help='IATA code for airport of origin', required=True)
parser.add_argument('-a','--destination', help='IATA code for airport of destination', required=True)
parser.add_argument('-d','--date', help='Flight date in YYYY-MM-DD format', required=True)
parser.add_argument('-f','--flexdays', help='How many days to look for via flexDate?', required=False)
args = vars(parser.parse_args())

# Other variables for the API call
airport_code_origin = args['origin']
airport_code_destination = args['destination']
flight_date = args['date']
flex_days = args['flexdays'] if (args['flexdays'] and int(args['flexdays']) < 7) else '6'




# Define the url for the JSON API
url = "https://desktopapps.ryanair.com/en-gb/availability?ADT=1&CHD=0&DateOut=%s&Origin=%s&Destination=%s&FlexDaysOut=%s&INF=0&RoundTrip=false&TEEN=0" % (flight_date, airport_code_origin, airport_code_destination, flex_days)

print url
print "\r\n\r\n"
# Define how we will format the results coming back
def printResults(data):
    lowest_price = 0.00
    lowest_date = ''

    theJSON = json.loads(data)

    print "From "  + theJSON["trips"][0]["originName"] + " <" + theJSON["trips"][0]["origin"] + ">" + " to  " + theJSON["trips"][0]["destinationName"] + " <" + theJSON["trips"][0]["destination"] + ">"

    # for each result brought back by the JSON API query, extract relevant data
    for date in theJSON["trips"][0]["dates"]:
        for i in date["flights"]:
            fares_left = str(i["faresLeft"]) # string the departure date
            if int(fares_left) == 0:
                continue

            flight_number = str(i["flightNumber"]) # string the departure date
            dep_date = str(i["time"][0]) # string the departure date
            arr_date = str(i["time"][1]) # string the departure date

            formatted_dep_date = datetime.datetime.strptime(dep_date[:-4], "%Y-%m-%dT%H:%M:%S").strftime("%d %B %Y @ %H:%M") # tidy up the date
            formatted_arr_date = datetime.datetime.strptime(arr_date[:-4], "%Y-%m-%dT%H:%M:%S").strftime("%d %B %Y @ %H:%M") # tidy up the date

            current_price = float(i["regularFare"]["fares"][0]["amount"])

            if (lowest_price == 0.00 or current_price < lowest_price):
                lowest_price = current_price
                lowest_date = dep_date
            print formatted_dep_date + " for " + str(current_price) + " (" + fares_left + " left)"

    if (lowest_price == 0):
        print "All prices are equal!"
    else:
        print "Lowest price is %s flying out on %s" % (lowest_price, lowest_date)

# use urllib2 to open the URL and output it to variable named data
webUrl = urllib2.urlopen(url)
if (webUrl.getcode() == 200): # Check that we got a 200 HTTP response
    data = webUrl.read()
    printResults(data)
else:
    print "Error!"
