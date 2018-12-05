import numpy as np
import TwoLayerPersep

x = np.array((3,4))
w2 = np.array([[0.5, 0.7, -0.7], [0.64, -0.1, 0.1]])
w3 = np.array((2, 1.5, 3))

pers = TwoLayerPersep.TwoLayerPersep(x, w2, w3, 0.677, 0.001)
print("Output: %f" % pers.predict(x))
