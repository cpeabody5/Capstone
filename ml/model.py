import tensorflow as tf 
import numpy as np 

class SirenDetection():
	def __init__(self):
		self._create_model()

	def _create_model(self):
		self.model = tf.keras.Sequential(
			(tf.keras.layers.Flatten(),
						tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
						tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
						tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
						tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
						tf.keras.layers.Dense(2, activation=tf.keras.activations.softmax)
						))

	def run(self, inputs):
		#model takes in inputs and returns output
		return self.model(inputs)

	def loss(self, pred, actu):
		# returns the loss
		return tf.keras.losses.MSE(actu, pred)
	
	def train(self, loss, **kwargs):
		# trains the loss functions
		return 

	def save(self, file):
		# saves the model to the file
		pass 

	def load(self, file):
		# loads the model from te file
		pass

def main():
	inputs = np.zeros((4,5,5))
	siren = SirenDetection()
	print(siren.run(inputs))



if __name__ == '__main__':
	main()