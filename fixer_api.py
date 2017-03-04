#!/usr/bin/env python
import json # json parser module
import urllib2 # urllib2 to open links to API
import re # regex module to strip out the exchange rate

original_currency = "GBP" # What currency are you converting from?
new_currency = "EUR" # What currency are you converting to?

# Set up the URL for the Fixer API - substitute in strings for selected currencies
url = "http://api.fixer.io/latest?base=%s&symbols=%s" % (original_currency, new_currency)

# Grab the data using the URL from above through urllib2
data = json.load(urllib2.urlopen(url))

# String the result so regex can work on it
string = str(data)

# User regex to match on the exchange rate
exchange_rate = re.findall('\d.[0-9]{3}', string)

# Strip off unnecessary bumph from regex
stripped_rate = exchange_rate[0].replace("'", '')

# Convert the exchange rate to a float for use in mathematical operations on currencies
rate_float = float(stripped_rate)

# Keep a string version of it for use in strings such as that below
string_rate = str(stripped_rate)

# Proof of conversion
print "The exchange rate between %s and %s"  % (original_currency, new_currency) + " is %s %s to the %s" % (string_rate, new_currency, original_currency) 


