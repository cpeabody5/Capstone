import numpy as np

''' Functions used by test.py to post-process results '''

def moving_avg():
	pass

# Computes a weighted sum with more recent data prioritized over older data
# data: array in chronological order (oldest data first, more recent data last)
# gamma: decay rate
# returns float (weighted sum)
def decay(data, gamma):
	weights = np.power([gamma]*len(data), np.arange(len(data)-1, -1, -1))
	weighted_results = np.multiply(data, weights)
	return np.sum(weighted_results)