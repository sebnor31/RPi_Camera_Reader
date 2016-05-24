#! /usr/bin/python3
import picamera
from datetime import datetime
from subprocess import call
import threading
from time import sleep


def startCamera(e):
    outputDir = "/home/pi/Desktop/Video_Capture/Data/"
    maxVidLen = 10   # Length of each video file (in seconds)
    inc = 1         # Time Increment to check if a key was pressed to stop recording (in seconds)
    
     
    for i in range(0, 10):
        ts = datetime.now() 
        video_name = "video_{0}-{1}-{2}_{3}-{4}_{5}".format(ts.year, ts.month, ts.day, ts.hour, ts.minute, i)
        raw_video =  outputDir + video_name + ".h264"

        if (i == 0):
            camera.start_recording(raw_video)

        else:
            camera.split_recording(raw_video)

        # Verify periodically if a stop recoprding signal was emitted (using thread event "e")
        time = 0
        while(time < maxVidLen):
            time += 1
            if e.is_set():
                return
            
            else:
                sleep(inc)


def stopCamera(e):
    # Wait for user to press a key to stop recording
    input("Press any key to stop recording....")
    e.set()

    # Closing procedure
    camera.stop_recording()
    camera.close()
    print("Camera close")


# Setup camera
camera = picamera.PiCamera()
camera.framerate = 30
camera.resolution = (1920, 1080)    # HD Resolution (1080p)

# Start threads for starting and stopping video recording 
e = threading.Event()
t1 = threading.Thread(name='Record_Cam', target=startCamera, args=(e,))
t2 = threading.Thread(name='Stop_Cam', target=stopCamera, args=(e,))
t1.start()
t2.start()   
