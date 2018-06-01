import freenect
import cv2
import numpy as np
 
"""
Toma un mapa de profundidad del sensor Kinect y crea una imagen a partir de el.
"""
def getDepthMap():	
	depth, timestamp = freenect.sync_get_depth()
 
	np.clip(depth, 0, 2**10 - 1, depth)
	depth >>= 2
	depth = depth.astype(np.uint8)
 
	return depth
 
while True:
	depth = getDepthMap()
 
	blur = cv2.GaussianBlur(depth, (5, 5), 0)
 
	cv2.imshow('image', blur)
	cv2.waitKey(10)
