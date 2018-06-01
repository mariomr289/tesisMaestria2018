#!/usr/bin/python

from freenect import sync_get_depth as get_depth 
import numpy as np
import cv,cv2
import pygame
import sys
import time
import random
import os

#The libaries below are used for mouse manipulation
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

# Gives a list of size length filled with the variable val. length is a list and val is dynamic
constList = lambda length, val: [val for _ in range(length)] 

# Class for bouncing animal image
class BouncingSprite(pygame.sprite.Sprite):
	def __init__(self, image, scrWidth, scrHeight, startW, startH, speed=[2,2]):
		pygame.sprite.Sprite.__init__(self)
		self.speed = speed
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.move_ip(startW if startW == 0 else startW - self.rect.width, startH)
		self.scrWidth = scrWidth
		self.scrHeight = scrHeight

	def update(self):
		if (self.rect.x < 0) or (self.rect.x > self.scrWidth - self.rect.width):
			self.speed[0] *= -1
		if (self.rect.y < 0) or (self.rect.y > self.scrHeight - self.rect.height):
			self.speed[1] *= -1

		self.rect.x = self.rect.x + self.speed[0]
		self.rect.y = self.rect.y + self.speed[1]

	def draw(self, screen):
		screen.blit(self.image, self.rect)

# Class for one menu item (welp, actually we have two menu items, but whatever)
class MenuItem(pygame.font.Font):
	def __init__(self, name, xpos, ypos, width, height, font, fontColor):
		self.name = name
		self.xpos = xpos
		self.ypos = ypos
		self.width = width
		self.height = height
		self.font = font
		self.fontColor = fontColor
		self.label = pygame.transform.flip(self.font.render(self.name, 1, self.fontColor), 1, 0)
		self.itemImage = pygame.image.load("../graphics/menuico.png").convert()
		self.itemImage.set_colorkey((255, 255, 255))

	# Checks, if given coordinates are in object's frame
	def isMouseSelect(self, (xpos, ypos)):
		if(xpos >= self.xpos and xpos <= self.xpos + self.width) and \
			(ypos >= self.ypos and ypos <= self.ypos + self.height):
				return True
		
		return False

	# Applies focus on actual menu item
	def applyFocus(self, screen):
		self.label = pygame.transform.flip(self.font.render(self.name, 1, (255, 0, 0)), 1, 0)
		self.label = pygame.transform.smoothscale(self.label, (self.width + 25, self.height + 25))
		screen.blit(self.itemImage, (self.xpos - 70, self.ypos + 25))

	# Removes focus from actual menu item
	def removeFocus(self):
		self.label = pygame.transform.flip(self.font.render(self.name, 1, self.fontColor), 1, 0)
		self.label = pygame.transform.smoothscale(self.label, (self.width, self.height))

