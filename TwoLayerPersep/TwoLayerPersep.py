import numpy as np

class TwoLayerPersep:
	def __init__(self, x: np.array, weights_2: np.array, weights_3: np.array, y_expected: float, 
			  max_fault: float):
		self.__w2 = [weights_2]
		self.__w3 = [weights_3]
		self.__x = x
		self.__y_expected = y_expected
		self.__max_fault = max_fault
		self.learn()

	def activation_func(self, xw):
		return 1 / (1 + np.exp(-xw))
		#return np.tanh(xw)

	def predict(self, x):
		y2 = np.zeros(len(self.__w3[-1]))
		for i in range(len(self.__w3[-1])):
			y2[i] = self.activation_func(np.sum(self.__x * self.__w2[-1][:,i]))

		return self.activation_func(np.sum(y2 * self.__w3[-1]))

	def learn(self):
		x2 = []
		y2 = []
		x3 = []
		y3 = []
		fault = []
		delta3 = []
		delta_w3 = []
		delta2 = []
		delta_w2 = []

		temp_x = np.ones((len(self.__w3[-1])))
		temp_y = np.ones((len(self.__w3[-1])))
		while 1:
			for j in range(len(self.__w3[-1])):
				temp_x[j] = np.sum(self.__x * self.__w2[-1][:,j])
				temp_y[j] = self.activation_func(temp_x[j])

			x2.append(np.copy(temp_x))
			y2.append(np.copy(temp_y))
			x3.append(np.sum(y2[-1] * self.__w3[-1]))
			y3.append(self.activation_func(x3[-1]))
			fault.append(abs((self.__y_expected - y3[-1]) / self.__y_expected))
			
			if fault[-1] <= self.__max_fault: 
				print("On iteration %i found optimal weights." %len(y3))
				print("W2:")
				print(self.__w2[-1])
				print("W3:")
				print(self.__w3[-1])
				break
			
			delta3.append(y3[-1] * (1 - y3[-1]) * (self.__y_expected - y3[-1]))
			delta_w3.append(x3[-1] * delta3[-1])
			self.__w3.append(self.__w3[-1] + delta_w3[-1])

			delta2.append(y2[-1] * (1 - y2[-1]) * (delta3[-1] * self.__w3[-1]))
			delta_w2.append(x2[-1] * delta2[-1])
			self.__w2.append(self.__w2[-1] + delta_w2[-1])