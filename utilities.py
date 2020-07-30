import os
import csv
import time
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from PIL import Image
from itertools import izip

# For Color Printing
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Valid Extensions
extensions = ("jpeg", "png", "gif", "jpg")

# Temporary directory for uploaded datasets
dir1 = "./dataset/temp1/"
dir2 = "./dataset/temp2/"

# Default datasets
dataset1 = "./dataset/dataset1/"
dataset2 = "./dataset/dataset2/"

# For the similarity score calculation between two images
def mse(imgA, imgB):
	return np.square(np.subtract(imgA,imgB)).mean()

# Unzip custom datasets (to be compared)
def unzip(zip1, zip2):
    # unzip the first dataset to temp directory 1
    with zipfile.ZipFile(zip1, 'r') as ref:
        ref.extractall(dir1)
    # unzip the second dataset to temp directory 2
    with zipfile.ZipFile(zip2, 'r') as ref:
        ref.extractall(dir2)

# To clear temporary directory after the program finished running
def clear_temp_dir(dir):
    files = [file for file in os.listdir(dir)]
    for file in files:
        os.remove(os.path.join(dir, file))

# Open (one) directory being passed to read the files
def open_dir(dir_path):
    count = 0
    file_names = []

    if not os.path.exists(dir_path):
        print(colors.FAIL + "Directory doesn't exist" + colors.ENDC)
        return False

    # List all files in the folder; sorted by name ascendingly
    for file in sorted(os.listdir(dir_path)):
        # If file has valid extension, count and save the file name
        if file.endswith(extensions):
            count += 1
            file_names.append(file)
        # Stop the program
        else:
            print(colors.FAIL + "Invalid file format" + colors.ENDC)
            return False

    return count, file_names

# Save result to csv format
def generate_csv(output):
    try:
        # Open new csv to save the result
        with open('output.csv', 'w') as file:
            writer = csv.writer(file)

            # csv column header
            header = ["image1", "image2", "similar", "elapsed"]
            print(header[0], "\t\t", header[1], "\t\t", header[2], "\t\t", header[3])
            writer.writerow(header)

            # append result per row
            for o in output:
                print(o[0], "\t\t", o[1], "\t\t", o[2], "\t\t", o[3])
                writer.writerow(o)
    except:
        print(colors.FAIL + "Something went wrong when generating CSV" + colors.ENDC)

# Preprocessing image
def preprocess_image(image_path):
    img = Image.open(image_path)
    # Resize image for the case where comparing two different size of images
    img = img.resize((500, 500), Image.ANTIALIAS)
    img.save(image_path)
    return img

# Convert any images to grayscale to uniform the shape 
# As some channels is >= 3 to 1 channel only
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

# Compare images in two datasets
def compare_images(a = dataset1, b = dataset2):
    # List of outputs, declared as a list
    # Will be a 2D list as the format will be:
    # [[example1.png, example2.jpg, 0.0, 0.2], [.., .., .., ..], ...]
    output = []

    # If not default dataset from web, unzip
    if (a != dataset1 and b != dataset2) and (dataset1.endswith("zip") and dataset2.endswith("zip")):
        unzip(a,b)

    # Find how many files and files in the directory
    len_a, files_a = open_dir(a)
    len_b, files_b = open_dir(b)

    # If any of the dataset is empty return false
    if len_a == 0 or len_b == 0:
        print(colors.FAIL + "Error, one or both of the folders are empty" + colors.ENDC)
        return False
    # If datasets has unmatch number of photos to compare, return false
    if len_a != len_b:
        print(colors.FAIL + "Mismatch number of images to compared" + colors.ENDC)
        return False

    # Loop through all files in the folder
    for i in range(len_a):
        # Start time
        start = time.time()

        # Path
        imgA = a + files_a[i]
        imgB = b + files_b[i]

        # Preprocess images and read image
        preprocess_image(imgA)
        preprocess_image(imgB)
        imgA, imgB = rgb2gray(image.imread(imgA)), rgb2gray(image.imread(imgB))
        
        # Calculate similarity score
        # Where the image format is in matrix format
        similar = mse(imgA, imgB)

        # Calculate Elapsed = end time - start time
        elapsed = time.time() - start

        # Round decimals to two point decimals
        # Replace image with the name of the image
        similar = "{:.2f}".format(round(similar, 2))
        elapsed = "{:.2f}".format(round(elapsed, 2))
        imgA, imgB = files_a[i], files_b[i]

        # Append to output list
        output.append([imgA, imgB, similar, elapsed])

        # For debugging purposes
        #print(imgA, imgB, similar, "{:.2f}".format(round(elapsed, 2)))

    # Generate CSV, pass list of outputs
    generate_csv(output)