'''
Required:
	numpy
	scipy
	SharedArray
	atexit
'''

import numpy as np 
from scipy.io import wavfile
import atexit

class AudioObject:
	'''
	Keeps track of reading & writing audio samples and manages
	shared memory relating to audio segments
	'''
	def __init__(self, DEFAULT_SAMPLE_RATE=9000, BUFFER_DURATION=0.03, 
								SHARED_MEM_NAME='shm://capstone-memory-buffer'):
		self.DEFAULT_SAMPLE_RATE = DEFAULT_SAMPLE_RATE
		self.BUFFER_DURATION = BUFFER_DURATION   # in seconds
		self.SHARED_MEM_NAME = SHARED_MEM_NAME
		self.data = np.array([], dtype=np.float32)
		self.fs = self.DEFAULT_SAMPLE_RATE
		self.is_shared_memory = False

	# reads from wav file & populates data field
	def read_wav(self, filename):
		fs, data = wavfile.read(filename)
		self.fs = fs
		self.data = data

	# Retrieves given window (window n given window size and step size)
	# n: Window number required (0-indexed, 0 gives first window etc.)
	# window_len: length of window (seconds)
	# step size: number of samples to skip from beginning of one window to the next
	# Returns array, returns empty array if window is out of bounds
	def get_window(self, n, window_len, step_size):
		start_pos = n * int(step_size * self.fs)
		end_pos = start_pos + int(window_len * self.fs)
		if end_pos >= len(self.data):
			return np.array([])
		else:
			return self.data[start_pos : end_pos]

	# Initializes a Memory Location and links self.data to the memory location
	# Does not return anything
	def init_mem(self, create=False):
		self.is_shared_memory = True
		import SharedArray as sa
		num_samples = int(self.BUFFER_DURATION * self.fs)
		if create:
			self.data = sa.create(self.SHARED_MEM_NAME, num_samples, np.float32)
			atexit.register(self.cleanup_mem)	# Run cleanup on exit
		else:
			self.data = sa.attach(self.SHARED_MEM_NAME)
	
	# Deletes shared memory
	def cleanup_mem(self):
		import SharedArray as sa
		print('cleanup memory')
		sa.delete(self.SHARED_MEM_NAME)

	# Writes audio data to shared memory
	def write_audio_data(self, samples):
		self.data[:] = samples[:]   # shallow copy

	# Reads shared memory
	def read_audio_data(self):
		return self.data