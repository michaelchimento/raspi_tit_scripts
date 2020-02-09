#!/usr/bin/python3

import subprocess, socket, os, shutil, time, picamera, signal
from io import StringIO
from datetime import datetime
from PIL import Image
from rpi_info import name
from camera_settings import *
from sigterm_exception import *

filepath = "/home/pi/APAPORIS/CURRENT/"
moved_path = "/home/pi/APAPORIS/MOVED/"
filenamePrefix = name

def crop_folder(directory):
    for item in os.listdir(directory):
        try:
            fullpath = directory+"/"+item
            if os.path.isfile(fullpath):
                im = Image.open(fullpath)
                imCrop = im.crop((0,1080/4,1920,1080/4*3))
                imCrop.save(fullpath, 'JPEG', quality=100)
        except Exception:
            raise Exception

def make_photos(hour):
    global filepath
    global moved_path
    with picamera.PiCamera() as camera:
        camera.rotation = camera_rotation
        camera.zoom = observ_zoom
        camera.resolution = camera_resolution
        camera.brightness = camera_brightness
        camera.sharpness = camera_sharpness
        camera.contrast = camera_contrast
        camera.awb_mode = camera_awb_mode
        camera.iso = camera_ISO
        camera.color_effects = camera_color_effects
        camera.exposure_mode, camera.shutter_speed = set_exposure_shutter(hour)
        time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dir_name = '{}{}_{}'.format(filepath,filenamePrefix,time_stamp)
        os.mkdir(dir_name)
        camera.annotate_text_size = 15
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        #resize_tuple = (int(camera.resolution[0]),int(resize_scale*camera.resolution[1]))
        try:        
            for i, filename in enumerate(camera.capture_continuous("{}/{}_".format(dir_name,filenamePrefix)+"{timestamp:%Y-%m-%d-%H-%M-%S-%f}.jpg")):
                camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                if i == 599:
                    return dir_name
        except Exception:
            print("error during photo capture")
            return dir_name

signal.signal(signal.SIGTERM, signal_handler)

try:
    while True:
        hour = datetime.now().hour
        if hour >= observ_start and hour < observ_end:
            dir_name = make_photos(hour)
            crop_folder(dir_name)
            shutil.move(dir_name,moved_path)
        else:
            pass

except SigTermException:
    try:
        crop_folder(dir_name)
        shutil.move(dir_name,moved_path)
    except:
        print("failed to crop folder and move directory")
    finally:
        sys.exit(0)
        
