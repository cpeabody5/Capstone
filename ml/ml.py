# must use python 3.7

from data import MelSpectrogram
from data import GenerateData
import time

def main():
	t = time.time()
	x = 100000
	for i in range(x):
		MelData = GenerateData(samplerate=16000, time=5)
		MelData.generate_siren()
		MelData.add_noise()
	tim = time.time()-t
	print(MelData.spec.shape)
	tps = tim/x
	print("%f s per sample, %f per %d samples"%(tps,tim, x))





if __name__ == '__main__':
	main()


