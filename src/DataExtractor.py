#import requests only supported for python3
import time
from collections import OrderedDict
import urllib2
from BeautifulSoup import BeautifulSoup

class DataExtractor(object):

	def __init__(self, url):
		self.url = url
		print("Data extractor initialised.")
		print("Extracting options data from: " + str(self.url))

	def getOptionsDataDictFromUrl(self, url, expiryTimestamp):
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page)
		results = soup.findAll('tbody')
		currentTime = int(time.time())
		
		# Results are BeautifulSoup tags
		calls = results[0]
		puts = results[1]

		callsDict = OrderedDict()
		putsDict = OrderedDict()

		callStrike = []
		callMidPrice = []
		callBid = []
		callAsk = []
		callErrors = []

		putStrike = []
		putMidPrice = [] 
		putBid = []
		putAsk = []
		putErrors = []

		def commaFloatToFloat(string):
			result = ''
			for char in string:
				if char != ',':
					result = result + char
			return float(result)

		for option in calls:
			attr = option.findAll('td')
			callStrike.append( commaFloatToFloat(attr[2].text) )
			callBid.append( commaFloatToFloat(attr[4].text) )
			callAsk.append( commaFloatToFloat(attr[5].text) )
			callMidPrice.append( 0.5 * (callBid[-1] + callAsk[-1]) )
			callErrors.append(0.5 * (callAsk[-1] - callBid[-1]))

		for option in puts:
			attr = option.findAll('td')
			putStrike.append( commaFloatToFloat(attr[2].text) )
			putBid.append( commaFloatToFloat(attr[4].text) )
			putAsk.append( commaFloatToFloat(attr[5].text) )
			putMidPrice.append( 0.5 * (putBid[-1] + putAsk[-1]) )
			putErrors.append(0.5 * (putAsk[-1] - putBid[-1]))

		callsDict['callStrike'] = callStrike 
		callsDict['callMidPrice'] = callMidPrice
		callsDict['callBid'] = callBid
		callsDict['callAsk'] = callAsk
		callsDict['callErrors'] = callErrors

		putsDict['putStrike'] = putStrike 
		putsDict['putMidPrice'] = putMidPrice
		putsDict['putBid'] = putBid
		putsDict['putAsk'] = putAsk
		putsDict['putErrors'] = putErrors

		return callsDict, putsDict