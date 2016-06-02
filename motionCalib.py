from datetime import datetime
import time
from Adafruit_BNO055 import BNO055

bno = BNO055.BNO055()
bno.begin(mode=BNO055.OPERATION_MODE_NDOF)

outputDir = "/home/pi/Desktop/Video_Capture/Data/"
ts = datetime.now()
outFile = outputDir + "calib_motion_{0}-{1}-{2}_{3}-{4}-{5}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)
with open(outFile, 'w') as f:
    header = 'ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z,MAG_X,MAG_Y,MAG_Z,ELAPSED_TIME\n'
    f.write(header)


startTime = time.time()
elapsedTime = 0.0

print("Collecting Data....")
while elapsedTime < 60:
    # Accelerometer data (in meters per second squared):
    accel_x, accel_y, accel_z = bno.read_accelerometer()

    # Gyroscope data (in degrees per second):
    gyro_x, gyro_y, gyro_z = bno.read_gyroscope()

    # Magnetometer data (in micro-Teslas):
    mag_x, mag_y, mag_z = bno.read_magnetometer()

    elapsedTime = time.time() - startTime

    with open(outFile, 'a') as f:
        f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(
            accel_x, accel_y, accel_z,
            gyro_x, gyro_y, gyro_z,
            mag_x, mag_y, mag_z,
            elapsedTime))
            
    time.sleep(0.01)

print("Calibration Done!!")
