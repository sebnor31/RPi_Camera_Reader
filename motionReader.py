from threading import Thread
from datetime import datetime
import time
import RTIMU
import os.path
from math import degrees


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
                    print(("IMU: {0} Connected!!".format(imu.IMUName())))

            except:
                time.sleep(1)

        # this is a good time to set any fusion parameters

        imu.setSlerpPower(0.02)
        imu.setGyroEnable(True)
        imu.setAccelEnable(True)
        imu.setCompassEnable(True)

        ts = datetime.now()
        outFile = self.outDir + "motion_{0}-{1}-{2}_{3}-{4}-{5}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)

        with open(outFile, 'w') as f:
            header = 'ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z,MAG_X,MAG_Y,MAG_Z,HEAD,ROLL,PITCH,QPOS_A,QPS_B,QPOS_C,QPOS_D,TIME\n'
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
                roll, pitch, heading = data["fusionPose"]

                # Quaternion position
                qpos_a, qpos_b, qpos_c, qpos_d = data["fusionQPose"]

                with open(outFile, 'a') as f:
                    f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}\n'.format(
                        accel_x, accel_y, accel_z,
                        gyro_x, gyro_y, gyro_z,
                        mag_x, mag_y, mag_z,
                        degrees(heading), degrees(roll), degrees(pitch),
                        qpos_a, qpos_b, qpos_c, qpos_d,
                        ts))

                time.sleep(1 / 120.0)    # Read data at ~120Hz
