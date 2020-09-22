import cv2 
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt
import platform
import time
from matplotlib.patches import Circle
import itertools


#Extract Metadata
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from exif_extract import *


inum  = 1
lnum  = 8

sumx=0
val = 0
sumy=0
square=[]
sumxR=0
sumyR=0
boolCounter=0
loop=1
loopR=1
loop2=1
minArea=2000
temp=0
x1=0
y1=0
x2=0
y2=0
x3=0
y3=0
x1R=0
y1R=0
x2R=0
y2R=0
x3R=0
y3R=0
x4R=0
y4R=0
tArea=0
loopX=0

for i in range(inum, lnum):

    image    = '40m/DJI_0{}.JPG'.format(i)
    filename = '40m/DJI_0{}_output.JPG'.format(i)
    img      = cv2.imread(image)
    #Metadata
############################################################################################################
    exif       = get_exif(image)
    labeled    = get_labeled_exif(exif)
    geotags    = get_geotagging(exif)
    imgcenter  = get_coordinates(geotags)
    datetime   = get_date_time(labeled)
    spatialres = get_spatial_resolution(labeled)
############################################################################################################    

    # scale_percent = 100
    # width         = int(img.shape[1] * scale_percent / 100)
    # height        = int(img.shape[0] * scale_percent / 100)
    # dim           = (width, height)
    # img           = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    hsv           = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    hMin              = 150
    hMax              = 255
    sMin              = 130
    sMax              = 255
    vMin              = 0
    vMax              = 110
    Kernel1           = 5
    Kernel2           = 5
    ErosionIteration  = 8
    DilationIteration = 2
    closing           = 0
    opening           = 1

    lower=np.array([hMin,sMin,vMin])
    upper=np.array([hMax,sMax,vMax])
    mask = cv2.inRange(hsv, lower, upper)
    moments = cv2.moments(mask, True)

    if closing==1:
        kernel = np.ones((Kernel1,Kernel2),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    if opening==1:
        kernel = np.ones((Kernel1,Kernel2),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    if DilationIteration>0:
        kernel = np.ones((Kernel1,Kernel2),np.uint8)
        mask = cv2.dilate(mask,kernel,iterations = DilationIteration)
    if ErosionIteration>0:
        kernel = np.ones((Kernel1,Kernel2),np.uint8)
        mask = cv2.erode(mask,kernel,iterations = ErosionIteration)

#---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#
    blur = cv2.GaussianBlur(mask, (9, 9), 3)

    #Apply canny edge, will be easier to find shapes
    edges = cv2.Canny(blur,x1,x2)

    if DilationIteration>0:
        kernel = np.ones((Kernel1,Kernel2),np.uint8)
        edges = cv2.dilate(mask,kernel,iterations = DilationIteration)
    #If the area of the white part of the mask is larger than 500px, probably it's not noise
    if moments['m00'] >= 300:

        #Find all the contour points and store them inside contours
        contours,hier = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        d    = 200
        t    = 5
        rmin = 0
        rmax = 20

        detected_circles = cv2.HoughCircles(edges,  
                                            cv2.HOUGH_GRADIENT, 1, d, param1 = 200, 
                                            param2 = t, minRadius = rmin, maxRadius = rmax)

        if detected_circles is not None: 
  
            # Convert the circle parameters a, b and r to integers. 
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]: 
                a, b, r = pt[0], pt[1], pt[2] 
  
                # Draw the circumference of the circle. 
                # cv2.circle(img, (a, b), r, (0, 0, 255), 3) 
  
                # Draw a small circle (of radius 1) to show the center. 
                cv2.circle(img, (a, b), 1, (255, 0, 0), 30)
    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#
    #-----Detecting circles----#

    plt.imshow(img)
    plt.show()
    cv2.imwrite(filename, img)
    print(image,datetime)