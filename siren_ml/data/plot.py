import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SpecAnimate():
	def __init__(self, func, **kwargs):
		self.func = func
		z = self.func()
		self.fig = plt.figure()
		ax2 = plt.subplot()
		#ax2.set_ylim(5,120)
		self.quad1 = ax2.pcolormesh(z)


	def _animate(self,iter):
		z = self.func()
		self.quad1.set_array(z.ravel())
		return self.quad1

	def run(self, interval=30):
		#interval is the delay in miliseconds
		anim = animation.FuncAnimation(self.fig, self._animate,
			frames=100,interval=interval,blit=False,repeat=True)
		plt.show()