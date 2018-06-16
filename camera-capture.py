import time
import cv2

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        continue

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('s'):
       cv2.imwrite("~/Documents/TechFest/test.jpg",image) 
       break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
camera_port = 0
camera = cv2.VideoCapture(camera_port)
time.sleep(0.1)  # If you don't wait, the image will be dark
return_value, image = camera.read()
cv2.imwrite("opencv.png", image)
del(camera)  # so that others can use the camera as soon as possible
