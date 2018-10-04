from tensorflow.contrib.learn.python.learn.datasets.mnist import extract_images, extract_labels
import numpy as np

with open('train-images-idx3-ubyte.gz', 'rb') as f:
	train_images = extract_images(f)

with open('train-labels-idx1-ubyte.gz', 'rb') as f:
	train_labels = extract_labels(f)

# norming values
train_images = train_images.reshape(-1, 28 * 28) / 255.0

with open('train_images.txt', 'w') as f:
	i = 0 
	for ar in train_images:
		print(i)
		f.writelines("label: %i \n" % (train_labels[i]))
		# values rounded to 2 decimals
		ar = np.reshape(ar, (28,28))
		np.savetxt(f, ar, '%.2f', delimiter = ';')
		i += 1

np.savetxt('train_labels.txt', train_labels)