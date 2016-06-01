# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 10:25:02 2016

@author: pi
"""

import numpy as np
import matplotlib.pyplot as plt


rawCalibFile = "/home/pi/Desktop/Video_Capture/Data/calib_motion_2016-6-1_11-52.csv"
a = np.genfromtxt(rawCalibFile, delimiter=',')

print('Num of Rows: %d' % len(a))

t = a[1:, 9]
acc_x = a[1:, 0]
acc_y = a[1:, 1]
acc_z = a[1:, 2]

gyro_x = a[1:, 3]
gyro_y = a[1:, 4]
gyro_z = a[1:, 5] 

plt.subplot(2,3,1)
plt.plot(t, acc_x)

plt.subplot(2,3,2)
plt.plot(t, acc_y)

plt.subplot(2,3,3)
plt.plot(t, acc_z)

plt.subplot(2,3,4)
plt.plot(t, gyro_x)

plt.subplot(2,3,5)
plt.plot(t, gyro_y)

plt.subplot(2,3,6)
plt.plot(t, gyro_z)

plt.show()

# Remove DC component