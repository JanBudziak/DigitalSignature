import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imageio
from PIL import Image
from PIL import ImageGrab
import time


def generate_new_TRNG(bin_file_path):
    counter = 0
    while counter < 1:
        if counter == 0:
            print("Od teraz masz 10 sekund na przelączenie obrazu ekranu na wizję która często się zmienia.Gdy program zacznie przechwytywać ekran w outpucie pojawi się słowo \"Start\"")
            time.sleep(10)
            print("Start")


        print("Dataset no.", counter) 

        img = ImageGrab.grab()
        img.save(f"{counter}.jpg")

        img = Image.open(f"{counter}.jpg")
        img.save(f"{counter}.bmp")
            

        #read img - screenshot or lena

        img = imageio.imread(f"{counter}.bmp")

        #img = imageio.imread(f"0.bmp")

        height= img.shape[0]
        img = np.resize(img,(height,height,3) )
        
       


        #Truning image to grayscale

        def grayscaleImage(img):
            R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]
            imgGray = np.array(0.2989*R + 0.5870*G + 0.1140*B, dtype='uint8')
            return imgGray
            
        img_gray=grayscaleImage(img)


        # Simple error dithering made by me, please work

        def simpleDithering(img):
            height, width = img.shape
            
            for y in range (height):
                for x in range (width):
                    #calculatin if error is positive or negative
                    if img[x,y] >= 127:
                        error = -(255 - img[x,y])
                    if img[x,y] < 127:     
                        error = 255 - img[x,y]
                    #adding error values to neighboring pixels
                    if x + 1 < width:
                        img[y, x + 1] += error * 0.375 # right, 7 / 16
                    if (y + 1 < height) and (x + 1 < width):
                        img[y + 1, x + 1] += error * 0.0625 # right, down, 1 / 16
                    if y + 1 < height:
                        img[y + 1, x] += error * 0.3125 # down, 5 / 16
                    if (x - 1 >= 0) and (y + 1 < height): 
                        img[y + 1, x - 1] += error * 0.1875 # left, down, 3 / 16
            return img

        img_to_dither = img_gray

        img_dithered = simpleDithering(img_to_dither)

        # Chat GPT Version v0.1

        def arnold_cat_map(image, iterations):
            height, width = image.shape
            new_image = np.copy(image)

            for _ in range(iterations):
                temp_image = np.copy(new_image)
                for i in range(height):
                    for j in range(width):
                        new_i = (2*i + j) % height
                        new_j = (i + j) % width
                        new_image[new_i, new_j] = temp_image[i, j]

            return new_image


        # Set the number of iterations for scrambling
        iterations = 10

        # Scramble the image
        scrambled_image = arnold_cat_map(img_dithered, iterations)

        #Write to File

        binaryFile = open(bin_file_path, "ab")

        binaryFile.write(scrambled_image)
        binaryFile.close()

        counter += 1
    
    return 