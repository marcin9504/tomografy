import matplotlib.pyplot as plt
from PIL import Image
img = Image.open('../img/img.bmp').convert('LA')

plt.imshow(img)
plt.savefig('../out/out.jpg')
