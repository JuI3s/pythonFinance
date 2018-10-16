import numpy as np 
from scipy.stats import norm
from scipy.optimize import brentq

class PricerI(object):
	
	def __init__(self, underlierType = 'FUTURES'):
		self.underlierType = underlierType
		print("Loading pricer factory...")

	def price(self, vol, underlierPrice, strike, discountFactor, timeToExpiry, optionType):
		raise NotImplementedError() 

class BlackScholes(PricerI):

	def __init__(self, underlierType = 'FUTURES'):
		PricerI.__init__(self, underlierType)
		print("Black Scholes options pricer initialised.")

	def price(self, vol, underlierPrice, strike, discountFactor, timeToExpiry, optionType):
		if self.underlierType == 'FUTURES':
			if optionType == 'CALL':
				optionPrice = self.priceCall(vol, underlierPrice, strike, discountFactor, timeToExpiry)
			else:
				optionPrice = self.pricePut(vol, underlierPrice, strike, discountFactor, timeToExpiry)
		return optionPrice

	def priceCall(self, vol, underlierPrice, strike, discountFactor, timeToExpiry):
		future = underlierPrice
		dPlus = self.calDplus(vol, timeToExpiry, future, strike)
		dMinus = self.calDminus(dPlus, vol, timeToExpiry)
		optionPrice = discountFactor * (norm.cdf(dPlus) * future - norm.cdf(dMinus) * strike)
		return optionPrice

	def pricePut(self, vol, underlierPrice, strike, discountFactor, timeToExpiry):
		future = underlierPrice
		dPlus = self.calDplus(vol, timeToExpiry, future, strike)
		dMinus = self.calDminus(dPlus, vol, timeToExpiry)
		optionPrice = discountFactor * (strike * norm.cdf(0 - dMinus) - future * norm.cdf(0 - dPlus))
		return optionPrice

	def calDplus(self, vol, timeToExpiry, underlierPrice, strike):
		if self.underlierType == 'FUTURES':
			result = 1 / (vol * np.sqrt(timeToExpiry)) * (np.log(underlierPrice / strike) 
				+ 0.5 * vol ** 2 * timeToExpiry)
		return result

	def calDminus(self, dPlus, vol, timeToExpiry):
		result = dPlus - vol * np.sqrt(timeToExpiry)
		return result

	def calImpliedVol(self, marketPrice, underlierPrice, strike, discountFactor, timeToExpiry, optionType):
		#return an np array of implied vols
		#scipy.optimize.brenqt does not take array inputs
		try:
			len(marketPrice) > 0
		except:
			raise TypeError 
		
		results = []
		for i in range(len(marketPrice)):
			_marketPrice = marketPrice[i]
			_underlierPrice = underlierPrice
			_strike = strike[i]
			_timeToExpiry = timeToExpiry
			_discountFactor = discountFactor 
			vol = brentq(lambda vol: self.pricingError(vol, _marketPrice, _underlierPrice, 
				_strike, _discountFactor, _timeToExpiry, optionType), -100, 100)
			results.append(vol)
		results = np.array(results)
		return results

	def pricingError(self, vol, marketPrice, underlierPrice, strike, discountFactor, timeToExpiry, optionType):
		#Outputs the signed difference between predicted price and market price
		#Used in least square error minimisation in implied volatility calculation 
		return (marketPrice - self.price(vol, underlierPrice, strike, discountFactor, timeToExpiry, optionType))


