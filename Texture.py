import base64
import math

import numpy as np
from io import BytesIO
from PIL import Image

def grayscaled(elmt):
    #terima tuple 3 elemen (r,g,b) dan return floor value grayscalednya
    #(floor supaya comparison element, utk pembuatan co-occurance matrix, konsisten)
    r = elmt[0]
    g = elmt[1]
    b = elmt[2]
    value = 0.299*r + 0.587*g + 0.114*b
    return math.floor(value)

def cosSim(vec1, vec2):
    #return cos(theta) antara 2 vector
    dot = (vec1[0]*vec2[0])+(vec1[1]*vec2[1])+(vec1[2]*vec2[2])
    len1 = math.sqrt((vec1[0]**2)+(vec1[1]**2)+(vec1[2]**2))
    len2 = math.sqrt((vec2[0]**2)+(vec2[1]**2)+(vec2[2]**2))
    return dot/(len1*len2)

def getTexture(loc):
    # return tuple 3 elemen: (contrast,homogeneity,entropy)

    # convert base64 to image
    img = Image.open(loc)
    #img.show() #cek image sesuai

    width, height = img.size
    #print(width,height)

    # create matrix of grayscale value
    if (len(img.mode) < 3):
        gray_arr = [[img.getpixel((j,i)) for j in range(width)] for i in range(height)]
    else :
        gray_arr = [[grayscaled(img.getpixel((j,i))) for j in range(width)] for i in range(height)] 
    gray_arr = np.array(gray_arr) 
    # gray_arr = np.array(gray_arr) # cek grayscale sesuai
    # test_im = Image.fromarray(gray_arr) 
    # test_im.show()

    # create co-occurance Matrix
    coMatrix = [[0 for j in range(256)] for i in range(256)]
    #distance = 0, angle = 0
    for i in range(height):
        for j in range(width-1):
            coMatrix[gray_arr[i][j]][gray_arr[i][j+1]] += 1
    # symMatrix = np.array(coMatrix)

    glcmSum = 0
    for i in range(256):
        for j in range(i+1):
            if (i==j):
                coMatrix[i][j] *= 2
                glcmSum += coMatrix[i][j]
            else:
                temp = coMatrix[i][j]
                coMatrix[i][j] += coMatrix[j][i]
                coMatrix[j][i] += temp
                glcmSum += coMatrix[i][j]*2

    # calculate contrast, homogeneity, entropy
    contrast, homogeneity, entropy = 0, 0, 0
    for i in range(256):
        for j in range(256):
            p = (coMatrix[i][j]/glcmSum)
            d = (i-j)
            contrast += p*(d**2)
            homogeneity += p/(1+(d**2))
            if (p != 0):
                entropy -= p*(math.log(p))
                
    return (contrast,homogeneity,entropy)

def compareImage(b64_1, b64_2):
    vector1 = getTexture(b64_1)
    vector2 = getTexture(b64_2)

    similarity = cosSim(vector1,vector2)

    return similarity

img_1 = "C:/Users/Sean Nugroho/Pictures/gambarbuattesalgeo/tiger1.jpg"
img_3 = "C:/Users/Sean Nugroho/Pictures/gambarbuattesalgeo/apel.jpg"
img_2 = "C:/Users/Sean Nugroho/Pictures/gambarbuattesalgeo/dog.jpg"
img_4 = "C:/Users/Sean Nugroho/Pictures/gambarbuattesalgeo/gajah.jpg"
print(compareImage(img_1,img_2))