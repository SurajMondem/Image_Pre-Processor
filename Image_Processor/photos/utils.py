import cv2
import numpy as np
from .algorithms.Convolution import convolution


def get_filtered_image(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (50, 50)
        elif width > 200 and width <= 500:
            k = (25, 25)
        else:
            k = (10, 10)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == 'BINARY':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'INVERT':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)
    elif action == 'BOX_BLUR':
        kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        filtered = convolution(image, kernel, average=True)
    elif action == 'EMBOSS':
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        filtered = convolution(img, kernel, average=False)
    elif action == 'SHARPEN':
        kernel = np.array([[-1, -1, -1], [-1, 11, -1], [-1, -1, -1]])
        filtered = convolution(img, kernel, average=False)
    elif action == 'IDENTITY':
        kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        filtered = convolution(img, kernel, average=False)
    elif action == 'HIGHPASS':
        kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        filtered = convolution(img, kernel, average=False)

    return filtered
