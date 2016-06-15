from threading import Thread
from datetime import datetime
import time
import RTIMU
import os.path
import math


class MotionReader(Thread):

    def __init__(self, outputDir):
        Thread.__init__(self)
        self.outDir = outputDir

    def run(self):
        # Connect to the motion sensor (IMU)
        print("IMU: Connecting...")

        SETTINGS_FILE = "RTIMULib"

        if not os.path.exists(SETTINGS_FILE + ".ini"):
            print("Settings file does not exist, will be created")

        bnoConnected = False

        while not bnoConnected:
            try:

                s = RTIMU.Settings(SETTINGS_FILE)
                imu = RTIMU.RTIMU(s)

                if (not imu.IMUInit()):
                    time.sleep(0.5)
                    continue

                else:
                    bnoConnected = True
                    print("IMU: {0} Connected!!".format(imu.IMUName()))

            except:
                time.sleep(1)

        # this is a good time to set any fusion parameters

        imu.setSlerpPower(0.02)
        imu.setGyroEnable(True)
        imu.setAccelEnable(True)
        imu.setCompassEnable(True)

        poll_interval = imu.IMUGetPollInterval()
        print("IMU: Recommended Poll Interval: %dmS\n" % poll_interval)

        ts = datetime.now()
        outFile = self.outDir + "motion_{0}-{1}-{2}_{3}-{4}-{5}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)

        with open(outFile, 'w') as f:
            header = 'ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z,MAG_X,MAG_Y,MAG_Z,HEAD,ROLL,PITCH,LIN_X,LIN_Y,LIN_Z,GRAV_X,GRAV_Y,GRAV_Z,TIME\n'
            f.write(header)

        # Main loop that polls data indefinitely
        while True:

            if imu.IMURead():
                # Get current sample time stamp
                ts = datetime.now()        # Might need to use GMT-0 to protect agst local time changes???

                # x, y, z = imu.getFusionData()
                # print("%f %f %f" % (x,y,z))
                data = imu.getIMUData()

                # Accelerometer data (in meters per second squared):
                accel_x, accel_y, accel_z = data["accel"]

                # Gyroscope data (in degrees per second):
                gyro_x, gyro_y, gyro_z = data["gyro"]

                # Magnetometer data (in micro-Teslas):
                mag_x, mag_y, mag_z = data["compass"]

                # Read the Euler angles (in degrees)
                heading, roll, pitch = data["fusionPose"]

                # Linear acceleration data (i.e. acceleration from movement, not gravity--
                # returned in meters per second squared):
                #lin_x, lin_y, lin_z = bno.read_linear_acceleration()
                lin_x, lin_y, lin_z = (0, 0, 0)

                # Gravity acceleration data (i.e. acceleration just from gravity--returned
                # in meters per second squared):
                #grav_x, grav_y, grav_z = bno.read_gravity()
                grav_x, grav_y, grav_z = (0, 0, 0)

                with open(outFile, 'a') as f:
                    f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}\n'.format(
                        accel_x, accel_y, accel_z,
                        gyro_x, gyro_y, gyro_z,
                        mag_x, mag_y, mag_z,
                        heading, roll, pitch,
                        lin_x, lin_y, lin_z,
                        grav_x, grav_y, grav_z,
                        ts))

                #time.sleep(poll_interval * 1.0 / 1000.0)
                time.sleep(1/120.0)    # Read data at ~120Hz
