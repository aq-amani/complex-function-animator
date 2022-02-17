import numpy as np
import mpmath
mpmath.dps = 5

import multiprocessing
from multiprocessing import Pool
from datetime import datetime

startTime = datetime.now()
print(f'Started at {startTime}')

polar = True

def riemann_zeta(s):
    return mpmath.zeta(s)

def inner_loop(xn):
    out_r = []
    out_i = []

    for yn in range(s_columns):
        try:
            s = complex(X[xn,yn],Y[xn,yn])
            z = mpmath.chop(riemann_zeta(s))
            if z != z:
                raise ValueError
            if polar:
                # Polar form
                z_r, z_i = mpmath.polar(z)
                # For polar form only. Convert negative angles to positive ones
                # This is to ensure that 0 is the lowest value of z_i
                # and for it to map to red on an hsv color map
                if z_i < 0:
                    z_i += 2*(np.pi)
            else:
                # Rectangular form
                z_r = float(z.real)
                z_i = float(z.imag)
            out_r.append(z_r)
            out_i.append(z_i)
        except (ValueError, TypeError, ZeroDivisionError):
            # Append nan for singularities and other special values
            out_r.append(np.nan)
            out_i.append(np.nan)
    return out_r, out_i

# Large part of the Riemann_zeta function plane
# X = np.arange(-4, 4, 0.1)
# Y = np.arange(-30, 30, 0.1)
## Critical strip
# X = np.arange(0, 1, 0.05)
# Y = np.arange(-30, 30, 0.05)
## Slice of the plane at the non-trivial zeros
X = np.arange(0.5, 0.56, 0.05)
Y = np.arange(-30, 30, 0.05)

X, Y = np.meshgrid(X, Y)
s_rows, s_columns = X.shape
Z_r = X*0
Z_i = X*0

# Use multiprocessing to speed things up
# Set worker count to the number of threads
worker_count = multiprocessing.cpu_count()
p = Pool(worker_count)
out = p.map(inner_loop, [xn for xn in range(s_rows)])
Z = np.asarray(out, dtype=float)

# Real part and imaginary part of the Riemann_zeta function output
Z_r = Z[:,0,:]
Z_i = Z[:,1,:]

# Don't plot singularities
# cutoff value set to 5
Z_r[Z_r > 5] = np.nan
Z_r[Z_r < -5] = np.nan

# Save X, Y, Z_r, Z_i in files
with open('./Z_r.npy', 'wb') as fr:
    np.save(fr, Z_r)

with open('./Z_i.npy', 'wb') as fi:
    np.save(fi, Z_i)

with open('./X.npy', 'wb') as fx:
    np.save(fx, X)

with open('./Y.npy', 'wb') as fy:
    np.save(fy, Y)

print(f'Execution time with {worker_count} workers: {datetime.now() - startTime}')
