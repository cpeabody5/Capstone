"""This file includes frequency and amplitude objects, 
and effects that would be applied directly on one frequency 
structure.
"""
import numpy as np
try:
	from . import constants as cn
	from . import frequency_functions as ff
except ImportError:
	import constants as cn
	import frequency_functions as ff


class _GenerateFreqMeta(type):
	#makes sure that the required attributes and methods are specified.
	def __new__(cls, name, bases, body):
		print(body, bases)
		required_methods = {
			"amplitude_func":"amplitudes must be specified and takes in timesteps in seconds and frequency in Hz, should return a matrix of the same shape as the frequency input",
			"frequency_func":"This should take in the timestep input, in seconds and output a 2D matrix of [frequency traversal, frequency value]",
			}
		for method, explanation in required_methods.items():
			if name is not "_GenerateFreq" and not method in body:
				raise TypeError("You must specify %s as a method in your frequency class. %s"%(method, explanation))
		return super().__new__(cls, name, bases, body)


class _GenerateFreq():#metaclass=_GenerateFreqMeta):
	#inhereted class
	def add_doppler_effect(self, source_speed=100/3.6, observer_velocity=60/3.6): #TBD: convert delay to incoming speed, and position
		"""Speed is in meters per second
			- specify direction of increase or decrease
		"""
		speed_of_sound = 343
		def frequency(**kwargs):
			freq = self.frequency(**kwargs)
			freq = np.where(freq>=0, (speed_of_sound+observer_velocity)/(speed_of_sound-source_speed)*freq, freq)
		self.frequency = frequency			

	def add_echoing_effect(self, sd_distance, deflect_ang, dd_distance): 
		#sd_distance is the source to deflection distance
		#deflect_ang is the deflection angle
		#dd_distance is the deflection to destination (listener) distance  
		#TBD: add the echoing effect as a factor of a deflecting surface, and two distances (signal source, and user pos)
		# this could be done in a finite state manner, where we can add more for multiple signals and complexity.
		pass

	def add_partial_occlusions(self, spec, min_show_period):
		# min_show period is the amount of frames needed to show the the siren in a continuous amount of time.
		return spec

	def sound_diffraction(self, matrix):
		# deffracts the sound as if going through a medium.
		# similar to going into water.
		pass

class SirenFreq(_GenerateFreq):

	def __init__(self, amp=cn.siren_amp, f=cn.siren_f, offset=cn.siren_offset, 
		waveform=cn.siren_waveform, phase_shift=cn.phase_shift, sound_amplitude=cn.sound_amplitude, 
		verbose=False, **kwargs):
		"""initializes a siren signal.
	
		
		Args:
		    doppler (bool): True if want doppler effect # TBD: add randomization
		    amp (None, float): amplitude of siren sweep
		    f (None, float): frequency of siren sweep
		    offset (None, float): offset o siren sweep
		    waveform (None, string): see waveform_choices for list of available waveforms, should be a stric to choose from there.
		"""
		# set siren parameters, will be amp*waveform(2*pi*f*t)+offset
		self.frequency = ff.Wave(waveform=waveform, amp=amp, f=f, phase_shift=phase_shift, offset=offset)
		
		# save parameters
		self.freq_params = {
			"f":self.frequency.f, 
			"amp":self.frequency.amp, 
			"offset":self.frequency.offset, 
			"waveform":self.frequency.waveform, 
			"phase_shift":self.frequency.phase_shift}
		
		# define these here so they can be extracted for later.
		if verbose:
			print("\tFrequency: {}\n\tAmplitude: {}\n\tOffset: {}\n\tFunc: {}\n---".format(*list(self.freq_params.values())))

		self.sound_amplitude = sound_amplitude

	def amplitude_func(self, timesteps, freq):
		#TBD: should randomize this according to distance
		distributional_sound_amp = lambda size: np.random.normal(0.001, cn.max_amp/12, size=size)

		gain = ff.choose_random_in_range(self.sound_amplitude, 
			distribution_to_choose=distributional_sound_amp)
		gain = np.ones(freq.shape)*gain
		amps = ff.choose_random_in_range([gain*0.7,gain*1.3]) #noises with 0.3 spread
		amps = np.minimum(amps, 1)
		amps = np.maximum(amps, 0)
		return amps

	def frequency_func(self, timesteps):
		#generate waveform
		#TBD: save the parameters below into a file when logging (save to database)
		freq = self.frequency(timesteps) #eg. freq = -500*np.cos(2*np.pi*timesteps*1)+1000
		return freq

