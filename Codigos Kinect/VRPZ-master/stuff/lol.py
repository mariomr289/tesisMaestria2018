#!/usr/bin/env python

from freenect import sync_get_depth as get_depth #Uses freenect to get depth information from the Kinect
import numpy as np #Imports NumPy
import cv,cv2 #Uses both of cv and cv2
import pygame #Uses pygame
import sys
import socket
import random

smoothing = 5
smoothingAngle = 10
smoothingCriminal = 10
constList = lambda length, val: [val for _ in range(length)] #Gives a list of size length filled with the variable val. length is a list and val is dynamic

score = 0

bangTime = 5
#chance in %
#speed of  food
movechance = 1
#speed of  junk food
movechanceBad = 0.5
#chance of food
movespeed = 6
#chance of junk food
movespeedBad = 12

"""
This class is a less extensive form of regionprops() developed by MATLAB. It finds properties of contours and sets them to fields
"""
class BlobAnalysis:
    def __init__(self,BW): #Constructor. BW is a binary image in the form of a numpy array
        self.BW = BW
        cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) #Finds the contours
        counter = 0
        """
        These are dynamic lists used to store variables
        """
        centroid = list()
        cHull = list()
        contours = list()
        cHullArea = list()
        contourArea = list()
        while cs: #Iterate through the CvSeq, cs.
            if abs(cv.ContourArea(cs)) > 2000: #Filters out contours smaller than 2000 pixels in area
                contourArea.append(cv.ContourArea(cs)) #Appends contourArea with newest contour area
                m = cv.Moments(cs) #Finds all of the moments of the filtered contour
                try:
                    m10 = int(cv.GetSpatialMoment(m,1,0)) #Spatial moment m10
                    m00 = int(cv.GetSpatialMoment(m,0,0)) #Spatial moment m00
                    m01 = int(cv.GetSpatialMoment(m,0,1)) #Spatial moment m01
                    centroid.append((int(m10/m00), int(m01/m00))) #Appends centroid list with newest coordinates of centroid of contour
                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) #Finds the convex hull of cs in type CvSeq
                    cHullArea.append(cv.ContourArea(convexHull)) #Adds the area of the convex hull to cHullArea list
                    cHull.append(list(convexHull)) #Adds the list form of the convex hull to cHull list
                    contours.append(list(cs)) #Adds the list form of the contour to contours list
                    counter += 1 #Adds to the counter to see how many blobs are there
                except:
                    pass
            cs = cs.h_next() #Goes to next contour in cs CvSeq
        """
        Below the variables are made into fields for referencing later
        """
        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea

def distance(x1,y1,x2,y2):
     """
     Calculates distance of two points
     """
     dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

def in_hull(p, hull):
    """
    Test if points in `p` are in `hull`

    `p` should be a `NxK` coordinates of `N` points in `K` dimension
    `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the
    coordinates of `M` points in `K`dimension for which a Delaunay triangulation
    will be computed
    """
    from scipy.spatial import Delaunay
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 5005))
s.setblocking(0)
data =''
address = ''


