import cv2
import os

def adjust_brightness(image, brightness=1.0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[...,2] = cv2.convertScaleAbs(hsv[...,2], alpha=brightness)
    bright_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bright_image

# Load the model
net = cv2.dnn.readNetFromTensorflow('opencv_face_detector_uint8.pb', 'opencv_face_detector.pbtxt')

video=cv2.VideoCapture(0)

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
    
    # Pass the frame through the network
    blob = cv2.dnn.blobFromImage(bright_frame, 1.0, (300, 300), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            x1 = int(detections[0, 0, i, 3] * bright_frame.shape[1])
            y1 = int(detections[0, 0, i, 4] * bright_frame.shape[0])
            x2 = int(detections[0, 0, i, 5] * bright_frame.shape[1])
            y2 = int(detections[0, 0, i, 6] * bright_frame.shape[0])
            count=count+1
            name='./images/'+nameID+'/'+ str(count) + '.jpg'
            print("Creating Images........." +name)
            cv2.imwrite(name, bright_frame[y1:y2,x1:x2])
            cv2.rectangle(bright_frame, (x1,y1), (x2,y2), (0,255,0), 3)
    cv2.imshow("WindowFrame", bright_frame)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count>50:
        break

video.release()
cv2.destroyAllWindows()
