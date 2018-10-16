import numpy as np 
from datetime import datetime

def calNormalisedVol0(vol, timeToExpiry): 
	#Return the at the money normalised vol
	vol0 = np.average(vol)
	normalisedVol0 = vol0 * np.sqrt(timeToExpiry)
	return normalisedVol0

def calNormalisedStrikes(strikes, future, normalisedVol0):
	normalisedStrikes = np.log(strikes / future) / normalisedVol0
	return normalisedStrikes

def convertTimestampToDateTime(timestamp):
	return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def calTimeToExpiry(startTimestamp, expiryTimestamp): 
	# calculate time to expiry in year from timestamps
	timeToExpiry = expiryTimestamp - startTimestamp
	timeToExpiry = float(timeToExpiry) / 31536000
	return timeToExpiry

def displayExpirayDates(expirayDates):
	# expiryDates is an array of timestamps
	for each in expirayDates:
		print(convertTimestampToDateTime(each))
 
def getCallPutDataForSameStrikes(callsDictData, putsDictData):
	# Get call and put prices where there is the same strike for both
	# Input call and put strikes sorted in increasing order
	callMidPrices = callsDictData['callMidPrice']
	callBid = callsDictData['callBid']
	callAsk = callsDictData['callAsk']
	putMidPrices = putsDictData['putMidPrice']
	putBid = putsDictData['putBid']
	putAsk = putsDictData['putAsk']

	callStrikes = callsDictData['callStrike']
	putStrikes = putsDictData['putStrike']

	callIndex = 0
	putIndex = 0 
	callLen = len(callStrikes)
	putLen = len(putStrikes)
	
	retStrikes = []
	retCallMidPrices = []
	retCallBid = []
	retCallAsk = []
	retPutMidPrice = []
	retPutBid = []
	retPutAsk = []
	retErrors = []		#call error plus put error

	while callIndex < callLen and putIndex < putLen: 
		if callStrikes[callIndex] == putStrikes[putIndex]:
			retStrikes.append(callStrikes[callIndex])

			retCallMidPrices.append(callMidPrices[callIndex])
			retCallBid.append(callBid[callIndex])
			retCallAsk.append(callAsk[callIndex])
			retPutMidPrice.append(putMidPrices[putIndex])
			retPutBid.append(putBid[putIndex])
			retPutAsk.append(putAsk[putIndex])

			retErrors.append(0.5 * (callAsk[callIndex] + putAsk[putIndex] - callBid[callIndex] - putBid[putIndex]))
			callIndex = callIndex + 1
			putIndex = putIndex + 1
		elif callStrikes[callIndex] < putStrikes[putIndex]:
			callIndex = callIndex + 1
		else: 
			putIndex = putIndex + 1 
	return retCallMidPrices, retCallAsk, retCallBid, retPutMidPrice, retPutAsk, retPutBid, retStrikes, retErrors