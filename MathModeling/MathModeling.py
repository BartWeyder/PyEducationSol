
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def kolmogorov_equations(lambda_in, mu):
    A = np.array([[lambda_in, -mu, 0, 0, 0],
                  [-lambda_in, mu + lambda_in, -2*mu, 0, 0],
                  [1, 1, 1, 1, 1],
                  [0, 0, -lambda_in, 2*mu + lambda_in, -2*mu],
                  [0, 0, 0, -lambda_in, 2*mu]])
    B = np.array([0, 0, 1, 0, 0])
    det = np.array([0, 0, 0, 0, 0, np.linalg.det(A)])
    p = np.array([])
    A_new = np.zeros([5, 5])

    for i in range(5):
        for k in range(5):
            for l in range(5):
                A_new[k, l] = A[k, l]

        for j in range(5):
            A_new[j, i] = B[j]

        det[i] = np.linalg.det(A_new)
        p = np.append(p, [det[i]/det[5]], axis=0)
    return p


def kolmogorov_dif_equations(p, t, lambda_in, mu):
    p0, p1, p2, p3, p4 = p
    return [mu * p1 - lambda_in * p0,
            lambda_in * p0 + 2 * mu * p2 - p1 * (mu + lambda_in),
            lambda_in * p1 + 2 * mu * p3 - p2 * (2 * mu + lambda_in),
            lambda_in * p2 + 2 * mu * p4 - p3 * (2 * mu + lambda_in),
            lambda_in * p3 - 2 * mu * p4]


def loaded_channels_t(p_t): # loaded channels factor
    result = 0
    for i in range(n + m):
        if i <= 1:
            result += i * p_t[:, i]
        elif i > 1:
            result += n * p_t[:, i]
    return result/n


def free_channels_t(p_t): # free channels factor
    result = 0
    for i in range(n):
        if i == 0:
            continue
        result += i * p_t[:, n - i]
    return result/n


# variant 2:
lambda_in = 4.46
mu_out = 2.7
n = 2
m = 2

p = kolmogorov_equations(lambda_in, mu_out)
print("\nProbabilities: ", p)

# parameters:
ro = lambda_in/mu_out
Hi = ro/n
z = ro * (1 - ((ro ** n) * (Hi ** m) * p[0])/math.factorial(n))
P_zk = z/n
r = ((1 - (Hi ** m) * (1 + m - (Hi ** m))) * Hi * p[0] * (ro ** n))/(math.factorial(n) * (1 - Hi ** 2))

print("\nAverage number of busy channels: ", z)
print("\nAverage number of free channels: ", n - z)
print("\nLoaded channels factor: ", P_zk)
print("\nFree channels factor: ", 1 - P_zk)
print("\nAverage number of requests in the queue: ", r)

t = np.linspace(0, 2.5, 5000)
p_start = [1, 0, 0, 0, 0]
p_t = odeint(kolmogorov_dif_equations, p_start, t, (lambda_in, mu_out))

plt.plot(t, p_t[:, 0], color = 'red', label = 'p0(t)')
plt.plot(t, p_t[:, 1], color = 'orange', label = 'p1(t)')
plt.plot(t, p_t[:, 2], color = 'green', label = 'p2(t)')
plt.plot(t, p_t[:, 3], color = 'blue', label = 'p3(t)')
plt.plot(t, p_t[:, 4], color = 'violet', label = 'p4(t)')
plt.ylabel('p(t)')
plt.xlabel('t, hours')
plt.title('Probabilities from time dependency')
plt.legend()
plt.grid()
plt.show()

t = np.linspace(0, 50, 5000)

plt.plot(t, loaded_channels_t(p_t), color = 'red', label = 'loaded channels factor')
plt.plot(t, free_channels_t(p_t), color = 'blue', label = 'free channels factor')
plt.ylabel('factor value(t)')
plt.xlabel('t, hours')
plt.title('Loaded and free channels factors from time dependency')
plt.legend()
plt.grid()
plt.show()