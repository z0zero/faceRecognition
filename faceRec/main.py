import os.path
import subprocess
import numpy as np
import csv
import datetime

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import util

# Load Haar cascades for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        # Define self.db_dir before calling add_webcam
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        # Define log file
        self.log_file = './log.csv'
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Nomor', 'Nama', 'Waktu', 'Status'])

        self.register_new_user_button_main_window = util.get_button(self.main_window, "Register new user", "gray", 
                                                                    self.register_new_user, fg="black")
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Use Haar cascades to detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # If a face is detected and not already counting down, start the countdown
        if len(faces) > 0 and not hasattr(self, 'counting_down'):
            self.counting_down = 3
            self.main_window.after(1000, self.countdown)
        elif len(faces) == 0 and hasattr(self, 'counting_down'):
            # If no face is detected and countdown was in progress, reset
            del self.counting_down
    
        # Display webcam image (possibly with countdown overlay)
        self.most_recent_capture_arr = frame
        self.most_recent_capture_pil = Image.fromarray(img_)
        if hasattr(self, 'counting_down'):
            self.most_recent_capture_pil = self.add_countdown_to_image(self.most_recent_capture_pil, self.counting_down)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def countdown(self):
        if hasattr(self, 'counting_down'):
            self.counting_down -= 1
            if self.counting_down == 0:
                # Execute face recognition after countdown finishes
                self.execute_face_recognition()
                if hasattr(self, 'counting_down'):
                    del self.counting_down
                # Stop further processing until user acknowledges the notification
                return
            else:
                if self.counting_down > 0:
                    self.main_window.after(1000, self.countdown)
                else:
                    # Remove countdown text from the image
                    self.process_webcam()

    def execute_face_recognition(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]

        os.remove(unknown_img_path)

        # Track the latest status of the user
        latest_status = None

        if name not in ['unknown_person', 'no_persons_found']:
            # Check if user is already in the log file
            with open(self.log_file, mode='r') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    if row[1] == name:
                        latest_status = row[3]

            # If user's latest status is 'keluar' or the user is new, mark them as 'masuk'
            if latest_status == 'keluar' or latest_status is None:
                with open(self.log_file, mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    nomor = self.get_next_nomor()
                    waktu = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    writer.writerow([nomor, name, waktu, 'masuk'])
                response = util.msg_box('Success!', 'Welcome {}!'.format(name))
            else:  # If user's latest status is 'masuk', mark them as 'keluar'
                with open(self.log_file, mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    nomor = self.get_next_nomor()
                    waktu = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    writer.writerow([nomor, name, waktu, 'keluar'])
                response = util.msg_box('Success!', 'Goodbye {}!'.format(name))

            # After displaying the message, wait for user acknowledgment
            if response == 'ok':
                self.process_webcam()
        else:
            # Direct user to register their face
            response = util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            if response == 'ok':
                self.register_new_user()

    def get_next_nomor(self):
        with open(self.log_file, mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            nomor = 1
            for i, row in enumerate(reader):
                if i == 0:
                    continue  # Skip header row
                nomor = int(row[0]) + 1
        return nomor

    def add_countdown_to_image(self, img_pil, countdown_value):
        # Convert PIL Image to OpenCV format
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        # Set position and font
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (img_cv.shape[1] // 2 - 50, img_cv.shape[0] // 2 + 50)
        color = (255, 0, 0)  # Blue color
        thickness = 5
        size = 3.0
        cv2.putText(img_cv, str(countdown_value), position, font, size, color, thickness)
        # Convert back to PIL Image
        img_pil_modified = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        return img_pil_modified

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+350+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, "Accept", "green", self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, "Try Again", "red", self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, "Enter your name:")
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box("Success", "User {} registered successfully".format(name))
        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()