# Class for idle/game menu
class IdleScreen():
	def __init__(self, screen):
		pygame.init()
		self.screen = screen
		self.scrWidth = self.screen.get_rect().width
		self.scrHeight = self.screen.get_rect().height
		self.bgColor = (0, 0, 0)
		self.bgImage = pygame.transform.flip(pygame.image.load("../graphics/mainbg.jpg").convert(), 1, 0)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("LDFComicSans", 40)
		self.fontColor = (255, 255, 255)
		self.menuItems = list()
		self.itemNames = ("New game", "Quit")
		self.menuFuncs = {  "New game" : self.startNewGame,
							"Quit" : sys.exit}
		self.animalImgs = []
		self.animalPictures = ["bison.png", "elephant.png", "giraffe.png", "goat.png", "lion.png",
								"monkey.png", "sheep.png"]
		self.activeFocus = 0
		self.lastActiveFocus = 1

	# Creates array with menu labels ready for drawing
	def buildMenu(self):
		self.items = []

		for index, item in enumerate(self.itemNames):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNames) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItems.append(mi)

	# This should somehow start new game with lol.py script - SHOULD, but it doesn't
	def startNewGame(self):
		print "newgame"
		sys.exit(128)

	# Main loop of this script
	def run(self):
		screenloop = True
		(depth,_) = get_depth()
		# Blank cache list for convex hull area
		cHullAreaCache = constList(5,12000)
		# Blank cache list for the area ratio of contour area to convex hull area
		areaRatioCache = constList(5,1)
		# Initiate centroid list
		centroidList = list()
		screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.RESIZABLE)
		# Iterator boolean --> Tells programw when to terminate
		done = False 
		# Very important bool for mouse manipulation
		dummy = False 
		self.buildMenu()

		while screenloop:
			self.clock.tick(30)
			# Get the depth from the kinect
			(depth,_) = get_depth()  
			old_depth = depth
			depth = cv2.resize(old_depth, (1024, 768))
			# Convert the depth to a 32 bit float
			depth = depth.astype(np.float32)
			# Threshold the depth for a binary image. Thresholded at 600 arbitary units
			_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV) 
			# Threshold the background in order to have an outlined background and segmented foreground
			_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV) 
			# Creates blobData object using BlobAnalysis class
			blobData = BlobAnalysis(depthThresh) 
			# Creates blobDataBack object using BlobAnalysis class
			blobDataBack = BlobAnalysis(back) 
			
			mpos = pygame.mouse.get_pos() 

			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					screenloop = False
				elif e.type == pygame.MOUSEBUTTONDOWN:
					screenloop = self.menuFuncs[self.itemNames[self.activeFocus]]()
					break;

			self.screen.blit(self.bgImage, (0, 0))
			self.floatingPicture()
			self.menuItems[self.activeFocus].applyFocus(self.screen)
			self.menuItems[self.lastActiveFocus].removeFocus()
			
			for item in self.menuItems:
				self.screen.blit(item.label, (item.xpos, item.ypos))

			# 2 lazy 2 do somethin' beautiful and universal
			if mpos[1] > self.scrHeight / 2:
				self.activeFocus = 1
				self.lastActiveFocus = 0
			else:
				self.activeFocus = 0
				self.lastActiveFocus = 1


			#for cont in blobDataBack.contours: #Iterates through contours in the background
			#	pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colors the binary boundaries of the background yellow
			for i in range(blobData.counter): #Iterate from 0 to the number of blobs minus 1
			#	pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Draws a blue circle at each centroid
				centroidList.append(blobData.centroid[i]) #Adds the centroid tuple to the centroidList --> used for drawing
			#	pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Draws the convex hull for each blob
			#	pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Draws the contour of each blob
		
			#	for tips in blobData.cHull[i]: #Iterates through the verticies of the convex hull for each blob
			#		pygame.draw.circle(screen,(255,0,255),tips,5) #Draws the vertices purple

			# Deletes depth --> opencv memory issue
			del depth 
			# Flips the screen so that it is a mirror display
			screenFlipped = pygame.transform.flip(screen,1,0) 
			# Updates the main screen --> screen
			screen.blit(screenFlipped,(0,0))
			# Updates everything on the window
			pygame.display.flip() 
		
			# Mouse Try statement
			try:
				centroidX = blobData.centroid[0][0]
				centroidY = blobData.centroid[0][1]
				if dummy:
					# Gets current mouse attributes
					mousePtr = display.Display().screen().root.query_pointer()._data 
					# Finds the change in X
					dX = centroidX - strX 
					# Finds the change in Y
					dY = strY - centroidY 
					minChange = 3
					# If there was a change in X greater than minChange...
					if abs(dX) > minChange:
						# New X coordinate of mouse
						mouseX = mousePtr["root_x"] - 2*dX 
						if mouseX < 0:
							mouseX = 0
						elif mouseX > self.scrWidth:
							mouseX = self.scrWidth
					# If there was a change in Y greater than minChange...
					if abs(dY) > minChange: 
						# New Y coordinate of mouse
						mouseY = mousePtr["root_y"] - 2*dY 
						if mouseY < 0:
							mouseY = 0
						elif mouseY > self.scrHeight:
							mouseY = self.scrHeight
					print mouseX, mouseY
					# Moves mouse to new location
					move_mouse(mouseX, mouseY)
					# Makes the new starting X of mouse to current X of newest centroid 
					strX = centroidX 
					# Makes the new starting Y of mouse to current Y of newest centroid
					strY = centroidY 
					# Normalizes (gets rid of noise) in the convex hull area
					cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0]) 
					# Normalizes the ratio between the contour area and convex hull area
					areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
					print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
					# Defines what a click down is. Area must be small and the hand must look like a binary circle (nearly)
					if cArea < 25000 and areaRatio > 0.82: 
						click_down(1)
					else:
						click_up(1)
				else:
					# Initializes the starting X
					strX = centroidX 
					# Initializes the starting Y
					strY = centroidY
					# Lets the function continue to the first part of the if statement 
					dummy = True 
			except: 
				# There may be no centroids and therefore blobData.centroid[0] will be out of range
				# Waits for a new starting point
				dummy = False 

	# Handles, creates and updates floating/bouncing animals in menu screen
	def floatingPicture(self):
		self.animalAct = None
		self.animalPos = [[0, 0], [1024, 0]]
		if self.animalImgs == []:
			for i in range(0, 2):
				self.animalAct = self.animalPictures.pop(random.randrange(len(self.animalPictures)))
				self.animalImgs.append(BouncingSprite("../graphics/" + self.animalAct, self.scrWidth, self.scrHeight,
					self.animalPos[i][0], self.animalPos[i][1], [3, 3]))
		else:
			for img in self.animalImgs:
				img.update()

		for img in self.animalImgs:
			img.draw(self.screen)

