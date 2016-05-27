from motionReader import MotionReader
from videoReader import VideoReader
from gpsReader import GpsReader


outputDir = "/home/pi/Desktop/Video_Capture/Data/"

motionReader = MotionReader(outputDir)
motionReader.start()

videoReader = VideoReader(outputDir)
videoReader.start()

gpsReader = GpsReader(outputDir)
gpsReader.start()