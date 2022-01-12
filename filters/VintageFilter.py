import cv2
import numpy as np


class Vintage(object):
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
        img_color = img_rgb

        newImage = img_color.copy()
        i, j, k = img_color.shape
        for x in range(i):
            for y in range(j):
                R = img_color[x, y, 2] * 0.393 + img_color[x, y, 1] * 0.769 + img_color[x, y, 0] * 0.189
                G = img_color[x, y, 2] * 0.349 + img_color[x, y, 1] * 0.686 + img_color[x, y, 0] * 0.168
                B = img_color[x, y, 2] * 0.272 + img_color[x, y, 1] * 0.534 + img_color[x, y, 0] * 0.131
                if R > 255:
                    newImage[x, y, 2] = 255
                else:
                    newImage[x, y, 2] = R
                if G > 255:
                    newImage[x, y, 1] = 255
                else:
                    newImage[x, y, 1] = G
                if B > 255:
                    newImage[x, y, 0] = 255
                else:
                    newImage[x, y, 0] = B

        return cv2.imencode('.jpg', newImage)[1].tostring()
