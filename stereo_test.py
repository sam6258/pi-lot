import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('tsukuba_left.jpeg',0)
imgR = cv2.imread('tsukuba_right.jpeg',0)

stereo = cv2.StereoBM(0, ndisparities=16, SADWindowSize=15)
disparity = stereo.compute(imgL, imgR)

plt.imshow(disparity,'gray')
plt.show()
