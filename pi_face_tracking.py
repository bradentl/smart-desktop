### Changes: 
    # integrated dlib, which has correlation filter to track objects, and wrote code for tracking once detected instead of redetection
    # changed to largest face only being detected and tracked, no storing a list of faces + random

import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import dlib

# Constants
width, height = 640, 480
y_adj = 0 # Deviation from center
mov_tol = 50 # Movement tolerance

# Initializing PiCamera
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(w,h))

time.sleep(0.1)

past_y = None

# Face Detection model loaded
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# initialise tracker
tracker = dlib.correlation_tracker()
#whether or not face is being tracked
trackingFace = 0

# changes for every frame, same as while loop for vid capture
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    unResizedImg = frame.array
    img = cv2.resize(unResizedImg, (320, 240))
    
    # detect face if not already tracking one
    if trackingFace==0:
        # Attempts to detect faces
        user_faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 15)
        
        # to track largest face, also reinitialise all vars
        maxFaceArea = 0
        past_y = None
        x = 0
        y = 0
        w = 0
        h = 0

        for (fx,fy,fw,fh) in user_faces:
            if fw*fh > maxFaceArea:
                x = int(fx)
                y = int(fy)
                w = int(fw)
                h = int(fh)
                maxFaceArea = w*h
        
        # if actually are faces in image start tracking
        if maxFaceArea > 0:
            #start the tracker
            tracker.start_track(img,
                                dlib.rectangle( x-10,
                                                y-20,
                                                x+w+10,
                                                y+h+20))
    
            #set tracking vairable to indicate tracking
            trackingFace = 1
                
    if trackingFace == 1:
        # handy dlib tracking quality check using
        trackingRes = tracker.update(img)
        
        # quality threshold for adjusting to being tracking
        if trackingRes > 8:
            tracked_position =  tracker.get_position()
            tx = int(tracked_position.left())
            ty = int(tracked_position.top())
            tw = int(tracked_position.width())
            th = int(tracked_position.height())
            cv2.rectangle(img, (tx, ty),
                                        (tx + tw , ty + th),
                                        (255,0,0) ,2)
            cv2.putText(img, str(tx), (tx+tw, ty), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            

            # Aim is to adjust camera height until profile is approximately in center
            y_center = (th / 2) + y_adj
            # Tolerance is necessary to prevent adjustments for arbitrary movement
            # code to determine change from past y position
            if(ty > abs(y_center + mov_tol)):
                if(not past_y):
                    past_y = ty
                else:
                    # Determine direction of movement
                    dir = 1 if (ty - past_y >= 0) else -1
                    # TODO: Move servos
                    pass
        # if tracking quality not sufficient, ignore
        else:
            trackingFace = 0

    
    # ending code stuff
    cv2.imshow("image", img)
    rawCapture.truncate(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()
