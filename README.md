# Hand Gesture Controlled eBook Reader

An interactive eBook reader built using Python, OpenCV, MediaPipe, and Tkinter, enabling users to scroll or flip pages using simple hand gestures detected via webcam.

Inspired by accessibility needs and human-centered interaction principles, this project allows hands-free reading, making eBooks more accessible, intuitive, and engaging.

---

## Features

### Real-Time Hand Gesture Recognition
Detects hand gestures using:
- OpenCV
- MediaPipe Hand Tracking
- cvzone HandDetector

---

## Supported Hand Gestures

![Gestures](images/hand_gestures.png)

---

## eBook Viewer
- Renders PDF pages using PyMuPDF (fitz)
- Scroll and flip pages dynamically
- Smooth UI built with Tkinter 
- Works with any PDF file

---

## Installation
Clone the repo:

```bash
git clone git@github.com:i-am-sarthak/gesture-controlled-ebook-reader.git
cd hand-gesture-ebook-reader
```

Install Dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Step 1 — Start Gesture Recognition
```bash
python gesture_recognition.py
```
This opens the webcam and writes detected gestures to recognised_gestures.txt.

Step 2 — Start the eBook Reader UI
```bash
python pdf_viewer.py
```
The app continuously monitors the gesture file and responds immediately.

## System Workflow

1. Webcam captures live hand images

2. MediaPipe detects hand landmarks

3. Gestures are classified

4. Commands are written to recognised_gestures.txt

5. PDF viewer reads commands and scrolls/flips pages

6. User experiences a fully hands-free reading interface

## Screenshots
- App UI

![UI](images/app_ui.png)

- Gesture Detection

![Detection](images/detection.png)


