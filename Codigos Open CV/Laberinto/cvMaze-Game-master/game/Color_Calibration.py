import numpy as np
import imutils
import cv2
from opencvFunc import *

windowName = "Colour Calibration"
barNames = ["Hue Max", "Hue Min", "Sat Max", "Sat Min", "Value Max", "Value Min"]
maxV = [180, 180, 255, 255, 255, 255]
lowerBound = [79, 116, 176]
upperBound = [114, 255, 255]
	
def trackbarEvent(foo):
	for i in range(6):
		if i % 2 == 0:
			upperBound[i/2] = cv2.getTrackbarPos(barNames[i], windowName)
		else:
			lowerBound[(i-1)/2] = cv2.getTrackbarPos(barNames[i], windowName)


cv2.namedWindow(windowName)

for i in range(6):
	if i % 2 == 0:
		cv2.createTrackbar(barNames[i], windowName, upperBound[i/2], maxV[i], trackbarEvent)
	else:	
		cv2.createTrackbar(barNames[i], windowName, lowerBound[(i-1)/2], maxV[i], trackbarEvent)

capture = cv2.VideoCapture(0)

while True:

	(captured, frame) = capture.read()

	mask = processFrame(frame, 640, tuple(upperBound), tuple(lowerBound))

	cv2.imshow(windowName, mask)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		print(tuple(lowerBound))
		print(tuple(upperBound))
		break
 
capture.release()
cv2.destroyAllWindows()