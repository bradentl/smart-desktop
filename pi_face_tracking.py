import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

# Constants
w, h = 640, 480
y_adj = 0 # Deviation from center
mov_tol = 50 # Movement tolerance

# Initializing PiCamera
camera = PiCamera()
camera.resolution = (w,h)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(w,h))

time.sleep(0.1)

past_y = None

# Face Detection model loaded
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    
    # Attempts to detect faces
    user_faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 15)
    
    # Draw rectangles around detected faces
    for (x,y,w,h) in user_faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0))
        cv2.putText(img, str(y), (x+w, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    
    if(len(user_faces) > 0):
        tracked_face_y = user_faces[0][1]
        # Aim is to adjust camera height until profile is approximately in center
        y_center = (h / 2) + y_adj
        # Tolerance is necessary to prevent adjustments for arbitrary movement
        if(tracked_face_y > abs(y_center + mov_tol)):
            if(not past_y):
                past_y = tracked_face_y
            else:
                # Determine direction of movement
                dir = 1 if (tracked_face_y - past_y >= 0) else -1
                # TODO: Move servos
                pass
    else:
        # If face diappears from screen, erase memorized position
        past_y = None
    
    cv2.imshow("image", img)
    rawCapture.truncate(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()