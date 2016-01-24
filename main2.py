import cv2
import threading
from time import sleep
import pygame
import pygame.midi
import numpy as np
import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray

def nothing(x):
    pass

def testBlobs():
    cv2.namedWindow("win")

    #init pi camera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    sleep(.5)

    #init pygame
    pygame.init()
    pygame.midi.init()

    #Init midi 
    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    midi_out = pygame.midi.Output(port, 0)
    midi_out.set_instrument(0)

    #Made thread reference so it can be shut down later
    playThread = None
    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #Load image
            img = frame.array
            pimg = preprocessImage(img)

            #get dims
            height, width = gimg.shape[:2]

            #Find blobs
            blobs = getBlobs(pimg)
            drawBlobsAsCircles(img, blobs)
            notes = shittyConvertBlobsToNotes(blobs, 10, 72, 83, width, height)

            #Draw image
            cv2.imshow("win", img)

            #Launch thread to play music
            if playThread == None or not playThread.isAlive():
                playThread = threading.Thread(target=playNoteList, args = (notes,midi_out))
                playThread.daemon = True
                playThread.start()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
    finally:
        playThread.join()
        del midi_out
        pygame.midi.quit()
        cv2.destroyAllWindows()

#######################
#Helpers
#######################

def preprocessImage(img):
    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Threshold
    ret, thresh = cv2.threshold(gimg, 127, 255, 0)
    thresh = 255 - thresh

    #Fill holes
    kernel = np.ones((5,5), np.uint8)
    return cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 3)

#Returns a list [(time, note)...] sorted by time of ocurrence
def convertBlobsToNotes(blobs, totalTime):
    for b in blobs:
         pass

#This is lazy as hell, but like, I guess it works in literally PERFECT scenarios
def shittyConvertBlobsToNotes(blobs, totalTime, noteMin, noteMax, imgWidth, imgHeight):
    noteList = []

    for b in blobs:
        time = float(b[0]) /  imgWidth * totalTime
        spectrum = (noteMax-noteMin)
        note = int(noteMax - spectrum * (float(b[1]) /  imgHeight))
       
        noteList.append((time, note)) 

    return sorted(noteList)

def playNoteList(noteList, midi_out):
    print("Going to play notes")
    print(noteList)
    lastTime = 0
    lastNote = -1
    for notetuple in noteList:
        note = notetuple[1]
        time = notetuple[0]

        timeTill = time - lastTime
        print("Sleeping for %i seconds"%timeTill)
        sleep(timeTill)

        print("doot")
        if lastTime != -1:
            midi_out.note_off(lastNote, 127)
        midi_out.note_on(note, 127)
        print("doot")

        lastTime = time
        lastNote = note


def drawBlobsAsCircles(img, blobs):
    for b in blobs:
        x = int(b[0])
        y = int(b[1])
        radius = int((b[2] / np.pi) ** .5)
        cv2.circle(img, (x,y), radius, (0,255,0), -1)

#Returns the coordinate and time-to-erode of all objects in a binary image
#Return form: [(x,y,a),...]
#Warning: expensive as hell
def getBlobs(bimg):
    contours, hierarchy = cv2.findContours(bimg, 1, 2)
    #Change 1,2 later to be non magic

    blobs = []
    if contours == None:
        print("No contours!")
        return blobs
  
    print("%i contours found"%len(contours))
    for cnt in contours:
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        area = cv2.contourArea(cnt)

        blobs.append((cx,cy,area))

    return blobs

testBlobs()
