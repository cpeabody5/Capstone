"""constants and functions used by both train.py and test.py
"""

import numpy as np

from data import GenerateData
import time

import os


save_folder = "saved"
if not os.path.exists(save_folder):
	os.mkdir(save_folder)
save_file = os.path.join(save_folder, "model.h5")
saved_data_file = os.path.join(save_folder, "data.npz")
process_params_path = os.path.join(save_folder, "process_params.npz")


def gen_data(x=10000):
	# get data statistics. (amount of noise etc.)
	t = time.time()
	dset = None
	labels = None
	for i in range(x):
		MelData = GenerateData(samplerate=16000, time=0.5)
		if np.random.randint(2):
			MelData.generate_siren()
		MelData.add_noise(is_structured=1)
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