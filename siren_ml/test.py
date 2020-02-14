import numpy as np

f = 10
t = 15
bins = np.random.randint(0,f, size=(2,t))
weights = np.random.randint(0,f, size=(2,t))

array = np.zeros((f, t))
array[bins, np.arange(t)] = weights
print(array)
print(bins, weights)