from multiprocessing import Process, Queue
from threading import Thread
from wiringpi import *
import time
from datetime import datetime

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
CTRL_REG1_M =           0x20
CTRL_REG2_M =           0x21
CTRL_REG3_M =           0x22
CTRL_REG4_M =           0x23

OUT_X_L_M =             0x28
OUT_X_H_M =             0x29
OUT_Y_L_M =             0x2A
OUT_Y_H_M =             0x2B
OUT_Z_L_M =             0x2C
OUT_Z_H_M =             0x2D

########################################################################


class MotionReader(Thread):
    
    def __init__(self, outputDir):
        Thread.__init__(self)
        self.outDir = outputDir

    def run(self):
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

        # Set Mag ODR to 80 Hz
        ctrlReg1M_Data = 0b01111100
        wiringPiI2CWriteReg8(imuMag, CTRL_REG1_M, ctrlReg1M_Data)

        # Set Mag resolution to 8 gauss
        ctrlReg2M_Data = 0b00100000
        wiringPiI2CWriteReg8(imuMag, CTRL_REG2_M, ctrlReg2M_Data)

        # Enable Mag
        ctrlReg3M_Data = 0b00000000
        wiringPiI2CWriteReg8(imuMag, CTRL_REG3_M, ctrlReg3M_Data)

        # Set Z axis of Mag as ultra-high performance
        ctrlReg4M_Data = 0b00001100
        wiringPiI2CWriteReg8(imuMag, CTRL_REG4_M, ctrlReg4M_Data)
        
        # Create file to save data
        ts = datetime.now()
        outFile = self.outDir + "motion_{0}-{1}-{2}_{3}-{4}-{5}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)
        
        with open(outFile, 'w') as f:
            header = 'ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z,MAG_X,MAG_Y,MAG_Z,TIME,SAMPLE_TIME\n'
            f.write(header)

        # Start raw data reader process
        q = Queue()
        readerProcess = ImuReader(imuAG, imuMag, q)
        readerProcess.start()
        
        writerProcess = ImuWriter(outFile, q)
        writerProcess.start()
            
        
class ImuReader(Process):
    
    def __init__(self, imuAG, imuMag, q):
        Process.__init__(self)
        self.q = q
        self.imuAG = imuAG
        self.imuMag = imuMag
    
    def run(self):
        
        # Main loop that polls data indefinitely
        prevTime = time.time()
        
        while True:
            
            accel_X = wiringPiI2CReadReg16(self.imuAG, OUT_X_L_A)
            accel_Y = wiringPiI2CReadReg16(self.imuAG, OUT_Y_L_A)
            accel_Z = wiringPiI2CReadReg16(self.imuAG, OUT_Z_L_A)
                        
            gyro_X = wiringPiI2CReadReg16(self.imuAG, OUT_X_L_G)
            gyro_Y = wiringPiI2CReadReg16(self.imuAG, OUT_Y_L_G)
            gyro_Z = wiringPiI2CReadReg16(self.imuAG, OUT_Z_L_G)

            mag_X = wiringPiI2CReadReg16(self.imuMag, OUT_X_L_M)
            mag_Y = wiringPiI2CReadReg16(self.imuMag, OUT_Y_L_M)
            mag_Z = wiringPiI2CReadReg16(self.imuMag, OUT_Z_L_M)

            #~ mag_X_L = wiringPiI2CReadReg8(self.imuMag, OUT_X_L_M)
            #~ mag_X_H = wiringPiI2CReadReg8(self.imuMag, OUT_X_H_M)
            #~ mag_X = (mag_X_H << 8) | mag_X_L
            
            # Update time sampling variables
            ts = datetime.now()        # Might need to use GMT-0 to protect agst local time changes???
            mTime = time.time() - prevTime
            prevTime = time.time()
            
            
            self.q.put([accel_X, accel_Y, accel_Z, gyro_X, gyro_Y, gyro_Z, mag_X, mag_Y, mag_Z, ts, mTime])
            
            time.sleep(1.0 / 200.0)
      
        
class ImuWriter(Process):
    
    def __init__(self, outFile, q):
        Process.__init__(self)
        self.q = q
        self.outFile = outFile
    
    def run(self):
        
        while True:
            
            data = self.q.get(True, None)
            
            with open(self.outFile, 'a') as f:
                f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(*data))
