# must use python 3.7
import numpy as np
import tensorflow as tf

from data import LiveMelSpectrogram
from data import GenerateData

from model import SirenDetection
import time

def gen_data(x=10000):
	t = time.time()
	dset = None
	labels = None
	for i in range(x):
		MelData = GenerateData(samplerate=16000, time=0.5)
		if np.random.randint(2):
			MelData.generate_siren()
		MelData.add_noise(np.abs(np.random.normal()))
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

def main():
	# get data (TBD: should use tf.data.object.)
	inputs, outputs = gen_data(3)
	inputs, outputs = gen_data(100000)
	batch_size = 32

	#normalize

	# create model
	detector = SirenDetection()

	# train	

	detector.compile(optimizer=tf.keras.optimizers.Adam(0.0001),
		loss=tf.keras.losses.MSE,
		metrics=["accuracy"])
	detector.fit(inputs, outputs, batch_size=batch_size, epochs=1)

	# test
	inputs, outputs = gen_data(300)
	print("model accuracy on truth:")
	detector.evaluate(inputs, outputs)


	print("model accuracy on random baseline:")
	detector.evaluate(inputs, np.random.randint(2, size=outputs.shape))

	print(np.concatenate((np.round(detector(inputs[:batch_size])), outputs[:batch_size].reshape(-1,1)),-1))

if __name__ == '__main__':
	main()


