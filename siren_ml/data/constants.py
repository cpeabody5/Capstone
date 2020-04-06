import numpy as np

# general settings for mel spectrogram
default_mel = 128
default_hop_length = 512
max_amp = 0.3
sound_amplitude = [0.0000001,1] # amplitude for sounds

# general range constraints for wave generation
phase_shift = [0,2*np.pi] # The possible phase shifts we can have
freq_range = [0,8000] #this is the range of frequencies we can have with our mel spec.
f_range = [0.0001, 50] # arbitrarily picked
offset_range = [0, 8000]


# Siren Parameters
waveform_choices = {
	"cos":np.cos, 
	"square":lambda x: np.round(((np.cos(x)+1)+0.01*np.sin(x))/2),
	"linear":lambda x: x
	}

siren_amp = [200,500]
siren_f = [0.25,4]
siren_offset = [500,1500]
siren_waveform = ["cos", "square"]


