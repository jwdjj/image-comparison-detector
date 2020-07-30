# Image Comparison Detector

## Overview

This is a web based application used to compare two datasets of images and generate the result in a csv format

## Application

You can access the application [here](https://master.dktfyu48edg30.amplifyapp.com/)

## Output format 

| image1        | image2        | similar  | elapsed |
| ------------- | ------------- | -------- | ------- |
| ex1.png       | ex2.png       | 0.0      | 0.23    |


```
image1, image2, similar, elapse
ex1.png, ex2.png, 0.0, 0.23
```

## Developer Guide

### Depedencies

1. [Python 2.7](https://www.python.org/downloads/windows/)
2. [PIP](https://pip.pypa.io/en/stable/installing/)
2. [Flask 1.1.2](https://flask.palletsprojects.com/en/1.1.x/installation/)
3. [Pillow 6.2.2](https://pillow.readthedocs.io/en/stable/installation.html)
4. [matplotlib 2.2.5](https://ehmatthes.github.io/pcc/chapter_15/README.html#:~:text=Installing%20matplotlib%20on%20Windows,-To%20install%20matplotlib&text=Go%20to%20https%3A%2F%2Fdev,need%20an%20installer%20for%20matplotlib.)
5. [numpy 1.16.6](https://phoenixnap.com/kb/install-numpy)

Note: 
1. These dependencies is based during initial testing and the version can be adjusted and upgraded as necessary
2. For **MacOS** you can run `./run.sh` to install all of the dependencies
- To install, make sure you're local admin on your machine
- If it's blocked by security run one of the following: `xattr -d com.apple /path_to_binary` or run `sudo spctl --master-disable` install then `sudo spctl --master-enable`
3. For **Windows**, download and install of the dependencies above

### How to Run this Application

#### Web-based application
1. Once you have all of the depencies installed, run `python app.py`
3. Open on your localhost on port 5000 on your browser `http://localhost:5000/`

#### Console

Run this on CLI:
`./main.py dataset_path_1/ dataset_path_2/`

Note: make sure the path ends with '/'

### How to deploy the Web Application

Currently it is using AWS - GitHub connectivity
Customized pipeline as necessary or create one

### File and Folder details

1. app.py = main function, correspond to front-end requests
2. utilities.py = common functions to calculate and generate results
3. main.py = main function, but for console application
4. templates = Front-end (html/css/js) related files
5. dataset = default datasets and temp directory for custom database
6. requirements.txt = requirement list (pip)
7. run.sh = script to install depedencies on MacOS

## To Do and Known Bugs

1. Regression Testing (especially for unexpected input and cases)
2. Still missing some exception catch
3. Compatibility testing
4. Pipeline
5. Note how to use on the user-facing page how to use the app
6. Custom uploaded database for user facing

```
1. Make frontend into form to get the uploaded file
2. On main.py past the uploaded .zip folder
3. On utilities.py, needs to test the unzip functions (logic is in place line #95)
```

7. png - gif issues

```
For this issue, this happens if we processed the image using PIL
Using matplotlib solved this issue:

imgA = plt.imread('path_to_png')
imgB = plt.imread('path_to_gif')
mse(imgA, imgB)

but currently it will return large error margin
we can't use this version currently because of the result difference when reading using PIL and matplotlib
```

## Appendix

### Image Processing

1. Currently generalize preprocessing and normalizing by resizing and convert the image into greyscale
2. It's the easiest if we are using [opencv / cv2](https://pypi.org/project/opencv-python/) libraries, but have to consider installation and compatibility issue can be an issue
3. Currently using MSE (utilities.py line#34-35) to calculate the score but the following can be some things to consider:
- SSIM is another calculation technique to consider, can create the function or use PIL SSIM function
- Converting images to histogram - normalize - then compare is another technique to consider

### Design Choices

1. To avoid compatibility issue for users, decided to deploy and create this application as web-based application
2. As developer that can use console application, the script can be customized as required
3. Giving the ability for users to provide their own database, make the application is extensively reusable