# must use python 3.7

from data import MelSpectrogram
from data import SpecAnimate


def main():
	# view mel spectrogram of live audio
	func = MelSpectrogram().accum_live_ms
	plot = SpecAnimate(func)
	plot.run()


if __name__ == '__main__':
	main()


