import cv2 
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt
import platform
import time
from matplotlib.patches import Circle
import itertools

I = imread('data/10m_hotspot(3).jpg');
I = cat(3, I, I, I);

center = [100, 100];
slope = 1.5;

I(center(1)-1:center(1)+1, center(2)-1:center(2)+1, 1) = 255;

x0 = 123;y0 = 65;
x1 = 12;y1 = 232;
I(y0-1:y0+1, x0-1:x0+1, 2) = 255;I(y0, x0, 1) = 0;I(y0, x0, 3) = 0;
I(y1-1:y1+1, x1-1:x1+1, 2) = 255;I(y1, x1, 1) = 0;I(y1, x1, 3) = 0;


alpha = -atan2(slope, 1);

r = -norm(size(I))/2:0.2:norm(size(I))/2;

x = r*cos(alpha) + center(2);
y = r*sin(alpha) + center(1);

X = x;Y = y;
X((x < 1) | (x > size(I,2)) | (y < 1) | (y > size(I,1))) = [];
Y((x < 1) | (x > size(I,2)) | (y < 1) | (y > size(I,1))) = [];

X = round(X);
Y = round(Y);

R = zeros(size(X)) + 1; 
G = zeros(size(X)) + 2; 
B = zeros(size(X)) + 3; 

rV = I(sub2ind(size(I), Y, X, R)); %Red channel values.
gV = I(sub2ind(size(I), Y, X, G)); %Green channel values.
bV = I(sub2ind(size(I), Y, X, B)); %Blue channel values.

V = (rV == 0) & (gV == 255) & (bV == 0);

I(sub2ind(size(I), Y, X, B)) = 255;

figure;imshow(I)

v0 = find(V, 1, 'last');
v1 = find(V, 1);
greenDot0 = [Y(v0), X(v0)]
greenDot1 = [Y(v1), X(v1)]