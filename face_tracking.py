import cv2

#turn on webcam
capture = cv2.VideoCapture(0)

#The deisred image output width and height
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600

capture.set(3, OUTPUT_SIZE_WIDTH)
capture.set(4, OUTPUT_SIZE_HEIGHT)
capture.set(0,150)
 
# Face Detection model loaded
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#img = cv2.imread("test.webp")

#cv2.imshow("img", img)
#cv2.waitKey()

while True:
    success, img = capture.read()
    
    # convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detects user's face
    userFaces =  faceCascade.detectMultiScale(imgGray, 1.1, 15)
    
    # draw rectangles around detected face
    for (x,y,w,h) in userFaces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0))
        cv2.putText(img, str(y), (x+w, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    
    cv2.imshow("image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()