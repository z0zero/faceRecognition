# Import required libraries
import cv2
import os

def capture_images():
    # Get the user's name
    name = input("Enter Your Name: ").lower()

    # Create directory for images if it doesn't exist
    path = os.path.join('images', name)

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

        # Display the resulting frame
        cv2.imshow('Capture Images', frame)

        # Save the current image to the directory
        img_name = os.path.join(path, f'{count}.jpg')
        cv2.imwrite(img_name, frame)
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
