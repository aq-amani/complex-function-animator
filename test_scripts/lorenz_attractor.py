import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def lorenz(x, y, z, s=10, r=28, b=2.667):
    """
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    """
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


dt = 0.01
num_steps = 10000
# Need one more for the initial values
xs = np.empty(num_steps + 1)
ys = np.empty(num_steps + 1)
zs = np.empty(num_steps + 1)

# Set initial values
#xs[0], ys[0], zs[0] = (0., 1., 1.05)
xs[0], ys[0], zs[0] = (0., 1., 1.05)
for i in range(num_steps):
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + (x_dot * dt)
    ys[i + 1] = ys[i] + (y_dot * dt)
    zs[i + 1] = zs[i] + (z_dot * dt)

x = []
y = []
z = []

def animate(i):
    # Step through "time", calculating the partial derivatives at the current point
    # and using them to estimate the next point
    x.append(xs[i])
    y.append(ys[i])
    z.append(zs[i])

    line, = ax.plot(x, y, z, lw=0.5, color='b')
    point, = ax.plot(xs[i], ys[i], zs[i], marker='o', markersize=4, color='red')
    return line,point,


# Plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_zlim([-10, 50])
ax.set_xlim([-30, 30])
ax.set_ylim([-30, 30])

ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")

def init():
    return ax.plot([], [], [], lw=0.5, color='b')
anim = animation.FuncAnimation(fig, animate, frames=num_steps, init_func = init, interval=5, blit=True, repeat = False)
plt.show()
