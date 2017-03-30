from utils import bresenham
import numpy as np


class Pixel:
    def __init__(self):
        self.count = int(0)
        self.average = np.float(0)
        self.value = np.float(0)


def img_to_sinogram(picture, **kwargs):
    default_parameters = {
        'width': 90,
        'detector_amount': 360,
        'alpha': 2
    }

    default_parameters.update(kwargs)

    width = default_parameters['width']
    detector_amount = default_parameters['detector_amount']
    alpha = default_parameters['alpha']

    picture_size = len(picture[0])
    r = int(np.ceil(np.sqrt(picture_size * picture_size)))

    sinogram = []
    lines = []

    for i in range(0, 360, alpha):
        sinogram.append([])
        lines.append([])
        for detector in range(0, detector_amount):
            x0 = r * np.cos(i * np.pi / 180)
            y0 = r * np.sin(i * np.pi / 180)

            x1 = r * np.cos((i + 180 - (width / 2) + detector * (width / (detector_amount - 1))) * np.pi / 180)
            y1 = r * np.sin((i + 180 - (width / 2) + detector * (width / (detector_amount - 1))) * np.pi / 180)

            x0 = int(x0) + np.floor(picture_size / 2)
            y0 = int(y0) + np.floor(picture_size / 2)

            x1 = int(x1) + np.floor(picture_size / 2)
            y1 = int(y1) + np.floor(picture_size / 2)

            line = bresenham(x0, y0, x1, y1)

            pixel = get_normalised_pixel(picture, line)

            sinogram[-1].append(pixel.average)
            lines[-1].append([x0, y0, x1, y1])

    return sinogram, lines


def get_normalised_pixel(picture, line):
    pixel = Pixel()
    for pos in line:
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(picture) and pos[1] < len(picture):
            pixel.value += float(picture[int(pos[0]), int(pos[1])])
            pixel.count += 1
    assert pixel.count != 0
    pixel.average = pixel.value / pixel.count
    return pixel
