#!/usr/bin/python3
# You need to install PIL to run this script
# type "sudo apt-get install python-imaging-tk" in an terminal window to do this

from io import StringIO
import subprocess
import socket
import os
import shutil
import time
from datetime import datetime
from PIL import Image
import picamera
from rpi_info import name
from camera_settings import *

# Motion detection settings:
# Threshold          - how much a pixel has to change by to be marked as "changed"
# Sensitivity        - how many changed pixels before capturing an image, needs to be higher if noisy view
# ForceCapture       - whether to force an image to be captured every forceCaptureTime seconds, values True or False
# filepath           - location of folder to save photos
# filenamePrefix     - string that prefixes the file name for easier identification of files.
# diskSpaceToReserve - Delete oldest images to avoid filling disk. How much byte to keep free on disk.
# cameraSettings     - "" = no extra settings; "-hf" = Set horizontal flip of image; "-vf" = Set vertical flip; "-hf -vf" = both horizontal and vertical flip
threshold = 10
sensitivity = sensitivity_value
forceCapture = False
forceCaptureTime = 60 * 60 # Once an hour
filenamePrefix = name
filepath = "/home/pi/APAPORIS/CURRENT/"
moved_path = "/home/pi/APAPORIS/MOVED/"
video_duration = 180
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
cameraSettings = ""

# Test-Image settings
testWidth = 200
testHeight = 150

# this is the default setting, if the whole image should be scanned for changed pixel
testAreaCount = 1
# [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
testBorders = [ [[1,testWidth],[1,testHeight]] ]
debugMode = True

# Capture a small test image (for motion detection)
def captureTestImage(settings, width, height):
    command = "raspistill {} -w {} -h {} -t 200 -e bmp -n -o -".format(settings, width, height)
    output = subprocess.check_output(command, shell=True)
    im = Image.frombytes(mode="RGB",size=(width,height),data=output)
    buffer = im.load()
    return im, buffer

def make_photos(hour):
    global filepath
    global moved_path
    with picamera.PiCamera() as camera:
        camera.rotation = camera_rotation
        camera.zoom = social_zoom
        camera.resolution = camera_resolution
        camera.brightness = camera_brightness
        camera.sharpness = camera_sharpness
        camera.contrast = camera_contrast
        camera.awb_mode = camera_awb_mode
        camera.iso = camera_ISO
        camera.exposure_mode, camera.shutter_speed = set_exposure_shutter(hour)
        time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dir_name = '{}{}_{}'.format(filepath,filenamePrefix,time_stamp)
        os.mkdir(dir_name)
        camera.annotate_text_size = 15
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        for i, filename in enumerate(camera.capture_continuous("{}/{}_".format(dir_name,filenamePrefix)+"{timestamp:%Y-%m-%d-%H-%M-%S-%f}.jpg")):
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            if i == 599:
                return dir_name

while (True):
    hour = datetime.now().hour
    if hour >= social_start and hour < social_end:
        dir_name = make_photos(hour)
        shutil.move(dir_name,moved_path)
    else:
        pass
