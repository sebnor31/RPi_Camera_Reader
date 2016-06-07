# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 10:25:02 2016

@author: pi
"""

import numpy as np
import matplotlib.pyplot as plt


rawCalibFile = "C:\Users\sebnor\Desktop\data\motion_2016-6-7_10-55-27.csv"
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

head = a[1:, 9]
roll = a[1:, 10]
pitch = a[1:, 11]

lin_x = a[1:, 12]
lin_y = a[1:, 13]
lin_z = a[1:, 14] 

grav_x = a[1:, 15]
grav_y = a[1:, 16]
grav_z = a[1:, 17] 

# Plotting data
plt.subplot(6,3,1)
plt.plot(t, acc_x)

plt.subplot(6,3,2)
plt.plot(t, acc_y)

plt.subplot(6,3,3)
plt.plot(t, acc_z)

plt.subplot(6,3,4)
plt.plot(t, gyro_x)

plt.subplot(6,3,5)
plt.plot(t, gyro_y)

plt.subplot(6,3,6)
plt.plot(t, gyro_z)

plt.subplot(6,3,7)
plt.plot(t, mag_x)

plt.subplot(6,3,8)
plt.plot(t, mag_y)

plt.subplot(6,3,9)
plt.plot(t, mag_z)

plt.subplot(6,3,10)
plt.plot(t, head)

plt.subplot(6,3,11)
plt.plot(t, roll)

plt.subplot(6,3,12)
plt.plot(t, pitch)

plt.subplot(6,3,13)
plt.plot(t, lin_x)

plt.subplot(6,3,14)
plt.plot(t, lin_y)

plt.subplot(6,3,15)
plt.plot(t, lin_z)

plt.subplot(6,3,16)
plt.plot(t, grav_x)

plt.subplot(6,3,17)
plt.plot(t, grav_y)

plt.subplot(6,3,18)
plt.plot(t, grav_z)

plt.show()

# Remove DC component