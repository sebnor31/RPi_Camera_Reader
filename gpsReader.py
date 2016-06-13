#! /usr/bin/python
# Author: Nordine Sebkhi

import os
from gps import *
from time import *
import time
import threading
from datetime import datetime


class GpsReader(threading.Thread):

    def __init__(self, outputDir):
        threading.Thread.__init__(self)
        self.gpsPoller = GpsPoller()
        self.outDir = outputDir

    def run(self):
        print("GPS: Connecting...")
        self.gpsPoller.start()

        gpsFound = False

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
                        f.write('LAT,LON,ALT,SPEED,CLIMB,GPS_TIME,RPI_TIME\n')

                # Append gps data
                timeGPS = str(gpsData.time)
                lat = str(gpsData.lat)        # Degrees (North:+ South:-)
                lon = str(gpsData.lon)        # Degrees (East:+  West:-)
                alt = str(gpsData.alt)        # Meters
                speed = str(gpsData.speed)    # Meters per second
                climb = str(gpsData.climb)    # Climb(+) or Sink(-) in meters per second

                with open(gpsFile, 'a') as f:
                    f.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(lat, lon, alt, speed, climb, timeGPS, ts))

                # Print data
                #os.system('clear')
                #print(gpsData)
                #print
                #print ' GPS reading'
                #print '----------------------------------------'
                #print 'time        ', gpsData.time
                #print 'latitude    ', gpsData.lat
                #print 'longitude   ', gpsData.lon
                #print 'altitude (m)', gpsData.alt
                #print 'speed (m/s) ', gpsData.speed
                #print 'climb       ', gpsData.climb
                #print 'mode        ', gpsData.mode

                time.sleep(0.5)      # set to whatever


class GpsPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE)   # starting the stream of info
        self.current_value = None

    def getCurrentValue(self):
        return self.current_value

    def run(self):
        try:
            while True:
                self.current_value = self.gpsd.next()

        except StopIteration:
            pass
