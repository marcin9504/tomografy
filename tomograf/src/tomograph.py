import matplotlib.pyplot as plt
from PIL import Image
from math import sin,cos, sqrt, pi

def size(image):
    return min(img.size[0], img.size[1])

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

img = Image.open('../img/img.bmp').convert('LA')
pix = img.load()
outPic = img.load()
s = size(img)
print("center: ", center(s))
alpha = pi / 8
l1 = line(center(s), point(s, alpha))
print("line: ", l1)
print("distance: ", distance(l1, center(s)))
pointsOnLine = allPointsOnLine(l1, s)
print("points in circle: ", pointsOnLine)
for point in pointsOnLine:
    pix[(point[0], point[1])] = (0, 255)
    pass

for i in range(0, s):
    for j in range(0, s):
         # outPic[i,j] = (0, 255)
        pass
#
# first_line = [(s // 2, i) for i in range(0, s)]
# # print(first_line)
# sum = 0
# for pixel in first_line:
#     # print(pix[pixel])
#     sum = sum + pix[pixel][0]
# sum = sum / len(first_line)
#
# for pixel in first_line:
#     pix[pixel] = (int(sum), 255)
# # print(sum)

plt.imshow(img)
plt.savefig('../out/out.jpg')
