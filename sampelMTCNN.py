import cv2
import os
from mtcnn import MTCNN

def adjust_brightness(image, brightness=1.0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[...,2] = cv2.convertScaleAbs(hsv[...,2], alpha=brightness)
    bright_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bright_image

# Check and create 'images' directory if not exists
if not os.path.exists('images'):
    os.makedirs('images')

video = cv2.VideoCapture(0)
if not video.isOpened():
    print('Error! Unable to open video.')
    exit(1)

detector = MTCNN()

count=0

nameID = str(input("Enter Your Name: ")).lower()
path = 'images/' + nameID

while os.path.exists(path):
    print("Name Already Taken")
    nameID = str(input("Enter Your Name Again: ")).lower()
    path = 'images/' + nameID

try:
    os.makedirs(path)
except OSError:
    print('Error! Failed to create directory.')
    exit(1)

while True:
    ret, frame = video.read()

    if not ret:
        print('Error! Failed to read frame.')
        break

    bright_frame = adjust_brightness(frame, brightness=1.5)
    
    result = detector.detect_faces(bright_frame)
    if result != []:
        for person in result:
            bounding_box = person['box']
            keypoints = person['keypoints']
    
            x, y, w, h = bounding_box
            x = max(0, x)
            y = max(0, y)
    
            cv2.rectangle(bright_frame, (x, y), (x+w, y+h), (0,155,255), 2)
            
            count += 1
            name = path + '/' + str(count) + '.jpg'
            print("Creating Images........." + name)
            
            cropped_image = bright_frame[y : y + h, x : x + w]
            cv2.imwrite(name, cropped_image)
    
    cv2.imshow("WindowFrame", bright_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count > 500:
        break

video.release()
cv2.destroyAllWindows()
