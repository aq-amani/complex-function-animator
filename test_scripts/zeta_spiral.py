from mpmath import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import argparse

mp.dps = 10
mp.pretty = True

is_3d = False

si_min = 0
si_max = 50
steps = 0.1

s_i = []
z_r = []
z_i = []
count = []

fig = None
ax = None

def animate(i):
    if is_3d:
        line, = ax.plot(z_r[:i], z_i[:i], count[:i], lw=1.5, color='violet')
        point, = ax.plot(z_r[i], z_i[i], count[i], marker='o', markersize=8, color='red')
    else:
        line, = ax.plot(z_r[:i], z_i[:i], lw=1.5, color='orange')
        point, = ax.plot(z_r[i], z_i[i], marker='o', markersize=8, color='red')

    return line, point,

def init_data(args):
    global is_3d
    global fig
    global ax
    global z_r
    global z_i
    global count

    mode = args['mode']
    if mode == '3d':
        is_3d = True
    else:
        is_3d = False
    start = args['start']
    end = args['end']

####################
    si_min = start
    si_max = end
    frame_count = int((si_max-si_min)/steps)

    s_i = np.arange(si_min,si_max,steps)
    z_r = s_i * 0
    z_i = s_i * 0
    count = np.arange(0,frame_count,1)

    for i, n in enumerate(s_i):
        z = zeta(0.5 +n*1j)
        z_r[i] = z.real
        z_i[i] = z.imag

    if is_3d:
        fig = plt.figure(figsize=(10, 10), frameon=False)
        ax = fig.add_subplot(projection='3d')
    else:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot()
        fig.patch.set_facecolor('black')
        ax.set_facecolor('xkcd:navy')

        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_linewidth(2.0)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        ax.spines['bottom'].set_color('lightgray')
        ax.spines['left'].set_color('lightgray')

        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')
        ax.set_xlim([-2, 6])
        ax.set_ylim([-3, 3])
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_linewidth(2.0)

    if is_3d:
        ax.set_zlim([0, frame_count])
        ax.set_xlim([-4, 4])
        ax.set_ylim([-4, 4])

    return frame_count
####################

def main():

    parser = argparse.ArgumentParser(description='Plot riemann zeta function for 0.5+jt in 3D and in 2D')

    mode_choices = ['3d', '2d']

    parser.add_argument('-m','--mode', choices=mode_choices, help='3d or 2d', default = '2d', metavar = '')
    parser.add_argument('-s','--start', help='Starting value for imaginary part of input', default = 0, type = int, metavar = '')
    parser.add_argument('-e','--end', help='Ending value for imaginary part of input', default = 50, type = int, metavar = '')
    parser.add_argument('-a','--animate', help='Animate flag', action ='store_true')

    args = vars(parser.parse_args())
    animate_flag = args['animate']

    frame_count = init_data(args)


    if animate_flag:
        anim = animation.FuncAnimation(fig, animate, frames=frame_count, interval=10, blit=True, repeat = False)
    else:
        if is_3d:
            ax.plot(z_r, z_i, count, lw=1.5, color='violet')
        else:
            ax.plot(z_r, z_i, lw=1.5, color='violet')

    plt.show()


if __name__ == "__main__":
    main()
