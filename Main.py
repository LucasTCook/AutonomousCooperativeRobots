#CS360_Robot, Main.py
#Written By: Lucas Cook and Tyler Carrico

import threading
import time
import socket
import pickle
from copy import deepcopy
from DetectCV import DetectCV
import imutils
import cv2
import numpy as np
from picamera import PiCamera
import scipy.misc
from PIL import Image

def clientListener():
    global sock
    global currentChecklist
    print "---INITIAL CHECKLIST RECIEVED---"
    while True:
        received = sock.recv(1024)
        if (received == "-1"):
            print "---SEARCH COMPLETE---"
            sock.close()
            exit()
        elif (received == "HB"):
            continue
        else:
            print "---REVIEVED CHECKLIST---"
            currentChecklist = pickle.loads(received)
            print currentChecklist

def search():
    global currentChecklist
    camera = PiCamera()
    
    def hsvThresholding(color,loH,loS,loV,upH,upS,upV,imageName):
        #start_time = time.time()
        image = cv2.imread(imageName)
        resized = imutils.resize(image, width=300)
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        
        lower = np.array([loH,loS,loV])
        upper = np.array([upH,upS,upV])

        blur = cv2.GaussianBlur(hsv, (5, 5), 0)


        # mask the HSV image to get only  color searched for
        mask = cv2.inRange(blur, lower, upper)
        res = cv2.bitwise_and(resized,resized, mask= mask)


        #morphological transformations
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.dilate(res, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = cv2.erode(mask, kernel, iterations=2)


        #Create SimpleBlobdetector then create parameters
        params = cv2.SimpleBlobDetector_Params()


        #Circularity parameters
        params.filterByCircularity = True
        params.minCircularity = 0.1


        #Convexity parameters
        params.filterByConvexity = True
        params.minConvexity = 0.5

        detector = cv2.SimpleBlobDetector_create(params)
       
        #Detect blobs using detector and reverse mask
        reversemask=255-mask
        keypoints = detector.detect(reversemask)

        #end_time = time.time()
       # print (end_time - start_time)
        
        if keypoints:
            print "Found "+color+" ball"
            sock.send(color)
        else:
            print "not found"

        
    while True:
        ##Test case: image = 'pink1.jpg'
        time.sleep(.5)
        camera.capture('currentFrame.jpg')
        image = 'currentFrame.jpg'
        print "---search---"
        if currentChecklist[0] == 0:
            yellowImage = deepcopy(image)
            yellow = threading.Thread(name='yellow',target=hsvThresholding, args=('yellow',28,200,175,31,255,215,yellowImage))
            yellow.setDaemon(True)
            yellow.start()
        if currentChecklist[1] == 0:
            pinkImage = deepcopy(image)
            pink = threading.Thread(name='pink',target=hsvThresholding, args=('pink',1,0,50,4,255,255,pinkImage))
            pink.setDaemon(True)
            pink.start()
        if currentChecklist[2] == 0:
            blueImage = deepcopy(image)
            blue = threading.Thread(name='blue',target=hsvThresholding, args=('blue',93,0,50,105,255,255,blueImage))
            blue.setDaemon(True)
            blue.start()

#create a socket and connect to port 8080 on host network
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '161.6.252.200'
port = 8080;
sock.connect((host,port))

cL = threading.Thread(name='clentListener', target=clientListener)
search = threading.Thread(name='search',target=search)
search.setDaemon(True)

cL.start()
time.sleep(.5)
search.start()