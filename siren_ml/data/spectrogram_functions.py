import numpy as np 
import librosa.feature
import time
import sounddevice as sd
import pathlib
import os
import matplotlib.pyplot as plt
try:
	from . import record
	from . import constants as cn
except ImportError:
	import record
	import constants as cn

def loading_bar(cur, total):
	# this is a general tool that can be used
	# anywhere, move this in the future to the 
	# more appropriate place
	fraction = cur/total
	string = "[%-20s]\t%.2f%%\t%d/%d\t\t"%("="*int(20*fraction), fraction*100, cur, total)
	return string



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

def real_noise(shape):
	return RealNoise()(shape)

class RealNoise():
	"""This is meant to only be a quick test to sample outside noise.
	
	assumes that there is consistent noise. 

	This will sample and get the mean and standard 
	deviation for the noise
	"""
	def __init__(self, save_file="real_noise_sample.npz"):
		base_path = pathlib.Path(__file__).parent.absolute()
		self.save_file = os.path.join(base_path,save_file)

	def __call__(self, shape):
		# applies noise
		# shape must be 3D or 2D tensor, with the -2 dimension the same size as the noise saved.
		assert os.path.exists(self.save_file), "Run RealNoise().sample_noise() first to save parameters."
		data = np.load(self.save_file)
		if len(shape) == 3:
			mean = data["mean"].reshape(1,-1,1)
			std = data["std"].reshape(1,-1,1)
		elif len(shape) == 2:
			mean = data["mean"].reshape(-1,1)
			std = data["std"].reshape(-1,1)
		else:
			raise Exception("Invalid shape ndim")
		assert shape[-2] == mean.shape[-2]
		mean = np.broadcast_to(mean, shape)
		out = np.random.normal(mean, std, size =shape)
		out = np.power(10, out)
		return out


	def sample_noise(self):
		# gets log mel spectrogram noise
		# records, gets the mean and standard deviation
		spec = LiveMelSpectrogram(16000, 0.5)
		func = lambda x=None: np.log10(spec.create_ms())
		accum = None
		num_samples = 10
		for i in range(num_samples):
			print(loading_bar(i+1, num_samples), end = "\r")
			sample = np.average(func(), -1)
			if accum is None:
				accum = np.empty((num_samples, *sample.shape))
			accum[i] = sample
		mean = np.average(accum, axis=0)
		std = np.std(accum, axis=0)
		np.savez(self.save_file, mean=mean, std=std)




class LiveMelSpectrogram():
	def __init__(self, sr=None, t= None, n_mels=cn.default_mel, hop_length=cn.default_hop_length):
		self.recorder = record.AudioRecorder(sr, t) # real time data
		self.live_sample_rate = self.recorder.audio.DEFAULT_SAMPLE_RATE
		self.num_samples = self.recorder.audio.BUFFER_DURATION*self.live_sample_rate
		self.sample_accum = None
		self.n_mels = n_mels
		self.hop_length = hop_length

	def create_ms(self,new_samples=None,sr=None,is_log=False,is_mfcc=False): #using librosa
		"""
		if new_samples is None, samples will come from live audio 
		"""
		if new_samples is None:
			new_samples = self.recorder()
			sr = self.live_sample_rate
		else:
			assert not sr is None, "sr, sample rate must be defined if new_samples is specified."
		
		spectrogram = librosa.feature.melspectrogram(
					y=new_samples, sr=sr, n_mels=self.n_mels, hop_length=cn.default_hop_length)
		
		if is_log or is_mfcc:
			spectrogram = librosa.core.power_to_db(spectrogram)

		if is_mfcc:
			spectrogram = librosa.feature.mfcc(S=spectrogram)

		return spectrogram

	def accum_live_ms(self, spectrogram_accum_frames=50):
		while 1:
			spectrogram = self.create_ms()
			if self.sample_accum is None:
				self.sample_accum = spectrogram
			else:
				self.sample_accum = np.concatenate((
						self.sample_accum, 
						spectrogram),1)[:,-spectrogram_accum_frames:]
			if self.sample_accum.shape[-1] >= spectrogram_accum_frames:
				break

		return self.sample_accum

def main():
	out = real_noise((128, 30))
	plt.pcolormesh(out)
	plt.show()



def view_live_spectrogram():
	from plot import SpecAnimate
	spec = LiveMelSpectrogram(16000, 0.5)
	func = lambda x=None: np.log10(spec.create_ms())
	#plt.pcolormesh(func())
	#plt.show()

	plot = SpecAnimate(func)
	plot.run()




if __name__ == '__main__':
	main()