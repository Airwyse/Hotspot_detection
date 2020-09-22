import cv2 
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import platform
import time
from matplotlib.patches import Circle
import itertools

#Extract Metadata
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from exif_extract import *

img        = 'data/Hole5_fairway_dollarspot_1.JPG'

#Metadata
############################################################################################################
exif       = get_exif(img)
labeled    = get_labeled_exif(exif)
geotags    = get_geotagging(exif)
imgcenter  = get_coordinates(geotags)
datetime   = get_date_time(labeled)
spatialres = get_spatial_resolution(labeled)
############################################################################################################

cimg     = cv2.imread(img, cv2.IMREAD_COLOR)
cimg     = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
hsvimg   = cv2.cvtColor(cimg, cv2.COLOR_RGB2HSV)

#Check color range
############################################################################################################
light_brown = (10, 50, 100)
dark_brown  = (30, 200, 200)

lo_square = np.full((10, 10, 3), light_brown, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_brown, dtype=np.uint8) / 255.0

plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.show()
##########################################################################################################

mask = cv2.inRange(hsvimg, light_brown, dark_brown)
mask = cv2.dilate(mask, None)
mask = cv2.fastNlMeansDenoising(mask,None,300,1,41)

detected_circles = cv2.HoughCircles(mask,  
                   cv2.HOUGH_GRADIENT, 1, 30, param1 = 200, 
               param2 = 10, minRadius = 1, maxRadius = 20) 
  
# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0,:]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the surrounding.
        # cv2.circle(cimg, (a, b), r, (255, 0, 0), 20) 
        # cv2.rectangle(cimg, (a-5*r, b-10*r), (a+5*r, b+10*r), (255, 0, 0), 20) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(cimg, (a, b), 1, (0, 0, 0), 30)

        # spatialr = 0.25
        # area     = np.pi*(spatialr**2)
        # areain   = area*1550

        coordinates = a,b

    plt.imshow(cimg)
    plt.axis('off')
        # plt.text(0,2000,"Area= {:.2f} sq.m.".format(area), fontsize=15, fontweight='bold')
        # plt.text(0,2100,"Date and Time= {}".format(datetime), fontsize=15, fontweight='bold')
        # plt.text(0,1850,"Coordinates: (35.7 N, 76.03 W)", fontsize=15, fontweight='bold')
    plt.show()

#Testing
plt.imshow(mask)
plt.show()

