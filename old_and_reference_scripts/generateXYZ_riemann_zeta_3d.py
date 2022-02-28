import numpy as np
import mpmath
mpmath.dps = 5

f = lambda z: mpmath.zeta(z)

X = np.arange(0.5, 0.75, 0.5)
#X = np.arange(-4, 4, 0.01)
#X = np.arange(1.5, 3, 0.125)
Y = np.arange(-25, 25, 0.5)
#Y = np.arange(-30, 30, 0.01)
#Y = np.arange(11, 15, 0.01)
X, Y = np.meshgrid(X, Y)
xn, yn = X.shape

W_r = X*0
W_i = X*0
for xk in range(xn):
    for yk in range(yn):
        try:
            z = complex(X[xk,yk],Y[xk,yk])
            w = mpmath.chop(f(z))
            if w != w:
                raise ValueError
            #W_r[xk,yk] = float(w.real)
            #W_i[xk,yk] = float(w.imag)
            #W_r[xk,yk] = mpmath.chop(w.real)
            #W_i[xk,yk] = mpmath.chop(w.imag)
            W_r[xk,yk], W_i[xk,yk] = mpmath.polar(w)
            #W_i[xk,yk] = mpmath.chop(W_i[xk,yk])
            if W_i[xk,yk] < 0:
                W_i[xk,yk] += 2*(np.pi)
            #W_i[xk,yk] = mpmath.cos(W_i[xk,yk])
            #print(Y[xk,yk])
            #print(W_r[xk,yk], W_i[xk,yk])
        except (ValueError, TypeError, ZeroDivisionError):
            # can handle special values here
            pass
    #print(xk, xn)

## Don't plot singularities
## cutoff value set to 5
W_r[W_r > 5] = np.nan
W_r[W_r < -5] = np.nan

with open('./W_r.npy', 'wb') as fr:
    np.save(fr, W_r)

with open('./W_i.npy', 'wb') as fi:
    np.save(fi, W_i)

with open('./X.npy', 'wb') as fx:
    np.save(fx, X)

with open('./Y.npy', 'wb') as fy:
    np.save(fy, Y)
