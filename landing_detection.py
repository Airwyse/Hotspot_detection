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
#Metadata
############################################################################################################
exif       = get_exif('data/Hole6_nearTeebox_dollarspot_1.JPG')
labeled    = get_labeled_exif(exif)
geotags    = get_geotagging(exif)
imgcenter  = get_coordinates(geotags)
datetime   = get_date_time(labeled)
spatialres = get_spatial_resolution(labeled)
############################################################################################################

cimg     = cv2.imread('data/Hole6_nearTeebox_dollarspot_1.JPG', cv2.IMREAD_COLOR)
img      = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)
img      = cv2.erode(img, None)
img      = cv2.fastNlMeansDenoising(img,None,300,1,40)

if platform.system() == 'Windows':
    NIX = False
    print("Running on Windows system")
else:
    NIX = True
    print("Running on Linux/OS X system")

# Blur using 3 * 3 kernel. 
# blurred = cv2.blur(img, (3, 3)) 

#Dilate image
# dilated  = cv2.dilate(img,None)
# eroded   = cv2.erode(img, None)
  
# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(img,  
                   cv2.HOUGH_GRADIENT, 1, 350, param1 = 200, 
               param2 = 20, minRadius = 70, maxRadius = 80) 
  
# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0, 22:23]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the surrounding.
        cv2.circle(cimg, (a, b), r, (255, 0, 0), 20) 
        # cv2.rectangle(cimg, (a-5*r, b-10*r), (a+5*r, b+10*r), (255, 0, 0), 20) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(cimg, (a, b), 1, (0, 0, 0), 30)

        spatialr = 0.25
        area     = np.pi*(spatialr**2)
        areain   = area*1550

        coordinates = a,b

        plt.imshow(cimg)
        plt.axis('off')
        plt.text(0,2000,"Area= {:.2f} sq.m.".format(area), fontsize=15, fontweight='bold')
        plt.text(0,2100,"Date and Time= {}".format(datetime), fontsize=15, fontweight='bold')
        plt.text(0,1850,"Coordinates: (35.7 N, 76.03 W)", fontsize=15, fontweight='bold')
        plt.show()

#Testing
plt.imshow(img)
plt.show()