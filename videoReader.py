#! /usr/bin/python
from threading import Thread
import picamera
from datetime import datetime
from subprocess import call
from time import sleep
import os


class VideoReader(Thread):

    def __init__(self, outputDir):
        Thread.__init__(self)
        self.outDir = outputDir

    def run(self):
        # Setup camera
        mFrameRate = 30
        mResolution = (1920, 1080)    # HD Resolution (1080p)
        camera = picamera.PiCamera(resolution=mResolution, framerate=mFrameRate)

        # Setup recording parameters
        maxVidLen = 3600       # Length of each video file (in seconds)
        mBitRate = 25000000    # Max supported bit rate to provide higher quality
        mQuality = 10	       # For H264 format, 10 is min value for the highest quality

        prevRawVideo = ""
        prevVidName = ""

        vidIdx = 0
        while True:
            ts = datetime.now()
            video_name = "video_{0}-{1}-{2}_{3}-{4}-{5}_{6}".format(ts.year, ts.month,
                                                                ts.day, ts.hour, ts.minute, ts.second, vidIdx)
            raw_video = self.outDir + video_name + ".h264"

            if (vidIdx == 0):
                camera.start_recording(raw_video, bitrate=mBitRate, quality=mQuality)
                camera.wait_recording(maxVidLen)

            else:
                try:  
                    camera.split_recording(raw_video)
                    
                except picamera.PiCameraRuntimeError:
                    camera.stop_recording()
                    camera.start_recording(raw_video, bitrate=mBitRate, quality=mQuality)

                # Video Format conversion must be done after splitting occured
                # Otherwise, an exception is thrown by picamera
                #formatVidThread = Thread(target=self.convertVidFormat, args=(prevVidName, prevRawVideo))
                #formatVidThread.start()
                camera.wait_recording(maxVidLen)

            prevRawVideo = raw_video
            prevVidName = video_name
            vidIdx += 1

    def convertVidFormat(self, baseFilename, origFilepath):
            # Convert from h264 to MP4 format
            out_video = self.outDir + baseFilename + ".mp4"

            command = "MP4Box -add " + origFilepath + " " + out_video
            sleep(2)  	# Wait for video splitting to complete
            call([command], shell=True)

            # Remove original video file
            sleep(2)  	# wait for format conversion to complete
            os.remove(origFilepath)
