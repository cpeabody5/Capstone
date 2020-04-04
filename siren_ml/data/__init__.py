import numpy as np
import matplotlib.pyplot as plt
#import tensorflow as tf
import librosa.feature
import time
from scipy import signal

import sounddevice as sd

if not __name__ == '__main__':
	from . import sharedmemory
	from .plot import SpecAnimate 
	from .spectrogram import GenerateData
	from .spectrogram_functions import LiveMelSpectrogram
else:
	import sharedmemory
	from plot import SpecAnimate 
	from spectrogram import GenerateData
	from .spectrogram_functions import LiveMelSpectrogram



