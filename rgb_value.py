import cv2 
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt
import platform
import time
from matplotlib.patches import Circle
import itertools

img = 'data/Hole5_fairway_dollarspot_1.JPG'
# img = 'data/Hole6_nearTeebox_dollarspot_2.JPG'
# img = 'data/IMG_3072.jpg'
scale_percent = 35

def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = image[y,x,0]
        colorsG = image[y,x,1]
        colorsR = image[y,x,2]
        colors = image[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)

# Read an image, a window and bind the function to window
image1 = cv2.imread(img)
width = int(image1.shape[1] * scale_percent / 100)
height = int(image1.shape[0] * scale_percent / 100)
dim = (width, height)
image1 = cv2.resize(image1, dim, interpolation = cv2.INTER_AREA)
cv2.namedWindow('mouseRGB')
cv2.setMouseCallback('mouseRGB',mouseRGB)

#Do until esc pressed
while(1):
    cv2.imshow('mouseRGB',image1)
    if cv2.waitKey(20) & 0xFF == 27:
        break
#if esc pressed, finish.
cv2.destroyAllWindows()


def mouseHSV(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsH = image[y,x,0]
        colorsS = image[y,x,1]
        colorsV = image[y,x,2]
        colors = image[y,x]
        print("H: ",colorsH)
        print("S: ",colorsS)
        print("V: ",colorsV)
        print("HSV Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)

# Read an image, a window and bind the function to window
image = cv2.imread(img)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image2 = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
width = int(image2.shape[1] * scale_percent / 100)
height = int(image2.shape[0] * scale_percent / 100)
dim = (width, height)
image2 = cv2.resize(image2, dim, interpolation = cv2.INTER_AREA)
cv2.namedWindow('mouseHSV')
cv2.setMouseCallback('mouseHSV',mouseHSV)

#Do until esc pressed
while(1):
    cv2.imshow('mouseHSV',image2)
    if cv2.waitKey(20) & 0xFF == 27:
        break
#if esc pressed, finish.
cv2.destroyAllWindows()

def mouseHLS(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsH = image[y,x,0]
        colorsL = image[y,x,1]
        colorsS = image[y,x,2]
        colors = image[y,x]
        print("H: ",colorsH)
        print("L: ",colorsL)
        print("S: ",colorsS)
        print("HLS Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)

# Read an image, a window and bind the function to window
image = cv2.imread(img)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image3 = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
width = int(image3.shape[1] * scale_percent / 100)
height = int(image3.shape[0] * scale_percent / 100)
dim = (width, height)
image3 = cv2.resize(image3, dim, interpolation = cv2.INTER_AREA)
cv2.namedWindow('mouseHLS')
cv2.setMouseCallback('mouseHLS',mouseHLS)

#Do until esc pressed
while(1):
    cv2.imshow('mouseHLS',image3)
    if cv2.waitKey(20) & 0xFF == 27:
        break
#if esc pressed, finish.
cv2.destroyAllWindows()

