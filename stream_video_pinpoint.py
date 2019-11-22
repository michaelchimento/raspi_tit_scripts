import io
import itertools
import picamera
import logging
import socketserver
from datetime import datetime
from threading import Condition
from http import server
from rpi_info import name
from camera_settings import *
from PIL import Image
import cv2 
import numpy as np
import datetime as dt
from scipy.spatial import distance as dist
import TagList
from imutils.video import VideoStream
from imutils.video import FPS
from barcode_tracker_web_stream.py import *

PAGE="<html><head><title>Greti Live Stream</title></head><body><h1>{}</h1><img src=\"stream.mjpg\" width=\"1280\" height=\"720\" /></body></html>".format(name)

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = np.fromstring(self.buffer.getvalue(), dtype=np.uint8)
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        image = cv2.imdecode(output.frame, 1)
                        gray = get_grayscale(image, channel = 'green')
                        gray = cv2.GaussianBlur(gray, (1,1), 1)
                        thresh = get_threshold(gray, block_size = 101, offset = -10)
                        contours = get_contours(thresh)
                        display_img = image.copy()

                        #this begins to loop through the detected contours
                        detected_tags, num_detections = contour_loop(contours, image, dst, gray,
                                         maxSide, barcode_size, barcodes,
                                         flat_len, IDs, font, timeofframe, frame, pt1)
                        frame = Image.fromarray(display_img, 'RGB')
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
    def service_actions(self):
        global camera
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.5)

# ## Import list of barcodes
tags = TagList.TagList()
dir(TagList)
tags.load("master_list_outdoor.pkl")
master_list = tags.master_list
IDs = tags.id_list

barcode_size = (7,7)
barcodes = []
for barcode in master_list:
    tag_shape, barcode = add_border(barcode, (5,5), white_width = 1, black_width = 0)
    barcode = barcode.reshape(tag_shape)
    barcode = cv2.resize(barcode, barcode_size, interpolation = cv2.INTER_AREA)
    barcode = barcode.flatten()
    barcodes.append(barcode)
barcodes = np.array(barcodes)
# set various parameters for tracker subroutines
flat_len = barcode_size[0]*barcode_size[1]   
maxSide = 100
length = maxSide - 1
dst = np.array([
            [0, 0],
            [length, 0],
            [length, length],
            [0, length]], dtype = "float32")
#set cropped area, default is full frame
frame_width = camera_resolution[1] #frame width as integer
print(frame_width)
frame_height = camera_resolution[0]#frame height as integer
pt1 = (0,0) #top-left corner
pt2 = (frame_width,frame_height) #bottom-right corner
font = cv2.FONT_HERSHEY_SIMPLEX # set font

with picamera.PiCamera() as camera:
    camera.rotation = camera_rotation
    camera.contrast = camera_contrast
    camera.resolution = camera_resolution
    camera.brightness = camera_brightness
    camera.framerate = camera_framerate
    camera.awb_mode = camera_awb_mode
    camera.iso = camera_ISO
    output = StreamingOutput()
    camera.annotate_text = "{}".format(name)
    camera.start_recording(output, format='bgr')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    finally:
        camera.stop_recording()
