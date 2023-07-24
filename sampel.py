# Import required libraries
import cv2
import os
import numpy as np

# Here's a function that will adjust the brightness of an image
def adjust_brightness(image, brightness=1.0):
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Scale the V (Value/Brightness) channel
    hsv[...,2] = cv2.convertScaleAbs(hsv[...,2], alpha=brightness)
    # Convert the image back to the BGR color space
    bright_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bright_image

# Here's your original function, but now it applies brightness adjustment to each frame before saving it
def capture_images():
    # Get the user's name
    name = input("Enter Your Name: ").lower()

    # Create directory for images if it doesn't exist
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    path = os.path.join(images_dir, name)

    # Check if directory already exists
    if os.path.exists(path):
        print("Name Already Taken")
        name = input("Enter Your Name Again: ").lower()
    else:
        os.makedirs(path)

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Initialize image count
    count = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame reading was successful
        if not ret:
            break

        # Adjust the brightness of the frame
        bright_frame = adjust_brightness(frame, brightness=1.5)  # Increase brightness by 50%

        # Display the resulting frame
        cv2.imshow('Capture Images', bright_frame)

        # Save the current image to the directory
        img_name = os.path.join(path, f'{count}.jpg')
        cv2.imwrite(img_name, bright_frame)
        print(f'Creating Images.........{img_name}')
        count += 1

        # Break if 'q' is pressed or we have enough images
        if cv2.waitKey(1) & 0xFF == ord('q') or count > 500:
            break

    # When everything is done, release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function
capture_images() 
