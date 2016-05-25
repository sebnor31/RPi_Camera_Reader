#! /usr/bin/python
import picamera
from datetime import datetime
from subprocess import call
import threading
from time import sleep
import os


def startCamera(e):

    maxVidLen = 10         # Length of each video file (in seconds)
    inc = 1                # Increment (seconds) to check if key pressed to stop recording
    mBitRate = 25000000    # Max supported bit rate to provide higher quality
    mQuality = 10		# For H264 format, 10 is min value for the highest quality

    prevRawVideo = ""
    prevVidName = ""

    for i in range(0, 10):
        ts = datetime.now()
        video_name = "video_{0}-{1}-{2}_{3}-{4}_{5}".format(ts.year, ts.month,
                                                            ts.day, ts.hour, ts.minute, i)
        raw_video = outputDir + video_name + ".h264"

        if (i == 0):
            camera.start_recording(raw_video, bitrate=mBitRate, quality=mQuality)

        else:
            camera.split_recording(raw_video)

            # Video Format conversion must be done after splitting occured
            # Otherwise, an exception is thrown by picamera
            formatVidThread = threading.Thread( name='Format_Video',
            									target=convertVidFormat,
            									args=(prevVidName, prevRawVideo))
            formatVidThread.start()

        # Verify periodically if stop recording signal emitted (using thread event "e")
        time = 0
        while(time < maxVidLen):
            time += 1
            if e.is_set():
                return

            else:
                sleep(inc)

    prevRawVideo = raw_video
    prevVidName = video_name

    return


def stopCamera(e):
    # Wait for user to press a key to stop recording
    raw_input("Press any key to stop recording....")
    e.set()

    # Closing procedure
    camera.stop_recording()
    camera.close()
    print("Camera close")
    return


def convertVidFormat(baseFilename, origFilepath):
        # Convert from h264 to MP4 format
        out_video = outputDir + baseFilename + ".mp4"

        command = "MP4Box -add " + origFilepath + " " + out_video
        sleep(5)  	# Wait for video splitting to complete
        call([command], shell=True)

        # Remove original video file
        sleep(5)  	# wait for format conversion to complete
        os.remove(origFilepath)
        return


# Setup camera
mFrameRate = 30
mResolution = (1920, 1080)    # HD Resolution (1080p)
camera = picamera.PiCamera(resolution=mResolution, framerate=mFrameRate)
#camera.framerate = 30
#camera.resolution = (1920, 1080)    # HD Resolution (1080p)

outputDir = "/home/pi/Desktop/Video_Capture/Data/"


# Start threads for starting and stopping video recording
e = threading.Event()
t1 = threading.Thread(name='Record_Cam', target=startCamera, args=(e,))
t2 = threading.Thread(name='Stop_Cam', target=stopCamera, args=(e,))
t1.start()
t2.start()
