from threading import Thread
from datetime import datetime
import time
from Adafruit_BNO055 import BNO055


class MotionReader(Thread):

    def __init__(self, outputDir):
        Thread.__init__(self)
        self.outDir = outputDir

    def run(self):
        # Connect to the motion sensor (BNO055)
        bno = BNO055.BNO055()

        bnoConnected = False

        while not bnoConnected:
            try:
                bno.begin()
                bnoConnected = True

            except:
                time.sleep(1)
                continue

        print("BNO Connected !!!")

        # Get BNO status
        status, self_test, error = bno.get_system_status()
        print(("System status: {0}".format(status)))

        if status == 0x01:
            raise RuntimeError("BNO: Error reported by internal status")

        ts = datetime.now()
        outFile = self.outDir + "motion_{0}-{1}-{2}_{3}-{4}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute)

        with open(outFile, 'w') as f:
            header = 'HEAD,ROLL,PITCH,ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z,MAG_X,MAG_Y,MAG_Z,LIN_X,LIN_Y,LIN_Z,GRAV_X,GRAV_Y,GRAV_Z,TIME\n'
            f.write(header)

        # Main loop that polls data indefinitely
        while True:
            # Get current sample time stamp
            ts = datetime.now()        # Might need to use GMT-0 to protect agst local time changes???

            # Read the Euler angles (in degrees)
            heading, roll, pitch = bno.read_euler()

            # Accelerometer data (in meters per second squared):
            accel_x, accel_y, accel_z = bno.read_accelerometer()

            # Gyroscope data (in degrees per second):
            gyro_x, gyro_y, gyro_z = bno.read_gyroscope()

            # Magnetometer data (in micro-Teslas):
            mag_x, mag_y, mag_z = bno.read_magnetometer()

            # Linear acceleration data (i.e. acceleration from movement, not gravity--
            # returned in meters per second squared):
            lin_x, lin_y, lin_z = bno.read_linear_acceleration()

            # Gravity acceleration data (i.e. acceleration just from gravity--returned
            # in meters per second squared):
            grav_x, grav_y, grav_z = bno.read_gravity()

            with open(outFile, 'a') as f:
                f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}\n'.format(
                    heading % 360, roll % 360, pitch % 360,
                    accel_x, accel_y, accel_z,
                    gyro_x, gyro_y, gyro_z,
                    mag_x, mag_y, mag_z,
                    lin_x, lin_y, lin_z,
                    grav_x, grav_y, grav_z,
                    ts))

            time.sleep(1)