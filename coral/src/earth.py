from PIL import Image
import numpy


image = Image.open('img0000.jpg')

print(image.size)
print(image.format)
print(image.mode)

np_img = numpy.array(image)
print(np_img.shape)

