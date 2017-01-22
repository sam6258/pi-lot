import RPi.GPIO as GPIO
import time
import os
import cv2
import threading
import numpy as np
import datetime as dt
import pygame

def rewrite(arg):
	f = open('log', 'a')
	n1=dt.datetime.now()
	filename= arg
	print("Before IMREAD in process")
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
	print("Before line iteration")
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
		    #if x2 != x1:
			#print "x1: %d y1: %d x2: %d y2: %d slope: %f" % (x1, y1, x2, y2, (y2 - y1) / float(x2 - x1))
		    #else:
			#print("Vertical line")
		    
		numLines = len(lines[0])
		x1avg = x1sum / numLines     
		x2avg = x2sum / numLines   
		y1avg = y1sum / numLines   
		y2avg = y2sum / numLines   
	if(x2sum-x1sum==0):
		print("0 slope.")
		f.write("0 slope for " + str(arg) +"\n")
		return
	slopeAvg = (y2sum - y1sum) / float(x2sum - x1sum)
	cv2.line(img,(x1avg,y1avg),(x2avg,y2avg),(0,0,255),2)
	cv2.imwrite('houghlines' + arg + '.jpg',img)
	
	f.write("Avg Slope for " + arg + ": " + str(slopeAvg)+"\n")
	#print "x1avg: %f y1avg: %f x2avg: %f y2avg: %f slopeavg: %f" % (x1sum / float(numLines), y1sum / float(numLines), x2sum / float(numLines), y2sum / float(numLines), slopeSum / float(numLines))


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
counter=0
while True:
    input_state = GPIO.input(18)
    input_state2 = GPIO.input(23)
    if input_state == False:
        #print('Start tracking')
        #time.sleep(0.2)
	#os.system("python SwervCode.py &")
	camera_port=0
	camera=cv2.VideoCapture(camera_port)
	ret,image = camera.read()
	filename = "opencv" + str(counter) + ".png"
	cv2.imwrite(filename, image)
	t = threading.Timer(0.1, rewrite, [filename])
	t.start()
	ret,image = camera.read()
	counter+=1
    if input_state2 == False:
        print('Stop tracking')
        time.sleep(0.2)
  	os.system("kill $(ps -ax | grep SwervCode.py | grep -v \"grep\" | awk '{print $1}')")
