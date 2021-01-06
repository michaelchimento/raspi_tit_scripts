#!/usr/bin/python3

from datetime import datetime

camera_rotation = 0
camera_resolution = "1080p"
social_camera_resolution = (3280, 2464)
camera_color_effects = (128,128)
focus_zoom = (0.25, 0.25, 0.5, 0.5)
feeder_zoom = (0, 0, 1, 1)
observ_zoom = (0, 0, 1, 1)
social_zoom = (0, 0, 1, 1)
resize_scale = .6
feeder_resize_scale = .8
camera_ISO = 0
camera_brightness = 40
camera_shutter_speed = 3500
camera_framerate = 30
camera_exposure_mode = 'auto'
camera_awb_mode = 'tungsten'
camera_sharpness = 30
camera_contrast = 25
feeder_start = 7
feeder_end = 17
social_start = 7
social_end = 17
puzzle_start = 7
puzzle_end = 18
observ_start = 7
observ_end = 17
sensitivity_value = 200

def set_exposure_shutter(hour):
    if hour < 8:
        camera_exposure_mode = 'auto'
        camera_shutter_speed = 6000    
    elif hour >=8 and hour < 10:
        camera_exposure_mode = 'auto'
        camera_shutter_speed = 5000
    elif hour >= 10 and hour < 16:
        camera_exposure_mode = 'auto'
        camera_shutter_speed = 3000
    elif hour >= 16 and hour < 19:
        camera_exposure_mode = 'auto'
        camera_shutter_speed = 5000

    return camera_exposure_mode, camera_shutter_speed
