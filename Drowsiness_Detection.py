import cv2
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance
from threading import Thread
import numpy as np
import time
from pygame import mixer
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
from datetime import datetime

# Initialize Pygame mixer
mixer.init()
mixer.music.load("music.wav")

# Define constants
THRESH = 0.25
FRAME_CHECK = 20

# Load models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Get facial landmark indices for the eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# Local file path of the brand image
brand_image_path = r'C:\Users\Ashwin\Desktop\Driver Drowsy project\DrowsyDriving_Dashboard.webp'
brand_image = Image.open(brand_image_path)

# Function to calculate eye aspect ratio (EAR)
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Function to stop the detection
def stop_detection():
    global running
    running = False

# Drowsiness detection function
def drowsiness_detection(label, text_widget, history):
    global running
    cap = cv2.VideoCapture(0)
    flag = 0

    while running:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detector(gray, 0)

        for subject in subjects:
            shape = predictor(gray, subject)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < THRESH:
                flag += 1
                if flag >= FRAME_CHECK:
                    cv2.putText(frame, "**ALERT!**", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    mixer.music.play()
                    # Record and display the timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    history.append(f"Drowsiness detected at: {timestamp}")
                    text_widget.insert(tk.END, f"Drowsiness detected at: {timestamp}\n")
                    text_widget.see(tk.END)
            else:
                flag = 0

        # Convert the frame to ImageTk format
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to start drowsiness detection in a new thread
def start_detection(label, text_widget, history):
    global running
    running = True
    # Remove the brand image and start the detection
    label.configure(image='')
    detection_thread = Thread(target=drowsiness_detection, args=(label, text_widget, history))
    detection_thread.start()

# Function to save detection history to a file
def save_history(name, phone, history):
    phone = phone.strip()  # Ensure phone number is treated as a string
    if history:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("Drowsiness Detection History\n")
                file.write("===========================\n\n")
                file.write(f"Name: {name}\n")
                file.write(f"Phone Number: {phone}\n\n")  # Preserve leading zeros
                for record in history:
                    file.write(f"{record}\n")
                messagebox.showinfo("Info", "History saved successfully!")
    else:
        messagebox.showwarning("Warning", "No history to save!")

# Function to quit the application
def quit_application():
    stop_detection()
    root.destroy()

# Tkinter GUI setup
root = tk.Tk()
root.title("Drowsiness Detection System - ASA Group of Companies")

# Set up main frames
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

video_frame = tk.Frame(root)
video_frame.pack(side=tk.LEFT, padx=10)

controls_frame = tk.Frame(root)
controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# Create input fields for user details
name_label = tk.Label(input_frame, text="Name:", font=("Arial", 12))
name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
name_entry = tk.Entry(input_frame, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = tk.Label(input_frame, text="Phone Number:", font=("Arial", 12))
phone_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
phone_entry = tk.Entry(input_frame, font=("Arial", 12))
phone_entry.grid(row=1, column=1, padx=5, pady=5)

# Create a label to display the brand image
brand_image = brand_image.resize((450, 300), Image.LANCZOS)
brand_imgtk = ImageTk.PhotoImage(image=brand_image)
video_label = tk.Label(video_frame, image=brand_imgtk)
video_label.pack()

# Create a scrolled text widget to display the timestamps
text_widget = scrolledtext.ScrolledText(video_frame, width=50, height=10)
text_widget.pack(pady=20)

# Create a list to store drowsiness detection history
history = []

# Create buttons to start and stop detection
start_button = tk.Button(controls_frame, text="Start Detection", bg='green', fg='white', font="Impact", padx=5, pady=5,
                         command=lambda: start_detection(video_label, text_widget, history))
start_button.pack(pady=10)

stop_button = tk.Button(controls_frame, text="Stop Detection", bg='red', fg='white', font="Impact", padx=5, pady=5,
                        command=stop_detection)
stop_button.pack(pady=10)

# Create a button to save the detection history
save_button = tk.Button(controls_frame, text="Save History", bg='blue', fg='white', font="Impact", padx=5, pady=5,
                        command=lambda: save_history(name_entry.get(), phone_entry.get(), history))
save_button.pack(pady=10)

# Create a button to quit the application
quit_button = tk.Button(controls_frame, text='Quit', command=quit_application, bg='grey', fg='white', font="Impact", padx=5, pady=5)
quit_button.pack(pady=10)

root.mainloop()
