import numpy as np
import mpmath
mpmath.dps = 5

import multiprocessing
from multiprocessing import Pool
from datetime import datetime

import configparser
import re

config = configparser.ConfigParser()
config.read('./config.ini')

POLAR = config.getboolean('GLOBAL', 'POLAR')
DATA_PATH = config['GLOBAL']['DATA_PATH']

# Read input intervals (start, end, step) to feed to np.arange
# X --> Real part , Y --> Imagiary part of the function input.
x_interval_settings = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", config['GENERATOR']['X_INTERVAL'])
y_interval_settings = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", config['GENERATOR']['Y_INTERVAL'])
# Input interval settings
X = np.arange(*np.array(x_interval_settings, dtype=float))
Y = np.arange(*np.array(y_interval_settings, dtype=float))
X, Y = np.meshgrid(X, Y)
S_ROWS, S_COLUMNS = X.shape

def riemann_zeta(s):
    return mpmath.zeta(s)

def complex_function_y_looper(xn):
    """Loops over y values using one x value.
    x and y and real and imaginary parts of the complex function input.

    Arguments:
    xn -- Fixed x value to loop over y values with
    """
    out_r = []
    out_i = []

    for yn in range(S_COLUMNS):
        try:
            s = complex(X[xn,yn],Y[xn,yn])
            z = mpmath.chop(riemann_zeta(s))
            if z != z:
                raise ValueError
            if POLAR:
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

def generate_complex_data():
    """Creates numpy arrays for X, Y, Z_r, Z_i and saves them in files
    """
    start_time = datetime.now()
    print(f'{start_time.strftime("%Y-%m-%d %H:%M:%S")} Generating complex function data..')
    Z_r = X*0
    Z_i = X*0
    # Use multiprocessing to speed things up
    # Set worker count to the number of threads
    worker_count = multiprocessing.cpu_count()
    p = Pool(worker_count)
    out = p.map(complex_function_y_looper, [xn for xn in range(S_ROWS)])
    Z = np.asarray(out, dtype=float)

    # Real part and imaginary part of the Riemann_zeta function output
    Z_r = Z[:,0,:]
    Z_i = Z[:,1,:]

    # Don't plot singularities
    # cutoff value set to 5
    Z_r[Z_r > 5] = np.nan
    Z_r[Z_r < -5] = np.nan

    # Save X, Y, Z_r, Z_i in files
    with open(f'{DATA_PATH}Z_r.npy', 'wb') as fr:
        np.save(fr, Z_r)

    with open(f'{DATA_PATH}Z_i.npy', 'wb') as fi:
        np.save(fi, Z_i)

    with open(f'{DATA_PATH}X.npy', 'wb') as fx:
        np.save(fx, X)

    with open(f'{DATA_PATH}Y.npy', 'wb') as fy:
        np.save(fy, Y)

    finish_time = datetime.now()
    print(f'{finish_time.strftime("%Y-%m-%d %H:%M:%S")} Done. Execution time with {worker_count} workers: [{finish_time - start_time}]')

def main():
    import header
    generate_complex_data()

if __name__ == '__main__':
    main()
