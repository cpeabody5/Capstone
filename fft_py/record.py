'''
Records Audio from built-in microphone and stores samples
in a shared memory buffer

Required:
    numpy
    sounddevice
'''

import numpy
import sounddevice as sd
from multiprocessing import shared_memory

# Configuration parameters
SAMPLING_RATE = 48000
DURATION = 0.1 # In seconds

def main():
    sd.default.samplerate = SAMPLING_RATE
    sd.default.channels = 1
    
    # Listening Loop
    while(True):
        audio_samples = sd.rec(int(DURATION * SAMPLING_RATE), dtype='float16', blocking=True)
        


# Run program
main()