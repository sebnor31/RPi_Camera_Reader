#from motionReader import MotionReader
from motionRaw import MotionReader
from videoReader import VideoReader
#from gpsReader import GpsReader
from subprocess import call
from datetime import datetime
import os


# Mount Falsh drive to wheego folder
command = 'sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt/wheego'
call(command, shell=True)

# Root directory where data will be saved
# Make sure it also corresponds to the mount dir
rootDir = "/mnt/wheego/Data"

if not os.path.exists(rootDir):
    os.makedirs(rootDir)

# Read MAC address (et0) as unique ID of device
macAddr = ''
with open('/sys/class/net/eth0/address') as f:
    macAddr = f.read().rstrip('\n')
    macAddr = macAddr.replace(":", "")  # Cannot create folder name that includes ":"

macDir = "{0}/{1}".format(rootDir, macAddr)

if not os.path.exists(macDir):
    os.makedirs(macDir)

# Dir witch current time stamp
ts = datetime.now()
outputDir = macDir + "/{0}-{1}-{2}_{3}-{4}-{5}/".format(
                        ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, macAddr)

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# Launch data capture threads
motionReader = MotionReader(outputDir)
motionReader.start()

#videoReader = VideoReader(outputDir)
#videoReader.start()

#gpsReader = GpsReader(outputDir)
#gpsReader.start()
