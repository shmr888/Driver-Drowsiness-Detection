# Drowsiness Detection System

This is a Python-based Drowsiness Detection System designed to monitor a user's eye aspect ratio (EAR) in real-time using a webcam. The system raises an alert when it detects that the user is drowsy, helping to prevent accidents caused by drowsiness, particularly during driving.

## Features

- **Real-time Eye Aspect Ratio (EAR) Calculation**: Monitors the user's eye state in real-time to detect drowsiness.
- **Alert System**: Plays an alert sound when drowsiness is detected.
- **GUI Interface**: Simple Tkinter-based graphical user interface to start and stop the detection, display video feed, and manage detection history.
- **Detection History**: Logs timestamps of drowsiness events and allows saving them to a file.

## Requirements

To run this project, you need the following libraries:

- Python 3.x
- OpenCV (`cv2`)
- dlib
- imutils
- scipy
- numpy
- pygame
- tkinter


You can install the required packages using pip:

```bash
pip install opencv-python dlib imutils scipy numpy pygame 
```

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/drowsiness-detection-system.git
   cd drowsiness-detection-system
   ```

2. **Download the Pre-trained Shape Predictor**:
   - Download the `shape_predictor_68_face_landmarks.dat` file from [dlib's model zoo](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) and place it in the same directory as the script.

3. **Run the Application**:
   ```bash
   python drowsiness_detection.py
   ```

4. **Using the GUI**:
   - **Name and Phone Number**: Enter your name and phone number in the provided fields.
   - **Start Detection**: Click the "Start Detection" button to begin monitoring. The video feed will replace the brand image, and the system will start analyzing your eye aspect ratio.
   - **Stop Detection**: Click the "Stop Detection" button to stop monitoring.
   - **Save History**: Save the detection history (timestamps when drowsiness was detected) by clicking the "Save History" button.
   - **Quit**: Exit the application using the "Quit" button.

5. **Alert Mechanism**:
   - If drowsiness is detected (eyes closed for a prolonged period), an alert sound will play, and the event will be logged with a timestamp in the detection history.

## Code Overview

- **drowsiness_detection.py**: The main script that handles video capture, face detection, eye aspect ratio calculation, and GUI interactions.
- **music.wav**: The alert sound file played when drowsiness is detected.
- **shape_predictor_68_face_landmarks.dat**: Pre-trained facial landmark detector (not included, must be downloaded separately).

## How It Works

- **Eye Aspect Ratio (EAR)**: The system calculates the EAR for both eyes using the Euclidean distance between specific facial landmarks. If the EAR falls below a certain threshold for a set number of consecutive frames, the system triggers an alert.
  
- **Detection Logic**: The detection logic runs in a separate thread to ensure that the GUI remains responsive during video processing. The video feed is displayed within the GUI, and the user is notified of drowsiness both visually and audibly.

## Limitations

- The system's accuracy depends on the lighting conditions and the positioning of the user's face relative to the camera.
- The EAR threshold and the frame check count may need adjustment based on the user's unique facial features and the environment.
