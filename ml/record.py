'''
Records Audio from built-in microphone and stores samples
in a shared memory buffer

Required:
	numpy
	sounddevice
'''

import numpy as np
import sounddevice as sd
from objects import AudioObject

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

	def __init__(self):
		sd.default.channels = 1
		self.audio = AudioObject()
		sd.default.samplerate = self.audio.fs
		#self.audio.init_mem(create=True)

# Run program
def main():
	recorder = AudioRecorder()
	while 1:
		print(recorder())

if __name__ == '__main__':
	main()