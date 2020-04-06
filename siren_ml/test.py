import os
import numpy as np
import utilities as ut
from data import LiveMelSpectrogram
from model import SirenDetection
from train import gen_data
#from alert import Alerter
import processing

def test(history_size, output_threshold, process_func, output_func):
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

	past_results = np.zeros(history_size)

	# run detector on live data
	spec = LiveMelSpectrogram()
	while 1:
		live_input = np.expand_dims(spec.create_ms(is_mfcc=True),0)
		#print(np.amax(live_input), max_val)
		current_val = np.round(detector(live_input/max_val).numpy())[0][0]

		# Add current result to past results
		past_results = np.roll(past_results, -1)	# shift elements backwards to preserve chronological order
		past_results[len(past_results) - 1] = current_val

		# Process Results and get output
		val = process_func(past_results)
		output_func(val > output_threshold)
		print('{:3.2f}\t{}'.format(val, past_results))

def main():
	alerter = Alerter()
	test(7, 1.2, lambda x:processing.decay(x, 0.7), alerter.set_alert_status)

if __name__ == '__main__':
	main()