#!/usr/bin/env python

# import the necessary modules
import json
import urllib2
import datetime

""" To do:  learn more about argparse module to make the script more versatile
Specifically, use argparse to allow passing of specific source airports, price
limits and dates etc
"""

# Get dates in raw format to allow for datetime.timedelta functions
today_raw = datetime.datetime.today()
next_week_raw = today_raw + datetime.timedelta(days=7)
next_month_raw = today_raw + datetime.timedelta (days=30)

# Convert those into something the JSON API will like
today_formatted = today_raw.strftime('%Y-%m-%d')
next_week_formatted = next_week_raw.strftime('%Y-%m-%d')
next_month_formatted = next_month_raw.strftime('%Y-%m-%d')

# Other variables for the API call - should we do it this way?
airport_code = "BHX" # Birmingham. Choose departure airport here.
date_limit = next_month_formatted # Choose the date limit here
price_limit = 20 # Price limit for single fare, in Euros. See jsonrates.com for next version converting to/from pounds

# For now - define the url for the JSON API
url = "https://api.ryanair.com/farefinder/3/oneWayFares?&departureAirportIataCode=%s&language=en&limit=30&market=en-gb&offset=0&outboundDepartureDateFrom=%s&outboundDepartureDateTo=%s&priceValueTo=%s" % (airport_code, today_formatted, date_limit, price_limit)

# Define how we will format the results coming back

def printResults(data):
    theJSON = json.loads(data)

    # for each result brought back by the JSON API query, extract relevant data
    for i in theJSON["fares"]:
        print "From "  + i["outbound"]["departureAirport"]["seoName"].upper() + " to  " +  i["outbound"]["arrivalAirport"]["seoName"].upper()
        print "On " + str(i["outbound"]["departureDate"]) + " for " + str(i["outbound"]["price"]["value"])
        print '\n'

# use urllib2 to open the URL and output it to variable named data

webUrl = urllib2.urlopen(url)
print webUrl.getcode()
if (webUrl.getcode() == 200): # Check that we got a 200 HTTP response
    data = webUrl.read()
    printResults(data)
else:
    print "Error!"
