'''
Records Audio from built-in microphone and stores samples
in a shared memory buffer

Required:
    numpy
    sounddevice
'''

import numpy
import sounddevice as sd

SAMPLING_RATE = 48000
BUFFER_LENGTH = 0.1 # In seconds