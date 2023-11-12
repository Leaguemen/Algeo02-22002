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
    # image.show() #cek image sesuai

    # resize image (agar pas pembagian blocknya)
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


def create_hsv_array_from_rgb_array(rgb_array):
# menerima array 2D berisi RGB
# mengembalikan array 2D berisi HSV

    # vectorized_rgb_to_hsv = np.vectorize(rgb_to_hsv, otypes=[np.ndarray])
    hsv_array = np.empty((rgb_array.shape[0], rgb_array.shape[1]), dtype=np.ndarray)
    for i in range(0, rgb_array.shape[0]):
        for j in range(0, rgb_array.shape[1]):
            hsv_array[i][j] = rgb_to_hsv(rgb_array[i][j])
    
    return hsv_array


def create_blocks_hsv_array(hsv_array):
# Membagi matriks 512x512 menjadi blok-blok berukuran 4x4,
# lalu menghitung rata-rata nilai hsv dari tiap-tiap blok

    blocks_hsv_array = np.empty((4, 4), dtype=np.ndarray)
    for i in range(0, hsv_array.shape[0], hsv_array.shape[0] // 4):
        for j in range(0, hsv_array.shape[1], hsv_array.shape[1] // 4):
            sum_hsv = np.zeros(3)
            for k in range(i, i + hsv_array.shape[0] // 4):
                for l in range(j, j + hsv_array.shape[1] // 4):
                    sum_hsv = np.add(sum_hsv, hsv_array[k][l])
            
            average_hsv = np.divide(sum_hsv, (hsv_array.shape[0] // 4) * (hsv_array.shape[1] // 4))
            blocks_hsv_array[i // (hsv_array.shape[0] // 4)][j // (hsv_array.shape[1] // 4)] = average_hsv
    
    return blocks_hsv_array


def cos_similarity(hsv1, hsv2):
# menerima 2 buah HSV
# mengembalikan nilai cosine similarity antara 2 buah HSV

    dot_product = hsv1[0] * hsv2[0] + hsv1[1] * hsv2[1] + hsv1[2] * hsv2[2]
    norm_hsv1 = math.sqrt(hsv1[0] ** 2 + hsv1[1] ** 2 + hsv1[2] ** 2)
    norm_hsv2 = math.sqrt(hsv2[0] ** 2 + hsv2[1] ** 2 + hsv2[2] ** 2)
    return dot_product / (norm_hsv1 * norm_hsv2)


def average_cos_similarity(blocks_hsv_array1, blocks_hsv_array2):
# menerima 2 buah array 2D berisi nilai rata-rata nilai HSV dari tiap-tiap blok gambar
# menjumlahkan nilai cosine similarity dari setiap elemen di dalam array 2D,
# kemudian mengembalikan nilai rata-rata cosine similarity

    total_cos_similarity = 0
    for i in range(blocks_hsv_array1.shape[0]):
        for j in range(blocks_hsv_array1.shape[1]):
            total_cos_similarity += cos_similarity(blocks_hsv_array1[i][j], blocks_hsv_array2[i][j])
    
    return total_cos_similarity / (blocks_hsv_array1.shape[0] * blocks_hsv_array1.shape[1])


def compare_image_by_color(path_image1, path_image2):
# menerima 2 buah path gambar
# mengembalikan hasil perbandingan kedua gambar
    
    # Memproses gambar 1
    rgb_array1 = get_rgb_array_from_image(path_image1)
    hsv_array1 = create_hsv_array_from_rgb_array(rgb_array1)
    blocks_hsv_array1 = create_blocks_hsv_array(hsv_array1)

    # Memproses gambar 2
    rgb_array2 = get_rgb_array_from_image(path_image2)
    hsv_array2 = create_hsv_array_from_rgb_array(rgb_array2)
    blocks_hsv_array2 = create_blocks_hsv_array(hsv_array2)

    # Membandingkan gambar 1 dan gambar 2 dengan cosine similarity
    result = average_cos_similarity(blocks_hsv_array1, blocks_hsv_array2)
    
    return result


file1 = open("img2_base64.txt")
file2 = open("img4_base64.txt")
image1 = file1.read()
image2 = file2.read()
file1.close
file2.close

start = time.time()
print("cos similarity:", compare_image_by_color(image1, image2))
finish = time.time()