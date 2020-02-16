"""This file contains the types of curves for the frequencies.py
"""
import numpy as np 

def choose_random_in_range(item, is_choice=False):
	"""Chooses random in range
	if this is scalar, will return scalar
	if this is a list, will choose items bounded by the list
	
	Args:
	    item (list or scalar): Description
	
	Returns:
	    scalar: this is a selected value
	"""
	def rand(mini=0, maxi=1):
		# random selection funcion
		shape = np.asarray(mini).shape
		return (maxi - mini) * np.random.random(size=shape) + mini

	if type(item) == list:
		if not is_choice:
			assert not len(item)%2, "must specify the maximum and minimum intervals for a list, the list len must be divisible by 2"
			choices = []
			for i in range(len(item)//2): #pseudo random selection
				choices.append(rand(item[i], item[i+1]))
			item = choices[np.random.choice(range(len(choices)))]
		else:
			item = np.random.choice(items)

	return item


class Wave():
	def __init__(self, waveform, amp, f, phase_shift, offset):
		self.amp = choose_random_in_range(amp)
		self.f = choose_random_in_range(f)
		self.offset = choose_random_in_range(offset)
		self.phase_shift = choose_random_in_range(phase_shift)
		self.waveform = waveform

	def __call__(self, time):
		freq = self.amp * self.waveform(2*np.pi*self.f*time+self.phase_shift) + self.offset
		return freq

def main():
	ranges = [np.ones((3,4,5))*0.001, np.ones((3,4,5))]
	print(choose_random_in_range(ranges))
	print(choose_random_in_range([0.001,1]))
if __name__ == '__main__':
	main()