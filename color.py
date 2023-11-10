import base64
from io import BytesIO
from PIL import Image
import numpy as np
import math
import time


def get_rgb_array_from_image(str):

    # convert base64 to image
    # img_decoded = base64.b64decode(str)
    # img_file = BytesIO(img_decoded)
    image = Image.open(str)
    # img.show() #cek image sesuai

    # resize image to 510 x 510 px (biar pas pembagian blocknya)
    resized_image = image.resize((510, 510))
    
    return np.array(resized_image)


def get_c_max(norm_rgb):
# menerima array rgb yang sudah dinormalisasi
# mengembalikan nilai Cmax
    
    c_max = norm_rgb[0]
    if norm_rgb[1] > c_max:
        c_max = norm_rgb[1]

    if norm_rgb[2] > c_max:
        c_max = norm_rgb[2]

    return c_max


def get_c_min(norm_rgb):
# menerima array rgb yang sudah dinormalisasi
# mengembalikan nilai Cmin
    
    c_min = norm_rgb[0]
    if norm_rgb[1] < c_min:
        c_min = norm_rgb[1]

    if norm_rgb[2] < c_min:
        c_min = norm_rgb[2]

    return c_min


def rgb_to_hsv(rgb):
# menerima rgb, yaitu array dengan 3 elemen: red, green, dan blue
# mengembalikan hsv, yaitu array dengan 3 elemen: hue, saturation, value
    
    # Normalize rgb
    norm_rgb = np.divide(rgb, 255)

    # Calculate Cmax, Cmin, and delta
    c_max = get_c_max(norm_rgb)
    c_min = get_c_min(norm_rgb)
    delta = c_max - c_min
    
    # Menghitung nilai H (hue)
    if delta == 0:
        hue = 0
    elif c_max == norm_rgb[0]:
        hue = 60 * (((norm_rgb[1] - norm_rgb[2]) / delta) % 6) 
    elif c_max == norm_rgb[1]:
        hue = 60 * (((norm_rgb[2] - norm_rgb[0]) / delta) + 2)
    else:
        hue = 60 * (((norm_rgb[0] - norm_rgb[1]) / delta) + 4)
    
    # Menghitung nilai S (saturation)
    if c_max == 0:
        saturation = 0
    else:
        saturation = delta / c_max
    
    # Menghitung nilai V (value)
    value = c_max

    return np.array([hue, saturation, value])


def create_hsv_array_from_rgb_array(rgb_array):
    hsv_array = np.empty((rgb_array.shape[0], rgb_array.shape[1]), dtype=np.ndarray)
    for i in range(0, rgb_array.shape[0]):
        for j in range(0, rgb_array.shape[1]):
            hsv_array[i][j] = rgb_to_hsv(rgb_array[i][j])
    
    return hsv_array


def create_blocks_hsv_array(hsv_array):
# Membagi matriks 510x510 menjadi blok-blok berukuran 3x3,
# lalu menghitung rata-rata nilai hsv dari tiap-tiap blok
    blocks_hsv_array = np.empty((hsv_array.shape[0] // 3, hsv_array.shape[1] // 3), dtype=np.ndarray)
    for i in range(0, hsv_array.shape[0], 3):
        for j in range(0, hsv_array.shape[1], 3):
            sum_hsv = np.zeros(3)
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    # sum_hsv += hsv_array[k][l]
                    sum_hsv = np.add(sum_hsv, hsv_array[k][l])
            
            average_hsv = np.divide(sum_hsv, 9)
            blocks_hsv_array[i // 3][j // 3] = average_hsv
    
    return blocks_hsv_array


def cos_similarity(hsv1, hsv2):
    dot_product = hsv1[0] * hsv2[0] + hsv1[1] * hsv2[1] + hsv1[2] * hsv2[2]
    norm_hsv1 = math.sqrt(hsv1[0] ** 2 + hsv1[1] ** 2 + hsv1[2] ** 2)
    norm_hsv2 = math.sqrt(hsv2[0] ** 2 + hsv2[1] ** 2 + hsv2[2] ** 2)
    return dot_product / (norm_hsv1 * norm_hsv2)


def compare_image_by_color(src_img1, src_img2):
    blocks_hsv_array1 = create_blocks_hsv_array(create_hsv_array_from_rgb_array(get_rgb_array_from_image(src_img1)))
    blocks_hsv_array2 = create_blocks_hsv_array(create_hsv_array_from_rgb_array(get_rgb_array_from_image(src_img2)))
    total_cos_similarity = 0
    for i in range(blocks_hsv_array1.shape[0]):
        for j in range(blocks_hsv_array1.shape[1]):
            x = cos_similarity(blocks_hsv_array1[i][j], blocks_hsv_array2[i][j])
            # print(x)
            total_cos_similarity += x
    
    return total_cos_similarity / (blocks_hsv_array1.shape[0] * blocks_hsv_array1.shape[1])


start = time.time()
result = compare_image_by_color("dataset/100.jpg", "dataset/100.jpg")
end = time.time()

print(result)
print("waktu eksekusi:", end - start, "detik")
