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
import numpy as np
import datetime
import time
from sklearn.metrics import mean_squared_error
import pydicom
from pydicom.dataset import Dataset, FileDataset
import pydicom.uid

global_width = 90
global_detector_amount = 180
global_alpha = 2


def write_dicom(pixel_array,filename):
    """
    INPUTS:
    pixel_array: 2D numpy ndarray.  If pixel_array is larger than 2D, errors.
    filename: string name for the output file.
    """

    ## This code block was taken from the output of a MATLAB secondary
    ## capture.  I do not know what the long dotted UIDs mean, but
    ## this code works.
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = 'Secondary Capture Image Storage'
    file_meta.MediaStorageSOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.0.100.4.0'
    ds = FileDataset(filename, {},file_meta = file_meta,preamble=b"\0"*128)
    ds.Modality = 'WSD'
    ds.ContentDate = str(datetime.date.today()).replace('-','')
    ds.ContentTime = str(time.time()) #milliseconds since the epoch
    ds.StudyInstanceUID =  '1.3.6.1.4.1.9590.100.1.1.124313977412360175234271287472804872093'
    ds.SeriesInstanceUID = '1.3.6.1.4.1.9590.100.1.1.369231118011061003403421859172643143649'
    ds.SOPInstanceUID =    '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    ds.SOPClassUID = 'Secondary Capture Image Storage'
    ds.SecondaryCaptureDeviceManufctur = b'Python 2.7.3'

    ## These are the necessary imaging components of the FileDataset object.
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0
    ds.HighBit = 15
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SmallestImagePixelValue = b'\\x00\\x00'
    ds.LargestImagePixelValue = b'\\xff\\xff'
    ds.Columns = pixel_array.shape[0]
    ds.Rows = pixel_array.shape[1]
    if pixel_array.dtype != np.uint16:
        pixel_array = pixel_array.astype(np.uint16)
    ds.PixelData = pixel_array.tostring()

    ds.save_as(filename)
    return


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
        #plots[0].imshow(self.original, cmap='gray')
        #plots[1].imshow(self.sinogram, cmap='gray')
        ##plt.show()()
        # print("Oryginalny obraz:")
        # print(np.shape(self.original))
        # print("Stenogram:")
        # print(np.shape(self.sinogram))
        plt.savefig("sinogram.jpg")
        return self.sinogram

    def sinogram_to_img(self):
        self.reconstructed = iradon.sinogram_to_img(self.original, self.sinogram, self.lines)
        fig, plots = plt.subplots(1, 2)
        # print("Końcowy obraz bez filtracji sinogramu")
        #plots[0].imshow(self.original, cmap='gray')
        #plots[1].imshow(self.reconstructed, cmap='gray')
        ##plt.show()()
        return self.result

    def filter_img(self):
        self.filtered = iradon.sinogram_to_img_f(self.original, self.sinogram, self.lines)

        self.intImg = np.array([[int(x * 255) for x in row] for row in self.filtered])

        write_dicom(self.intImg, 'output.dcm')

        fig, plots = plt.subplots(1, 2)
        # print("Końcowy obraz z filtracją sinogramu")
        #plots[0].imshow(self.original, cmap='gray')
        #plots[1].imshow(self.filtered, cmap='gray')
        #plt.show()()
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
    # calculate_error(final_image)
    print("Done")
