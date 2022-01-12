import cv2
import numpy as np


def findMax(k):
    mx = 0
    for i in k:
        if i > mx:
            mx = i
    return mx


class Negative(object):
    def __init__(self):
        pass

    def resize(self, image, window_height=500):
        aspect_ratio = float(image.shape[1]) / float(image.shape[0])
        window_width = window_height / aspect_ratio
        image = cv2.resize(image, (int(window_height), int(window_width)))
        return image

    def render(self, img_rgb):
        img_gray = cv2.imdecode(np.frombuffer(img_rgb, np.uint8), 0)
        img_gray = self.resize(img_gray, 500)
        k = []
        for i in range(img_gray.shape[0]):
            for j in range(img_gray.shape[1]):
                k.append(img_gray[i, j])
        L = findMax(k)
        dst = img_gray[:]
        for i in range(img_gray.shape[0]):
            for j in range(img_gray.shape[1]):
                dst[i, j] = L - dst[i, j]
        return cv2.imencode('.jpg', dst)[1].tostring()
