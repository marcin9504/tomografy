import matplotlib.pyplot as plt
from PIL import Image
from math import sin,cos, sqrt, pi
from datetime import datetime


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
outPic = img.load()
sizeOfImage = size(img)

allLines = []

count = 100
shiftCount = 10

beta_step = 2 * pi * (5 / 360)

for i in range(1, count + 1):
    if(i % 50 == 0):
        print("getting line ", i, "/", count)
    alpha = 2 * pi * (i / count)
    for eachShift in range(shiftCount):
        beta = beta_step * (-shiftCount / 2 + eachShift)
        l1 = bresenhamPointsOnLine(point(sizeOfImage, alpha), point(sizeOfImage, alpha + beta + pi))

        l2 = []
        for i in range(len(l1)):
            if(l1[i][0] < 0 or l1[i][0] >= sizeOfImage or l1[i][1] < 0 or l1[i][1] >= sizeOfImage):
                pass
            else:
                l2.append(l1[i])

        allLines.append(l2)

sinogram = []

for eachLine in allLines:
    localSum = 0
    for p in eachLine:
        localSum = localSum + pix[(p[0], p[1])][0]
    avg = localSum / len(eachLine)

    sinogram.append((eachLine, avg))

for i in range(0, sizeOfImage):
    for j in range(0, sizeOfImage):
        pix[i, j] = (255, 255)

localMax = 1
localMin = 255

outArray = [[(0, 0) for x in range(sizeOfImage)] for y in range(sizeOfImage)]

for eachGoodLine in sinogram:
    for p in eachGoodLine[0]:
        value = int(outArray[p[0]][p[1]][0] + eachGoodLine[1])
        numberOfLinesHere = outArray[p[0]][p[1]][1] + 1
        outArray[p[0]][p[1]] = (value, numberOfLinesHere)

for i in range(0, sizeOfImage):
    for j in range(0, sizeOfImage):
        value = 0
        if(outArray[i][j][1] > 1):
            value = outArray[i][j][0] / outArray[i][j][1]
            pix[i, j] = (int(value), 255)
        if (value > localMax):
            localMax = value
        if (value < localMin):
            localMin = value

for i in range(0, sizeOfImage):
    for j in range(0, sizeOfImage):
        # value = (outArray[i][j][0] - localMin) / (localMax - localMin) * 255
        value = (outArray[i][j][0] / localMax) * 255
        pix[i, j] = (int(value), 255)

plt.imshow(img)
plt.savefig("../out/" + str(datetime.now()) + ".jpg")
