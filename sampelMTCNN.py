import cv2
import os
from mtcnn import MTCNN

def adjust_brightness(image, brightness=1.0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[...,2] = cv2.convertScaleAbs(hsv[...,2], alpha=brightness)
    bright_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bright_image

video = cv2.VideoCapture(0)

detector = MTCNN()

count=0

nameID = str(input("Enter Your Name: ")).lower()

path = 'images/' + nameID

isExist = os.path.exists(path)

if isExist:
    print("Name Already Taken")
    nameID = str(input("Enter Your Name Again: "))
else:
    os.makedirs(path)

while True:
    ret,frame = video.read()
    
    # Adjust the brightness of the frame
    bright_frame = adjust_brightness(frame, brightness=1.5)
    
    # Detect faces
    result = detector.detect_faces(bright_frame)
    if result != []:
        for person in result:
            bounding_box = person['box']
            keypoints = person['keypoints']
    
            cv2.rectangle(bright_frame,
                          (bounding_box[0], bounding_box[1]),
                          (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                          (0,155,255),
                          2)
            count += 1
            name = './images/' + nameID + '/' + str(count) + '.jpg'
            print("Creating Images........." + name)
            cv2.imwrite(name, bright_frame[bounding_box[1] : bounding_box[1] + bounding_box[3], bounding_box[0] : bounding_box[0]+bounding_box[2]])
    
    # Display the frame
    cv2.imshow("WindowFrame", bright_frame)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count > 500:
        break

video.release()
cv2.destroyAllWindows()
