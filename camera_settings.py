#!/usr/bin/python3

camera_rotation = 0
camera_resolution = (1920,1080)
camera_ISO = 0
camera_brightness = 50
camera_shutter_speed = 3500
camera_framerate = 30
camera_awb_mode = 'tungsten'
camera_sharpness = 25
camera_contrast = 25
feeder_start = 7
feeder_end = 17
social_start = 11
social_end = 16
puzzle_start = 7
puzzle_end = 17
observ_start = 7
observ_end = 17
sensitivity_value = 200

hour = datetime.now().hour
if hour < 10:
    camera_exposure_mode = 'auto'
    camera_shutter_speed = 5000
elif hour >= 10 and hour < 16:
    camera_exposure_mode = 'auto'
    camera_shutter_speed = 4000
elif hour >= 16 and hour < 19:
    camera_exposure_mode = 'auto'
    camera_shutter_speed = 5000
