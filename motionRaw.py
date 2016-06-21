from wiringpi import *
from time import sleep


########################################################################
#               REGISTER ADDRESS MAP

I2C_ADDR_XL_GYRO =      0x6B
I2C_ADDR_MAG =          0x1E

# Accel (A) and Gyro (G)
WHO_AM_I_AG =           0x0F
AG_ID =                 0x68
FIFO_CTRL =             0x2E
CTRL_REG4 =             0x1E

# Gyro (G)
CTRL_REG_1_G =          0x10
CTRL_REG3_G =           0x12

OUT_X_L_G =             0x18
OUT_X_H_G =             0x19
OUT_Y_L_G =             0x1A
OUT_Y_H_G =             0x1B
OUT_Z_L_G =             0x1C
OUT_Z_H_G =             0x1D

# Accelerometer (A)
CTRL_REG6_A =           0x20
CTRL_REG7_A =           0x21

OUT_X_L_A =             0x28
OUT_X_H_A =             0x29
OUT_Y_L_A =             0x2A
OUT_Y_H_A =             0x2B
OUT_Z_L_A =             0x2C
OUT_Z_H_A =             0x2D

# Magnetometer (M)
WHO_AM_I_M =            0x0F
M_ID =                  0x3D

########################################################################


# Initialize I2C communication
setupStat = wiringPiSetup()
imuAG = wiringPiI2CSetup(I2C_ADDR_XL_GYRO)
imuMag = wiringPiI2CSetup(I2C_ADDR_MAG)

# Verify connection is successfull by reading AG and Mag sensor IDs 
whoAmIAG = wiringPiI2CReadReg8(imuAG, WHO_AM_I_AG)
whoAmIMag = wiringPiI2CReadReg8(imuMag, WHO_AM_I_M)

# Set ODR to 238 Hz, CutOff freq to 78 and Gyro Res to 500 dps
CtrlReg1G_Data = 0b10001011
wiringPiI2CWriteReg8(imuAG, CTRL_REG_1_G, CtrlReg1G_Data)

#print("CTRL_REG1_G = {:08b}".format(wiringPiI2CReadReg8(imuAG, CTRL_REG_1_G)))

# Deactivate High-Pass Filter on Gyro
CtrlReg3G_Data = 0b00000000
wiringPiI2CWriteReg8(imuAG, CTRL_REG_1_G, CtrlReg1G_Data)

# Set accel + gyro mode and accel res to 8g
CtrlReg6A_Data = 0b00011000
wiringPiI2CWriteReg8(imuAG, CTRL_REG6_A, CtrlReg6A_Data)

# Set linear accel to high res and cutoff freq, also bypass internal filter
CtrlReg7A_Data = 0b11000000
wiringPiI2CWriteReg8(imuAG, CTRL_REG7_A, CtrlReg7A_Data)

# Disable FIFO, only read latest value to control sampling frequency
fifoCtrl_Data = 0b00000000
wiringPiI2CWriteReg8(imuAG, FIFO_CTRL, fifoCtrl_Data)


while True:
    
    gyro_X_L = wiringPiI2CReadReg8(imuAG, OUT_X_L_G)
    gyro_X_H = wiringPiI2CReadReg8(imuAG, OUT_X_H_G)
    gyro_X = (gyro_X_H << 4) | gyro_X_L
    
    gyro_Y_L = wiringPiI2CReadReg8(imuAG, OUT_Y_L_G)
    gyro_Y_H = wiringPiI2CReadReg8(imuAG, OUT_Y_H_G)
    gyro_Y = (gyro_Y_H << 4) | gyro_Y_L

    gyro_Z_L = wiringPiI2CReadReg8(imuAG, OUT_Z_L_G)
    gyro_Z_H = wiringPiI2CReadReg8(imuAG, OUT_Z_H_G)
    gyro_Z = (gyro_Z_H << 4) | gyro_Z_L

    print("Gyro: {0:d} ; {1:d} ; {2:d}".format(gyro_X, gyro_Y, gyro_Z))
    
    accel_X_L = wiringPiI2CReadReg8(imuAG, OUT_X_L_A)
    accel_X_H = wiringPiI2CReadReg8(imuAG, OUT_X_H_A)
    accel_X = (accel_X_H << 4) | accel_X_L
    
    accel_Y_L = wiringPiI2CReadReg8(imuAG, OUT_Y_L_A)
    accel_Y_H = wiringPiI2CReadReg8(imuAG, OUT_Y_H_A)
    accel_Y = (accel_Y_H << 4) | accel_Y_L

    accel_Z_L = wiringPiI2CReadReg8(imuAG, OUT_Z_L_A)
    accel_Z_H = wiringPiI2CReadReg8(imuAG, OUT_Z_H_A)
    accel_Z = (accel_Z_H << 4) | accel_Z_L
    
    print("Accel: {0:d} ; {1:d} ; {2:d}".format(accel_X, accel_Y, accel_Z))
    
    print("-------------\n")
    sleep(1.0/200.0)
    




