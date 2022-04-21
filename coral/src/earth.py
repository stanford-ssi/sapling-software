from PIL import Image
import numpy as np


image = Image.open('img0000.jpg')
imageR = Image.open('img0001.jpg')

print(image.size)
print(image.format)
print(image.mode)

np_img = np.array(image)
np_imgR = np.array(imageR)

print(np_img.shape)
print(np_img[20, 20])
print(np_imgR[20, 20])

totalPixels = total = np_img.shape[0] * np_img.shape[1]
print(totalPixels)
#TODO calculate using a threshold instead of a

black = np.count_nonzero(np.all(np_img < [20, 20, 20], axis = 2));
print(f"Black pixels {black}")
roundedPercent = round(black/totalPixels, 3)
print(f"Percentage black pixles: {roundedPercent}")


