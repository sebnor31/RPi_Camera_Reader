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
        print("BNO: Connecting...")

        while not bnoConnected:
            try:
                # Get raw and fusion sensor data
                bno.begin(mode=BNO055.OPERATION_MODE_NDOF)
                bnoConnected = True
                print("BNO: Connected !!")

            except:
                time.sleep(1)

        # Get BNO status
        status, self_test, error = bno.get_system_status()
        print(("BNO Status:\n\tSystem    = {0:x}\n\tSelf Test = {1:x}\n\tError     = {2:x}".format(
            status & 0x0F, self_test & 0x0F, error & 0x0F)))

        if status == 0x01:
            raise RuntimeError("BNO: Error reported by internal status")

        ts = datetime.now()
        outFile = self.outDir + "motion_{0}-{1}-{2}_{3}-{4}-{5}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)

        with open(outFile, 'w') as f:
            header = 'ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z,MAG_X,MAG_Y,MAG_Z,HEAD,ROLL,PITCH,LIN_X,LIN_Y,LIN_Z,GRAV_X,GRAV_Y,GRAV_Z,TIME\n'
            f.write(header)

        # Main loop that polls data indefinitely
        while True:
            # Get current sample time stamp
            ts = datetime.now()        # Might need to use GMT-0 to protect agst local time changes???

            # Accelerometer data (in meters per second squared):
            accel_x, accel_y, accel_z = bno.read_accelerometer()

            # Gyroscope data (in degrees per second):
            gyro_x, gyro_y, gyro_z = bno.read_gyroscope()

            # Magnetometer data (in micro-Teslas):
            mag_x, mag_y, mag_z = bno.read_magnetometer()

            # Read the Euler angles (in degrees)
            heading, roll, pitch = bno.read_euler()

            # Linear acceleration data (i.e. acceleration from movement, not gravity--
            # returned in meters per second squared):
            lin_x, lin_y, lin_z = bno.read_linear_acceleration()

            # Gravity acceleration data (i.e. acceleration just from gravity--returned
            # in meters per second squared):
            grav_x, grav_y, grav_z = bno.read_gravity()

            with open(outFile, 'a') as f:
                f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}\n'.format(
                    accel_x, accel_y, accel_z,
                    gyro_x, gyro_y, gyro_z,
                    mag_x, mag_y, mag_z,
                    heading, roll, pitch,
                    lin_x, lin_y, lin_z,
                    grav_x, grav_y, grav_z,
                    ts))

            time.sleep(1/30.0)    # Read data at ~30Hz
