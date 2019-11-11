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
forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour
filepath = "/home/pi/APAPORIS/CURRENT/"
moved_path = "/home/pi/APAPORIS/MOVED/"
filepathphotos = "/home/pi/greti_photos/"
filenamePrefix = socket.gethostname()
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
    #imageData.write(output)
    #imageData.seek(0)
    im = Image.frombytes(mode="RGB",size=(width,height),data=output)
    buffer = im.load()
    imageData.close()
    return im, buffer

# Save a full size image to disk
def saveImage(settings, width, height, quality, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = filepathphotos + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)
    #print "Captured %s" % filename

# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(filepath + "/" + filename)
                print("Deleted %s/%s to avoid filling disk" % (filepath,filename))
                if (getFreeSpace() > bytesToReserve):
                    return

# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du

def make_video():
    with picamera.PiCamera() as camera:
        camera.rotation = 0
        camera.resolution = (1280,720)
        camera.brightness = 50
        camera.shutter_speed = (0)
        camera.awb_mode = 'tungsten' 
        camera.ISO = (0)
        timest = ('_{:%Y-%m-%d_%H%M%S}'.format(datetime.now()))
        filename = str(filenamePrefix + timest + '.h264')
        camera.annotate_text_size = 15
        camera.start_recording(filepath + filename)
        start = datetime.now()
        while (datetime.now()-start).seconds < 60:
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        	
            camera.wait_recording(0.5)
        camera.stop_recording()
    os.rename(filename, moved_path + timest + '.h264')

# Get first image
image1, buffer1 = captureTestImage(cameraSettings, testWidth, testHeight)

# Reset last capture time
lastCapture = time.time()

while (True):

    # Get comparison image
    image2, buffer2 = captureTestImage(cameraSettings, testWidth, testHeight)

    # Count changed pixels
    changedPixels = 0
    takePicture = False

    if (debugMode): # in debug mode, save a bitmap-file with marked changed pixels and with visible testarea-borders
        debugimage = Image.new("RGB",(testWidth, testHeight))
        debugim = debugimage.load()

    for z in range(0, testAreaCount): # = xrange(0,1) with default-values = z will only have the value of 0 = only one scan-area = whole picture
        for x in range(testBorders[z][0][0]-1, testBorders[z][0][1]): # = xrange(0,100) with default-values
            for y in range(testBorders[z][1][0]-1, testBorders[z][1][1]):   # = xrange(0,75) with default-values; testBorders are NOT zero-based, buffer1[x,y] are zero-based (0,0 is top left of image, testWidth-1,testHeight-1 is botton right)
                if (debugMode):
                    debugim[x,y] = buffer2[x,y]
                    if ((x == testBorders[z][0][0]-1) or (x == testBorders[z][0][1]-1) or (y == testBorders[z][1][0]-1) or (y == testBorders[z][1][1]-1)):
                        # print "Border %s %s" % (x,y)
                        debugim[x,y] = (0, 0, 255) # in debug mode, mark all border pixel to blue
                # Just check green channel as it's the highest quality channel
                pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
                if pixdiff > threshold:
                    changedPixels += 1
                    if (debugMode):
                        debugim[x,y] = (0, 255, 0) # in debug mode, mark all changed pixel to green
                # Save an image if pixels changed
                if (changedPixels > sensitivity):
                    takePicture = True # will shoot the photo later
                if ((debugMode == False) and (changedPixels > sensitivity)):
                    break  # break the y loop
            if ((debugMode == False) and (changedPixels > sensitivity)):
                break  # break the x loop
        if ((debugMode == False) and (changedPixels > sensitivity)):
            break  # break the z loop

    if (debugMode):
        debugimage.save(filepath + "/debug.bmp") # save debug image as bmp
        print("debug.bmp saved, %s changed pixel" % changedPixels)
    # else:
    #     print "%s changed pixel" % changedPixels

    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            takePicture = True

    if takePicture:
        lastCapture = time.time()
        make_video()
        #saveImage(cameraSettings, saveWidth, saveHeight, saveQuality, diskSpaceToReserve)
        
        
    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2
