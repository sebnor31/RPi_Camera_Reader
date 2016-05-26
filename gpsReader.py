import gps
from datetime import datetime


# Input
ts = datetime.now()
gpsDir = "/home/pi/Desktop/Video_Capture/Data/"
gpsFile = gpsDir + "gps_{0}-{1}-{2}_{3}-{4}.csv".format(ts.year, ts.month, ts.day, ts.hour, ts.minute)

with open(gpsFile, 'w') as f:
    f.write('LAT,LON,ALT,SPEED,CLIMB,TIME\n')


# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
#        print((report))

        # Wait for a "TPV" report and display current time
        if report['class'] == 'TPV':
            time = str(report.time)
            lat = str(report.lat)        # Degrees (North:+ South:-)
            lon = str(report.lon)        # Degrees (East:+  West:-)
            alt = str(report.alt)        # Meters
            speed = str(report.speed)    # Meters per second
            climb = str(report.climb)    # Climb(+) or Sink(-) in meters per second

            with open(gpsFile, 'a') as f:
                f.write('{0},{1},{2},{3},{4},{5}\n'.format(lat, lon, alt, speed, climb, time))

    except KeyError:
        pass

    except KeyboardInterrupt:
        quit()

    except StopIteration:
        session = None
        print("GPSD has terminated")

