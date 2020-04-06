'''
Records Audio from built-in microphone and stores samples
in a shared memory buffer

Required:
	numpy
	sounddevice
'''

import numpy as np
import sounddevice as sd
from scipy.io import wavfile

class AudioObject:
	'''
	Keeps track of reading & writing audio samples and manages
	shared memory relating to audio segments
	'''
	DEFAULT_SAMPLE_RATE=16000
	BUFFER_DURATION=0.5
	def __init__(self, DEFAULT_SAMPLE_RATE=None, BUFFER_DURATION=None,
								SHARED_MEM_NAME='capstone-memory-buffer'):
		if not DEFAULT_SAMPLE_RATE is None:
			self.DEFAULT_SAMPLE_RATE = DEFAULT_SAMPLE_RATE
		if not BUFFER_DURATION is None:
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
		from multiprocessing import shared_memory
		num_samples = int(self.BUFFER_DURATION * self.fs)
		num_bytes =  num_samples * 4   # float32 - 4 bytes per float
		self.mem = shared_memory.SharedMemory(create=create, size=num_bytes, name=self.SHARED_MEM_NAME)
		self.data = np.ndarray((num_samples,), dtype=np.float32, buffer=self.mem.buf)

	# Writes audio data to shared memory
	def write_audio_data(self, samples):
		self.data[:] = samples[:]   # shallow copy

	# Reads shared memory
	def read_audio_data(self):
		return self.data


class AudioRecorder:

	def __call__(self):
		audio_samples = sd.rec(
			int(self.audio.BUFFER_DURATION * self.audio.fs),
			dtype='float32', 
			blocking=True)
		
		samples = audio_samples[:,0]
		samples = np.array(samples, dtype=np.float32)
		if self.audio.is_shared_memory:
			self.audio.write_audio_data(samples)
		else:
			return samples

	def __init__(self, sr=None, t=None):
		sd.default.channels = 1
		self.audio = AudioObject(sr, t)
		sd.default.samplerate = self.audio.fs
		#self.audio.init_mem(create=True)

# Run program
def main():
	recorder = AudioRecorder()
	while 1:
		print(recorder())

if __name__ == '__main__':
	main()