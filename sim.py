import numpy
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

pyplot = matplotlib.pyplot
matplotlib.use("tkagg")

frames = 5000
simulation_interval = 10 # ms

air_brake_constant = 0.5
motor_power_constant = 3
kp = 4
ki = 1 / 10
kd = 1 / 10

class Box:
    def __init__(self):
        self.mass = 0.4
        self.velocity = 0

    def update(self, outside_power):
        delta_time = simulation_interval / 1000
        self.velocity += -((air_brake_constant / self.mass) * self.velocity) * delta_time
        self.velocity += (outside_power / self.mass) * delta_time

class Motor:
    def __init__(self):
        self.target_rpm = 50
        self.integral = 0
        self.derivative = 0

    def update(self, current_rpm):
        error = (self.target_rpm - current_rpm)
        self.integral += error
        return kp * error + ki * self.integral

fig,axes = pyplot.subplots(3)
ax = axes[0]
obj1, = ax.plot([],[],'o')
obj2, = ax.plot([],[],'x')
obj2.set_data((50, 2.5,))
ax.set_xlim(0, 100)
ax.set_ylim(0, 5)
ax.set_aspect('equal')

ax = axes[1]
integralHistoryObj, = ax.plot([], [])
ax.set_xlim(0, 1000)
ax.set_ylim(-500, 500)

box = Box()
motor = Motor()
integralHistory = []

def update(frame_num):
    global box
    global motor

    power = motor.update(box.velocity)
    box.update(power)

    if frame_num == 0:
        box.__init__()

    obj1.set_data((box.velocity, 2.5,))

    integralHistory.append(motor.integral)
    integralHistoryObj.set_data(list(range(len(integralHistory))), integralHistory[:])

    return obj1, integralHistoryObj

_animation = FuncAnimation(fig, update, frames=frames, interval=simulation_interval, blit=True, repeat=True)
pyplot.show()
