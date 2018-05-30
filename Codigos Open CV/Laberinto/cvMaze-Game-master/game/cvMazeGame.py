
from collections import deque
import numpy as np
import imutils
import cv2
from opencvFunc import *
import time

orangeLower = (0, 120, 130)
orangeUpper= (20, 255, 255)
greenLower = (79, 116, 176)
greenUpper = (114, 255, 255)
whiteUpper = (255,255,255)
whiteLower = (100,100,100)
blueUpper = (255, 0, 0)
blueLower = (100, 0, 0)

windowHeight = 480
windowWidth = 640
numberOfPoints = 32
numberOfMazes = 3
currentMaze = 0
touchedWall = False
finished = False
wallBuffer = 0
pts = deque(maxlen=numberOfPoints)  # Deque containing last 32 point history
counter = 0  # Frame counter
(dX, dY) = (0, 0)  # Velocity of movement in x,y directions
direction = ""
 
capture = cv2.VideoCapture(0)  # Create camera capture object
# Blank image for drawing shapes
mazeData = createMaze(windowHeight, windowWidth, currentMaze)
mazeImage = mazeData[0]
templateContours = mazeData[1]
finishContours = mazeData[2]

#print finishContours

while True:
    # get the current frame
    (captured, frame) = capture.read()
    frame = cv2.flip(frame, 1)
    
    # Image manipulations to draw out single colour
    mask = processFrame(frame, windowWidth, greenUpper, greenLower)
    
    # Test if pointer crossed wall of maze
    # Expensive so only run every 10th frame
    if counter % 10 == 0:

        wallDiff = compareFrames(templateContours, mazeImage, whiteUpper, whiteLower)
        finishDiff = compareFrames(finishContours, mazeImage, blueUpper, blueLower)
        
        # If you hit the wall
        if(wallDiff != 0 and touchedWall is False):
            print("You hit the wall!")
            touchedWall = True
            counter = 0
            pts = deque(maxlen=numberOfPoints)
            cv2.putText(mazeImage, "You Lose!", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
            cv2.imshow("Drawing", mazeImage)

        # If you make it to the finish
        if(finishDiff != 0 and finished is False):
            print("finished!")
            finished = True
            counter = 0
            currentMaze += 1
            if currentMaze == numberOfMazes:
                currentMaze = 0
            pts = deque(maxlen=numberOfPoints)
            cv2.putText(mazeImage, "Finished!", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 5)
            cv2.imshow("Drawing", mazeImage)

    # Couple seconds to get ready after reset
    if counter < 100 and (touchedWall is True or finished is True):

        text = ["Rst", "3..", "2..", "1.."]
        if finished == True:
            text[0] = "Nxt"

        i = counter/20
        iF = counter/float(20)
        if i == iF and i != 0:
            cv2.putText(mazeImage, text[i-1], (150+i*80, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

    # Buffer for resets so old frames don't screw up new images       
    if counter >= 100 and (touchedWall is True or finished is True):
        touchedWall = False
        finished = False
        mazeData = createMaze(windowHeight, windowWidth, currentMaze)
        mazeImage = mazeData[0]
        templateContours = mazeData[1]
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    circle = findCenter(mask)
    center = circle[0]
    radius = circle[1]
 
        # only proceed if the radius meets a minimum size
    if radius > 10 and (touchedWall is False and finished is False):
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, center, int(radius), (0, 0, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        pts.appendleft(center)  # Append x,y coords of center

        # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them

        if pts[i - 1] is None or pts[i] is None:
            continue
 
        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 10 and i == 1 and len(pts) > 22:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[0][0] - pts[22][0]
            dY = pts[0][1] - pts[22][1]
            

        # Write buffer lines
        cv2.line(mazeImage, pts[i - 1], pts[i], (0, 255, 0), 10)
 
 
    # show the frame to the screen and increment the frame counter
    cv2.imshow("Pyctionary", frame)
    cv2.imshow("Drawing", mazeImage)

    key = cv2.waitKey(1) & 0xFF
    counter += 1
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
capture.release()
cv2.destroyAllWindows()