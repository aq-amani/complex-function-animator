from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import pylab
import numpy as np
import mpmath
mpmath.dps = 5

f = lambda z: mpmath.zeta(z)

#fig = pylab.figure()
fig = pylab.figure(figsize=(7, 5))
ax = Axes3D(fig)
#ax.view_init(elev=30, azim=30)
X = np.arange(0.5, 0.75, 0.125)
#X = np.arange(-4, 4, 0.125)
#X = np.arange(1.5, 3, 0.125)
#Y = np.arange(-30, 30, 0.125)
Y = np.arange(11, 15, 0.01)
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

# Don't plot singularities
# cutoff value set to 5
W_r[W_r > 5] = np.nan
W_r[W_r < -5] = np.nan
# Limits of Z axis
ax.set_zlim([0, 4])
# Axi labels
ax.set_xlabel('Re(s)')
ax.set_ylabel('Im(s)')
ax.set_zlabel('|ζ(s)|')
ax.zaxis.set_rotate_label(False)
ax.zaxis.label.set_rotation(90)
# Hide all axes
#ax.set_axis_off()

# Hide Z axis
#ax.w_zaxis.line.set_lw(0.)
#ax.set_zticks([])

# Code required for domain coloring based on Imaginary part of f(z)
color_dimension = W_i
min, max = color_dimension.min(), color_dimension.max()
norm = matplotlib.colors.Normalize(min, max)
m = plt.cm.ScalarMappable(norm=norm, cmap='hsv')
m.set_array([])
fcolors = m.to_rgba(color_dimension)

# Plot real part of f(z) with domain coloring based on the imaginary part
surf = ax.plot_surface(X,Y,W_r, rstride=1, cstride=1, facecolors=fcolors, vmin=min, vmax=max, shade=False)
# Add an opaque surface for zero level to better see riemann zeta zeros
#surf_zero = ax.plot_surface(X,Y,W_r*0, rstride=1, cstride=1, vmin=min, vmax=max, shade=False, alpha=0.3, antialiased = True)

# to plot a wireframe
#ax.plot_wireframe(X, Y, W_r, rstride=5, cstride=5)

# Color bar
#cbaxes = fig.add_axes([0.05, 0.1, 0.03, 0.8])
cb = fig.colorbar(m, shrink=0.5, aspect=5)
#cb = fig.colorbar(m, cax = cbaxes)
cb.ax.set_title('arg(ζ(s))',fontsize=10)

#pylab.show()
plt.show()
plt.close()
plt.show()
