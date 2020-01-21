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
    def main(self):
        sd.default.samplerate = self.audio.fs
        sd.default.channels = 1

        # Listening Loop
        while(True):
            audio_samples = sd.rec(
                int(self.audio.BUFFER_DURATION * self.audio.fs),
                dtype='float32', 
                blocking=True)
            samples = [i[0] for i in audio_samples]
            samples = np.array(samples, dtype=np.float32)
            self.audio.write_audio_data(samples)
            
    def __init__(self):
        self.audio = AudioObject()
        self.audio.init_mem(create=True)
        self.main()

# Run program
AudioRecorder()