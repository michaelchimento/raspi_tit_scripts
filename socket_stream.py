import socket
import time
import picamera
from camera_settings import *

camera = picamera.PiCamera()
camera.resolution = "720p"
camera.framerate = 24

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
with picamera.PiCamera() as camera:
    camera.resolution = "720p"
    camera.framerate = 24
    camera.brightness = camera_brightness
    camera.sharpness = camera_sharpness
    camera.contrast = camera_contrast
    camera.awb_mode = camera_awb_mode
    camera.iso = camera_ISO
    camera.start_recording(connection, format='h264')
finally:
    camera.stop_recording()
    connection.close()
    server_socket.close()
