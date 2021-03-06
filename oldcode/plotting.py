'''This code is used for only plotting lidar data'''

'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import serial

# ser = serial.Serial()
# ser.port = 'COM4'
# ser.baudrate = 9600
PORT_NAME = 'COM4'
# PORT_NAME = '/dev/ttyUSB0'

DMAX = 5000
IMIN = 0
IMAX = 50


def update_line(num, iterator, line):
    scan = next(iterator)
    # print(np.radians(meas[1]) for meas in scan)
    # intens = np.array([meas[0] for meas in scan])

    offsets = np.array(
        [(meas[0], np.radians(meas[1]), meas[2]) for meas in scan])  # if meas[1] < 225 and meas[1] > 315])
    # real_offsets = np.array([])
    # print(offsets)
    real_offsets = []
    real_intens = []
    for i in offsets:
        if i[1] >= 5.2359 or i[1] <= 1.0472:
            # print(i)
            real_offsets.append([i[1], i[2]])
            real_intens.append(i[0])
    offsets = np.array(real_offsets)
    intens = np.array(real_intens)
    line.set_array(intens)
    line.set_offsets(offsets)

    # 225 3.92 315 5.49

    return line,


def run():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                      cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
                                  fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()


if __name__ == '__main__':
    run()
