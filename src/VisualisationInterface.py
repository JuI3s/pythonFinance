import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

class VisualisationHelper(object):

	def __init__(self):
		print("VisualisingHelper initialised.")

	@staticmethod
	def plotYieldCurves(curveFuncs, xLeft = -6, xRight = 3, numOfPoints = 5000):
		# Curve funcs: array of yield curve functions to plot
		# xLeft: leftmost x coordinate
		# xRight: rightmost x coordinate
		# numOfPoints: how many ponits to plot 
		plt.xlabel('Normalised strikes')
		plt.ylabel('Volatility')
		for eachCurve in curveFuncs: 
			x = np.linspace(xLeft, xRight, numOfPoints)
			y = eachCurve(x)
			plt.plot(x, y, 'o', markersize = 0.5)
		plt.show()