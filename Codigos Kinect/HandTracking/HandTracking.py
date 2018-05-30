from freenect import sync_get_depth as get_depth #Utiliza freenect para obtener informacion detallada del Kinect
import numpy as np #Importar NumPy
import cv,cv2 #Utiliza tanto cv como cv2
import pygame #Utiliza pygame

#Las siguientes bibliotecas se usan para la manipulacion del mouse
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

constList = lambda length, val: [val for _ in range(length)] #Da una lista de longitud del tamanio lleno con la variable val. la longitud es una lista y val es dinamica

"""
Esta clase es una forma menos extensa de regionprops () desarrollada por MATLAB. Encuentra propiedades de contornos y los establece en campos
"""
class BlobAnalysis:
    def __init__(self,BW): #Constructor. BW es una imagen binaria en forma de una matriz numpy
        self.BW = BW
        cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) #Encuentra los contornos
        counter = 0
        """
        Estas son listas dinamicas usadas para almacenar variables
        """
        centroid = list()
        cHull = list()
        contours = list()
        cHullArea = list()
        contourArea = list()
        while cs: #Iterar a traves de CvSeq, cs.
            if abs(cv.ContourArea(cs)) > 2000: #Filtra contornos de menos de 2000 pixeles en el area
                contourArea.append(cv.ContourArea(cs)) #Se agrega contourArea con el area de contorno mas reciente
                m = cv.Moments(cs) #Encuentra todos los momentos del contorno filtrado
                try:
                    m10 = int(cv.GetSpatialMoment(m,1,0)) #Momento espacial m10
                    m00 = int(cv.GetSpatialMoment(m,0,0)) #Momento espacial m00
                    m01 = int(cv.GetSpatialMoment(m,0,1)) #Momento espacial m01
                    centroid.append((int(m10/m00), int(m01/m00))) #Aniade la lista de centroides con las coordenadas mas nuevas del centro de gravedad del contorno
                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True) #Encuentra el casco convexo de cs en el tipo CvSeq
                    cHullArea.append(cv.ContourArea(convexHull)) #Agrega el area del casco convexo a la lista cHullArea
                    cHull.append(list(convexHull)) #Agrega la lista del casco convexo a la lista de cHull
                    contours.append(list(cs)) #Agrega la forma de lista del contorno a la lista de contornos
                    counter += 1 #Agrega al mostrador para ver cuantos blobs hay
                except:
                    pass
            cs = cs.h_next() #Pasa al siguiente contorno en cs CvSeq
        """
        A continuacion, las variables se convierten en campos para hacer referencias posteriores
        """
        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea

d = display.Display() #Muestra la referencia para la manipulacion Xlib
def move_mouse(x,y):#Mueve el mouse a (x, y). x y y son enteros
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()

def click_down(button):#Simula un clic hacia abajo. El boton es un int
    Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
    d.sync()

def click_up(button): #Simula un clic arriba. El boton es un int
    Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
    d.sync()

"""
La funcion siguiente es un filtro de base basico. Aniade una lista de cache y toma el valor de eso.
Es util para filtrar datos ruidosos
cache es una lista de flotantes o ints y val es un float o un int
devuelve la media filtrada
"""
def cacheAppendMean(cache, val):
    cache.append(val)
    del cache[0]
    return np.mean(cache)

