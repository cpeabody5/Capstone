'''
Emerge'N'See

Usage: python3 <file_name> <wav_file>

'''

from scipy.io import wavfile
import numpy as np
import sys
import time
import matplotlib.pyplot as plt

def plot(x1, y1, x2, y2, x3, y3, filename='Audio File', hold=True):
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


def main():
    # Read wave file specified in command line args
    filename = sys.argv[1]
    fs, data = wavfile.read(filename)   # returns sampling frequency and data
    audio_len = len(data) / fs  # Audio length in seconds

    # Sliding Window
    window_sec = 0.1    # number of seconds in the window
    window_samples = int(window_sec * fs)   # number of samples in the window
    step_size = 0.1     # number of seconds to step the window by

    for i in range(0, len(data) - window_samples, int(step_size * fs)):
        # Current Window & Window parameters
        window = data[i : i+window_samples]     # Actual samples in the window
        w_start_time = float(i) / fs
        w_end_time = float(i+window_samples) / fs

        # Perform fft
        # Apply Hanning window to the samples
        windowed_samples = np.multiply(window, np.hanning(window_samples))
        freq = np.abs(np.fft.rfft(windowed_samples))    # np.abs() returns the magnitude of the returned complex fft results
        freq = freq[0:int(len(window)/2)]  # Discard negative half of fft

        # Plot - freq array is dependent on length of audio
        f_min = 0
        f_max = 20000
        min_pos = int(f_min * window_sec)   # position in the freq array corresponding to f_min
        max_pos = int(f_max * window_sec)

        # Setting up Axes and data for the plots
        x_freq = np.linspace(f_min, f_max, max_pos - min_pos)
        # Converting freq values to dB -- got this formula off the internet, need to confirm if correct
        y_freq = 20*np.log10(freq[min_pos:max_pos] / freq[min_pos:max_pos].max())   

        # Time (for audio signal plot)
        x_time = np.linspace(w_start_time, w_end_time, window_samples)
        title = '{}: Time {}s - {}s'.format(filename, w_start_time, w_end_time)
        plot(x_time, window, x_freq, freq[min_pos:max_pos], x_freq, y_freq, title, hold=False)
        
        # LOOP delay in s
        time.sleep(0.05)

# Run Program
main()