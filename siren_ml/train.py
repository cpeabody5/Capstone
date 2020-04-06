# must use python 3.7
import numpy as np
import tensorflow as tf

from data import GenerateData, SpecAnimate
from model import SirenDetection
from utilities import gen_data
import utilities as ut
import time

import os

save_folder = ut.save_folder
save_file = ut.save_file
saved_data_file = ut.saved_data_file
process_params_path = ut.process_params_path

def main():
	analyze_data()

def analyze_data():
	data = np.load(saved_data_file)
	inputs = data["inputs"]
	outputs = data["outputs"]
	class IncrementPlot:
		def __init__(self):
			self.i = 0
		def get_data(self, x=None):
			im = inputs[self.i]
			print(im.shape)
			self.i+=1
			return im
	plot = SpecAnimate(IncrementPlot().get_data)
	plot.run(500)




def train():

	is_use_saved = False


	if (not os.path.exists(saved_data_file)) or (not is_use_saved):
		# get data (TBD: should use tf.data.object.)
		inputs, outputs = gen_data(10000)
		np.savez(saved_data_file, 
				inputs=inputs,
				outputs=outputs)
	else:
		data = np.load(saved_data_file)
		inputs = data["inputs"]
		outputs = data["outputs"]

	batch_size = 32

	tinputs, toutputs = gen_data(300)
	#normalize

	max_val = np.amax(inputs)
	np.savez(process_params_path,
		max_val=max_val)

	tinputs = tinputs/max_val
	inputs = inputs/max_val

	# create model
	detector = SirenDetection()

	# train	
	detector.compile(optimizer=tf.keras.optimizers.Adam(0.002),
		loss=tf.keras.losses.MSE,
		metrics=["accuracy"])
	detector.fit(inputs, outputs, batch_size=batch_size, epochs=1)

	# test
	print("model accuracy on truth:")
	detector.evaluate(tinputs, toutputs)


	print("model accuracy on random baseline:")
	detector.evaluate(tinputs, np.random.randint(2, size=toutputs.shape))

	print(np.concatenate((np.round(detector(tinputs[:batch_size])), toutputs[:batch_size].reshape(-1,1)),-1))

	detector.save_weights(save_file)



if __name__ == '__main__':
	main()


