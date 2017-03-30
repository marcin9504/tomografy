#inspired by: https://github.com/huntekah/Informatyka-w-Medycynie-Tomograf
import matplotlib.pyplot as plt
from PIL import Image
from math import sin,cos, sqrt, pi, ceil, floor
from datetime import datetime
import numpy as np
from skimage.exposure import rescale_intensity, equalize_adapthist
from skimage import img_as_float, img_as_ubyte, filters
import skimage.morphology as mp
from skimage.transform import rotate, AffineTransform
from skimage.transform import radon, iradon

def size(image):
    return min(image.size[0], image.size[1])


def bresenhams_line(x1, y1, x2, y2):
    ''' Bresenhams algorithm as described here:
    http://eduinf.waw.pl/inf/utils/002_roz/2008_06.php'''

    line = []
    kx = 1 if x1 <= x2 else -1
    ky = 1 if y1 <= y2 else -1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x = x1
    y = y1
    line.append([x, y])
    if (dx >= dy):
        e = dx / 2
        for i in range(0, int(dx)):
            x = x + kx
            e = e - dy
            if (e < 0):
                y = y + ky
                e = e + dx
            line.append([x, y])
    else:
        e = dy / 2
        for i in range(0, int(dy)):
            y = y + ky
            e = e - dx
            if (e < 0):
                x = x + kx
                e = e + dy
            line.append([x, y])
    return line

class Pixel:
    def __init__(self):
        self.maximum = int(0)
        self.normalized = np.float(0)
        self.raw = np.float(0)


def get_pixel_value(picture, line):
    pixel = Pixel()
    for pos in line:
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < picture_size and pos[1] < picture_size:
            pixel.raw += float(picture[int(pos[0]), int(pos[1])][0])
            pixel.maximum += 1
    assert pixel.maximum != 0
    pixel.normalized = pixel.raw / pixel.maximum
    return pixel


img = Image.open('../img/phantom.bmp').convert('LA')
pix = img.load()
sizeOfImage = size(img)

width = 90
detector_amount = 180
alpha = 2

picture_size = sizeOfImage

# r = int(np.ceil(np.sqrt(picture_size * picture_size)))
r = int(picture_size)
sinogram = []
lines = []


# poruszaj emiterem 360/n razy o kąt alpha i zbierz próbki promieni.
for i in range(0, 360, alpha):
    sinogram.append([])
    lines.append([])
    for detector in range(0, detector_amount):
        x0 = r * np.cos(i * np.pi / 180)
        y0 = r * np.sin(i * np.pi / 180)

        x1 = r * np.cos((i + 180 - (width / 2) + detector * (width / (detector_amount - 1))) * np.pi / 180)
        y1 = r * np.sin((i + 180 - (width / 2) + detector * (width / (detector_amount - 1))) * np.pi / 180)

        x0 = int(x0) + np.floor(picture_size / 2)
        x1 = int(x1) + np.floor(picture_size / 2)
        y0 = int(y0) + np.floor(picture_size / 2)
        y1 = int(y1) + np.floor(picture_size / 2)
        # print(x0,y0,x1,y1)
        line = bresenhams_line(x0, y0, x1, y1)

        pixel = get_pixel_value(pix, line)


        sinogram[-1].append(pixel.normalized)
        lines[-1].append([x0, y0, x1, y1])

fig, plots = plt.subplots(1, 3)
plots[0].imshow(img, cmap='gray')
plots[1].imshow(sinogram, cmap='gray')

picture = pix

def normalizing_picture(reconstructed, helper):
    normalized = np.copy(reconstructed)
    picture_shape = np.shape(normalized)
    width = picture_shape[0]
    height = picture_shape[1]
    for i in range (0, width, 1):
        for j in range (0, height, 1):
            if helper[i][j] != 0:
                normalized[i][j] = normalized[i][j]/helper[i][j]
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

def gamma(img, gamma):
    new = img ** gamma
    return new

def filtering_picture(img) :
    new = filters.gaussian(img, sigma=1)
    #new = rescale_intensity(new)
    new = mp.dilation(mp.erosion(new))
    return new

# wymiary zdjęcia końcowego
picture_shape = np.shape(picture)
width = sizeOfImage
height = sizeOfImage
# width = picture_shape[0]
# height = picture_shape[1]

# dane o projekcjach i detektorach
sinogram_shape = np.shape(sinogram)
number_of_projections = sinogram_shape[0]
number_of_detectors = sinogram_shape[1]

# dane do tworzenia gifa i statystyk
images = []
iterator = 0
mse = np.zeros(ceil(number_of_projections / 10) + 1)

# dane do rekonstrukcji zdjęcia
# reconstructed = np.zeros(shape=picture_shape)
# helper = np.zeros(shape=picture_shape)
reconstructed = np.zeros(shape=(width,height))
helper = np.zeros(shape=(width,height))

# obserwacje
# plot_images(picture, sinogram)
# plot_diagram(sinogram, sinogram)

filtr = True
# rekonstrukcja zdjęcia
for projection in range(0, number_of_projections, 1):
    for detector in range(0, number_of_detectors, 1):
        x0, y0, x1, y1 = lines[projection][detector]
        line = bresenhams_line(x0, y0, x1, y1)
        value = sinogram[projection][detector]
        for i in range(0, len(line), 1):
            x, y = line[i]
            if x >= 0 and y >= 0 and x < width and y < height:
                reconstructed[int(x)][int(y)] += value
                helper[int(x)][int(y)] += 1

    # tworzenie gifa i zbieranie statystyk
    fragment = normalizing_picture(reconstructed, helper)
    if (filtr):
        fragment[fragment[:, :] < 0] = 0
        fragment = rescale_intensity(fragment)

    images.append(gamma(fragment, 1))


# tworzenie gifa i zbieranie statystyk
fragment = normalizing_picture(reconstructed, helper)
if (filtr):
    fragment[fragment[:,:] < 0] = 0
    fragment = rescale_intensity(fragment)
images.append(gamma(fragment, 1))

# obserwacje
# plot_images(picture, fragment)

# tworzenie gifa i zbieranie statystyk
if (filtr):
        reconstructed = filtering_picture(fragment)
        images.append(gamma(reconstructed, 1))
else:
    reconstructed = fragment
    images.append(gamma(reconstructed, 1))



reconstructed = rotate(reconstructed, 90, resize=True)

plots[2].imshow(reconstructed, cmap='gray')

plt.show()
plt.savefig("../out/" + str(datetime.now()) + "width:" + str(width) + "d_a: " + str(detector_amount) + "alpha: " + str(alpha) + ".jpg")