def hand_tracker():
    level = 1
    movechance = 1
    movechanceBad = 0.5
    movespeed = 6
    movespeedBad = 12
    hasic =0
    (depth,_) = get_depth()
    centroidList = list() #Initiate centroid list
    #RGB Color tuples
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (255,0,255)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    score = 0
    pygame.init() #Initiates pygame
    xSize,ySize = 1024,768 #Sets size of window
    WIDTH,HEIGHT = xSize,ySize
    screen = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #creates main surface
    screenFlipped = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #creates surface that will be flipped (mirror display)

    trex1Img = pygame.image.load('../graphics/trex1.png')
    trex2Img = pygame.image.load('../graphics/trex2.png')
    trex3Img = pygame.image.load('../graphics/trex3.png')
    trexW, trexH = 200, 210
    trexMaxW, trexMaxH = trex1Img.get_size()
    trexCoord = [-200, 300]
    trex = False


    screen.fill(BLACK) #Make the window black
    done = False #Iterator boolean --> Tells programw when to terminate


    # HOLY COW!!
    zbran = sys.argv[1]+'_weapon.png'
    headPic = sys.argv[1]
    scale = 1.0
    imgCow = pygame.image.load('../graphics/' +sys.argv[1]+'.png')
    cowW, cowH = imgCow.get_size()
    imgCow = pygame.transform.scale(imgCow, (int(cowW * scale), int(cowH * scale)))
    smoothVector = list()
    smoothAngle = list()
    smoothCriminal = list()

    movingObject = list()
    movingObjectBad = list()
    maxCont = (0, 1000)
    banged = list()

    imgFood, imgCandy = list(), list()

    for i in range(6):
        imgFood.append('../graphics/food'+str(i) + '.png')

    for i in range(4):
        imgCandy.append('../graphics/candy'+str(i) + '.png')

    wall = pygame.image.load('../graphics/'+sys.argv[1]+'_bg.jpg')
    bangImg = pygame.image.load('../graphics/bang.png')
    accX = 0
    accY = 0
    accZ = 0

    pygame.mixer.init()
    sound = pygame.mixer.Sound('../sound/' + sys.argv[1]+'.wav')
    crunch = pygame.mixer.Sound('../sound/crunch.wav')
    buzzer = pygame.mixer.Sound('../sound/buzzer.wav')
    slash = pygame.mixer.Sound('../sound/slash.wav')
    saber = pygame.mixer.Sound('../sound/saber.wav')
    buzzer.set_volume(1.0)
    crunch.set_volume(1.0)
    slash.set_volume(1.0)
    sound.set_volume(1.0)
    saber.set_volume(1.0)
    sound.play()

    while not done:
        try:
            data,address = s.recvfrom(10000)
            #print "recv:", data, " from:", address
            if data == "ping":
                s.sendto("ready", address)
            if 'ksicht' in data:
                print "Menim ksicht"
                imgCow = pygame.image.load('../graphics/' + data.replace('ksicht:', ''))
                cowW, cowH = imgCow.get_size()
                imgCow = pygame.transform.scale(imgCow, (int(cowW * scale), int(cowH * scale)))
                headPic = data.replace('ksicht:', '').replace('.png','')
                zbran = headPic + '_weapon.png'
                wall = pygame.image.load('../graphics/'+headPic+'_bg.jpg')
                sound.stop()
                sound = pygame.mixer.Sound('../sound/' + data.replace('ksicht:', '').replace('.png','.wav'))
                sound.set_volume(1.0)
                sound.play()

            if 'zbran' in data:
                print "Menim zbran"
                zbran = data.replace('zbran:', '')
            if 'reset' in data:
                score = 0
                level = 1
                movechance = 1
                movechanceBad = 0.5
                movespeed = 6
                movespeedBad = 12
                hasic =0
            if 'bonus' in data:
                if trex:
                    trex = False
                else:
                    trex = True
                    trexW, trexH = 200, 210
                    trexCoord = [-200, 300]
            if ";" in data:
                # Suradnice
                try:
                    accX,accY,accZ = data.split(';')
                except Exception as e:
                    print "Suradnice: ", e


        except Exception as e:
            pass

        hasic +=1

        if hasic % 200 == 0 and level < 5:

            #speed of  food
            movechance *= 1.7
            #speed of  junk food
            movechanceBad *= 1.7
            #chance of food
            movespeed +=0.3
            #chance of junk food
            movespeedBad +=0.3
            level += 1

        #moving object
        if random.randint(0,10000) < movechance*100 and not trex:
            down, up = 1, 5
            if headPic == 'lion' or headPic == 'vader':
                down = 0
            food = random.randint(down,up)
            moveCordY = random.randint(0, 384)
            orientation = random.randint(0,1)
            if orientation == 1:
                movingObject.append([0, moveCordY, food, 1])
            else:
                movingObject.append([1024, moveCordY, food, -1])
        if random.randint(0,10000) < movechanceBad*100 and not trex:
            candy = random.randint(0,3)
            moveCordY = random.randint(0, 384)
            orientation = random.randint(0,1)
            if orientation == 1:
                movingObjectBad.append([0, moveCordY, candy, 1])
            else:
                movingObjectBad.append([1024, moveCordY, candy, -1])

        screen.fill(BLACK) #Make the window black
        screen.blit(wall, (0, 0))

        myfont = pygame.font.SysFont("Comic Sans MS", 90)
        label = myfont.render("Level: "+ str(level)+"       Score: " + str(score), 1, BLACK)
        label = pygame.transform.flip(label,1,0)
        screen.blit(label, (264, 50))

        # TREX BONUS!
        if trex:
            if trexCoord[0] > 240:
                screen.blit(trex3Img, trexCoord)
            else:
                trexCoord[0] += 1
                if trexW < trexMaxW:
                    trexW += 1
                if trexH < trexMaxH:
                    trexH += 1

                if hasic % 17 < 8:
                    trexOut = pygame.transform.scale(trex1Img, (trexW, trexH))
                else:
                    trexOut = pygame.transform.scale(trex2Img, (trexW, trexH))

                screen.blit(trexOut, trexCoord)

        #kiss kissbang bang
        for bang in banged:
            screen.blit(bangImg, (bang[0], bang[1]))
            bang[2] = bang[2] + 1
            if bang[2] > bangTime:
                banged.remove(bang)
                break

        for i in range(len(movingObject)):
            img = pygame.image.load(imgFood[movingObject[i][2]])
            screen.blit(img, (movingObject[i][0], movingObject[i][1]))
            movingObject[i][0] = movingObject[i][0] + movespeed * movingObject[i][3]
            if movingObject[i][0] > 1024 or movingObject[i][0] < 0:
                movingObject.remove(movingObject[i])
                break
        for i in range(len(movingObjectBad)):
            img = pygame.image.load(imgCandy[movingObjectBad[i][2]])
            screen.blit(img, (movingObjectBad[i][0], movingObjectBad[i][1]))
            movingObjectBad[i][0] = movingObjectBad[i][0] +movespeedBad * movingObjectBad[i][3]
            if movingObjectBad[i][0] > 1024 or movingObjectBad[i][0] < 0:
                movingObjectBad.remove(movingObjectBad[i])
                break

        (depth,_) = get_depth() #Get the depth from the kinect
        old_depth = depth
        depth = cv2.resize(old_depth, (1024, 768))
        depth = depth.astype(np.float32) #Convert the depth to a 32 bit float
        _,depthThresh = cv2.threshold(depth, 800, 255, cv2.THRESH_BINARY_INV) #Threshold the depth for a binary image. Thresholded at 600 arbitary units
        _,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV) #Threshold the background in order to have an outlined background and segmented foreground
        blobData = BlobAnalysis(depthThresh) #Creates blobData object using BlobAnalysis class
        blobDataBack = BlobAnalysis(back) #Creates blobDataBack object using BlobAnalysis class

        # Boundaries
        hullBound = []
        for i in range(blobData.counter):
            hullLeft = 1000
            hullRight = 0
            for x,y in blobData.cHull[i]:
                if x < hullLeft:
                    hullLeft = x
                if x > hullRight:
                    hullRight = x
            hullBound.append([hullRight, hullLeft])


        tempCont = []
        for cont in blobDataBack.contours: #Iterates through contours in the background
            pygame.draw.lines(screen,BLACK,True,cont,5) #Colors the binary boundaries of the background yellow

            for xcont,ycont in cont:
                valid = True
                for bound in hullBound:
                    if xcont <= bound[0] and xcont >= bound[1]:
                        # in Hull boundaries
                        valid = False
                if valid:
                    tempCont.append([xcont, ycont])




        maxCont = (0, 1000)

        #print tempCont
        for coords in tempCont:
            #print coords
            if coords[1] < maxCont[1]:
                maxCont = coords

        smoothVector.append(maxCont)
        if len(smoothVector) > smoothing:
            smoothVector.pop(0)

        mean = [0, 0]
        for val in smoothVector:
            mean[0] = mean[0]+val[0]
            mean[1] = mean[1]+val[1]

        mean[0]=int(mean[0]/len(smoothVector))
        mean[1]=int(mean[1]/len(smoothVector))

        xcord = mean[0] - (imgCow.get_rect().size[0]/2)
        ycord = mean[1] - (imgCow.get_rect().size[1]/2)

        headCords = [xcord, ycord+75]
        # Hlava?
        screen.blit(imgCow, headCords)

        for i in range(len(movingObject)):
            if distance(movingObject[i][0], movingObject[i][1], headCords[0], headCords[1]) < 75:
                movingObject.remove(movingObject[i])
                crunch.play()
                score += 10
                break

        for i in range(len(movingObjectBad)):
            if distance(movingObjectBad[i][0], movingObjectBad[i][1], headCords[0], headCords[1]) < 75:
                movingObjectBad.remove(movingObjectBad[i])
                buzzer.play()
                score -=50
                break

        for i in range(blobData.counter): #Iterate from 0 to the number of blobs minus 1

            #pygame.draw.circle(screen,BLUE,blobData.centroid[i],10) #Draws a blue circle at each centroid
            smoothCriminal.append(blobData.centroid[i])

            if len(smoothCriminal) > smoothingCriminal:
                smoothCriminal.pop(0)

            mean = [0, 0]
            for val in smoothCriminal:
                mean[0] = mean[0]+val[0]
                mean[1] = mean[1]+val[1]

            mean[0]=int(mean[0]/len(smoothCriminal))
            mean[1]=int(mean[1]/len(smoothCriminal))

            centroidList.append((mean[0], mean[1])) #Adds the centroid tuple to the centroidList --> used for drawing
            #pygame.draw.lines(screen,RED,True,blobData.cHull[i],3) #Draws the convex hull for each blob
            #pygame.draw.lines(screen,GREEN,True,blobData.contours[i],3) #Draws the contour of each blob
            mostLeft = (xSize, 0)
            mostRight = (0, 0)

            # Body ruky
            for tips in blobData.cHull[i]: #Iterates through the verticies of the convex hull for each blob
                #pygame.draw.circle(screen,PURPLE,tips,5) #Draws the vertices purple

                if tips[0] < mostLeft[0]:
                    mostLeft = tips
                if tips[0] > mostRight[0]:
                    mostRight = tips


            if blobData.centroid[i][0] > headCords[0]:
                #continue
                pass

            # Centrum ruky
            #pygame.draw.circle(screen,WHITE,blobData.centroid[i],10)
            # pygame.draw.circle(screen,RED,(blobData.centroid[i][0]-80,blobData.centroid[i][1]-80),10)

            imgZbran = pygame.image.load('../graphics/' + zbran)
            zbranW, zbranH = imgZbran.get_size()

            # Hit trex?
            if trex:
                if (blobData.centroid[i][0] - int(zbranW/2)) < (trexCoord[0] + trexMaxW/2) and (blobData.centroid[i][1] > trexCoord[1]):
                    screen.blit(bangImg, (trexCoord[0] + trexMaxW/2, blobData.centroid[i][1] - 150))
                    if 'vader' in zbran:
                        saber.play()
                    else:
                        print zbran
                        slash.play()



            #old_center = imgZbran.get_rect().center
            #imgZbran = pygame.transform.rotate(imgZbran, (float(accX) + 90) * -1)
            #imgZbran = pygame.transform.rotate(imgZbran, tmp)
            angle = 180 - (float(accX))



            smoothAngle.append(angle)
            if len(smoothAngle) > smoothingAngle:
                smoothAngle.pop(0)

            meanAngle = 0
            for val in smoothAngle:
                meanAngle = meanAngle+val

            meanAngle=int(meanAngle/len(smoothAngle))

            imgZbran = rot_center(imgZbran, meanAngle)
            #imgZbran.get_rect().center = old_center

            screen.blit(imgZbran, (blobData.centroid[i][0] - int(zbranW/2), blobData.centroid[i][1] - int(zbranH/2)))
            if 'sheep' not in zbran:
                for brick in range(len(movingObjectBad)):
                    if distance(movingObjectBad[brick][0], movingObjectBad[brick][1], blobData.centroid[i][0]-80, blobData.centroid[i][1]-80) < 150:
                        print zbran
                        if 'vader' in zbran:
                            saber.play()
                        else:
                            print zbran
                            slash.play()
                        banged.append([movingObjectBad[brick][0], movingObjectBad[brick][1], 0])
                        movingObjectBad.remove(movingObjectBad[brick])
                        break

        pygame.display.set_caption('ZOO') #Makes the caption of the pygame screen 'Kinect Tracking'
        del depth #Deletes depth --> opencv memory issue
        screenFlipped = pygame.transform.flip(screen,1,0) #Flips the screen so that it is a mirror display
        screen.blit(screenFlipped,(0,0)) #Updates the main screen --> screen
        pygame.display.flip() #Updates everything on the window


        for e in pygame.event.get(): #Itertates through current events
            if e.type is pygame.QUIT: #If the close button is pressed, the while loop ends
                done = True

try: #Kinect may not be plugged in --> weird erros
    #hand_tracker()
    pass
except: #Lets the libfreenect errors be shown instead of python ones
    pass

hand_tracker()
