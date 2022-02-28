from mpmath import *
import numpy as np
import matplotlib.pyplot as plt

mp.dps = 10
mp.pretty = True

print('First 100 Riemann zeta function zeros with 10 digits of precision')
s_i = np.arange(0,50,0.01)
z_r = s_i * 0
z_i = s_i * 0

k = 0
for i in s_i:
    z = zeta(0.5 +i*1j)
    z_r[k] = z.real
    z_i[k] = z.imag
    k += 1


fig = plt.figure(figsize=(10, 10), frameon=False)
ax = fig.add_subplot()
#ax = plt.axes(xlim=(-2, 6), ylim=(-3, 3))  # create an axes object
plt.plot(z_r, z_i, lw=2, color='g')
plt.show()
