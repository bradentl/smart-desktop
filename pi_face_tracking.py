import cv2
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
 
# Face Detection model loaded
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    # convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detects user's face
    userFaces = faceCascade.detectMultiScale(imgGray, 1.1, 15)
    
    # draw rectangles around detected face
    for (x,y,w,h) in userFaces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0))
        cv2.putText(img, str(y), (x+w, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    
    cv2.imshow("image", img)
    rawCapture.truncate(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()