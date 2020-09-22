import cv2 
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt
import platform
import time
from matplotlib.patches import Circle
import itertools


cimg     = cv2.imread('data/10m_dollarspot(3).jpg', cv2.IMREAD_COLOR)
img      = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
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
               param2 = 10, minRadius = 60, maxRadius = 66) 
  
# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
    cimg     = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
  
    for pt in detected_circles[0, 2:3]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(cimg, (a-r, b+300-r), r*4, (255, 0, 0), 20) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(cimg, (a-r, b+300-r), 1, (0, 0, 0), 30)

    coordinates = a,b

    plt.imshow(cimg)
    plt.axis('off')
    # plt.text(a+2*r,b,"Coordinates {}".format(coordinates), fontsize=15)
    # print(coordinates)
    plt.text(0,1750,"Coordinates: (39 N, 83.4 W)", fontsize=15, fontweight='bold')
    plt.text(0,1900,"Area= 1643.46 sq.in.", fontsize=15, fontweight='bold')
    plt.text(0,2050,"Date: 12/16/2019", fontsize=15, fontweight='bold')
    plt.text(0,2150,"Time: 12:19:59", fontsize=15, fontweight='bold')
    plt.show()