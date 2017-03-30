#!/usr/bin/python

# sources:
# http://eduinf.waw.pl/inf/utils/002_roz/2008_06.php
# http://www.dspguide.com/ch25/5.htm
# https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
# https://en.wikipedia.org/wiki/DICOM
# https://github.com/darcymason/pydicom

import radon
import iradon
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage import io
import numpy as np
from sklearn.metrics import mean_squared_error

global_width = 90
global_detector_amount = 180
global_alpha = 2


class Result:
    def __init__(self, picture=[]):
        self.raw = picture
        self.improved = picture


class MyImage:
    original = []
    sinogram = []
    filtered = []
    reconstructed = []
    result = Result()

    def __init__(self, picture_):
        self.original = picture_

    def img_to_sinogram(self):
        self.sinogram, self.lines = radon.img_to_sinogram(self.original, width=global_width,
                                                          detector_amount=global_detector_amount, alpha=global_alpha)
        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.original, cmap='gray')
        plots[1].imshow(self.sinogram, cmap='gray')
        plt.show()
        plt.savefig("sinogram.jpg")
        return self.sinogram

    def sinogram_to_img(self):
        self.reconstructed = iradon.sinogram_to_img(self.original, self.sinogram, self.lines)
        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.original, cmap='gray')
        plots[1].imshow(self.reconstructed, cmap='gray')
        plt.show()
        return self.result

    def filter_img(self):
        self.filtered = iradon.sinogram_to_img_f(self.original, self.sinogram, self.lines)
        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.original, cmap='gray')
        plots[1].imshow(self.filtered, cmap='gray')
        plt.show()
        return self.filtered


def calculate_error(picture):
    print(mean_squared_error(picture.original, picture.reconstructed))
    print(mean_squared_error(picture.original, picture.filtered))


def tomograf(img_):
    picture = MyImage(img_)
    picture.img_to_sinogram()
    picture.sinogram_to_img()
    picture.filter_img()
    return picture


def do_tomography():
    img = np.zeros([200, 200])
    img[24:174, 24:174] = rgb2gray(io.imread("in/banana.bmp"))

    final_image = tomograf(img)
    calculate_error(final_image)
