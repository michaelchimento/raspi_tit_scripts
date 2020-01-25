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

def crop_folder(directory):
    for item in os.listdir(directory):
        print(item)
        fullpath = directory+"/"+item
        print(fullpath)
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            imCrop = im.crop((0,1080/5,1920,1080/5*4))
            print("cropped")
            imCrop.save(fullpath, 'JPEG', quality=100)

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
        camera.color_effects = camera_color_effects
        camera.iso = camera_ISO
        camera.exposure_mode, camera.shutter_speed = set_exposure_shutter(hour)
        time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dir_name = '{}{}_{}'.format(filepath,filenamePrefix,time_stamp)
        os.mkdir(dir_name)
        camera.annotate_text_size = 15
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        #resize_tuple = (int(camera.resolution[0]),int(resize_scale*camera.resolution[1]))
        for i, filename in enumerate(camera.capture_continuous("{}/{}_".format(dir_name,filenamePrefix)+"{timestamp:%Y-%m-%d-%H-%M-%S-%f}.jpg")):
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            if i == 599:
                return dir_name

while (True):
    hour = datetime.now().hour
    if hour >= social_start and hour < social_end:
        dir_name = make_photos(hour)
        crop_folder(dir_name)
        shutil.move(dir_name,moved_path)
    else:
        pass
