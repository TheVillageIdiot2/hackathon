import cv2
import numpy as np
import pprint
from matplotlib import pyplot as plt

class NoCircleException(RuntimeError):
    pass

def getCircles(img, p1, p2):
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 4, 10, param1=p1, param2=p2, minRadius = 10, maxRadius = 200)
    if circles == None:
        ex = NoCircleException()
        raise ex

    circles = np.uint16(np.around(circles))
    return circles

def getLines(edges, threshold, minLength, maxGap):
    #Args for houghlines are img, lenAcc, radAcc, threshold
    return cv2.HoughLinesP(edges, 2, np.pi/90, threshold, minLength, maxGap)

def getGrayImage(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def getEdgeImage(gray, minVal, maxVal):
    return cv2.Canny(gray, minVal, maxVal, apertureSize = 5)

def renderFoundCircles(cimg, circles, copy=True):
    ret = cimg
    if copy:
        ret = cimg.copy()
    for i in circles[0,:]: 
        cv2.circle(ret,(i[0],i[1]), i[2], (0,255,0), 2)

    return ret

def renderFoundLines(cimg, lines, copy=True):
    ret = cimg
    if copy:
        ret = cimg.copy()
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(ret, (x1,y1), (x2,y2), (0,255,0), 2)
    return ret

video_capture = cv2.VideoCapture(0)
cv2.namedWindow("webcam")

#Tweak canniness
def nothing(x):
    pass
cv2.createTrackbar('MinLen','webcam', 10, 100,nothing)
cv2.createTrackbar('Thresh','webcam', 10, 100,nothing) 
cv2.createTrackbar('MaxGap','webcam', 10, 100,nothing)
cv2.createTrackbar('MinEdge','webcam', 10, 600,nothing)
cv2.createTrackbar('MaxEdge','webcam', 10, 600,nothing)
# create switch for ON/OFF functionality
switch = '0 : Edges \n1 : Lines'
cv2.createTrackbar(switch, 'webcam',0,1,nothing)

framecounter = 0
while(1):
    #Line vals
    minLen = cv2.getTrackbarPos('MinLen','webcam')
    threshold = cv2.getTrackbarPos('Thresh','webcam')
    maxGap = cv2.getTrackbarPos('MaxGap','webcam')

    #Edge vals
    minVal = cv2.getTrackbarPos('MinEdge','webcam')
    maxVal = cv2.getTrackbarPos('MaxEdge','webcam')

    framecounter+=1
    ret, frame = video_capture.read()
    # Our operations on the frame come here
    gray = getGrayImage(frame)
    gray = cv2.GaussianBlur(gray,(9,9),1)
    edges = getEdgeImage(gray, minVal, maxVal)
    lines = getLines(edges, threshold, minLen, maxGap)

    if lines != None:
        renderFoundLines(frame, lines, copy=False)

    # Display the resulting frame
    if cv2.getTrackbarPos(switch, 'webcam') == 0:
        cv2.imshow("webcam", edges)
    else:
        cv2.imshow("webcam",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
