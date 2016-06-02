from motionReader import MotionReader
from videoReader import VideoReader
from gpsReader import GpsReader


outputDir = "/home/pi/Desktop/Data_Collection/Data/"

motionReader = MotionReader(outputDir)
motionReader.start()

videoReader = VideoReader(outputDir)
videoReader.start()

gpsReader = GpsReader(outputDir)
gpsReader.start()
