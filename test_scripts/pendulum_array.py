class Pendulum:

    def __init__(self, l1, l2, m1, m2, th1, w1, th2, w2):
        #Ensure first character of name is in upper case
        self._l1 = l1
        self._l2 = l2
        self._l = l1 + l2
        self._m1 = m1
        self._m2 = m2
        self._th1 = th1
        self._th1 = th2
        self._w1 = w1
        self._w2 = w2
        self._state = np.radians([th1, w1, th2, w2])


    @property
    def l1(self):
        return self._l1
    @property
    def l2(self):
        return self._l2
    @property
    def l(self):
        return self._l
    @property
    def m1(self):
        return self._m1
    @property
    def m2(self):
        return self._m2
    @property
    def th1(self):
        return self._th1
    @property
    def th2(self):
        return self._th2
    @property
    def w1(self):
        return self._w1
    @property
    def w2(self):
        return self._w2
    @property
    def state(self):
        return self._state
    @property
    def x1(self):
        return self.x2
    @property
    def x2(self):
        return self.x2
    @property
    def y1(self):
        return self.y2
    @property
    def y2(self):
        return self.y2
    @property
    def y(self):
        return self.y
    @property
    def history_x(self):
        return self.history_x
    @property
    def history_y(self):
        return self.history_y

    def set_y(self, t):
        self.y = integrate.odeint(derivs, self.state, t)




from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque

G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
L = L1 + L2  # maximal length of the combined pendulum
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg
t_stop = 30  # how many seconds to simulate
history_len = 500  # how many trajectory points to display


def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    delta = state[2] - state[0]
    den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1+M2) * G * sin(state[0]))
               / den1)

    dydx[2] = state[3]

    den2 = (L2/L1) * den1
    dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1+M2) * G * sin(state[0]) * cos(delta)
                - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1+M2) * G * sin(state[2]))
               / den2)

    return dydx

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)

#             l1, l2,  m1,  m2,  th1,   w1, th2,   w2
P = Pendulum(1.0, 1.0, 1.0, 1.0, 120.0, 0.0,-10.0, 0.0)


# integrate your ODE using scipy.integrate.
#P.y = integrate.odeint(derivs, P.state, t)
P.set_y(t)


P.x1 = P.l1*sin(P.y[:, 0])
P.y1 = -P.l1*cos(P.y[:, 0])

P.x2 = P.l2*sin(P.y[:, 2]) + P.x1
P.y2 = -P.l2*cos(P.y[:, 2]) + P.y1


fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(autoscale_on=False, xlim=(-P.l, P.L), ylim=(-P.L, 1.))
ax.set_aspect('equal')
ax.grid(False)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

line, = ax.plot([], [], 'o-', lw=2)

trace, = ax.plot([], [], '-', lw=1, ms=2)


time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
P.history_x, P.history_y = deque(maxlen=history_len), deque(maxlen=history_len)

def animate(i):
    thisx = [0, P.x1[i], P.x2[i]]
    thisy = [0, P.y1[i], P.y2[i]]


    if i == 0:
        P.history_x.clear()
        P.history_y.clear()


    P.history_x.appendleft(thisx[2])
    P.history_y.appendleft(thisy[2])




    line.set_data(thisx, thisy)
    trace.set_data(P.history_x, P.history_y)

    time_text.set_text(time_template % (i*dt))
    return line, trace, time_text


ani = animation.FuncAnimation(
    fig, animate, len(P.y), interval=dt*1000, blit=True, repeat = False)
plt.show()
