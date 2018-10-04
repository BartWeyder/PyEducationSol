import math
import numpy as np
import csv

#to import from archives
from tensorflow.contrib.learn.python.learn.datasets.mnist import extract_images, extract_labels

with open('train-images-idx3-ubyte.gz', 'rb') as f:
	train_images = extract_images(f)

with open('train-labels-idx1-ubyte.gz', 'rb') as f:
	train_labels = extract_labels(f)

with open('train-labels-idx1-ubyte.gz', 'rb') as f:
	test_labels = extract_labels(f)

with open('t10k-images-idx3-ubyte.gz', 'rb') as f:
	test_images = extract_images(f)

def recognize(test_image):
	sigma = 0.5 ** 2
	y = list(range(10))
	for i in range(10):
		y[i] = 0
		for m in range(len(train_labels)):
			if i == train_labels[m]:
				y[i] += math.exp(-sum((train_images[m] - test_image) ** 2) / sigma)

	return np.argmax(y)

#to import from server:
#import tensorflow as tf
#from tensorflow import keras
#(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# define how many train examples and tests you want to do:
train_count = 60000
test_count = 10

train_labels = train_labels[:train_count]
test_labels = test_labels[:test_count]
# norming values
train_images = train_images[:train_count].reshape(-1, 28 * 28) / 255.0
test_images = test_images[:test_count].reshape(-1, 28 * 28) / 255.0

result = []

# this loop writes output of recognition to csv file
with open('recs.csv', 'w') as f:
	recs = csv.writer(f,delimiter = ',')
	recog_result = 0
	for i in range(len(test_images)):
		recog_result = recognize(test_images[i])
		if recog_result == test_labels[i]:
			result.append(1)
			recs.writerow([recog_result, test_labels[i], 1])
		else:
			result.append(0)
			recs.writerow([recog_result, test_labels[i], 0])

	print(sum(result)/len(result))