import cv2
import numpy as np


def is_checked(image, coordinates, threshold = 0.50):

    x1, y1, x2, y2 = coordinates

    roi = image[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    dark_ratio = np.mean(gray < 100)

    return dark_ratio > threshold