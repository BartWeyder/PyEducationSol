# first task:

import numpy as np
import pandas as pd
import csv
import math

class PNN:
	def __init__(self, classes='classes.csv', examples='examples.csv'):
		self.classes = np.genfromtxt(classes, delimiter=',', dtype=str)
		self.examples = pd.read_csv(examples, header = None)

	def recognize(self, parameters):
		sigma = 0.5 ** 2
		y = []
		for i in range(self.classes.size):
			y.append(0)
			for m in range(len(self.examples.index)):
				if self.classes[i] == self.examples.at[m, len(self.examples.columns) - 1]:
					y[i] += math.exp(-sum((self.examples.iloc[1,0:(len(self.examples.columns) - 1)] - 
							parameters) ** 2) / sigma)

		return self.classes[np.argmax(y)]

test = PNN()
# this is close to last example, so answer should be 'b'
print(test.recognize([3.7, 3.5, 3.4]))