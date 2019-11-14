#!/usr/bin/python3
# You need to install PIL to run this script
# type "sudo apt-get install python-imaging-tk" in an terminal window to do this

from io import StringIO
import subprocess
import socket
import os
import time
from datetime import datetime
from PIL import Image
import picamera
from rpi_info import name

# Motion detection settings:
# Threshold          - how much a pixel has to change by to be marked as "changed"
# Sensitivity        - how many changed pixels before capturing an image, needs to be higher if noisy view
# ForceCapture       - whether to force an image to be captured every forceCaptureTime seconds, values True or False
# filepath           - location of folder to save photos
# filenamePrefix     - string that prefixes the file name for easier identification of files.
# diskSpaceToReserve - Delete oldest images to avoid filling disk. How much byte to keep free on disk.
# cameraSettings     - "" = no extra settings; "-hf" = Set horizontal flip of image; "-vf" = Set vertical flip; "-hf -vf" = both horizontal and vertical flip
threshold = 10
sensitivity = 250
forceCapture = False
forceCaptureTime = 60 * 60 # Once an hour
filepath = "/home/pi/APAPORIS/CURRENT/"
moved_path = "/home/pi/APAPORIS/MOVED/"
video_duration = 30
filepathphotos = "~/greti_photos/"
filenamePrefix = name
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
cameraSettings = ""

# settings of the photos to save
saveWidth   = 1296
saveHeight  = 972
saveQuality = 15 # Set jpeg quality (0 to 100)

# Test-Image settings
testWidth = 200
testHeight = 150

# this is the default setting, if the whole image should be scanned for changed pixel
testAreaCount = 1
testBorders = [ [[1,testWidth],[1,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
debugMode = True # False or True

# Capture a small test image (for motion detection)
def captureTestImage(settings, width, height):
    command = "raspistill {} -w {} -h {} -t 200 -e bmp -n -o -".format(settings, width, height)
    imageData = StringIO()
    output = subprocess.check_output(command, shell=True)
    im = Image.frombytes(mode="RGB",size=(width,height),data=output)
    buffer = im.load()
    imageData.close()
    return im, buffer

# Save a full size image to disk
def saveImage(settings, width, height, quality, diskSpaceToReserve):
    filename = moved_path + filenamePrefix + datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    subprocess.check_output("raspistill {} -w {} -h {} -t 200 -e jpg -q {} -n -o {}".format(settings, width, height, quality, filename), shell=True)
    #print "Captured %s" % filename

# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(moved_path + filename)
                print("Deleted {} to avoid filling disk".format(filename))
                if (getFreeSpace() > bytesToReserve):
                    return

# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du

def make_photos():
    global filepath
    global moved_path
    with picamera.PiCamera() as camera:
        camera.rotation = 0
        camera.resolution = (1280,720)
        camera.brightness = 50
        camera.shutter_speed = (0)
        camera.awb_mode = 'tungsten' 
        camera.ISO = (0)
        camera.annotate_text_size = 15
        for i, filename in camera.capture_continuous("{}{timestamp:%Y-%m-%d_%H-%M-%S-%f}.jpg".format(filepath)):
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sleep(1)
            if i == 10:
            break

while (True):
    saveImage()
    keepDiskSpaceFree(diskSpaceToReserve)
    time.sleep(.25)
        
