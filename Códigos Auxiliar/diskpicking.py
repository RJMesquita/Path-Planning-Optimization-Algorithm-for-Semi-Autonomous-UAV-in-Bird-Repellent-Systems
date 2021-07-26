import numpy as np
from matplotlib import pyplot as plt

dx = np.zeros(2000)
dy = np.zeros(2000)
for i in range(2000):
    r = np.sqrt(np.random.random(1))
    theta = 2 * np.pi * np.random.random(1)
    dx[i] = r * np.cos(theta)
    dy[i] = r * np.sin(theta)
t = np.linspace(0,np.pi*2,100)
plt.plot(dx,dy,'r.')
plt.plot(np.cos(t), np.sin(t), linewidth=1,color = 'black')

plt.savefig('sinc.png', dpi =300)