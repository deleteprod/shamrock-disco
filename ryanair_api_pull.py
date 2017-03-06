#!/usr/bin/env python

# import the necessary modules
import json
import urllib2
import datetime
import argparse

parser = argparse.ArgumentParser(description='Shamrock Disco - the Ryanair Fare Finder')
parser.add_argument('-o','--origin', help='IATA code for airport of origin', required=True)
parser.add_argument('-w','--window', help='Time window for search in days', required=True)
parser.add_argument('-m','--maxprice', help='Maximum price you want to pay', required=False)
args = vars(parser.parse_args())

# Get date in raw format to allow for datetime.timedelta function
today_raw = datetime.datetime.today()

# Accept the window parameter from argparse and make it an integer for timedelta
window=int(args['window'])
date_to = today_raw + datetime.timedelta(days=window)

# Convert dates into something the JSON API will take
today_formatted = today_raw.strftime('%Y-%m-%d')
date_limit = date_to.strftime('%Y-%m-%d')

# Other variables for the API call
airport_code = args['origin']
price_limit = args['maxprice'] # Price limit for single fare

# Define the url for the JSON API
url = "https://api.ryanair.com/farefinder/3/oneWayFares?&departureAirportIataCode=%s&language=en&limit=30&market=en-gb&offset=0&outboundDepartureDateFrom=%s&outboundDepartureDateTo=%s&priceValueTo=%s" % (airport_code, today_formatted, date_limit, price_limit)

# Define how we will format the results coming back
def printResults(data):
    theJSON = json.loads(data)

    # for each result brought back by the JSON API query, extract relevant data
    for i in theJSON["fares"]:
        departure_date = str(i["outbound"]["departureDate"]) # string the departure date
        the_date = datetime.datetime.strptime(departure_date, "%Y-%m-%dT%H:%M:%S").strftime("%d %B - %H:%M") # tidy up the date
        print "From "  + i["outbound"]["departureAirport"]["seoName"].upper() + " to  " +  i["outbound"]["arrivalAirport"]["seoName"].upper()
        print "On " + the_date + " for " + str(i["outbound"]["price"]["value"])

# use urllib2 to open the URL and output it to variable named data
webUrl = urllib2.urlopen(url)
if (webUrl.getcode() == 200): # Check that we got a 200 HTTP response
    data = webUrl.read()
    printResults(data)
else:
    print "Error!"
