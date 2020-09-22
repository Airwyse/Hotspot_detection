import cv2
import numpy as np

image = 'field_data/DJI_0498.JPG'
img   = cv2.imread(image)

r=True
l=True
m=True
n=True
def nothing(z):
    pass
cv2.namedWindow('image')
cv2.createTrackbar('Closing','image',0,1,nothing)
cv2.createTrackbar('Opening','image',0,1,nothing)
cv2.createTrackbar('Kernel1','image',1,10,nothing)
cv2.createTrackbar('Kernel2','image',1,10,nothing)
cv2.createTrackbar('ErosionIteration','image',0,10,nothing)
cv2.createTrackbar('DilationIteration','image',0,10,nothing)
cv2.createTrackbar('Distance','image',0,200,nothing)
cv2.createTrackbar('Circle treshold','image',0,50,nothing)
cv2.createTrackbar('Minimum Radius','image',0,200,nothing)
cv2.createTrackbar('Maximum Radius','image',0,200,nothing)
cv2.createTrackbar('hMin','image',0,255,nothing)
cv2.createTrackbar('hMax','image',0,255,nothing)
cv2.createTrackbar('sMin','image',0,255,nothing)
cv2.createTrackbar('sMax','image',0,255,nothing)
cv2.createTrackbar('vMin','image',0,255,nothing)
cv2.createTrackbar('vMax','image',0,255,nothing)
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
while(1):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    hMin = cv2.getTrackbarPos('hMin','image')
    hMax = cv2.getTrackbarPos('hMax','image')
    sMin = cv2.getTrackbarPos('sMin','image')
    sMax = cv2.getTrackbarPos('sMax','image')
    vMin = cv2.getTrackbarPos('vMin','image')
    vMax = cv2.getTrackbarPos('vMax','image')
    Kernel1 = cv2.getTrackbarPos('Kernel1','image')
    Kernel2 = cv2.getTrackbarPos('Kernel2','image')
    ErosionIteration = cv2.getTrackbarPos('ErosionIteration','image')
    DilationIteration = cv2.getTrackbarPos('DilationIteration','image')
    closing = cv2.getTrackbarPos('Closing','image')
    opening = cv2.getTrackbarPos('Opening','image')
    lower=np.array([hMin,sMin,vMin])
    upper=np.array([hMax,sMax,vMax])
    mask = cv2.inRange(ycc, lower, upper)
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
    #We need to blur the mask in order to get rid of the square-shaped contours
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

        d    = cv2.getTrackbarPos('Distance','image')
        t    = cv2.getTrackbarPos('Circle treshold','image')
        rmin = cv2.getTrackbarPos('Minimum Radius','image')
        rmax = cv2.getTrackbarPos('Maximum Radius','image')

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
                cv2.circle(img, (a, b), 1, (0, 0, 255), 2)
    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#

    scale_percent = 30
    width         = int(img.shape[1] * scale_percent / 100)
    height        = int(img.shape[0] * scale_percent / 100)
    dim           = (width, height)
    img           = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow('img',img)
    cv2.imshow('mask',mask)
    cv2.imshow('edge',edges)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()

