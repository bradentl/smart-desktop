import cv2
import time
import dlib

from lx16a import *
from picamera import PiCamera
from picamera.array import PiRGBArray

# Constants
width, height = 640, 480
y_adj = 0 # Deviation from center
mov_tol = 50 # Movement tolerance

# Initializing PiCamera
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width, height))

# Initializing Servo
# If doesn't work, try each port in /dev/
LX16A.initialize('/dev/ttyUSB0')
servo = LX16A(1)

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
    img = cv2.resize(unResizedImg, (width, height))
    
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
            
            # Tracked face bounding box
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
                    servo.move(10 * dir)
        # if tracking quality not sufficient, ignore
        else:
            trackingFace = 0
    
    # Crosshairs visualization
    cv2.line(img, (0, height // 2 + y_adj), (width, height // 2 + y_adj), (0, 255, 0), 1)
    cv2.line(img, (width // 2, 0), (width // 2, height), (0, 255, 0), 1)
    
    # ending code stuff
    cv2.imshow("image", img)
    rawCapture.truncate(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
rawCapture.release()
