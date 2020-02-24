# must use python 3.7
import numpy as np
import tensorflow as tf

from data import LiveMelSpectrogram
from data import GenerateData
from model import SirenDetection
import time

import os

def gen_data(x=10000):
	# get data statistics. (amount of noise etc.)
	t = time.time()
	dset = None
	labels = None
	for i in range(x):
		MelData = GenerateData(samplerate=16000, time=0.5)
		if np.random.randint(2):
			MelData.generate_siren()
		MelData.add_noise(np.abs(np.random.normal(0,0.25)))
		spec = MelData.mfcc
		label = MelData.label #TBD: this should be length of time series, which indicates siren at each point
		if dset is None:
			dset = np.empty((x,*spec.shape))
			labels = np.empty((x,*label.shape))
		dset[i] = spec
		labels[i] = label

	tim = time.time()-t
	print(dset.shape)
	tps = tim/x
	print("%f s per sample, %f per %d samples"%(tps,tim, x))

	#l = np.random.randint(2, size=(x))
	#labels = np.zeros((l.size,2))
	#labels[np.arange(l.size),l] = 1
	return dset, labels

def test():
	save_folder = "saved"
	if not os.path.exists(save_folder):
		os.mkdir(save_folder)
	save_file = os.path.join(save_folder, "model.h5")
	process_params = os.path.join(save_folder, "process_params.npz")
	process_params = np.load(process_params)
	
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

def train():
	save_folder = "saved"
	if not os.path.exists(save_folder):
		os.mkdir(save_folder)
	save_file = os.path.join(save_folder, "model.h5")
	saved_data_file = os.path.join(save_folder, "data.npz")
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
	np.savez(os.path.join(save_folder, "process_params"),
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


