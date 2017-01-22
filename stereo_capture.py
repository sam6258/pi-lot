import RPi.GPIO as GPIO
import time
import os
import cv2
import threading
import numpy as np
import datetime as dt
import pygame
import matlab.engine

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
camera_port=0
camera_port2=1
while True:
    input_state = GPIO.input(18)
    input_state2 = GPIO.input(23)
    if input_state == False:
	camera=cv2.VideoCapture(camera_port)
	ret,image = camera.read()
	filename = "stereo_left.png"
	cv2.imwrite(filename, image)
	eng = matlab.engine.start_matlab()
	eng.coleDisparity(nargout=0)
    if input_state2 == False:
	camera=cv2.VideoCapture(camera_port2)
	ret,image = camera.read()
	filename = "stereo_right.png"
	cv2.imwrite(filename, image)
	eng = matlab.engine.start_matlab()
	eng.coleDisparity(nargout=0)
