import cv2
import numpy as np
#import datetime as dt
#n1=dt.datetime.now()
for i in range(13, 38):

    img = cv2.imread('images/opencv' + str(i) + '.png')
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
    print("Image " + str(i))
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
        slopeAvg = (y2sum - y1sum) / float(x2sum - x1sum)
        #print "x1avg: %f y1avg: %f x2avg: %f y2avg: %f slopeavg: %f" % (x1sum / float(numLines), y1sum / float(numLines), x2sum / float(numLines), y2sum / float(numLines), slopeSum / float(numLines))
        #cv2.line(img,(x1avg,y1avg),(x2avg,y2avg),(0,0,255),2)
    #cv2.imwrite('houghlines' + str(i) + '.jpg',img)
        print(slopeAvg)

        if slopeAvg < -.5:
            print("swerving right")
        elif slopeAvg > .5:
            print("swerving left")
#n2=dt.datetime.now()
#print("timing: " + str((n2-n1).microseconds))