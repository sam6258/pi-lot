import os
import time
import cv2
import threading
import numpy as np
import datetime as dt
import pygame
playing=False
def leftSwervePlay():
	global playing
	if(not playing):
		pygame.mixer.init()
		pygame.mixer.music.load("swerve_left.mp3")
		pygame.mixer.music.play()
		playing=True
		while pygame.mixer.music.get_busy() == True:
			x=1
		playing=False
		pygame.mixer.quit()
def rightSwervePlay():
	global playing
	if(not playing):
		pygame.mixer.init()
		pygame.mixer.music.load("swerve_right.mp3")
		pygame.mixer.music.play()
		playing=True
		while pygame.mixer.music.get_busy() == True:
			continue
		playing=False	
		pygame.mixer.quit()
def rewrite(arg):
	filename= arg
	img = cv2.imread(filename)
	blur = cv2.GaussianBlur(img,(11,11),0)
	#cv2.imwrite('blurred' + str(i) + '.jpg', blur);
	gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	#cv2.imwrite('canny' + str(i) + '.jpg', edges)
	ret,thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_TRUNC)
	#cv2.imwrite('thresh' + str(i) + '.jpg', thresh)

	lines = cv2.HoughLines(thresh,1,np.pi/180,50)
	x1sum = 0
	y1sum = 0
	x2sum = 0
	y2sum = 0
	slopeSum = 0
	
	if lines is not None:
		for rho,theta in lines[0]:
		    a = np.cos(theta)
		    b = np.sin(theta)
		    x0 = a*rho
		    y0 = b*rho
		    x1 = int(x0 + 1000*(-b))
		    y1 = int(y0 + 1000*(a))
		    x2 = int(x0 - 1000*(-b))
		    y2 = int(y0 - 1000*(a))
		    x1sum += x1
		    x2sum += x2
		    y1sum += y1
		    y2sum += y2
		    
		numLines = len(lines[0])
		x1avg = x1sum / numLines     
		x2avg = x2sum / numLines   
		y1avg = y1sum / numLines   
		y2avg = y2sum / numLines   
	if(x2sum-x1sum==0):
		print("0 slope.")
		os.chmod(arg, 777)
		return
	slopeAvg = (y2sum - y1sum) / float(x2sum - x1sum)
	cv2.line(img,(x1avg,y1avg),(x2avg,y2avg),(0,0,255),2)
	cv2.imwrite('houghlines.jpg',img)
	print("slope" + str(slopeAvg))

	if slopeAvg > .15:
		if(playing):
			os.chmod(arg, 777)
			return
		t = threading.Timer(0.00001, rightSwervePlay)
		t.start()
		print("swerving right")
	elif slopeAvg < -.15:
		if(playing):
			os.chmod(arg, 777)
			return
		t = threading.Timer(0.00001, leftSwervePlay)
		t.start()
		print("swerving left")
	os.chmod(arg, 777)

#main method

camera_port=0
camera=cv2.VideoCapture(camera_port)
ret,image = camera.read()
filename = "opencv.png"
os.system("sudo rm " + filename)

while True:
	cv2.imwrite(filename, image)
	os.chmod(filename, 0444)
	t = threading.Timer(0.1, rewrite, [filename])
	t.start()
	ret,image = camera.read()
	while(os.stat(filename).st_mode & 0777 == 0444):
		x = 1
	os.remove("opencv.png")
del(camera)
