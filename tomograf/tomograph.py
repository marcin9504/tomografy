# !/usr/bin/python

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
from dicom.dataset import Dataset, FileDataset
import numpy as np
import datetime
import time
from sklearn.metrics import mean_squared_error
import dicom

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
        self.save_as_dicom(self.filtered)

        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.original, cmap='gray')
        plots[1].imshow(self.filtered, cmap='gray')
        plt.show()
        return self.filtered

    def save_as_dicom(self, img):
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here for real work
        file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here

        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        ds = FileDataset('output.dcm', {}, file_meta=file_meta, preamble=b"\0" * 128)

        # Add the data elements -- not trying to set all required here. Check DICOM standard
        ds.PatientName = "Test^Firstname"
        ds.PatientID = "123456"
        ds.pixel_array = img

        # Set the transfer syntax
        ds.is_little_endian = True
        ds.is_implicit_VR = True

        # Set creation date/time
        dt = datetime.datetime.now()
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        ds.ContentTime = timeStr

        ds.save_as('output.dcm')


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
    img[24:174, 24:174] = rgb2gray(io.imread("in/phantom.png"))

    final_image = tomograf(img)
    # calculate_error(final_image)
    print("Done")
