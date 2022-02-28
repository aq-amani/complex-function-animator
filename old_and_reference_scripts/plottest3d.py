import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import mpmath
from mpmath import nsum, inf, zeta
import cmath
mpmath.dps = 5

# Use instead of arg for a continuous phase
def arg2(x):
    return mpmath.sin(mpmath.arg(x))
#
##f = lambda z: abs(mpmath.loggamma(z))
##f = lambda z: arg2(mpmath.exp(z))
##f = lambda z: abs(mpmath.besselj(3,z))
#f = lambda z: arg2(mpmath.cos(z))
def zeta_function(z):
    #out = 1
    #for i in range(2,50):
    #    out += 1/(i**z)
    #out += nsum(lambda n: 1/(n**z), [2, 10])
    #return zeta(z).real
    return zeta(z)
    #return arg2(1 + 1/(2**z) + 1/(3**z) + 1/(4**z) + 1/(5**z) + 1/(6**z) + 1/(7**z) + 1/(8**z) + 1/(9**z) + 1/(10**z) + 1/(11**z) + 1/(12**z) + 1/(13**z) + 1/(14**z) + 1/(15**z) + 1/(16**z) + 1/(17**z) + 1/(18**z))

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig.patch.set_facecolor('black')
X = np.arange(-1, 1, 0.125)
Y = np.arange(0, 26, 0.125)
X, Y = np.meshgrid(X, Y)

###
xn, yn = X.shape
W = X*0
for xk in range(xn):
    for yk in range(yn):
        try:
            z = complex(X[xk,yk],Y[xk,yk])
            w = float(zeta_function(z))
            if w != w:
                raise ValueError
            W[xk,yk] = w
            print(w)
        except (ValueError, TypeError, ZeroDivisionError):
            # can handle special values here
            pass
    #print(xk, xn)
###

# Plot the surface.
surf = ax.plot_surface(X, Y, W, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
surf = ax.plot_surface(X, Y, W, cmap=cm.jet,
                       linewidth=0, rstride=1, cstride=1, antialiased=False)
surf = ax.plot_surface(X, Y, W, cmap=cm.jet, antialiased=True)
for point in W:
    p = cmath.polar(point)
    #print(type(point))
    plt.polar(cmath.polar(point), 'ro')

surf = ax.plot_wireframe(X, Y, W, rstride=2, cstride=2)
## Customize the z axis.
ax.set_zlim(0, 2.01)
ax.zaxis.set_major_locator(LinearLocator(10))
## A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')
#
## Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
