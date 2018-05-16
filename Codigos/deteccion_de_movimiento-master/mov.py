import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3,320)
cap.set(4,240)
_, prev = cap.read()
prevG = cv2.cvtColor(prev, cv2.COLOR_RGB2GRAY)
kernel = np.ones((5,5),np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
PrevCen = np.array([0,0])
while True:
	_, next = cap.read()
	nextG = cv2.cvtColor(next, cv2.COLOR_RGB2GRAY)
	flow = np.array(abs(np.array(nextG,np.float32) - np.array(prevG,np.float32)), np.uint8)
	cv2.imshow('flow',flow)

	rang = cv2.inRange(flow, 20,255)
	cv2.imshow('rang',rang)
	opening = cv2.morphologyEx(rang, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
	cv2.imshow('closing',closing)

	_,contours, _ = cv2.findContours(closing, 1, 2)

	M = [0,0]
	n = 0

	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		if w>15 and h>15 and w<200 and h<200:
			M[0] += x + float(w)/2.
			M[1] += y + float(h)/2.
			n += 1

	if M[0]!=0 and M[0]!=0:
		M = np.array(M)
		NewCen = PrevCen + 0.9*(M-PrevCen)
		cntX = int(NewCen[0]/n)
		cntY = int(NewCen[1]/n)
		cv2.circle(next, (cntX, cntY), 5, (130,50,200),-1)
		cv2.putText(next, str(cntX)+','+str(cntY),(cntX+10,cntY+10),font, 1, (130,50,200))
		PrevCen = NewCen

	prevG = nextG

	cv2.imshow('next',next)
	k =cv2.waitKey(1) & 0xFF
	if k == 27: break

cap.release()
cv2.destroyAllWindows()
