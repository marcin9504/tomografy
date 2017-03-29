#inspired by: https://github.com/huntekah/Informatyka-w-Medycynie-Tomograf
import matplotlib.pyplot as plt
from PIL import Image
from math import sin,cos, sqrt, pi, ceil, floor
from datetime import datetime
import numpy as np

def size(image):
    return min(image.size[0], image.size[1])


def center(size):
    center = [size / 2, size / 2]
    return center


def point(size, alpha):
    r = size / 2
    c = center(size)
    x = c[0] + r*sin(alpha)
    y = c[1] + r*cos(alpha)
    return [x,y]


def line(p1, p2):
    if(abs(p2[0] - p1[0]) > 0.01):
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        if (p2[0] < p1[0]):
            a = -a
        b = -a * p1[0] + p1[1]
        return [-a, 1, -b]
    else:
        return [1.0, 0.0, -p1[0]]


def bresenhamPointsOnLine(p1, p2):
    points = []
    x1 = int(p1[0])
    y1 = int(p1[1])
    x2 = int(p2[0])
    y2 = int(p2[1])

    d = dx = dy = ai = bi = xi = yi = 0

    x = x1
    y = y1

    if (x1 < x2):
        xi = 1
        dx = x2 - x1
    else:
        xi = -1
        dx = x1 - x2

    if (y1 < y2):
        yi = 1
        dy = y2 - y1
    else:
        yi = -1
        dy = y1 - y2

    points.append([int(x),int(y)])
    if (dx > dy):
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        while (x != x2):
            if (d >= 0):
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi
            points.append([int(x), int(y)])
    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy
        while (y != y2):
            if (d >= 0):
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi
            points.append([int(x), int(y)])

    return points


def distance(line, point):
    return abs(line[0] * point[0] + line[1] * point[1] + line[2]) / sqrt(line[0] * line [0] + line[1] * line[1])


def allPointsOnLine(line, size):
    allPoints = []
    for x in range(0, size):
        for y in range(0, size):
            if((x - center(size)[0]) * (x - center(size)[0])
                   + (y - center(size)[1]) * (y - center(size)[1]) < (size / 2) * (size / 2)):#if is in circle
                point = [x, y]
                threshold = 0.6
                if(distance(line, point) < threshold):
                    allPoints.append([x, y])
    return allPoints


img = Image.open('../img/phantom.bmp').convert('LA')
pix = img.load()
sizeOfImage = size(img)
#
# allLines = []
#
# count = 100
# shiftCount = 34
#
# beta_step = 2 * pi * (5 / 360)
#
# for i in range(1, count + 1):
#     if(i % 50 == 0):
#         print("getting line ", i, "/", count)
#     alpha = 2 * pi * (i / count)
#     for eachShift in range(shiftCount):
#         beta = beta_step * (-shiftCount / 2 + eachShift)
#         l1 = bresenhamPointsOnLine(point(sizeOfImage, alpha), point(sizeOfImage, alpha + beta + pi))
#
#         l2 = []
#         for i in range(len(l1)):
#             if(l1[i][0] < 0 or l1[i][0] >= sizeOfImage or l1[i][1] < 0 or l1[i][1] >= sizeOfImage):
#                 pass
#             else:
#                 l2.append(l1[i])
#
#         allLines.append(l2)
#
# sinogram = []
#
# for eachLine in allLines:
#     localSum = 0
#     for p in eachLine:
#         localSum = localSum + pix[(p[0], p[1])][0]
#     avg = localSum / len(eachLine)
#
#     sinogram.append((eachLine, avg))
#
# for i in range(0, sizeOfImage):
#     for j in range(0, sizeOfImage):
#         pix[i, j] = (255, 255)
#
# localMax = 1
# localMin = 255
#
# outArray = [[(0, 0) for x in range(sizeOfImage)] for y in range(sizeOfImage)]
#
# for eachGoodLine in sinogram:
#     for p in eachGoodLine[0]:
#         value = int(outArray[p[0]][p[1]][0] + eachGoodLine[1])
#         numberOfLinesHere = outArray[p[0]][p[1]][1] + 1
#         outArray[p[0]][p[1]] = (value, numberOfLinesHere)
#
# for i in range(0, sizeOfImage):
#     for j in range(0, sizeOfImage):
#         value = 0
#         if(outArray[i][j][1] > 1):
#             value = outArray[i][j][0] / outArray[i][j][1]
#             pix[i, j] = (int(value), 255)
#         if (value > localMax):
#             localMax = value
#         if (value < localMin):
#             localMin = value
#
# for i in range(0, sizeOfImage):
#     for j in range(0, sizeOfImage):
#         # value = (outArray[i][j][0] - localMin) / (localMax - localMin) * 255
#         value = (outArray[i][j][0] / localMax) * 255
#         pix[i, j] = (int(value), 255)

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

width = 90
detector_amount = 360
alpha = 2
#
# picture = pix
# picture_size = len(picture[0])
picture_size = sizeOfImage

r = int(np.ceil(np.sqrt(picture_size * picture_size)))
sinogram = []
lines = []

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

    images.append(gamma(fragment, 1))


# tworzenie gifa i zbieranie statystyk
fragment = normalizing_picture(reconstructed, helper)

images.append(gamma(fragment, 1))

# obserwacje
# plot_images(picture, fragment)

# tworzenie gifa i zbieranie statystyk
reconstructed = fragment
images.append(gamma(reconstructed, 1))


plots[2].imshow(reconstructed, cmap='gray')

plt.show()
plt.savefig("../out/" + str(datetime.now()) + ".jpg")
