#! /usr/bin/python
from threading import Thread
import gps
from datetime import datetime
from subprocess import call


class GpsReader(Thread):

    def __init__(self, outputDir):
        Thread.__init__(self)
        self.outDir = outputDir

        #command = "sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock"
        #call([command], shell=True)

    def run(self):
        # Listen on port 2947 (gpsd) of localhost
        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        print("GPS : Connecting.... ")
        gpsFound = False

        while True:
            try:
                report = session.next()

                # Wait for a "TPV" report and display current time
                if hasattr(report, 'lat'):

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
                    time = str(report.time)
                    lat = str(report.lat)        # Degrees (North:+ South:-)
                    lon = str(report.lon)        # Degrees (East:+  West:-)
                    alt = str(report.alt)        # Meters
                    speed = str(report.speed)    # Meters per second
                    climb = str(report.climb)    # Climb(+) or Sink(-) in meters per second

                    with open(gpsFile, 'a') as f:
                        f.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(lat, lon, alt, speed, climb, time, ts))

	    except AttributeError:
                continue
				
            except KeyError:
                pass

            except StopIteration:
                session = None
                print("GPSD has terminated")

            except KeyboardInterrupt:
                quit()



