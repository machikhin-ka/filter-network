import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline


class Cool(object):
    """cool_filter ---
        This class will apply cool filter to an image
        by giving a sky blue effect to the input image.
    """

    def __init__(self):
        self.increaseChannel = self.LUT_8UC1([0, 64, 128, 192, 256],
                                             [0, 70, 140, 210, 256])
        self.decreaseChannel = self.LUT_8UC1([0, 64, 128, 192, 256],
                                             [0, 30, 80, 120, 192])

    def resize(self, image, window_height=500):
        aspect_ratio = float(image.shape[1]) / float(image.shape[0])
        window_width = window_height / aspect_ratio
        image = cv2.resize(image, (int(window_height), int(window_width)))
        return image

    def render(self, img_rgb):
        img_rgb = cv2.imdecode(np.frombuffer(img_rgb, np.uint8), -1)
        img_rgb = self.resize(img_rgb, 500)
        r, g, b = cv2.split(img_rgb)
        r = cv2.LUT(r, self.increaseChannel).astype(np.uint8)
        b = cv2.LUT(b, self.decreaseChannel).astype(np.uint8)
        img_rgb = cv2.merge((r, g, b))
        h, s, v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
        s = cv2.LUT(s, self.decreaseChannel).astype(np.uint8)

        dst = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2RGB)
        return cv2.imencode('.jpg', dst)[1].tostring()

    def LUT_8UC1(self, x, y):
        spl = UnivariateSpline(x, y)
        return spl(range(256))
