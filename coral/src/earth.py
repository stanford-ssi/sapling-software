from PIL import Image
import numpy as np
import os

def analyzeImage(image):
    np_img = np.array(image)
    print(image.filename)
    print(image.size)
    print(np_img.shape)

    totalPixels = total = np_img.shape[0] * np_img.shape[1]
    print(f"Total Pixels: {totalPixels}")

    #Test for actual expected thresholds
    black = np.count_nonzero(np.all(np_img < [45, 45, 45], axis = 2))
    white = np.count_nonzero(np.all(np_img > [235, 235, 235], axis = 2))
    
    print(f"Black pixels: {black}")
    print(f"White pixels: {white}")
    
    blackPercent = round(black/totalPixels, 3)
    whitePercent = round(white/totalPixels, 3)

    print(f"Percentage black pixles: {blackPercent}")
    print(f"Percentage white pixels: {whitePercent}")

    unusablePercent = round(blackPercent + whitePercent, 3)
    print(f"Combined unusable percent: {unusablePercent}")

    if unusablePercent > 0.6:
        print("Don't send image down\n")
        #return False
    else:
        print("Send image down\n")
        #return True

    # by default send image down
    print()
    #return true

for filename in os.listdir('Images'):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        image = Image.open("Images/"+filename)
        analyzeImage(image)
