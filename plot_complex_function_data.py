from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import pylab
import numpy as np

from datetime import datetime

startTime = datetime.now()
print(f'Started at {startTime}')

polar = True
function_name = 'ζ(s)'
# If true, hides some grid and axes for better looking animation
animation_view = False
# If true creates an image at every angle for animation.
# Only views the graph if false
create_frames = False

with open('./data/Z_r.npy', 'rb') as fr:
    Z_r = np.load(fr)
with open('./data/Z_i.npy', 'rb') as fi:
    Z_i = np.load(fi)
with open('./data/X.npy', 'rb') as fx:
    X = np.load(fx)
with open('./data/Y.npy', 'rb') as fy:
    Y = np.load(fy)

#print(Z_r)
#print(Z_i)
#print(X)
#print(Y)

#fig = pylab.figure()
fig = pylab.figure(figsize=(7, 5))
ax = Axes3D(fig)

# Limits of Z axis
ax.set_zlim([0, 4])
# Axi labels
ax.set_xlabel('Re(s)')
ax.set_ylabel('Im(s)')
if animation_view:
    ax.grid(False)
    # Hide panes on the Z axis
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # Hide all axes
    #ax.set_axis_off()

    # Hide Z axis
    ax.w_zaxis.line.set_lw(0.)
    ax.set_zticks([])
    #Remove fill from XY plane
    #ax.zaxis.pane.fill = False
else:
    ax.set_zlabel(f'|{function_name}|' if polar else f'Re({function_name})')
    ax.zaxis.set_rotate_label(False)
    ax.zaxis.label.set_rotation(90)
    # Workaround to avoid Z axis and color bar labels to be too close
    ax.view_init(elev=30, azim=30)

# Code required for domain coloring based on Imaginary part of f(z)
color_dimension = Z_i
min, max = color_dimension.min(), color_dimension.max()
norm = matplotlib.colors.Normalize(min, max)
m = plt.cm.ScalarMappable(norm=norm, cmap='hsv' if polar else 'jet')
m.set_array([])
fcolors = m.to_rgba(color_dimension)

# Plot real part of f(z) with domain coloring based on the imaginary part
surf = ax.plot_surface(X,Y,Z_r, rstride=1, cstride=1, facecolors=fcolors, vmin=min, vmax=max, shade=False)
# Add an opaque surface for zero level to better see riemann zeta zeros
#surf_zero = ax.plot_surface(X,Y,Z_r*0, rstride=1, cstride=1, vmin=min, vmax=max, shade=False, alpha=0.3, antialiased = True)

# to plot a wireframe
#ax.plot_wireframe(X, Y, Z_r, rstride=5, cstride=5)

# Color bar
#cbaxes = fig.add_axes([0.05, 0.1, 0.03, 0.8])
cb = fig.colorbar(m, shrink=0.5, aspect=5)
#cb = fig.colorbar(m, cax = cbaxes)
cb.ax.set_title(f'arg({function_name})' if polar else f'Im({function_name})',fontsize=10)

if not create_frames:
    plt.show()
else:
    j = 0
    angle = np.arange(0, 360.5, 0.5)
    for i in angle:
        i = round(i,2)
        # Rotation around Z axis
        ax.view_init(elev=30, azim=i)
        # Rotation around X axis
        # ax.view_init(elev=i, azim=270)
        # Rotation around Y axis
        # ax.view_init(elev=i, azim=0)
        plt.savefig(f'./pics/{j}.png', dpi = 300)
        j += 1
    plt.close()

print(f'Execution time: {datetime.now() - startTime}')
