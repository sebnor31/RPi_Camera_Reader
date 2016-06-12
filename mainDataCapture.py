#from motionReader import MotionReader
from motionReaderRich import MotionReader
from videoReader import VideoReader
from gpsReader import GpsReader
from subprocess import call

# Dir where data will be saved
# Make sure it also corresponds to the mount dir
outputDir = "/mnt/wheego/Data/"

# Mount Falsh drive to wheego folder
command = 'sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt/wheego'
call(command, shell=True)

# Launch data capture threads
#motionReader = MotionReader(outputDir)
#motionReader.start()

videoReader = VideoReader(outputDir)
videoReader.start()

gpsReader = GpsReader(outputDir)
gpsReader.start()
