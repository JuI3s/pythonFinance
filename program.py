#!/usr/bin/python
# -*- coding: latin-1 -*-
from src import DataExtractor, Pricer, CurveFitter
from src import VisualisationInterface
from src.finUtils import *
import time

url = 'https://finance.yahoo.com/quote/^GSPC/options?p=%5EGSPC&date='
expiryTimestamps = [ 1542326400, 1552608000, 1561075200]
curveFuncs = []
currentTime = int(time.time())
optionsDataExtractor = DataExtractor.DataExtractor('^SPX')
BS = Pricer.BlackScholes() 

for i in range(len(expiryTimestamps)):
	expiryUrl = url + str(expiryTimestamps[i])
	print(expiryUrl)
	calls, puts = optionsDataExtractor.getOptionsDataDictFromUrl(expiryUrl, expiryTimestamps[i])
	timeToExpiry = calTimeToExpiry(currentTime, expiryTimestamps[i])

	callMidPrices, callBid, callAsk, putMidPrices, putAsk, putBid, strikes, errors = getCallPutDataForSameStrikes(calls, puts)
	YC = CurveFitter.YieldCurve()
	discountFacotor, forward = YC.regressionYieldRate(strikes, callMidPrices, putMidPrices, errors)
	r = np.log(discountFacotor) / (-timeToExpiry)
	print("Rate: " + str(r))
	print("Discount Factor: " + str(discountFacotor))
	print("Forward: " + str(forward))

	callVols = BS.calImpliedVol(callMidPrices, forward, strikes, discountFacotor, timeToExpiry, 'CALL')
	callAskVols = BS.calImpliedVol(callAsk, forward, strikes, discountFacotor, timeToExpiry, 'CALL')
	callBidVols = BS.calImpliedVol(callBid, forward, strikes, discountFacotor, timeToExpiry, 'CALL')
	putVols = BS.calImpliedVol(putMidPrices, forward, strikes, discountFacotor, timeToExpiry, 'PUT')
	putAskVols = BS.calImpliedVol(putAsk, forward, strikes, discountFacotor, timeToExpiry, 'PUT')
	putBidVols = BS.calImpliedVol(putBid, forward, strikes, discountFacotor, timeToExpiry, 'PUT')

	midVols = 0.5 * (callVols + putVols)
	askVols = 0.5 * (callAskVols + putAskVols)
	bidVols = 0.5 * (callBidVols + putBidVols)
	volErrors = [midVols - bidVols, askVols - midVols]
	strikes = np.array(strikes)
	vols = []
	topErrors = []
	bottomErrors = []
	for i in range(len(strikes)):
		if strikes[i] <= forward:
			vols.append(putVols[i])
			topErrors.append(putAskVols[i] - putVols[i])
			bottomErrors.append(putVols[i] - putBidVols[i])
		else:
			vols.append(callVols[i])
			topErrors.append(callAskVols[i] - callVols[i])
			bottomErrors.append(callVols[i] - callBidVols[i])

	vols = np.array(vols)
	topErrors = np.array(topErrors)
	bottomErrors = np.array(bottomErrors)
	volErrors = []
	volErrors.append(bottomErrors)
	volErrors.append(topErrors)
	meanVolErrors = 0.5 * (topErrors + bottomErrors)

	normalisedVol0 = calNormalisedVol0(vols, timeToExpiry)
	normalisedStrikes = calNormalisedStrikes(strikes, forward, normalisedVol0)
	VC = CurveFitter.VolCurve(timeToExpiry, normalisedVol0)
	VC.fitCurve(normalisedStrikes, vols, meanVolErrors)
	curveFuncs.append(VC.yieldCurve)

VH = VisualisationInterface.VisualisationHelper()
VH.plotYieldCurves(curveFuncs)

# plt.errorbar(normalisedStrikes, vols, yerr = volErrors, ls = 'none', elinewidth=0.3)
# plt.scatter(normalisedStrikes, vols, s = 0.3, marker = 'x')
# VC.plotCurve()

