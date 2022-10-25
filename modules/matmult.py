import math
#Takes in a scalar and a matrix and returns a matrix representing the result of scalar multiplcation between the two
def mult_scalar(matrix, scale):
	result = []
	for row in range(len(matrix)):
		temp = []
		for col in range(len(matrix[row])):
			temp.append(matrix[row][col]*scale)
		result.append(temp)
	return result

#Takes in two matrices and returns a matrix representing the result of matrix multiplication between the two matrices
def mult_matrix(a, b):
	result = []
	if len(a[0]) != len(b):
		return None
	for row_a in range(len(a)):
		temp = []
		for col_b in range(len(b[0])): #assuming the list is in the shape of a rectangle
			dot_product = 0 
			for i in range(len(a[row_a])):
				dot_product += a[row_a][i] * b[i][col_b]
			temp.append(dot_product)
		result.append(temp)	
	return result

#Takes in two vectors and returns the euclidean distance between them
def euclidean_dist(a, b):
	sum = 0
	for i in range(len(a[0])):
		sum += (a[0][i]-b[0][i])**2
	return math.sqrt(sum)