#!/usr/bin/python

import sys
from utilities import compare_images, colors

def main():
    # Check if the argument passed is correct
    # Args: ./main.py DATASET_1_PATH/ DATASET_2_PATH/
    if len(sys.argv) != 3:
        print(colors.WARNING + "Accept two arguments: DATASET_1_PATH/ and DATASET_2_PATH" + colors.ENDC)
        return False

    # Compare Image, result is generated in output.csv
    compare_images(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()