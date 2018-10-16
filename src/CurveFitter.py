import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from finUtils import calNormalisedVol0, calNormalisedStrikes

class CurveFitterI(object):
	
	def __init__(self):
		print("Loading curve fitter factory...")

class YieldCurve(CurveFitterI):

	def __init__(self):
		print("Yield curve fitter initialised.")

	def putCallParity(self, strikes, discountFactor, forward):
		return -discountFactor * strikes + discountFactor * forward

	def regressionYieldRate(self, strikes, callPrices, putPrices, errors):
		callPrices = np.array(callPrices)
		putPrices = np.array(putPrices)
		y = callPrices - putPrices 
		params, cov = curve_fit(self.putCallParity, strikes, y, sigma = errors, absolute_sigma = True)
		discountFactor = params[0]
		forward = params[1]
		return discountFactor, forward 

class VolCurve(CurveFitterI):

	def __init__(self, timeToExpiry, normalisedVol0):
		CurveFitterI.__init__(self) 
		self.c2 = None
		self.s2 = None
		self.timeToExpiry = timeToExpiry
		self.normalisedVol0 = normalisedVol0
		print("Vol curve initialised for year to expiry: " + str(timeToExpiry))

	def display(self):
		print("c2: " + str(self.c2))
		print("s2: " + str(self.s2))
		print("timeToExpiry: " + str(self.timeToExpiry))
		print("normalised vol0: " + str(self.normalisedVol0))

	def changeTimeToExpiry(self, timeToExpiry):
		self.timeToExpiry = timeToExpiry
		print("Year to expiry changed to : " + str(self.timeToExpiry))

	def fitCurve(self, normalisedStrikes, vol, errors):
		params, cov = curve_fit(self.curveFuncToFit, normalisedStrikes, vol, p0 = [0.3, 0.5],
		 				bounds = ([0, -np.inf], [np.inf, np.inf]), sigma = errors, absolute_sigma = True)
		self.c2 = params[0]
		self.s2 = params[1]

	def curveFuncToFit(self, normalisedStrikes, c2, s2):
		z = normalisedStrikes
		vol0 = self.normalisedVol0
		variance = (vol0 ** 2 ) * ((1.0 + s2 * z) / 2 + np.sqrt((1.0 / 4 *
			(1.0 + s2 * z) ** 2 + 1.0 / 2 * (z ** 2) * c2 )))
		vol = np.sqrt(variance)
		return vol

	def yieldCurve(self, normalisedStrikes): 
		return self.curveFuncToFit(normalisedStrikes, self.c2, self.s2)

	def plotCurve(self):
		assert self.c2 > 0 and self.s2 is not None
		x = np.linspace(-6, 3, 5000)
		y = self.curveFuncToFit(x, self.c2, self.s2)
		print(y)
		print("Y: " + str(type(y)))
		plt.plot(x, y, 'o', markersize = 0.5)
		plt.xlabel('Normalised strikes')
		plt.ylabel('Volatility')
		plt.show()