import tensorflow as tf 
import numpy as np 

class SirenDetection(tf.keras.Model):
	def __init__(self, name="SirenDetection", **kwargs):
		super().__init__(name=name, **kwargs)
		self._create_model()

	def _create_model(self):
		self.model = tf.keras.Sequential((
				tf.keras.layers.Flatten(),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
				tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
				tf.keras.layers.Dense(2, activation=tf.keras.activations.softmax)
			))

	def call(self, inputs):
		#model takes in inputs and returns output
		return self.model(inputs)

def main():
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