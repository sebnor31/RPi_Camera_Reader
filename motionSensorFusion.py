# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 10:25:02 2016

@author: pi
"""

import numpy as np
import matplotlib.pyplot as plt


rawCalibFile = "C:\Users\sebnor\Desktop\data\Motion/motion_2016-6-16_9-17-29.csv"
a = np.genfromtxt(rawCalibFile, delimiter=',')

print('Num of Rows: %d' % len(a))

t = range(0,(len(a) -1))
acc_x = a[1:, 0]
acc_y = a[1:, 1]
acc_z = a[1:, 2]

gyro_x = a[1:, 3]
gyro_y = a[1:, 4]
gyro_z = a[1:, 5] 

mag_x = a[1:, 6]
mag_y = a[1:, 7]
mag_z = a[1:, 8] 

yaw = np.degrees(a[1:, 9])
roll = np.degrees(a[1:, 10])
pitch = np.degrees(a[1:, 11])


# Plotting data
plt.subplot(3,4,1)
plt.title("Accel_X")
plt.plot(t, acc_x)
plt.ylim([-2, 2])
plt.grid()

plt.subplot(3,4,5)
plt.title("Accel_Y")
plt.plot(t, acc_y)
plt.ylim([-2, 2])
plt.grid()

plt.subplot(3,4,9)
plt.title("Accel_Z")
plt.plot(t, acc_z)
plt.ylim([-2, 2])
plt.grid()

plt.subplot(3,4,2)
plt.title("Gyro_X")
plt.plot(t, gyro_x)
#plt.ylim([-100, 100])
plt.grid()

plt.subplot(3,4,6)
plt.title("Gyro_Y")
plt.plot(t, gyro_y)
#plt.ylim([-100, 100])
plt.grid()

plt.subplot(3,4,10)
plt.title("Gyro_Z")
plt.plot(t, gyro_z)
#plt.ylim([-100, 100])
plt.grid()

plt.subplot(3,4,3)
plt.title("Mag_X")
plt.plot(t, mag_x)
#plt.ylim([-400e-6, 400e-6])
plt.grid()

plt.subplot(3,4,7)
plt.title("Mag_Y")
plt.plot(t, mag_y)
#plt.ylim([-10, 10])
plt.grid()

plt.subplot(3,4,11)
plt.title("Mag_Z")
plt.plot(t, mag_z)
#plt.ylim([-10, 10])
plt.grid()

plt.subplot(3,4,4)
plt.title("Roll (X)")
plt.plot(t, roll)
plt.ylim([-90, 90])
plt.grid()

plt.subplot(3,4,8)
plt.title("Pitch (Y)")
plt.plot(t, pitch)
plt.ylim([0, 180])
plt.grid()

plt.subplot(3,4,12)
plt.title("Yaw (Z)")
plt.plot(t, yaw)
plt.ylim([-90, 90])
plt.grid()

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()

# Remove DC component