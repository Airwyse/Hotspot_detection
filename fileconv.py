import cv2 
import numpy as np
from datetime import datetime
import time
import os

#Extract Metadata
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from exif_extract import *

inum  = 480
lnum  = 612


for i in range(inum, lnum):

	image = 'DJI_0{}.JPG'.format(i)
	img   = cv2.imread(image)
    #Metadata
############################################################################################################
	exif       = get_exif(image)
	labeled    = get_labeled_exif(exif)
	geotags    = get_geotagging(exif)
	imgcenter  = get_coordinates(geotags)
	dateatime   = get_date_time(labeled)
	spatialres = get_spatial_resolution(labeled)
############################################################################################################

	pt     = datetime.strptime(dateatime,'%Y:%m:%d %H:%M:%S')
	minute = pt.hour*60 + pt.minute

	if (minute < 800):
		os.rename(image, 'hole1_img{}.JPG'.format(i)) 

	elif (minute < 817):
		os.rename(image, 'hole2_img{}.JPG'.format(i))

	elif (minute < 830):
		os.rename(image, 'hole3_img{}.JPG'.format(i))

	elif (minute < 860):
		os.rename(image, 'hole6_img{}.JPG'.format(i))

	elif (minute < 870):
		os.rename(image, 'hole7_img{}.JPG'.format(i))

	elif (minute < 885):
		os.rename(image, 'hole8_img{}.JPG'.format(i))

	elif (minute < 900):
		os.rename(image, 'hole9_img{}.JPG'.format(i))

	