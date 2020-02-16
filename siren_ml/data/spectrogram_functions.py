import numpy as np 

def static_noise(shape, low=0.4, mid=0.8, high=0.95):
	max_amp_noise = 1
	low_amp_freq = np.random.uniform(0, max_amp_noise*0.4, size=shape)
	
	mid_amp_freq = np.random.uniform(0, max_amp_noise, size=shape)
	mid_amp_freq = np.where(mid_amp_freq>max_amp_noise*0.8, mid_amp_freq, 0)
	
	high_amp_freq = np.random.uniform(0, max_amp_noise, size=shape)
	high_amp_freq = np.where(high_amp_freq>max_amp_noise*0.95, max_amp_noise, 0)
	return low_amp_freq+mid_amp_freq+high_amp_freq

def structured_noise():
	pass