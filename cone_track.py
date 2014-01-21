import cv2
import numpy as np

ORANGE_MIN = np.array([0, 50, 50],np.uint8)
ORANGE_MAX = np.array([30, 255, 250],np.uint8)

MAX_P = 1100
MIN_P = 15 

def get_obs(frame):
    boxes = []

	# Apply Gaussian
    frame_blurred = cv2.GaussianBlur(frame, (15, 15), 7)

	# Convert to HSV
    frame_threshed = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2HSV)

    frame_threshed = cv2.inRange(frame_threshed, ORANGE_MIN, ORANGE_MAX)
    contours, _ = cv2.findContours(frame_threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if  perimeter < MIN_P or perimeter > MAX_P: 
            continue
        boxes.append(cv2.boundingRect(cnt))
    return boxes
