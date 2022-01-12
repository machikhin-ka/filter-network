import cv2
import numpy as np


class Cartoonizer(object):
    def __init__(self):
        pass

    def resize(self, image, window_height=500):
        aspect_ratio = float(image.shape[1]) / float(image.shape[0])
        window_width = window_height / aspect_ratio
        image = cv2.resize(image, (int(window_height), int(window_width)))
        return image

    def render(self, img_rgb):
        img_rgb = cv2.imdecode(np.frombuffer(img_rgb, np.uint8), -1)
        img_rgb = self.resize(img_rgb, 500)
        numDownSamples = 2
        numBilateralFilters = 50
        img_color = img_rgb
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 3)
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                         cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, 9, 2)
        (x, y, z) = img_color.shape
        img_edge = cv2.resize(img_edge, (y, x))
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        dst = cv2.bitwise_and(img_color, img_edge)
        return cv2.imencode('.jpg', dst)[1].tostring()
