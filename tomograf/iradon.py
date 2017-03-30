import numpy as np
from math import floor, ceil
from utils import bresenham
from matplotlib import pyplot as plt
import skimage.morphology as mp
from skimage import filters
import scipy.signal as sig
import imageio
from sklearn.metrics import mean_squared_error
from skimage.exposure import rescale_intensity


def sinogram_to_img(img, sinogram, lines):
    reconstructed = sinogram_to_img2(img, sinogram, lines, 'reconstructingImg.gif', 'reconstructedImg', False)
    return reconstructed


def sinogram_to_img_f(img, sinogram, lines):
    sinogram = filter_sinogram(sinogram)
    reconstructed = sinogram_to_img2(img, sinogram, lines, 'reconstructingImg2.gif', 'reconstructedImg2', True)
    return reconstructed


def filter_sinogram(sinogram):
    sinogram_shape = np.shape(sinogram)
    projection_count = sinogram_shape[0]
    detector_count = sinogram_shape[1]

    filtered = np.zeros((projection_count, detector_count))
    mask = perform_mask(detector_count)

    for projection in range(0, projection_count, 1):
        filtered[projection] = sig.convolve(sinogram[projection], mask, mode='same', method='direct')

    return filtered


def perform_mask(detectors):
    mask_size = floor(detectors / 2)
    mask = np.zeros(mask_size)
    center = floor(mask_size / 2)
    for i in range(0, mask_size, 1):
        k = i - center
        if k % 2 != 0:
            mask[i] = (-4 / np.pi ** 2) / k ** 2
    mask[center] = 1
    return mask


def filter_img(img):
    new = filters.gaussian(img, sigma=1)
    new = mp.dilation(mp.erosion(new))
    return new

def normalise_img(reconstructed, helper):
    normalized = np.copy(reconstructed)
    picture_shape = np.shape(normalized)
    width = picture_shape[0]
    height = picture_shape[1]
    for i in range(0, width, 1):
        for j in range(0, height, 1):
            if helper[i][j] != 0:
                normalized[i][j] = normalized[i][j] / helper[i][j]
    return normalized


def plot_images(img1, img2):
    fig, plots = plt.subplots(1, 2)
    plots[0].imshow(img1, cmap='gray')
    plots[1].imshow(img2, cmap='gray')
    plt.show()


def plot_diagram(img1, img2):
    fig, plots = plt.subplots(1, 2)
    plots[0].plot(range(np.shape(img1)[1]), img1[0])
    plots[1].plot(range(np.shape(img2)[1]), img2[0])
    plt.show()


def save_plot(x, y, filename):
    plt.plot(range(x), y)
    plt.savefig(filename)


def sinogram_to_img2(img, sinogram, lines, filename1, filename2, filter):
    img_shape = np.shape(img)
    width = img_shape[0]
    height = img_shape[1]

    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]

    images = []
    iterator = 0
    mse = np.zeros(ceil(number_of_projections / 10) + 1)

    reconstructed = np.zeros(shape=img_shape)
    helper = np.zeros(shape=img_shape)

    plot_images(img, sinogram)
    plot_diagram(sinogram, sinogram)

    for projection in range(0, number_of_projections, 1):
        for detector in range(0, number_of_detectors, 1):
            x0, y0, x1, y1 = lines[projection][detector]
            line = bresenham(x0, y0, x1, y1)
            value = sinogram[projection][detector]
            for i in range(0, len(line), 1):
                x, y = line[i]
                if x >= 0 and y >= 0 and x < width and y < height:
                    reconstructed[int(x)][int(y)] += value
                    helper[int(x)][int(y)] += 1

        fragment = normalise_img(reconstructed, helper)
        if (filter):
            fragment[fragment[:, :] < 0] = 0
            fragment = rescale_intensity(fragment)
        images.append(fragment)
        if (projection != 0 and projection % 10 == 0):
            mse[iterator] = mean_squared_error(img, fragment)
            iterator += 1

    fragment = normalise_img(reconstructed, helper)
    if (filter):
        fragment[fragment[:, :] < 0] = 0
        fragment = rescale_intensity(fragment)
    images.append(fragment)
    mse[iterator] = mean_squared_error(img, fragment)
    iterator += 1

    plot_images(img, fragment)

    if (filter):
        reconstructed = filter_img(fragment)
        images.append(reconstructed)
        mse[iterator] = mean_squared_error(img, reconstructed)
    else:
        reconstructed = fragment
        images.append(reconstructed)
        mse[iterator] = mean_squared_error(img, reconstructed)
    iterator += 1
    imageio.mimsave(filename1, images)
    save_plot(iterator, mse, filename2)
    return reconstructed