class StructuredNoise(SirenFreq):
	def __init__(self, min_num_diff=2,**kwargs):
		"""Create this Noise basically the same way as the 
		siren specifications, just different parameters.

		Args:
			min_num_diff: this is the minimum number of different parameters we 
				can have with the siren The lower the number, the harder it is to distinguish from a siren
				The higher it is, the easier it is to distinguish.

		"""
		assert min_num_diff >=1 or min_num_diff<=4, "min_num_diff must be between 1 and 4 (inclusive)"
		# For this noise
		choices = ["a", "f", "o", "w"]
		np.random.shuffle(choices)
		choices = choices[:min_num_diff]

		amp=cn.siren_amp
		f=cn.siren_f
		offset=cn.siren_offset
		waveform=list(cn.waveform_choices.keys())

		# change selected choices to be different from a siren
		if "a" in choices:
			amp = [cn.freq_range[0], cn.siren_amp[0]-1, cn.siren_amp[1]+1, cn.freq_range[0]]
		if "f" in choices:
			f = [cn.f_range[0], cn.siren_f[0]-1, cn.siren_f[1]+1, cn.f_range[0]]
		if "o" in choices:
			offset = [cn.offset_range[0], cn.siren_offset[0]-1, cn.siren_offset[1]+1, cn.offset_range[0]]
		if "w" in choices:
			waveform = [i for i in waveform if not i in cn.siren_waveform]

		phase_shift=cn.phase_shift
		sound_amplitude=cn.sound_amplitude

		super().__init__(amp=amp, f=f, offset=offset, 
		waveform=waveform, phase_shift=phase_shift, sound_amplitude=sound_amplitude)



if __name__ == '__main__':
	main()

'''
	def generate_siren(self, doppler=False, amp=None, f=None, offset=None, waveform=None, verbose=False):
		"""generates the siren over a 2d array, bin size for time and frequency should be given as well
		this should start out with a sweep  then become more siren like.
	
		
		Args:
		    doppler (bool): True if want doppler effect # TBD: add randomization
		    amp (None, float): amplitude of siren sweep
		    f (None, float): frequency of siren sweep
		    offset (None, float): offset o siren sweep
		    waveform (None, string): see waveform_choices for list of available waveforms
		"""
		self.label = np.ones(())

		waveform_choices = {
			"cos":np.cos, 
			"square":lambda x: np.round(((np.cos(x)+1)+0.01*np.sin(x))/2),
			}
		

		# NOTE: min and max vals can be constants as well to ony need 1 random function
		def rand(mini=0, maxi=1):
			# random selection funcion
			return (maxi - mini) * np.random.random() + mini

		# set siren parameters, will be amp*waveform(2*pi*f*t)+offset
		waveform = waveform if not waveform is None else np.random.choice(list(waveform_choices.keys()))
		amp = amp if not amp is None else rand(200,500)
		f = f if not f is None else rand(0.25, 4)
		offset = offset if not offset is None else rand(500,1500)


		# get waveform
		if not waveform in waveform_choices:
			raise Exception("warning, waveform unknown")
		waveform = waveform_choices[waveform]
		
		# define these here so they can be extracted for later.
		self.freq_params = {
				"f":f,
				"amp":amp,
				"offset":offset,
				"waveform":waveform
			}
		if verbose:
			print("\tFrequency: {}\n\tAmplitude: {}\n\tOffset: {}\n\tFunc: {}\n---".format(*list(self.freq_params.values())))
		
		def frequency_func(timesteps):
			#generate waveform
			#TBD: save the parameters below into a file when logging (save to database)
			freq = amp * waveform(2*np.pi*f*timesteps) + offset #eg. freq = -500*np.cos(2*np.pi*timesteps*1)+1000

			#Add Doppler effect
			if doppler:
				freq = self.add_doppler_effect(freq)
			return freq

		def amplitude_func(timesteps,freq):
			#TBD: should randomize this according to distance
			amps = freq*0+1
			return amps

		# TBD should keep information about 
		spec = self.create_melspec(frequency_func, amplitude_func)
		self.spec +=spec
'''