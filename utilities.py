import os
import csv
import time
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from PIL import Image
from itertools import izip

# Valid Extensions
extensions = ("jpeg", "png", "gif", "jpg")

# Temporary directory for uploaded datasets
dir1 = "./dataset/temp1/"
dir2 = "./dataset/temp2/"

# Default datasets
dataset1 = "./dataset/dataset1/"
dataset2 = "./dataset/dataset2/"

def mse(imgA, imgB):
	return np.square(np.subtract(imgA,imgB)).mean()

def unzip(zip1, zip2):
    with zipfile.ZipFile(zip1, 'r') as ref:
        ref.extractall(dir1)
    with zipfile.ZipFile(zip2, 'r') as ref:
        ref.extractall(dir2)

def clear_temp_dir(dir):
    files = [file for file in os.listdir(dir)]
    for file in files:
        os.remove(os.path.join(dir, file))

def open_dir(dir_path):
    count = 0
    file_names = []

    for file in sorted(os.listdir(dir_path)):
        if file.endswith(extensions):
            count += 1
            file_names.append(file)
        else:
            print("Invalid file format")
            return False

    return count, file_names

def generate_csv(output):
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)

        header = ["image1", "image2", "similar", "elapsed"]
        print(header[0], "\t\t", header[1], "\t\t", header[2], "\t\t", header[3])
        writer.writerow(header)

        for o in output:
            print(o[0], "\t\t", o[1], "\t\t", o[2], "\t\t", o[3])
            writer.writerow(o)

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((500, 500), Image.ANTIALIAS)
    img.save(image_path)
    return img

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def compare_images(a = dataset1, b = dataset2):
    output = []

    # if not default dataset, unzip
    if a != dataset1 and b != dataset2:
        unzip(a,b)

    len_a, files_a = open_dir(a)
    len_b, files_b = open_dir(b)

    # if dataset is empty return false
    if len_a == 0 or len_b == 0:
        print("Error, one or both of the folders are empty")
        return False
    # if dataset has unmatch number of photos to compare, return false
    if len_a != len_b:
        print("Mismatch number of images to compared")
        return False

    for i in range(len_a):
        start = time.time()

        # path
        imgA = a + files_a[i]
        imgB = b + files_b[i]

        # preprocess images
        preprocess_image(imgA)
        preprocess_image(imgB)

        imgA, imgB = rgb2gray(image.imread(imgA)), rgb2gray(image.imread(imgB))
        similar = mse(imgA, imgB)

        elapsed = time.time() - start

        similar = "{:.2f}".format(round(similar, 2))
        elapsed = "{:.2f}".format(round(elapsed, 2))
        imgA, imgB = files_a[i], files_b[i]

        output.append([imgA, imgB, similar, elapsed])

    generate_csv(output)
        
    #print(imgA, imgB, similar, "{:.2f}".format(round(elapsed, 2)))