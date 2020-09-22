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
exif       = get_exif('data/10m_hotspot(3).jpg')
labeled    = get_labeled_exif(exif)
geotags    = get_geotagging(exif)
imgcenter  = get_coordinates(geotags)
datetime   = get_date_time(labeled)
spatialres = get_spatial_resolution(labeled)
############################################################################################################

cimg     = cv2.imread('data/10m_hotspot(3).jpg', cv2.IMREAD_COLOR)
cimg     = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
img      = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(img, 75, 255, cv2.THRESH_BINARY_INV)
img      = cv2.fastNlMeansDenoising(img,None,50,7,21)
# img  = cv2.Canny(img,10,50)

if platform.system() == 'Windows':
    NIX = False
    print("Running on Windows system")
else:
    NIX = True
    print("Running on Linux/OS X system")

# Blur using 3 * 3 kernel. 
blurred = cv2.blur(img, (3, 3)) 

#Dilate image
dilated  = cv2.dilate(img,None)
eroded   = cv2.erode(img, None)
  
# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(blurred,  
                   cv2.HOUGH_GRADIENT, 1, 90, param1 = 200, 
               param2 = 10, minRadius = 60, maxRadius = 70) 
  
# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(cimg, (a+r, b+r), r*2, (255, 0, 0), 20) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(cimg, (a+r, b+r), 1, (0, 0, 0), 30)

        spatialr = r*spatialres
        area     = np.pi*spatialr**2
        areain   = area*1550

    coordinates = a,b


    plt.imshow(cimg)
    plt.axis('off')
    plt.text(0,2000,"Area= {:.2f} sq.in.".format(area*20), fontsize=15, fontweight='bold')
    plt.text(0,2100,"Date and Time= {}".format(datetime), fontsize=15, fontweight='bold')
    plt.text(0,1850,"Coordinates: (35.7 N, 76.03 W)", fontsize=15, fontweight='bold')
    plt.show()

#Testing
# plt.imshow(img)
# plt.show()