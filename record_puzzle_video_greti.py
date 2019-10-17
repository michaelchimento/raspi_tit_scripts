import picamera
import datetime as dt

name = "raspi_test"
camera = picamera.PiCamera()
camera.resolution = (1280,720)
camera.rotation = 0
camera.brightness= 50
camera.ISO = 400
camera.annotate_text_size = 20
camera.awb_mode = 'tungsten'
filepath = "/home/pi/greti_videos/"

def record_video():
    time_start = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = name + time_start + '.h264'
    camera.start_recording(filepath + filename)
    start = dt.datetime.now()
    while(dt.datetime.now()-start).seconds < 30:
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.5)
    camera.stop_recording()

record_video()
