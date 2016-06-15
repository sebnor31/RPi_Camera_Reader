#! /usr/bin/python
# Author: Nordine Sebkhi

from gps import *
from time import *
import time
import threading
from datetime import datetime
from math import cos, sin, radians, degrees, atan2


class GpsReader(threading.Thread):

    def __init__(self, outputDir):
        threading.Thread.__init__(self)
        self.gpsPoller = GpsPoller()
        self.outDir = outputDir

    def run(self):
        print("GPS: Connecting...")
        self.gpsPoller.start()

        gpsFound = False
        prevLat = 0
        prevLon = 0

        while True:
            gpsData = self.gpsPoller.getCurrentValue()

            if (gpsData is not None and hasattr(gpsData, 'mode') and gpsData.mode == 3):

                # Get time stamp of current sample
                ts = datetime.now()

                # Create new file at each new data collection
                if not gpsFound:
                    print("GPS : Connected!!")
                    gpsFound = True
                    gpsFile = self.outDir + "gps_{0}-{1}-{2}_{3}-{4}-{5}.csv".format(
                        ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)

                    with open(gpsFile, 'w') as f:
                        f.write('LAT,LON,BEARING,ALT,SPEED,CLIMB,GPS_TIME,RPI_TIME\n')

                # Append gps data
                timeGPS = gpsData.time
                lat = gpsData.lat        # Degrees (North:+ South:-)
                lon = gpsData.lon        # Degrees (East:+  West:-)
                alt = gpsData.alt        # Meters
                speed = gpsData.speed    # Meters per second
                climb = gpsData.climb    # Climb(+) or Sink(-) in meters per second

                if (prevLat == 0):
                    bearing = 0
                else:
                    bearing = self.getBearing(prevLat, prevLon, lat, lon)

                with open(gpsFile, 'a') as f:
                    f.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(
                        lat, lon, bearing, alt, speed, climb, timeGPS, ts))

                # prepare for next iteration
                prevLat = lat
                prevLon = lon
                time.sleep(0.5)

    def getBearing(self, lat_start_deg, lon_start_deg, lat_end_deg, lon_end_deg):
        latStart = radians(lat_start_deg)
        lonStart = radians(lon_start_deg)
        latEnd = radians(lat_end_deg)
        lonEnd = radians(lon_end_deg)

        d_Lon = lonEnd - lonStart

        x = cos(latEnd) * sin(d_Lon)
        y = cos(latStart) * sin(latEnd) - sin(latStart) * cos(latEnd) * cos(d_Lon)

        bearingRad = atan2(x, y)
        return degrees(bearingRad)


class GpsPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.current_value = None

    def getCurrentValue(self):
        return self.current_value

    def run(self):

        gpsd = gps(mode=WATCH_ENABLE)   # starting the stream of info

        try:
            while True:
                self.current_value = gpsd.next()

        except StopIteration:
            pass

##################################
# Test
#############################
if __name__ == "__main__":
    latStart = 39.099912
    lonStart = -94.581213
    latEnd = 38.627089
    lonEnd = -90.200203

    gpsReader = GpsReader("don't care'")
    bearing = gpsReader.getBearing(latStart, lonStart, latEnd, lonEnd)
    print("Bearing (deg) = {0:f}".format(bearing))