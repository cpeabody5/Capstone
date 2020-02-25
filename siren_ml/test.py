import os
import numpy as np
import utilities as ut
from data import LiveMelSpectrogram
from model import SirenDetection
from train import gen_data

def test():
	save_folder = ut.save_folder
	save_file = ut.save_file
	saved_data_file = ut.saved_data_file
	process_params_path = ut.process_params_path

	process_params = np.load(process_params_path)
	
	detector = SirenDetection()

	# load weights
	inputs, actual = gen_data(3)
	detector(inputs) # tf requires detector to be run once, run for shape only
	detector.load_weights(save_file)
	

	# processing:
	max_val = process_params["max_val"]

	# run detector on live data
	spec = LiveMelSpectrogram()
	while 1:
		live_input = np.expand_dims(spec.create_ms(is_mfcc=True),0)
		
		#print(np.amax(live_input), max_val)
		print(np.round(detector(live_input/max_val).numpy()))

def main():
	test()

if __name__ == '__main__':
	main()