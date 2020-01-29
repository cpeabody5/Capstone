import record
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import tensorflow as tf
import librosa.feature
import time

import sounddevice as sd

class SpecAnimate():
	def __init__(self, func, **kwargs):
		self.func = func
		z = self.func()
		self.fig = plt.figure()
		ax2 = plt.subplot()
		#ax2.set_ylim(5,120)
		self.quad1 = ax2.pcolormesh(z)


	def _animate(self,iter):
		z = self.func()
		self.quad1.set_array(z.ravel())
		return self.quad1

	def run(self):
		anim = animation.FuncAnimation(self.fig, self._animate,
			frames=100,interval=30,blit=False,repeat=True)


		plt.show()
class MelSpectrogram():
	def __init__(self):
		self.recorder = record.AudioRecorder() # real time data
		self.sample_rate = self.recorder.audio.DEFAULT_SAMPLE_RATE
		self.num_samples = self.recorder.audio.BUFFER_DURATION*self.sample_rate
		self.sample_accum = None

	def create_ms(self,new_samples=None,sr=None): #using librosa
		"""
		if new_samples is None, samples will come from live audio 
		"""
		if new_samples is None:
			new_samples = self.recorder()
			sr = self.sample_rate
		else:
			assert not sr is None, "sr, sample rate must be defined if new_samples is specified."
		
		spectrogram = librosa.feature.melspectrogram(
					y=new_samples, sr=sr, n_mels=128)
		return np.log10(spectrogram)

	def accum_live_ms(self, spectrogram_accum_frames=50):
		while 1:
			spectrogram = self.create_ms()
			if self.sample_accum is None:
				self.sample_accum = spectrogram
			else:
				self.sample_accum = np.concatenate((
						self.sample_accum, spectrogram),1)[:,-spectrogram_accum_frames:]
			if self.sample_accum.shape[-1] >= spectrogram_accum_frames:
				break

		return self.sample_accum

class GenerateData():
	"""
	generates siren noise in an environment
	Accounts for:
	- Changes in amplitues.
	- Doppler effect
	- Echoing
	- Noisy environments
		- white noise
		- structured noise
	- distractors
		- non siren audio with similar sound range, different structure
		- non siren audio with similar structure, different sound
	- partial occlusions of siren
		- must have a minimum audible time. 
	- new siren noise types

	Final test dataset will be real siren audio
	"""
	def __init__(self):
		time = 2
		frequency = 440
		# Generate time of samples between 0 and two seconds
		samples = np.arange(44100 * time) / 44100.0
		# Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
		
		np.fft.ifft(frequency*np.ones(samples), len(samples))
		#wave = 10000 * np.sin(2 * np.pi * frequency * samples)
		
		# Convert it to wav format (16 bits)
		wav_wave = np.array(wave, dtype=np.int16)

		sd.play(wav_wave, blocking=True)


def main():
	# view mel spectrogram of live audio
	func = GenerateData()



if __name__ == '__main__':
	main()