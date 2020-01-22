'''
Emerge'N'See

Usage: python3 <file_name> <wav_file>

Required:
    numpy
    matplotlib
'''

import numpy as np
from scipy import ndimage
import sys
import time
import matplotlib.pyplot as plt
from objects import AudioObject

class AudioAnalyzer:
    # Constants
    # For plotting
    F_MIN = 0
    F_MAX = 2000

    # For windowing (sliding window)
    WIN_DURATION = 0.1  # in seconds
    STEP_SIZE = 0.1     # in seconds
    

    def plot(self, x1, y1, x2, y2, x3, y3, filename='Audio File', hold=True):
        plt.gcf().clear()

        # Audio Signal
        plt.subplot(3, 1, 1)
        plt.plot(x1, y1)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        plt.grid(True, linestyle = 'dotted', linewidth = '1')
        plt.title('FFT for {}'.format(filename))

        # Frequency
        plt.subplot(3, 1, 2)
        plt.plot(x2, y2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude (V)')
        plt.grid(True, linestyle = 'dotted', linewidth = '1')

        # Frequency (dB)
        plt.subplot(3, 1, 3)
        plt.plot(x3, y3)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.grid(True, linestyle = 'dotted', linewidth = '1')

        plt.pause(0.0001)
        plt.show(block = hold)

    # Returns frequency domain analysis of samples (discards negative frequencies)
    # Applies a Hanning window to the samples
    # Returns numpy array 
    def get_frequencies(self, samples):
        # Apply Hanning window to the samples
        windowed_samples = np.multiply(samples, np.hanning(len(samples)))
        freq = np.abs(np.fft.rfft(windowed_samples))    # np.abs() returns the magnitude of the returned complex fft results
        return freq[0:int(len(samples)/2)]  # Discard negative half of fft
    
    # Converts array of values to dB - this formula was gathered from the internet
    # Might need to do more research into whether this is correct
    def convert_to_db(self, values):
        return 20*np.log10(values / values.max())

    def analyze(self):
        i = 0
        if self.realtime:
            window = self.audio.read_audio_data()
            audio_len = self.audio.BUFFER_DURATION  # in seconds
        else:
            window = self.audio.get_window(i, self.WIN_DURATION, self.STEP_SIZE)
            audio_len = self.WIN_DURATION   # in seconds

        freq_accum = None        
        while window.any():
            # Perform fft
            freq = self.get_frequencies(window)
            freq_db = self.convert_to_db(freq)

            # Preprocess
            # standarization
            mean_freq = np.average(freq)
            std_freq = np.std(freq)
            freq = (freq - mean_freq)/std_freq

            # Gaussian Filter
            #freq = ndimage.gaussian_filter1d(freq,1)
            
            # Accumulate frequencies
            if freq_accum is None:
                freq_accum = np.expand_dims(freq,0) 
            else:
                if not np.all(freq == freq_accum[-1]):
                    freq_accum = np.concatenate((freq_accum, np.expand_dims(freq,0)), axis = 0)
                    freq_accum = freq_accum[-10:]

            weights = np.arange(len(freq_accum))+1
            weights =[np.power(weights,3)]*len(freq_accum[0])
            weights = np.transpose(weights)
            weights = weights/np.max(weights)
            freq_db = np.average(freq_accum,0,weights=weights)

            # Signal/Time plot
            if self.realtime:
                w_start_time = i * audio_len
            else:
                w_start_time = 0
           
            w_end_time = w_start_time + audio_len
            x_time = np.linspace(w_start_time, w_end_time, len(window))

            # Frequency / Time plot - freq array is dependent on length of audio
            min_pos = int(self.F_MIN * audio_len)   # position in the freq array corresponding to f_min
            max_pos = int(self.F_MAX * audio_len)
            x_freq = np.linspace(self.F_MIN, self.F_MAX, max_pos - min_pos)

            # Plotting            
            title = '{}: Time {}s - {}s'.format("Audio", w_start_time, w_end_time)
            self.plot(x_time, window, x_freq, freq[min_pos:max_pos], x_freq, freq_db[min_pos:max_pos], title, hold=False)

            # Next window
            i += 1
            if self.realtime:
                window = self.audio.read_audio_data()
            else:
                # LOOP delay in sec
                time.sleep(0.05)
                window = self.audio.get_window(i, self.WIN_DURATION, self.STEP_SIZE)

    
    def __init__(self):
        self.audio = AudioObject()
        if len(sys.argv) >= 2:
            self.audio.read_wav(sys.argv[1])
            self.realtime = False
        else:
            self.audio.init_mem(create=False)
            self.realtime = True

        self.analyze()



# Run Program
AudioAnalyzer()