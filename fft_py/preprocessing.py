def moving_avg(matrix, **kwargs):
	weights = np.arange(len(matrix))+1
	weights =[np.power(weights,3)]*len(matrix[0])
	weights = np.transpose(weights)
	weights = weights/np.max(weights)
	freq_db = np.average(matrix,0,weights=weights)
	return matrix

