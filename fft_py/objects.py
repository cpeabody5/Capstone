'''
Required:
    numpy
    scipy
    multiprocessing (Needs Python 3.8)
'''

import numpy as np 
from scipy.io import wavfile
from multiprocessing import shared_memory

class AudioObject:
    '''
    Keeps track of reading & writing audio samples and manages
    shared memory relating to audio segments
    '''

    DEFAULT_SAMPLE_RATE = 48000
    BUFFER_DURATION = 0.1   # in seconds
    SHARED_MEM_NAME = 'capstone-memory-buffer'

    def __init__(self):
        self.data = np.array([], dtype=np.float32)
        self.fs = self.DEFAULT_SAMPLE_RATE

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