
import matplotlib.pyplot as plt
import numpy as np

N = 10000

def P(x, y):
    return (x + y) ** 2 - 1

def Q(x, y):
    return 1 - x**2 - y**2

def Vx_wave(Vx, Vy):
    return Vx/np.sqrt(Vx ** 2 + Vy ** 2)

def Vy_wave(Vx, Vy):
    return Vy/np.sqrt(Vx ** 2 + Vy ** 2)

def get_phase_portrait_const(n, N, x, y, alpha_x, alpha_y):  # for constant alphas case
    for i in range(n):
        for k in range(N-1):
            Vx = P(x[i, k], y[i, k])
            Vy = Q(x[i, k], y[i, k])
            x[i, k + 1] = x[i, k] + alpha_x * Vx_wave(Vx, Vy)
            y[i, k + 1] = y[i, k] + alpha_y * Vy_wave(Vx, Vy)
        plt.plot(x[i], y[i], 'b')
    plt.axis([-3, 8, -3, 8])
    plt.show()

x = np.zeros((1,N))
x[0,0] = 1.0001
get_phase_portrait_const(1, N, x, np.zeros((1,N)), 0.001, 0.001)