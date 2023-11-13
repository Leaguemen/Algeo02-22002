import base64
from io import BytesIO
from PIL import Image
import numpy as np
import math
import time


def get_rgb_array_from_image(base64_image):
# menerima gambar dalam bentuk string base64
# mengembalikan array 2D berisi RGB

    # convert base64 to image
    decoded_image = base64.b64decode(base64_image)
    file_image = BytesIO(decoded_image)
    image = Image.open(file_image)

    # resize image (agar pembagian blocknya pas)
    resized_image = image.resize((512, 512))

    # mengambil hanya nilai RGB (karena format file mungkin bukan .jpg)
    rgb_resized_image = resized_image.convert("RGB")
    
    return np.array(rgb_resized_image)


def get_c_max(normalized_rgb):
# menerima array rgb yang sudah dinormalisasi
# mengembalikan nilai Cmax
    
    c_max = normalized_rgb[0]
    if normalized_rgb[1] > c_max:
        c_max = normalized_rgb[1]

    if normalized_rgb[2] > c_max:
        c_max = normalized_rgb[2]

    return c_max


def get_c_min(normalized_rgb):
# menerima array rgb yang sudah dinormalisasi
# mengembalikan nilai Cmin
    
    c_min = normalized_rgb[0]
    if normalized_rgb[1] < c_min:
        c_min = normalized_rgb[1]

    if normalized_rgb[2] < c_min:
        c_min = normalized_rgb[2]

    return c_min


def rgb_to_hsv(rgb):
# menerima rgb, yaitu array dengan 3 elemen: red, green, dan blue
# mengembalikan hsv, yaitu array dengan 3 elemen: hue, saturation, value
    
    # Normalize rgb
    normalized_rgb = np.divide(rgb, 255)

    # Calculate Cmax, Cmin, and delta
    c_max = get_c_max(normalized_rgb)
    c_min = get_c_min(normalized_rgb)
    delta = c_max - c_min
    
    # Menghitung nilai H (hue)
    if delta == 0:
        hue = 0
    elif c_max == normalized_rgb[0]:
        hue = 60 * (((normalized_rgb[1] - normalized_rgb[2]) / delta) % 6) 
    elif c_max == normalized_rgb[1]:
        hue = 60 * (((normalized_rgb[2] - normalized_rgb[0]) / delta) + 2)
    else:
        hue = 60 * (((normalized_rgb[0] - normalized_rgb[1]) / delta) + 4)
    
    # Menghitung nilai S (saturation)
    if c_max == 0:
        saturation = 0
    else:
        saturation = delta / c_max
    
    # Menghitung nilai V (value)
    value = c_max

    return np.array([hue, saturation, value])


def create_blocks_array(hsv_array):
# Membagi matriks 512x512 menjadi blok-blok berukuran 4x4,
# lalu menghitung rata-rata warna dalam blok tersebut

    blocks_array = np.empty((4, 4), dtype=np.ndarray)
    for i in range(0, hsv_array.shape[0], hsv_array.shape[0] // 4):
        for j in range(0, hsv_array.shape[1], hsv_array.shape[1] // 4):
            sum_hsv = np.zeros(3)
            for k in range(i, i + hsv_array.shape[0] // 4):
                for l in range(j, j + hsv_array.shape[1] // 4):
                    sum_hsv = np.add(sum_hsv, hsv_array[k][l])
            
            average_hsv = np.divide(sum_hsv, (hsv_array.shape[0] // 4) * (hsv_array.shape[1] // 4))
            blocks_array[i // (hsv_array.shape[0] // 4)][j // (hsv_array.shape[1] // 4)] = average_hsv
    
    return blocks_array


def create_hsv_array_from_rgb_array(rgb_array):
# menerima array 2D berisi RGB
# mengembalikan array 2D berisi HSV
    
    hsv_array = np.array([[rgb_to_hsv(j) for j in i] for i in rgb_array])
    return hsv_array


def cos_similarity(hsv1, hsv2):
# menerima 2 buah HSV
# mengembalikan nilai cosine similarity antara 2 buah HSV

    dot_product = hsv1[0] * hsv2[0] + hsv1[1] * hsv2[1] + hsv1[2] * hsv2[2]
    norm_hsv1 = math.sqrt(hsv1[0] ** 2 + hsv1[1] ** 2 + hsv1[2] ** 2)
    norm_hsv2 = math.sqrt(hsv2[0] ** 2 + hsv2[1] ** 2 + hsv2[2] ** 2)
    return dot_product / (norm_hsv1 * norm_hsv2)


def average_cos_similarity(blocks_hsv_array1, blocks_hsv_array2):
# menerima 2 buah array 2D berisi rata-rata nilai HSV dari setiap blok gambar
# menjumlahkan nilai cosine similarity dari setiap elemen di dalam array 2D tersebut,
# kemudian mengembalikan nilai rata-rata cosine similarity

    total_cos_similarity = 0
    for i in range(blocks_hsv_array1.shape[0]):
        for j in range(blocks_hsv_array1.shape[1]):
            total_cos_similarity += cos_similarity(blocks_hsv_array1[i][j], blocks_hsv_array2[i][j])
    
    return total_cos_similarity / (blocks_hsv_array1.shape[0] * blocks_hsv_array1.shape[1])


def compare_image_by_color(base64_image1, base64_image2):
# menerima 2 buah gambar dalam format base64
# mengembalikan hasil perbandingan kedua gambar

    # Memproses gambar 1
    rgb_array1 = get_rgb_array_from_image(base64_image1)
    blocks_rgb_array1 = create_blocks_array(rgb_array1)
    blocks_hsv_array1 = create_hsv_array_from_rgb_array(blocks_rgb_array1)

    # Memproses gambar 2
    rgb_array2 = get_rgb_array_from_image(base64_image2)
    blocks_rgb_array2 = create_blocks_array(rgb_array2)
    blocks_hsv_array2 = create_hsv_array_from_rgb_array(blocks_rgb_array2)

    # Membandingkan gambar 1 dan gambar 2 dengan cosine similarity
    result = average_cos_similarity(blocks_hsv_array1, blocks_hsv_array2)
    
    return result
