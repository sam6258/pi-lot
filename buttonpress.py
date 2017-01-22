import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    input_state = GPIO.input(18)
    input_state2 = GPIO.input(23)
    if input_state == False:
	print('Start Tracking')
	time.sleep(.2)
	os.system("python SwervCode.py &")
    if input_state2 == False:
        print('Stop tracking')
        time.sleep(0.2)
  	os.system("kill $(ps -ax | grep SwervCode.py | grep -v \"grep\" | awk '{print $1}')")
