# Webcam is required to run this
# Install opencv, cvzone and mediapipe
# Gesture 1 (thumbs up) to go to the previous slide
# Gesture 2 (pinkie finger pointed up) to go to the next slide
# Gesture 3 (index and middle finger upright) to scroll down
# Gesture 4 (index finger upright) to scroll up

from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np

import time

# Parameters of the pop-up webcam
width: int = 1280
height: int = 720
# Threshold for the line showing in the pop-up of webcam
gesture_threshold: int = 400

# Camera Setup
# noinspection PyUnresolvedReferences
video: cv2.VideoCapture = cv2.VideoCapture(0)
video.set(3, width)
video.set(4, height)

# Detect hand if accuracy is equal or more than 80% and consider one hand only
detector_hand: HandDetector = HandDetector(detectionCon=0.8, maxHands=1)

filename: str = 'recognised_gestures.txt'
scroll_write_interval: float = 0.4
flip_write_interval: float = 1.5
last_write_time: float = time.time()

while True:
    # Get image frame
    success: bool
    image: np.ndarray
    success, image = video.read()
    # Flip images to the horizontal direction so hands move in the proper direction
    # 1 means horizontal and 0 means vertical
    # noinspection PyUnresolvedReferences
    image = cv2.flip(image, 1)

    # Find the hand and its landmarks (left or right)
    hands: list[dict[str, list[list[int]] | tuple[int, int, int, int] | tuple[int, int] | str]]
    hands, image = detector_hand.findHands(image)
    # Draw Gesture Threshold line
    colour_green: tuple[int, int, int] = (0, 255, 0)
    width_of_line: int = 1
    # noinspection PyUnresolvedReferences
    cv2.line(image, (0, gesture_threshold), (width, gesture_threshold), colour_green, width_of_line)

    if hands:  # If hand is detected
        hand: dict[str, list[list[int]] | tuple[int, int, int, int] | tuple[int, int] | str] = hands[0]
        cx: int
        cy: int
        cx, cy = hand["center"]  # Get the center of hand
        fingers: list[int] = detector_hand.fingersUp(hand)  # List of which fingers are up

        if cy <= gesture_threshold:  # If hand is at the height of the face
            # Gesture 1 - Go to previous slide
            if fingers == [1, 0, 0, 0, 0]:
                if time.time() - last_write_time >= flip_write_interval:
                    print("Go to previous slide")
                    with open(filename, 'a') as f:
                        f.write("previous_page\n")
                    last_write_time = time.time()

            # Gesture 2 - Go to next slide
            if fingers == [0, 0, 0, 0, 1]:
                if time.time() - last_write_time >= flip_write_interval:
                    print("Go to next slide")
                    with open(filename, 'a') as f:
                        f.write("next_page\n")
                    last_write_time = time.time()

            # Gesture 3 - Scroll down
            if fingers == [0, 1, 1, 0, 0]:
                if time.time() - last_write_time >= scroll_write_interval:
                    print("Scroll down")
                    with open(filename, 'a') as f:
                        f.write("scroll_down\n")
                    last_write_time = time.time()

            # Gesture 4 - Scroll up
            if fingers == [0, 1, 0, 0, 0]:
                if time.time() - last_write_time >= scroll_write_interval:
                    print("Scroll up")
                    with open(filename, 'a') as f:
                        f.write("scroll_up\n")
                    last_write_time = time.time()

    # To show the webcam image
    # noinspection PyUnresolvedReferences
    cv2.imshow("Hand Gesture Recogniser", image)
    # To quit the application using q button
    # noinspection PyUnresolvedReferences
    key: int = cv2.waitKey(1)
    if key == ord('q'):
        break
