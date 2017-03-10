import matplotlib.pyplot as plt
from PIL import Image
from math import sin,cos, sqrt, pi

def point(size, alpha):
    r = size / 2
    center = [size / 2, size / 2]
    x = center[0] + r*sin(alpha)
    y = center[1] + r*cos(alpha)
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

img = Image.open('../img/img.bmp').convert('LA')
pix = img.load()
outPic = img.load()
size = min(img.size[0], img.size[1])
center = [size / 2, size / 2]
print("center: ", center)
l1 = line(center, point(size, pi))
print("line: ", l1)
print("distance: ", distance(l1, center))
for i in range(0, size):
    for j in range(0, size):
         outPic[i,j] = (0, 255)

first_line = [(size // 2, i) for i in range(0,size)]
# print(first_line)
sum = 0
for pixel in first_line:
    # print(pix[pixel])
    sum = sum + pix[pixel][0]
sum = sum / len(first_line)

for pixel in first_line:
    pix[pixel] = (int(sum), 255)
# print(sum)
plt.imshow(img)
plt.savefig('../out/out.jpg')
