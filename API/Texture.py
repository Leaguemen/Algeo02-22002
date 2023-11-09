import base64
import math
from flask_cors import CORS

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
    dot = vec1[0]*vec2[0]+vec1[1]+vec2[1]+vec1[2]+vec2[2]
    len1 = math.sqrt((vec1[0]**2)+(vec1[1]**2)+(vec1[2]**2))
    len2 = math.sqrt((vec2[0]**2)+(vec2[1]**2)+(vec2[2]**2))
    return dot/(len1*len2)

def getTexture(str):
    # return tuple 3 elemen: (contrast,homogeneity,entropy)

    # convert base64 to image
    img_decoded = base64.b64decode(str)
    img_file = BytesIO(img_decoded)
    img = Image.open(img_file)
    #img.show() #cek image sesuai

    # get image rgb and dimension
    img_arr = np.array(img)
    height = img_arr.shape[0]
    width = img_arr.shape[1]

    # create matrix of grayscale value
    gray_arr = [[grayscaled(img_arr[i,j]) for j in range(width)] for i in range(height)] 
    gray_arr = np.array(gray_arr)
    # test_im = Image.fromarray(gray_arr) # cek grayscale sesuai
    # test_im.show()

    # create co-occurance Matrix
    coMatrix = [[0 for j in range(256)] for i in range(256)]
    #distance = 0, angle = 0
    for i in range(height):
        for j in range(width-1):
            coMatrix[gray_arr[i,j]][gray_arr[i,j+1]] += 1
    # bisa di optimalisasi
    coMatrix = np.array(coMatrix)
    coMatrixT = coMatrix.transpose()
    symMatrix = np.add(coMatrix,coMatrixT) #add co-occurance matrix dengan transposenya
    #symMatrix == glcm
    glcmSum = 0
    for i in range(256):
        for j in range(256):
            glcmSum += symMatrix[i,j]

    # calculate contrast, homogeneity, entropy
    contrast, homogeneity, entropy = 0, 0, 0
    for i in range(256):
        for j in range(256):
            p = (symMatrix[i,j]/glcmSum)
            d = (i-j)
            contrast += p*(d**2)
            homogeneity += p/(1+(d**2))
            if (p > 0):
                entropy += p*(math.log(p,10))
                
    return (contrast,homogeneity,entropy)

def compareImage(b64_1, b64_2):
    vector1 = getTexture(b64_1)
    vector2 = getTexture(b64_2)

    similarity = cosSim(vector1,vector2)

    return similarity
