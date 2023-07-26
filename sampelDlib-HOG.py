import cv2
import os
import dlib

def adjust_brightness(image, brightness=1.0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[...,2] = cv2.convertScaleAbs(hsv[...,2], alpha=brightness)
    bright_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bright_image

video=cv2.VideoCapture(0)

hog_face_detector = dlib.get_frontal_face_detector()

count=0

nameID=str(input("Enter Your Name: ")).lower()

path='images/'+nameID

isExist = os.path.exists(path)

if isExist:
    print("Name Already Taken")
    nameID=str(input("Enter Your Name Again: "))
else:
    os.makedirs(path)

while True:
    ret, frame = video.read()
    
    # Adjust the brightness of the frame
    bright_frame = adjust_brightness(frame, brightness=1.5)
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(bright_frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = hog_face_detector(gray)
    for face in faces:
        x = face.left()
        y = face.top()
        w = face.width()
        h = face.height()
        count=count+1
        name='./images/'+nameID+'/'+ str(count) + '.jpg'
        print("Creating Images........." +name)
        cv2.imwrite(name, bright_frame[y:y+h,x:x+w])
        cv2.rectangle(bright_frame, (x,y), (x+w, y+h), (0,255,0), 3)
    cv2.imshow("WindowFrame", bright_frame)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count>50:
        break

video.release()
cv2.destroyAllWindows()
