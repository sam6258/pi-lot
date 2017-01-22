import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('stereo_left.png',0)
imgR = cv2.imread('stereo_right.png',0)

stereo = cv2.StereoBM(0, ndisparities=16, SADWindowSize=31)
img = stereo.compute(imgR, imgL)
h, w = img.shape[:2]
print (str(h) + " " + str(w))
imgWidth = 480
averagingWidth = imgWidth / 4
imgHeight = 640 
averagingHeight = imgHeight / 4
threshold = 160

#gray = cv2.cvtColor(disparity,cv2.COLOR_BGR2GRAY)
#cv2.imwrite('disparity.jpg', gray);

startX = imgWidth / 2 - averagingWidth
startY = imgHeight / 2 - averagingHeight
endX = imgWidth / 2 + averagingWidth
endY = imgHeight / 2 + averagingHeight

sum = 0
for i in range(startX, endX):
	for j in range(startY, endY):
		sum = sum + img[i, j]	

avg = sum / (averagingWidth * averagingHeight)
print(sum)
print(avg)
print(endX)
print(endY)

if(avg > threshold):
	print("WARNING")