"""
This class is a less extensive form of regionprops() developed by MATLAB. 
It finds properties of contours and sets them to fields
"""
class BlobAnalysis:
	# Constructor. BW is a binary image in the form of a numpy array
	def __init__(self,BW): 
		self.BW = BW
		# Finds the contours
		cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) 
		counter = 0
		"""
		These are dynamic lists used to store variables
		"""
		centroid = list()
		cHull = list()
		contours = list()
		cHullArea = list()
		contourArea = list()
		# Iterate through the CvSeq, cs.
		while cs: 
			# Filters out contours smaller than 2500 pixels in area
			if abs(cv.ContourArea(cs)) > 2000: 
				# Appends contourArea with newest contour area
				contourArea.append(cv.ContourArea(cs)) 
				# Finds all of the moments of the filtered contour
				m = cv.Moments(cs) 
				try:
					# Spatial moment m10
					m10 = int(cv.GetSpatialMoment(m,1,0)) 
					# Spatial moment m00
					m00 = int(cv.GetSpatialMoment(m,0,0))
					# Spatial moment m01 
					m01 = int(cv.GetSpatialMoment(m,0,1))
					# Appends centroid list with newest coordinates of centroid of contour
					centroid.append((int(m10/m00), int(m01/m00))) 
					# Finds the convex hull of cs in type CvSeq
					convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) 
					# Adds the area of the convex hull to cHullArea list
					cHullArea.append(cv.ContourArea(convexHull))
					# Adds the list form of the convex hull to cHull list
					cHull.append(list(convexHull))
					# Adds the list form of the contour to contours list 
					contours.append(list(cs)) 
					# Adds to the counter to see how many blobs are there
					counter += 1 
				except:
					pass
			# Goes to next contour in cs CvSeq
			cs = cs.h_next() 
		"""
		Below the variables are made into fields for referencing later
		"""
		self.centroid = centroid
		self.counter = counter
		self.cHull = cHull
		self.contours = contours
		self.cHullArea = cHullArea
		self.contourArea = contourArea

# Display reference for Xlib manipulation
d = display.Display()

# Moves the mouse to (x,y). x and y are ints
def move_mouse(x,y):
	print "Moving mouse to:", x, y
	s = d.screen()
	root = s.root
	root.warp_pointer(x,y)
	d.sync()
	
# Simulates a down click. Button is an int
def click_down(button):
	print "GOT CLICK DOWN"
	Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
	d.sync()
	
# Simulates a up click. Button is an int
def click_up(button):
	# print "GOT CLICK UP"
	Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
	d.sync()

"""
The function below is a basic mean filter. It appends a cache list and takes the mean of it.
It is useful for filtering noisy data
cache is a list of floats or ints and val is either a float or an int
it returns the filtered mean
"""
def cacheAppendMean(cache, val):
	cache.append(val)
	del cache[0]
	return np.mean(cache)

"""
This is the GUI that displays the thresholded image with the convex hull and centroids. It uses pygame.
Mouse control is also dictated in this function because the mouse commands are updated as the frame is updated
"""

if __name__ == "__main__":
	screen = pygame.display.set_mode((1024, 768), 0, 32)
	pygame.display.set_caption("ZOO")
	idscr = IdleScreen(screen)
	try: 
		idscr.run()
	except Exception, e:
		print "Something's wrong: %s" % e
		