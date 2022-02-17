from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import pylab
import numpy as np

import multiprocessing
from multiprocessing import Pool
from datetime import datetime

def capture_plot_frame(angle):
    # Rotation around Z axis
    ax.view_init(elev=30, azim=angle)
    # Figure names need to be consecutive integers for ffmpeg to work
    fig_name = int(angle/angle_increments)
    plt.savefig(f'{frames_path}{fig_name}.png', dpi = 300)

startTime = datetime.now()
print(f'Started at {startTime}')

data_path = './data/'
frames_path = './pics/'

polar = True
function_name = 'ζ(s)'
# If true, hides some grid and axes for better looking animation
animation_view = False
# If true creates an image at every angle for animation.
# Only views the graph if false
create_frames = False
# Angle increments when creating frames for rotation around any axis
angle_increments = 0.5

with open(f'{data_path}Z_r.npy', 'rb') as fr:
    Z_r = np.load(fr)
with open(f'{data_path}Z_i.npy', 'rb') as fi:
    Z_i = np.load(fi)
with open(f'{data_path}X.npy', 'rb') as fx:
    X = np.load(fx)
with open(f'{data_path}Y.npy', 'rb') as fy:
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
    angle = np.arange(0, 15.5, angle_increments)
    worker_count = multiprocessing.cpu_count()
    p = Pool(worker_count)
    out = p.map(capture_plot_frame, angle)
    plt.close()

print(f'Execution time with {worker_count} workers: {datetime.now() - startTime}')
