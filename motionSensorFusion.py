# -*- coding: utf-8 -*-
"""
@author: Nordine Sebkhi
"""

import numpy as np
import matplotlib.pyplot as plt

#==============================================================================
#                HELPER FUNCTIONS
#==============================================================================
def signedInt(rawArray):
    """Converts unsigned to signed 16-bit raw data."""
    signedList = []
    
    for i in range(0, len(rawArray) ):
        
        if int(rawArray[i]) < 32768:
            signedList.append(rawArray[i])
            
        else:
            signedList.append(~(int(rawArray[i]) ^ 0xFFFF))
            
    return np.array(signedList)

#==============================================================================
#                MAIN
#==============================================================================
if __name__ == "__main__":
    
    rawCalibFile = "C:\Users\sebnor\Desktop\data\Motion/Raw Data/motion_2016-6-23_15-44-30.csv"
    a = np.genfromtxt(rawCalibFile, delimiter=',')
    
    print('Num of Rows: %d' % len(a))
    
    # Get Raw Data
    t = range(0,(len(a) -1))
    acc_x_raw = a[1:, 0]
    acc_y_raw = a[1:, 1]
    acc_z_raw = a[1:, 2]
    
    gyro_x_raw = a[1:, 3]
    gyro_y_raw = a[1:, 4]
    gyro_z_raw = a[1:, 5] 
    
    mag_x_raw = a[1:, 6]
    mag_y_raw = a[1:, 7]
    mag_z_raw = a[1:, 8] 
    
    #==============================================================================
    # yaw = np.degrees(a[1:, 9])
    # roll = np.degrees(a[1:, 10])
    # pitch = np.degrees(a[1:, 11])
    #==============================================================================
    
    
    # Sign raw data
    acc_x_sign = signedInt(acc_x_raw)
    acc_y_sign = signedInt(acc_y_raw)
    acc_z_sign = signedInt(acc_z_raw)
    
    gyro_x_sign = signedInt(gyro_x_raw)
    gyro_y_sign = signedInt(gyro_y_raw)
    gyro_z_sign = signedInt(gyro_z_raw)
    
    mag_x_sign = signedInt(mag_x_raw)
    mag_y_sign = signedInt(mag_y_raw)
    mag_z_sign = signedInt(mag_z_raw)
    
    
    # Convert raw data to their physical value (refer to LSM9DS1 datasheet)
    accSensitivity = 0.000244              # +/- 8 g resolution
    acc_x = (acc_x_sign * accSensitivity)
    acc_y = (acc_y_sign * accSensitivity)
    acc_z = (acc_z_sign * accSensitivity) 
    
    gyroSensitivity = 0.0175              # +/- 500 dps resolution
    gyro_x = (gyro_x_sign * gyroSensitivity) 
    gyro_y = (gyro_y_sign * gyroSensitivity) 
    gyro_z = (gyro_z_sign * gyroSensitivity)
    
    magSensitivity = 0.00029              # +/- 8 gauss resolution
    mag_x = (mag_x_sign * magSensitivity) 
    mag_y = (mag_y_sign * magSensitivity) 
    mag_z = (mag_z_sign * magSensitivity)
    
    
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
    
    #==============================================================================
    # plt.subplot(3,4,4)
    # plt.title("Roll (X)")
    # plt.plot(t, roll)
    # plt.ylim([-90, 90])
    # plt.grid()
    # 
    # plt.subplot(3,4,8)
    # plt.title("Pitch (Y)")
    # plt.plot(t, pitch)
    # plt.ylim([0, 180])
    # plt.grid()
    # 
    # plt.subplot(3,4,12)
    # plt.title("Yaw (Z)")
    # plt.plot(t, yaw)
    # plt.ylim([-90, 90])
    # plt.grid()
    #==============================================================================
    
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.show()