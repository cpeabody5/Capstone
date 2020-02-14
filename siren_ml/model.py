import tensorflow as tf 
import numpy as np 

class SirenDetection(tf.keras.Model):
	def __init__(self, num_outputs=1, name="SirenDetection", **kwargs):
		super().__init__(name=name, **kwargs)
		self.num_outputs = num_outputs
		self._create_model()

	def _create_model(self):
		self.model = tf.keras.Sequential((
				tf.keras.layers.Flatten(),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.tanh),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.tanh),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.tanh),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.tanh),
				tf.keras.layers.Dense(self.num_outputs, activation=tf.keras.activations.sigmoid)
			))

	def call(self, inputs):
		#model takes in inputs and returns output
		return self.model(inputs)

def main():
	# load in mnist
	mnist = tf.keras.datasets.mnist
	(x,y), (xt,yt) = mnist.load_data()
	x,xt = x/255, xt/255
	#y = tf.one_hot(y,10).numpy()
	#yt = tf.one_hot(yt,10).numpy()


	detector = SirenDetection(10)

	detector.compile(optimizer=tf.keras.optimizers.Adam(),
		loss=tf.keras.losses.SparseCategoricalCrossentropy(True),
		metrics=["accuracy"]
		)
	detector.fit(x, y, batch_size=32, epochs=2)

	detector.evaluate(xt,yt)
	np.random.shuffle(yt)
	detector.evaluate(xt,yt)


def test1():
	inputs = np.random.normal(size=(10,5,5))
	outputs = np.random.normal(size =(10,2))
	detector = SirenDetection()
	detector(inputs)
	w1 = detector.get_weights()
	detector.compile(optimizer=tf.keras.optimizers.Adam(),
		loss=tf.keras.losses.MSE)
	detector.fit(inputs, outputs, batch_size=2, epochs=1)
	w2 = detector.get_weights()
	assert not (w1[0]==w2[0]).all(), "weights are not being trained"
if __name__ == '__main__':
	main()