"""
Esta es la GUI que muestra la imagen con umbral con el casco convexo y los centroides. Utiliza pygame.
El control del mouse tambien se dicta en esta funcion porque los comandos del mouse se actualizan a medida que se actualiza el marco.
"""
def hand_tracker():
    (depth,_) = get_depth()
    cHullAreaCache = constList(5,12000) #Lista de cache en blanco para el area convexa del casco
    areaRatioCache = constList(5,1) #Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
    centroidList = list() #Iniciar lista de centroides
    #Tuplas de colores RGB
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (255,0,255)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    pygame.init() #Inicia pygame
    xSize,ySize = 640,480 #Establece el tamanio de la ventana
    screen = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #crea la superficie principal
    screenFlipped = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) #crea una superficie que se volteara (pantalla de espejo)
    screen.fill(BLACK) #Haz que la ventana sea negra
    done = False #Iterador booleano --> Le dice al Programa cuando terminar
    dummy = False #Muy importante bool para la manipulacion del raton
    while not done:
        screen.fill(BLACK) #Haz que la ventana sea negra
        (depth,_) = get_depth() #Obtenga la profundidad del kinect
        depth = depth.astype(np.float32) #Convierta la profundidad en un float de 32 bits
        _,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV) #Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
        _,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV) #Umbral del fondo para tener un fondo delineado y un primer plano segmentado
        blobData = BlobAnalysis(depthThresh) #Crea el objeto blobData usando la clase BlobAnalysis
        blobDataBack = BlobAnalysis(back) #Crea el objeto blobDataBack usando la clase BlobAnalysis

        for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
            pygame.draw.lines(screen,YELLOW,True,cont,3) #Colorea los limites binarios del fondo amarillo
        for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
            pygame.draw.circle(screen,BLUE,blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
            centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
            pygame.draw.lines(screen,RED,True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
            pygame.draw.lines(screen,GREEN,True,blobData.contours[i],3) #Dibuja el contorno de cada blob
            for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
                pygame.draw.circle(screen,PURPLE,tips,5) #Dibuja los vertices purpura

        """
        #Drawing Loop
        #Esto se basa en las lineas de pantalla de los centroides
        #Posible exploracion en reconocimiento de gestos :D
        for cent in centroidList:
            pygame.draw.circle(screen,BLUE,cent,10)
        """

        pygame.display.set_caption('Kinect Tracking') #Hace que el pie de la pantalla de pygame 'Kinect Tracking'
        del depth #Elimina la profundidad -> problema de memoria opencv
        screenFlipped = pygame.transform.flip(screen,1,0) #Da vuelta la pantalla para que sea una pantalla de espejo
        screen.blit(screenFlipped,(0,0)) #Actualiza la pantalla principal -> pantalla
        pygame.display.flip() #Actualiza todo en la ventana

        #Declaracion de prueba de mouse
        try:
            centroidX = blobData.centroid[0][0]
            centroidY = blobData.centroid[0][1]
            if dummy:
                mousePtr = display.Display().screen().root.query_pointer()._data #Obtiene los atributos actuales del mouse
                dX = centroidX - strX #Encuentra el cambio en X
                dY = strY - centroidY #Encuentra el cambio en Y
                if abs(dX) > 1: #Si hubo un cambio en X mayor que 1 ...
                    mouseX = mousePtr["root_x"] - 2*dX #Nueva coordenada X del mouse
                if abs(dY) > 1: #Si hubo un cambio en Y mayor que 1 ...
                    mouseY = mousePtr["root_y"] - 2*dY #Nueva coordenada Y del mouse
                move_mouse(mouseX,mouseY) #Mueve el mouse a una nueva ubicacion
                strX = centroidX #Hace que la nueva X inicial del raton sea la X actual del centroide mas nuevo
                strY = centroidY #Hace que la nueva Y inicial del raton sea la Y actual del centroide mas nuevo
                cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0]) #Normaliza (elimina el ruido) en el area convexa del casco
                areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea) #Normaliza la relacion entre el area del contorno y el area convexa del casco
                if cArea < 10000 and areaRatio > 0.82: #Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
                    click_down(1)
                else:
                    click_up(1)
            else:
                strX = centroidX #Inicializa la X inicial
                strY = centroidY #Inicializa la Y inicial
                dummy = True #Permite que la funcion continue en la primera parte de la sentencia if
        except: #No puede haber centroides y, por lo tanto, blobData.centroid [0] estara fuera de rango
            dummy = False #Espera un nuevo punto de partida

        for e in pygame.event.get(): #Itera a traves de los eventos actuales
            if e.type is pygame.QUIT: #Si se presiona el boton de cerrar, el bucle while termina
                done = True

try: #Kinect puede no estar enchufado -> errores extranios
    hand_tracker()
except: #Deja que se muestren los errores libfreenect en lugar de los de python
    pass
