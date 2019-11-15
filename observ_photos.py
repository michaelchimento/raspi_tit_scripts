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

filepath = "/home/pi/APAPORIS/CURRENT/"
moved_path = "/home/pi/APAPORIS/MOVED/"
filenamePrefix = name


def make_photos():
    global filepath
    global moved_path
    with picamera.PiCamera() as camera:
        camera.rotation = camera_rotation
        camera.resolution = camera_resolution
        camera.brightness = camera_brightness
        camera.shutter_speed = camera_shutter_speed
        camera.awb_mode = camera_awb_mode 
        camera.ISO = camera_ISO
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dir_name = '{}{}_{}'.format(filepath,filenamePrefix,time_stamp)
        os.mkdir(dir_name)
        camera.annotate_text_size = 15
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        for i, filename in enumerate(camera.capture_continuous("{}/{}_".format(dir_name,filenamePrefix)+"{timestamp:%Y-%m-%d-%H-%M-%S-%f}.jpg")):
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            if i == 600:
                return dir_name

while (True):
    hour = datetime.now().hour
    while hour >= 7 and hour < 19:
        dir_name = make_photos()
        shutil.move(dir_name,moved_path)