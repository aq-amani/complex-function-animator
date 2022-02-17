from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import numpy as np

import multiprocessing
from multiprocessing import Pool
from datetime import datetime

import configparser
import re

config = configparser.ConfigParser()
config.read('./config.ini')

header = """
+-----------------------------+
| (c) 2022 Amani AbuQdais     |
| https://github.com/aq-amani |
+-----------------------------+
"""

DATA_PATH = config['GLOBAL']['DATA_PATH']
FRAMES_PATH = config['GLOBAL']['FRAMES_PATH']

POLAR = config.getboolean('GLOBAL', 'POLAR')
FUNCTION_NAME = 'ζ(s)'
# If true, hides some grid and axes for better looking animation
ANIMATION_VIEW = config.getboolean('PLOTTER', 'ANIMATION_VIEW')
# If true creates an image at every angle for animation.
# Only views the graph if false
CREATE_FRAMES = config.getboolean('PLOTTER', 'CREATE_FRAMES')
# Angle increments when creating frames for rotation around any axis
ANGLE_INCREMENTS = float(config['PLOTTER']['ANGLE_INCREMENTS'])
ROTATION_AXIS = config['PLOTTER']['ROTATION_AXIS']

FIG = plt.figure(figsize=(7, 5))
#ax = Axes3D(FIG)
AX = FIG.add_subplot(projection='3d')
FIG.tight_layout()

def capture_plot_frame_Z(angle):
    """Rotates plot around Z axis and saves the figure

    Arguments:
    angle -- angle to use for the plot's azimuth or elevation angles
    """
    # Rotation around Z axis
    AX.view_init(elev=30, azim=angle)
    save_fig(angle)

def capture_plot_frame_Y(angle):
    """Rotates plot around Y axis and saves the figure

    Arguments:
    angle -- angle to use for the plot's azimuth or elevation angles
    """
    # Rotation around Z axis
    AX.view_init(elev=angle, azim=0)
    save_fig(angle)

def capture_plot_frame_X(angle):
    """Rotates plot around X axis and saves the figure

    Arguments:
    angle -- angle to use for the plot's azimuth or elevation angles
    """
    # Rotation around Z axis
    AX.view_init(elev=angle, azim=90)
    save_fig(angle)

def save_fig(angle):
    """Saves a snapshot of the plot to use for creating axis rotation animations

    Arguments:
    angle -- angle that was used for the plot's azimuth or elevation angles
    """
    # Figure names need to be consecutive integers for ffmpeg to work
    fig_name = int(angle/ANGLE_INCREMENTS)
    plt.savefig(f'{FRAMES_PATH}{fig_name}.png', dpi = 300)

def plot_complex_data():
    """Depending on CREATE_FRAMES:
    If True: Plots data in 3D with domain coloring and saves snapshots(frames) to use in axis rotation animation
    If False: Plots data in 3D with domain coloring and only shows it.
    """
    # Only print execution time stats  in the create frames mode
    if CREATE_FRAMES:
        start_time = datetime.now()
        print(f'{start_time.strftime("%Y-%m-%d %H:%M:%S")} Generating animation frames..')
    else:
        print('Plotting the graph..')

    with open(f'{DATA_PATH}Z_r.npy', 'rb') as fr:
        Z_r = np.load(fr)
    with open(f'{DATA_PATH}Z_i.npy', 'rb') as fi:
        Z_i = np.load(fi)
    with open(f'{DATA_PATH}X.npy', 'rb') as fx:
        X = np.load(fx)
    with open(f'{DATA_PATH}Y.npy', 'rb') as fy:
        Y = np.load(fy)

    #print(Z_r)
    #print(Z_i)
    #print(X)
    #print(Y)

    # Limits of Z axis
    AX.set_zlim([0, 4])
    # Axi labels
    AX.set_xlabel('Re(s)')
    AX.set_ylabel('Im(s)')
    if ANIMATION_VIEW:
        AX.grid(False)
        # Hide panes on the Z axis
        AX.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        AX.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # Hide all axes
        #AX.set_axis_off()

        # Hide Z axis
        AX.w_zaxis.line.set_lw(0.)
        AX.set_zticks([])
        #Remove fill from XY plane
        #AX.zaxis.pane.fill = False
    else:
        AX.set_zlabel(f'|{FUNCTION_NAME}|' if POLAR else f'Re({FUNCTION_NAME})')
        AX.zaxis.set_rotate_label(False)
        AX.zaxis.label.set_rotation(90)
        # Workaround to avoid Z axis and color bar labels to be too close
        AX.view_init(elev=30, azim=30)

    # Code required for domain coloring based on Imaginary part of f(z)
    color_dimension = Z_i
    min, max = color_dimension.min(), color_dimension.max()
    norm = matplotlib.colors.Normalize(min, max)
    m = plt.cm.ScalarMappable(norm=norm, cmap='hsv' if POLAR else 'jet')
    m.set_array([])
    fcolors = m.to_rgba(color_dimension)

    # Plot real part of f(z) with domain coloring based on the imaginary part
    surf = AX.plot_surface(X,Y,Z_r, rstride=1, cstride=1, facecolors=fcolors, vmin=min, vmax=max, shade=False)
    # Add an opaque surface for zero level to better see riemann zeta zeros
    #surf_zero = AX.plot_surface(X,Y,Z_r*0, rstride=1, cstride=1, vmin=min, vmax=max, shade=False, alpha=0.3, antialiased = True)

    # to plot a wireframe
    #AX.plot_wireframe(X, Y, Z_r, rstride=5, cstride=5)

    # Color bar
    #cbaxes = FIG.add_axes([0.05, 0.1, 0.03, 0.8])
    cb = FIG.colorbar(m, shrink=0.5, aspect=5)
    #cb = FIG.colorbar(m, cax = cbaxes)
    cb.ax.set_title(f'arg({FUNCTION_NAME})' if POLAR else f'Im({FUNCTION_NAME})',fontsize=10)

    if not CREATE_FRAMES:
        plt.show()
    else:
        worker_count = multiprocessing.cpu_count()
        p = Pool(worker_count)
        START_ANGLE = float(config['PLOTTER']['START_ANGLE'])
        STOP_ANGLE = float(config['PLOTTER']['STOP_ANGLE'])
        angle = np.arange(START_ANGLE, STOP_ANGLE+ANGLE_INCREMENTS, ANGLE_INCREMENTS)
        if ROTATION_AXIS == 'X':
            rotation_function = capture_plot_frame_X
        elif ROTATION_AXIS == 'Y':
            rotation_function = capture_plot_frame_Y
        else:
            rotation_function = capture_plot_frame_Z
        out = p.map(rotation_function, angle)
        plt.close()
        finish_time = datetime.now()
        print(f'{finish_time.strftime("%Y-%m-%d %H:%M:%S")} Done. Execution time with {worker_count} workers: [{finish_time - start_time}]')

def main():
    print(header)
    plot_complex_data()

if __name__ == '__main__':
    main()
