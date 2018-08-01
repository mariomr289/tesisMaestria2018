#!/usr/bin/python
# -*- encoding: utf-8 -*-

from freenect import sync_get_depth as get_depth
import numpy as np
import cv
import cv2
import pygame
import sys
from pygame.locals import *
import time
import random
import os

# Importar libreria de números aleatorios
from random import randint

# Las siguientes bibliotecas se usan para la manipulación del mouse
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

# Importar las Clases del Juego Izquierda Derecha
from Clases import Jugador
from Clases import Gallina
# Importar las Clases del Juego  Arriba y Abajo
from Clases import Pez
from Clases import Obstaculo
# Importar la Clase de la Animacion Inicial de los Animales
from Clases import BouncingSprite
# Importar la Clase para crear el Menu
from Clases import MenuItem
# Importar las Clases del Juego Laberinto
from Clases import Player
# Importar la Clase para crear el Puntaje
from Clases import Puntaje
# Importar las Clases del Juego Laberinto TomYJerry
from Clases import mapa
from Clases import Raton
from Clases import Gato

# Da una lista de longitud del tamanio lleno con la variable val la longitud es una lista y val es dinamica
constList = lambda length, val: [val for _ in range(length)]
# Variable Auxiliar para crear el menu
done = False
# Variables para generar las imagenes
animales = False
movimiento = False
# Variable para seleccionar que boton Seleciono (izquierda o derecha)
identidad = None
# Lista de Enemigos del Juego de IzqDerecha
listaEnemigo = []
# lista de Obstaculos del Juego Arriba Abajo
listaObstaculos = []
# Imagen del Queso
imagenQueso = 'Imagenes/q.png'

# Clase para el menu inactivo / juego
class IdleScreen():
	def __init__(self, screen):
		pygame.init()
		self.screen = screen
		self.scrWidth = self.screen.get_rect().width
		self.scrHeight = self.screen.get_rect().height
		self.bgColor = (0, 0, 0)
		self.bgImage = pygame.transform.flip(pygame.image.load("Imagenes/FondoGranja2.jpg").convert(), 1, 0)
		self.bgImageArriba = pygame.transform.flip(pygame.image.load("Imagenes/FondoMarino.jpg").convert(), 1, 0)
		self.bgImageLaberinto = pygame.transform.flip(pygame.image.load("Imagenes/FondoJuego.jpg").convert(), 1, 0)
		self.bgImageIntro = pygame.transform.flip(pygame.image.load("Imagenes/FondoIntroduccion.jpg").convert(), 1, 0)
		self.bgImageMenuJuegos = pygame.transform.flip(pygame.image.load("Imagenes/MenuJuegos.jpg").convert(), 1, 0)
		self.bgImageFinJuego = pygame.transform.flip(pygame.image.load("Imagenes/MenuJuegos.jpg").convert(), 1, 0)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("gaban", 60)
		self.fontPuntaje = pygame.font.SysFont("Answer", 50)
		self.fontFinJuego = pygame.font.SysFont("RicksAmericanNF", 60)
		self.fontColor = (16, 4, 130)
		self.menuItems = list()
		self.menuItemsArriba = list()
		self.menuItemsLaberinto = list()
		self.menuItemsIntro = list()
		self.menuItemsMenuJuegos = list()
		self.menuItemsFinJuego = list()
		self.itemNames = ("Derecha", "Izquierda")
		self.menuFuncs = { 	"Derecha" : self.ClickDerecho,
							"Izquierda" : self.ClickIzquierdo}
		self.itemNamesArriba = ("Arriba", "Abajo")
		self.menuFuncsArriba = {"Arriba" : self.ClickArriba,
							"Abajo" : self.ClickAbajo}
		self.itemNamesIntro = ("Entrar", "Salir")
		self.menuFuncsIntro = {"Entrar" : self.ClickEntrar,
							"Salir" : self.ClickSalir}
		self.itemNamesMenuJuegos = ("Primero", "Segundo", "Tercero", "Cuarto")
		self.menuFuncsMenuJuegos = {"Primero" : self.ClickPrimerJuego,
							"Segundo" : self.ClickSegundoJuego,
							"Tercero" : self.ClickTercerJuego,
							"Cuarto" : self.ClickCuartoJuego}
		self.itemNamesFinJuego = ("Reiniciar Juego", "Menu Juegos", "Salir")
		self.menuFuncsFinJuego = {"Reiniciar Juego" : self.ClickReiniciar,
							"Menu Juegos" : self.ClickRegresar,
							"Salir" : self.ClickSalir}
		self.itemNamesLaberinto = ("Arriba", "Abajo", "Derecha", "Izquierda")
		self.menuFuncsLaberinto = {"Arriba" : self.ClickArriba,
							"Abajo" : self.ClickAbajo,
							"Derecha" : self.ClickDerecho,
							"Izquierda" : self.ClickIzquierdo}
		self.animalImgs = []
		self.animalPictures = ["bison.png", "elephant.png", "giraffe.png", "goat.png", "lion.png",
								"monkey.png", "sheep.png"]
		self.activeFocus = 0
		self.lastActiveFocus = 1
		self.secondActiveFocus = 2
		self.thirdActiveFocus = 3

	# Crea el menu de los Botones de la Interfaz del Juego Izquierda y Derecha
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

	# Crea el menu de los Botones de la Interfaz de Introduccion
	def buildMenuIntro(self):
		self.items = []

		for index, item in enumerate(self.itemNamesIntro):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesIntro) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsIntro.append(mi)

	# Crea el menu de los Botones de la Interfaz del Juego Arriba y Abajo
	def buildMenuArriba(self):
		self.items = []

		for index, item in enumerate(self.itemNamesArriba):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesArriba) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsArriba.append(mi)

	# Crea el menu de los Botones de la Interfaz del Memu de los Juegos
	def buildMenuJuegos(self):
		self.items = []

		for index, item in enumerate(self.itemNamesMenuJuegos):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesMenuJuegos) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsMenuJuegos.append(mi)

	# Crea el menu de los Botones de la Interfaz de Fin del Juego
	def buildFinJuego(self):
		self.items = []

		for index, item in enumerate(self.itemNamesFinJuego):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesFinJuego) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsFinJuego.append(mi)

	# Crea el menu de los Botones de la Interfaz de Introduccion
	def buildMenuLaberinto(self):
		self.items = []

		for index, item in enumerate(self.itemNamesLaberinto):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesLaberinto) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsLaberinto.append(mi)

	# Boton de entrar de la Pantalla de Introduccion
	def ClickEntrar(self):
		global done
		done = False
		self.MenuJuegos()

	# Boton de Salir de la Pantalla de Introduccion
	def ClickSalir(self):
		global done
		done = False
		print "SALIR"
		#sys.exit(128)

	# Boton de Reiniciar los VideoJuegos
	def ClickReiniciar(self):
		global done
		done = False
		print "REINICIAR"

	# Boton de Regresar al Menu de los Juegos
	def ClickRegresar(self):
		global done
		done = False
		print "REGRESAR"

	# Boton de Ingreso al Primer Juego
	def ClickPrimerJuego(self):
		global done
		done = False
		print "Primer Juego"
		self.JuegoDerIzq()

	# Boton de Ingreso al Segundo Juego
	def ClickSegundoJuego(self):
		global done
		done = False
		print "Segundo Juego"
		self.JuegoArriAba()

	# Boton de Ingreso al Tercer Juego
	def ClickTercerJuego(self):
		global done
		done = False
		print "Tercer Juego"
		self.JuegoLaberinto()

	# Boton de Ingreso al Cuarto Juego
	def ClickCuartoJuego(self):
		global done
		done = False
		print "Cuarto Juego"
		self.JuegoLaberintoTomJerry()

	# Menu del Juego Derecha e Izquierda
	def ClickDerecho(self):
		global done
		global identidad
		print "DERECHA"
		done = True
		identidad = "derecha"

	def ClickIzquierdo(self):
		global done
		#global movimiento
		global identidad
		print "IZQUIERDA"
		done = True
		identidad = "izquierda"

	# Menus del Juego Arriba y Abajo
	def ClickArriba(self):
		global done
		global identidad
		print "ARRIBA"
		done = True
		identidad = "arriba"

	def ClickAbajo(self):
		global done
		global identidad
		print "ABAJO"
		done = True
		identidad = "abajo"

	#Funcion que detiene todo en el Juego Izquierda Derecha
	def detenerTodo(self):
		for enemigo in listaEnemigo:
			for disparo in enemigo.listaDisparo:
				enemigo.listaDisparo.remove(disparo)

			enemigo.conquista = True

	# Funcion que detiene todo en el Juego Arriba Abajo
	def detenerTodoArrAba(self):
		for ObstaculoEne in listaObstaculos:
			ObstaculoEne.conquista = True

	# Funcion para cargar los enemigos
	def cargarEnemigos(self):
	    #posx = 100
	    #for x in range(1, 5):
	    #    enemigo = Invasor(posx,100,40,'Imagenes/GallinaTrans.png', 'Imagenes/GallinaTrans.png')
	    #    listaEnemigo.append(enemigo)
	    #    posx = posx + 200
	    posx = 470
	    for x in range(1, 2):
	        enemigo = Gallina.Gallinita(posx,80,460,'Imagenes/GallinaTrans.png', 'Imagenes/GallinaTransB.png')
	        listaEnemigo.append(enemigo)
	        posx = posx + 380

	    #posx = 100
	    #for x in range(1, 5):
	    #    enemigo = Invasor(posx,-100,40,'Imagenes/GallinaTrans.png', 'Imagenes/GallinaTrans.png')
	    #    listaEnemigo.append(enemigo)
	    #    posx = posx + 200

	# Funcion para cargar los Obstaculos del Juego Arriba Abajo
	def cargarObstaculos(self):
		posx = -1000
		for x in range(1,7):
			valor = np.random.randint(2, size=1)
			if valor == 1:
				# posicion Abajo de los Obstaculos
				posy = np.random.randint(0,100)
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/top.png', 'Imagenes/top.png')
				listaObstaculos.append(ObstaculoEne)
				posy = posy + 700
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/bottom.png', 'Imagenes/bottom.png')
				listaObstaculos.append(ObstaculoEne)
			else:
				# posicion Arriba de los Obstaculos
				posy = -300
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/top.png', 'Imagenes/top.png')
				listaObstaculos.append(ObstaculoEne)
				posy = 400
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/bottom.png', 'Imagenes/bottom.png')
				listaObstaculos.append(ObstaculoEne)
			posx = posx + 300

	# Juego de La Galina y los Huevos (Derecha e Izquierda)
	def JuegoDerIzq(self):
		global done
		global identidad
		screenloop = True
		(depth,_) = get_depth()
		# Lista de cache en blanco para el area convexa del casco
		cHullAreaCache = constList(5,12000)
		# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
		areaRatioCache = constList(5,1)
		# Iniciar lista de centroides
		centroidList = list()
		screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
		# Iterator boolean -> Indica a programa cuando finalizar
		# Muy importante bool para la manipulacion del raton
		dummy = False
		# Cargar sonido principal
		pygame.mixer.music.load('Sonidos/DonkeyKongCountry3-JangleBells.mp3')
		pygame.mixer.music.play(3)
		# Cargar la Palaba de Fin del Juego
		#Texto = pygame.transform.flip(self.font.render("Fin del Juego", 1, (255, 14, 0)), 1, 0)
		# Instancia del Objeto Nave Espacial
		jugador = Jugador.NenaCanasta(self.scrWidth,self.scrHeight)
		# Instancia del objeto Invasor
		#enemigo = Invasor(100,100)
		self.cargarEnemigos()
		# Instancia del Objeto Puntaje
		puntos = Puntaje.Score(self.fontPuntaje, (900, 50))
		# Instancia del Objeto Proyectil para el Jugador
		# DemoProyectil = Proyectil(self.scrWidth/2,self.scrHeight-80,"../Imagenes/bala.png", True)
		# Instancia del Objeto Proyectil para el enemigo
		# ProyectilInvasor = Proyectil(self.scrWidth/4,self.scrHeight-700,"../Imagenes/disparob.jpg", False)
		# Verificar si un jugador gano o perdio
		enJuego = True
		# Construye el Menu Principal si done = False
		if not done:
			self.buildMenu()

		while screenloop:
			# Cuando se crea el Proyectil del Jugador se empieza a mover
			# DemoProyectil.trayectoria()
			# Cuando se crea el Proyectil del enemigo se empieza a mover
			# ProyectilInvasor.trayectoria()
			# Regulamos los frames por segundo
			self.clock.tick(30)
			# Obtenemos el tiempo del Juego
			tiempo = pygame.time.get_ticks()/1000
			# Obtenga la profundidad del kinect
			(depth,_) = get_depth()
			old_depth = depth
			depth = cv2.resize(old_depth, (1024, 768))
			# Convierta la profundidad en un flotador de 32 bits
			depth = depth.astype(np.float32)
			# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
			_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
			# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
			_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
			# Crea el objeto blobData usando la clase BlobAnalysis
			blobData = BlobAnalysis(depthThresh)
			# Crea el objeto blobDataBack usando la clase BlobAnalysis
			blobDataBack = BlobAnalysis(back)

			mpos = pygame.mouse.get_pos()

			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					screenloop = False
					done = False
					pygame.mixer.music.fadeout(2000)
					pygame.quit()
					sys.exit()
				# Controlamos que cliqueo con el mouse
				if enJuego == True:
					if e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncs[self.itemNames[self.activeFocus]]()
						# break;
						# Verificar cual de los botones se ha pulsado
						if identidad == "izquierda":
							# Movimiento del Jugador a la Izquierda
							jugador.movimientoIzquierda()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "derecha":
							# Movimiento del Jugador a la Derecha
							jugador.movimientoDerecha()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)

					#elif e.type == pygame.KEYDOWN:
					#	screenloop = True
					#	if e.key == K_s:
					#		x,y = jugador.rect.center
					#		jugador.disparar(x,y)
			# Carga el Fondo del Juego
			self.screen.blit(self.bgImage, (0, 0))
			# Actualizar el Puntaje del Juego
			puntos.update(screen)
			# Se usa para que aparezca las imagenes con la variable animales = True
			#if animales:
				# Cuando se asigna a movimiento = True se empiezan a mover las imagenes
			#	self.floatingPicture(movimiento)

			# Llamada a que se dibuje el Proyectil del jugador
			# DemoProyectil.dibujar(screen)
			# Llamada a que se dibuje el Proyectil del enemigo
			# ProyectilInvasor.dibujar(screen)
			# Llamada al comportamiento del enemigo
			# enemigo.comportamiento(tiempo)
			# llamada a que se dibuje la nave espacial
			jugador.dibujar(screen)
			# Llamada a que se dibuje el enemigo
			# enemigo.dibujar(screen)
			# Verificar los disparos del jugador
			#if len(jugador.listaDisparo) > 0:
			#	for x in jugador.listaDisparo:
			#		x.dibujar(screen)
			#		x.trayectoria()
			#		if x.rect.top < -10:
			#			jugador.listaDisparo.remove(x)
			#		else:
						#Verificar que las balas del jugador dieron a los enemigos
			#			for enemigo in listaEnemigo:
			#				if x.rect.colliderect(enemigo.rect):
			#					listaEnemigo.remove(enemigo)
			#					jugador.listaDisparo.remove(x)

			# Cargar los enemigos
			if len(listaEnemigo) > 0:
				for enemigo in listaEnemigo:
					enemigo.comportamiento(tiempo)
					enemigo.dibujar(screen)
					# Verificar que el enemigo choco con el jugador
					#if enemigo.rect.colliderect(jugador.rect):
					#	pass
						#jugador.destruccion()
						# enJuego = False
						#self.detenerTodo()
					# Verificar los disparos del enemigo
					if len(enemigo.listaDisparo) > 0:
						for x in enemigo.listaDisparo:
							x.dibujar(screen)
							x.trayectoria()
							# Verificar que la bala del enemigo colisiono con el jugador
							if x.rect.colliderect(jugador.rect):
								# Suma al puntaje los huevos que alcanza el jugador
								puntos.score_up()
								#Remueve los huevos de la lista de Disparos
								enemigo.listaDisparo.remove(x)
								enJuego = True
							# Verificar que el huevo paso de la ventana se elimina
							if x.rect.top > 780:
								# Verifica que cuando el huevo pasa del limite el jugador pierde
								enemigo.listaDisparo.remove(x)
								jugador.destruccion()
								enJuego = False
								self.detenerTodo()
							#else:
								# Verificar que cuando un Proyectil enemigo choque con el del jugador los dos se eliminen
								#for disparo in jugador.listaDisparo:
									#if x.rect.colliderect(disparo.rect):
										#jugador.listaDisparo.remove(disparo)
										#enemigo.listaDisparo.remove(x)

			if enJuego == False:
				pygame.mixer.music.fadeout(3000)
				#screen.blit(Texto,(320,200))
				# Llamar a la pantalla de Fin del Juego
				done = False
				self.FinJuego(puntos.score, 1)

			# Se establece en el menu que boton se hizo click
			self.menuItems[self.activeFocus].applyFocus(self.screen)
			self.menuItems[self.lastActiveFocus].removeFocus()

			# Se muestra el menú de Interfaz Derecha, Izquierda
			for item in self.menuItems:
				self.screen.blit(item.label, (item.xpos, item.ypos))

			#  Se ejecuta la acción de click del mouse (Parte principal)
			if mpos[0] > self.scrWidth/ 2:
				self.activeFocus = 0
				self.lastActiveFocus = 1
			else:
				self.activeFocus = 1
				self.lastActiveFocus = 0

			for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
				pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
			for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
				pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
				centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
				pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
				pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

				for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
					pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

			# Elimina la profundidad --> opencv problema de memoria
			del depth
			# Da vuelta la pantalla para que sea una pantalla de espejo
			screenFlipped = pygame.transform.flip(screen,1,0)
			# Actualiza la pantalla principal -> pantalla
			screen.blit(screenFlipped,(0,0))
			# Actualiza todo en la ventana
			pygame.display.flip()

			# Declaracion de prueba de mouse
			try:
				centroidX = blobData.centroid[0][0]
				centroidY = blobData.centroid[0][1]
				if dummy:
					# Obtiene los atributos actuales del mouse
					mousePtr = display.Display().screen().root.query_pointer()._data
					# Encuentra el cambio en X
					dX = centroidX - strX
					# Encuentra el cambio en Y
					dY = strY - centroidY
					minChange = 3
					# Si hubo un cambio en X mayor que minChange ...
					if abs(dX) > minChange:
						# Nueva coordenada X del mouse
						mouseX = mousePtr["root_x"] - 2*dX
						if mouseX < 0:
							mouseX = 0
						elif mouseX > self.scrWidth:
							mouseX = self.scrWidth
					# Si hubo un cambio en Y mayor que minChange ...
					if abs(dY) > minChange:
						# Nueva coordenada Y del mouse
						mouseY = mousePtr["root_y"] - 2*dY
						if mouseY < 0:
							mouseY = 0
						elif mouseY > self.scrHeight:
							mouseY = self.scrHeight
					print mouseX, mouseY
					# Mueve el mouse a una nueva ubicación
					move_mouse(mouseX, mouseY)
					# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
					strX = centroidX
					# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
					strY = centroidY
					# Normaliza (elimina el ruido) en el area convexa del casco
					cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
					# Normaliza la relacion entre el area del contorno y el area convexa del casco
					areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
					print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
					# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
					if cArea < 25000 and areaRatio > 0.82:
						click_down(1)
					else:
						click_up(1)
				else:
					# Inicializa la X inicial
					strX = centroidX
					# Inicializa el inicio Y
					strY = centroidY
					# Permite que la función continue en la primera parte de la sentencia if
					dummy = True
			except:
				# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
				# Espera un nuevo punto de partida
				dummy = False

	# Juego de FlappyBirdy (Arriba y Abajo)
	def JuegoArriAba(self):
		global done
		global identidad
		screenloop = True
		(depth,_) = get_depth()
		# Lista de cache en blanco para el area convexa del casco
		cHullAreaCache = constList(5,12000)
		# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
		areaRatioCache = constList(5,1)
		# Iniciar lista de centroides
		centroidList = list()
		screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
		# Iterator boolean -> Indica a programa cuando finalizar
		# Muy importante bool para la manipulacion del raton
		dummy = False
		# Cargar sonido principal
		pygame.mixer.music.load('Sonidos/DonkeyKongCountry3-JangleBells.mp3')
		pygame.mixer.music.play(3)
		# Cargar la Palaba de Fin del Juego
		Texto = pygame.transform.flip(self.font.render("Fin del Juego", 1, (255, 14, 0)), 1, 0)
		# Instancia del Objeto Nave Espacial
		jugador = Pez.Pececito(self.scrWidth,self.scrHeight)
		# Instancia del objeto Invasor
		#enemigo = Enemigo(100,100)
		self.cargarObstaculos()
		# self.cargarEnemigos()
		# Instancia del Objeto Proyectil para el Jugador
		# DemoProyectil = Proyectil(self.scrWidth/2,self.scrHeight-80,"../Imagenes/bala.png", True)
		# Instancia del Objeto Proyectil para el enemigo
		# ProyectilInvasor = Proyectil(self.scrWidth/4,self.scrHeight-700,"../Imagenes/disparob.jpg", False)
		# Verificar si un jugador gano o perdio
		enJuego = True
		# Construye el Menu Principal si done = False
		if not done:
			self.buildMenuArriba()

		while screenloop:
			# Cuando se crea el Proyectil del Jugador se empieza a mover
			# DemoProyectil.trayectoria()
			# Cuando se crea el Proyectil del enemigo se empieza a mover
			# ProyectilInvasor.trayectoria()
			# Regulamos los frames por segundo
			self.clock.tick(30)
			# Obtenemos el tiempo del Juego
			tiempo = pygame.time.get_ticks()/1000
			# Obtenga la profundidad del kinect
			(depth,_) = get_depth()
			old_depth = depth
			depth = cv2.resize(old_depth, (1024, 768))
			# Convierta la profundidad en un flotador de 32 bits
			depth = depth.astype(np.float32)
			# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
			_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
			# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
			_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
			# Crea el objeto blobData usando la clase BlobAnalysis
			blobData = BlobAnalysis(depthThresh)
			# Crea el objeto blobDataBack usando la clase BlobAnalysis
			blobDataBack = BlobAnalysis(back)

			mpos = pygame.mouse.get_pos()

			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					screenloop = False
					pygame.quit()
					sys.exit()
				# Controlamos que cliqueo con el mouse
				if enJuego == True:
					if e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsArriba[self.itemNamesArriba[self.activeFocus]]()
						# break;
						# Verificar cual de los botones se ha pulsado
						if identidad == "arriba":
							# Movimiento del Jugador a la Izquierda
							jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "abajo":
							# Movimiento del Jugador a la Derecha
							jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)

					#elif e.type == pygame.KEYDOWN:
					#	screenloop = True
					#	if e.key == K_s:
					#		x,y = jugador.rect.center
					#		jugador.disparar(x,y)

			# Carga el Fondo del Juego
			self.screen.blit(self.bgImageArriba, (0, 0))
			# Se usa para que aparezca las imagenes con la variable animales = True
			#if animales:
				# Cuando se asigna a movimiento = True se empiezan a mover las imagenes
			#	self.floatingPicture(movimiento)

			# Llamada a que se dibuje el Proyectil del jugador
			# DemoProyectil.dibujar(screen)
			# Llamada a que se dibuje el Proyectil del enemigo
			# ProyectilInvasor.dibujar(screen)
			# Llamada al comportamiento del enemigo
			#enemigo.comportamiento(tiempo)
			# llamada a que se dibuje la nave espacial
			jugador.dibujar(screen)
			# Llamada a que se dibuje el enemigo
			#enemigo.dibujar(screen)
			# Verificar los disparos del jugador
			#if len(jugador.listaDisparo) > 0:
			#	for x in jugador.listaDisparo:
			#		x.dibujar(screen)
			#		x.trayectoria()
			#		if x.rect.top < -10:
			#			jugador.listaDisparo.remove(x)
			#		else:
						#Verificar que las balas del jugador dieron a los enemigos
			#			for enemigo in listaEnemigo:
			#				if x.rect.colliderect(enemigo.rect):
			#					listaEnemigo.remove(enemigo)
			#					jugador.listaDisparo.remove(x)

			# Cargar los enemigos
			if len(listaObstaculos) > 0:
				for ObstaculoEne in listaObstaculos:
					ObstaculoEne.comportamiento(tiempo)
					ObstaculoEne.dibujar(screen)
					# Verificar que el enemigo choco con el jugador
					if ObstaculoEne.rect.colliderect(jugador.rect):
						jugador.destruccion()
						enJuego = False
						self.detenerTodoArrAba()
					# Verificar los disparos del enemigo
			#		if len(enemigo.listaDisparo) > 0:
			#			for x in enemigo.listaDisparo:
			#				x.dibujar(screen)
			#				x.trayectoria()
							# Verificar si el enemigo colisiono con el jugador
			#				if x.rect.colliderect(jugador.rect):
			#					pass

			#				if x.rect.top > 900:
			#					enemigo.listaDisparo.remove(x)
			#				else:
								# Verificar que cuando un Proyectil enemigo choque con el del jugador los dos se eliminen
			#					for disparo in jugador.listaDisparo:
			#						if x.rect.colliderect(disparo.rect):
			#							jugador.listaDisparo.remove(disparo)
			#							enemigo.listaDisparo.remove(x)

			if enJuego == False:
				pygame.mixer.music.fadeout(3000)
				screen.blit(Texto,(320,200))
				# Llamar a la pantalla de Fin del Juego
				done = False
				self.FinJuego(4, 2)

			# Se establece en el menu que boton se hizo click
			self.menuItemsArriba[self.activeFocus].applyFocus(self.screen)
			self.menuItemsArriba[self.lastActiveFocus].removeFocus()

			# Se muestra el menú de Interfaz Derecha, Izquierda
			for item in self.menuItemsArriba:
				self.screen.blit(item.label, (item.xpos, item.ypos))

			#  Se ejecuta la acción de click del mouse (Parte principal)
			if mpos[1] > self.scrHeight / 2:
				self.activeFocus = 1
				self.lastActiveFocus = 0
			else:
				self.activeFocus = 0
				self.lastActiveFocus = 1

			for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
				pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
			for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
				pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
				centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
				pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
				pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

				for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
					pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

			# Elimina la profundidad --> opencv problema de memoria
			del depth
			# Da vuelta la pantalla para que sea una pantalla de espejo
			screenFlipped = pygame.transform.flip(screen,1,0)
			# Actualiza la pantalla principal -> pantalla
			screen.blit(screenFlipped,(0,0))
			# Actualiza todo en la ventana
			pygame.display.flip()

			# Declaracion de prueba de mouse
			try:
				centroidX = blobData.centroid[0][0]
				centroidY = blobData.centroid[0][1]
				if dummy:
					# Obtiene los atributos actuales del mouse
					mousePtr = display.Display().screen().root.query_pointer()._data
					# Encuentra el cambio en X
					dX = centroidX - strX
					# Encuentra el cambio en Y
					dY = strY - centroidY
					minChange = 3
					# Si hubo un cambio en X mayor que minChange ...
					if abs(dX) > minChange:
						# Nueva coordenada X del mouse
						mouseX = mousePtr["root_x"] - 2*dX
						if mouseX < 0:
							mouseX = 0
						elif mouseX > self.scrWidth:
							mouseX = self.scrWidth
					# Si hubo un cambio en Y mayor que minChange ...
					if abs(dY) > minChange:
						# Nueva coordenada Y del mouse
						mouseY = mousePtr["root_y"] - 2*dY
						if mouseY < 0:
							mouseY = 0
						elif mouseY > self.scrHeight:
							mouseY = self.scrHeight
					print mouseX, mouseY
					# Mueve el mouse a una nueva ubicación
					move_mouse(mouseX, mouseY)
					# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
					strX = centroidX
					# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
					strY = centroidY
					# Normaliza (elimina el ruido) en el area convexa del casco
					cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
					# Normaliza la relacion entre el area del contorno y el area convexa del casco
					areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
					print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
					# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
					if cArea < 25000 and areaRatio > 0.82:
						click_down(1)
					else:
						click_up(1)
				else:
					# Inicializa la X inicial
					strX = centroidX
					# Inicializa el inicio Y
					strY = centroidY
					# Permite que la función continue en la primera parte de la sentencia if
					dummy = True
			except:
				# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
				# Espera un nuevo punto de partida
				dummy = False

	# Juego de Labarinto (Arriba, Abajo, Derecha, Izquierda)
	def JuegoLaberinto(self):
		global done
		global identidad
		screenloop = True
		(depth,_) = get_depth()
		# Lista de cache en blanco para el area convexa del casco
		cHullAreaCache = constList(5,12000)
		# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
		areaRatioCache = constList(5,1)
		# Iniciar lista de centroides
		centroidList = list()
		screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
		# Iterator boolean -> Indica a programa cuando finalizar
		# Muy importante bool para la manipulacion del raton
		dummy = False
		# Cargar sonido principal
		# pygame.mixer.music.load('Sonidos/Intro.mp3')
		# pygame.mixer.music.play(3)
		# Instancia del Objeto Player
		jugador = Player.Kate((self.scrWidth/2,self.scrHeight/2))
		# Instancia del Objeto Nave Espacial
		# jugador = Protagonista(self.scrWidth,self.scrHeight)
		# Instancia del objeto Invasor
		# enemigo = Enemigo(100,100)
		# self.cargarEnemigos()
		# Instancia del Objeto Proyectil para el Jugador
		# DemoProyectil = Proyectil(self.scrWidth/2,self.scrHeight-80,"../Imagenes/bala.png", True)
		# Instancia del Objeto Proyectil para el enemigo
		# ProyectilInvasor = Proyectil(self.scrWidth/4,self.scrHeight-700,"../Imagenes/disparob.jpg", False)
		# Verificar si un jugador gano o perdio
		enJuego = True
		# Construye el Menu Principal si done = False
		if not done:
			self.buildMenuLaberinto()

		while screenloop:
			# Cuando se crea el Proyectil del Jugador se empieza a mover
			# DemoProyectil.trayectoria()
			# Cuando se crea el Proyectil del enemigo se empieza a mover
			# ProyectilInvasor.trayectoria()
			# Regulamos los frames por segundo
			self.clock.tick(30)
			# Obtenemos el tiempo del Juego
			tiempo = pygame.time.get_ticks()/1000
			# Obtenga la profundidad del kinect
			(depth,_) = get_depth()
			old_depth = depth
			depth = cv2.resize(old_depth, (1024, 768))
			# Convierta la profundidad en un flotador de 32 bits
			depth = depth.astype(np.float32)
			# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
			_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
			# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
			_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
			# Crea el objeto blobData usando la clase BlobAnalysis
			blobData = BlobAnalysis(depthThresh)
			# Crea el objeto blobDataBack usando la clase BlobAnalysis
			blobDataBack = BlobAnalysis(back)

			mpos = pygame.mouse.get_pos()

			for e in pygame.event.get():
				if e.type == pygame.QUIT or(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					screenloop = False
					pygame.quit()
					sys.exit()
				# Controlamos que cliqueo con el mouse
				if enJuego == True:
					if e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsLaberinto[self.itemNamesLaberinto[self.activeFocus]]()
						# break;
						# Verificar cual de los botones se ha pulsado
						if identidad == "arriba":
							jugador.update('up')
							# Movimiento del Jugador a la Izquierda
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "abajo":
							jugador.update('down')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "derecha":
							jugador.update('right')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "izquierda":
							jugador.update('left')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
					if e.type == pygame.MOUSEBUTTONUP:
						screenloop = True
						#opcion = self.menuFuncsLaberinto[self.itemNamesLaberinto[self.activeFocus]]()
						# break;
						# Verificar cual de los botones se ha pulsado
						if identidad == "arriba":
							jugador.update('stand_up')
							# Movimiento del Jugador a la Izquierda
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "abajo":
							jugador.update('stand_down')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "derecha":
							jugador.update('stand_right')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "izquierda":
							jugador.update('stand_left')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)

					#elif e.type == pygame.KEYDOWN:
					#	screenloop = True
					#	if e.key == K_s:
					#		x,y = jugador.rect.center
					#		jugador.disparar(x,y)

			#jugador.handle_event(e)
			# Carga el Fondo del Juego
			self.screen.blit(self.bgImageLaberinto, (0, 0))
			self.screen.blit(jugador.image, jugador.rect)
			# Se usa para que aparezca las imagenes con la variable animales = True
			#if animales:
				# Cuando se asigna a movimiento = True se empiezan a mover las imagenes
			#	self.floatingPicture(movimiento)

			# Llamada a que se dibuje el Proyectil del jugador
			# DemoProyectil.dibujar(screen)
			# Llamada a que se dibuje el Proyectil del enemigo
			# ProyectilInvasor.dibujar(screen)
			# Llamada al comportamiento del enemigo
			#enemigo.comportamiento(tiempo)
			# llamada a que se dibuje la nave espacial
			#jugador.dibujar(screen)
			# Llamada a que se dibuje el enemigo
			#enemigo.dibujar(screen)
			# Verificar los disparos del jugador
			#if len(jugador.listaDisparo) > 0:
			#	for x in jugador.listaDisparo:
			#		x.dibujar(screen)
			#		x.trayectoria()
			#		if x.rect.top < -10:
			#			jugador.listaDisparo.remove(x)
			#		else:
						#Verificar que las balas del jugador dieron a los enemigos
			#			for enemigo in listaEnemigo:
			#				if x.rect.colliderect(enemigo.rect):
			#					listaEnemigo.remove(enemigo)
			#					jugador.listaDisparo.remove(x)

			# Cargar los enemigos
			#if len(listaEnemigo) > 0:
			#	for enemigo in listaEnemigo:
			#		enemigo.comportamiento(tiempo)
			#		enemigo.dibujar(screen)
					# Verificar que la bala del enemigo dio al jugador
			#		if enemigo.rect.colliderect(jugador.rect):
			#			pass
					# Verificar los disparos del enemigo
			#		if len(enemigo.listaDisparo) > 0:
			#			for x in enemigo.listaDisparo:
			#				x.dibujar(screen)
			#				x.trayectoria()
							# Verificar si el enemigo colisiono con el jugador
			#				if x.rect.colliderect(jugador.rect):
			#					pass

			#				if x.rect.top > 900:
			#					enemigo.listaDisparo.remove(x)
			#				else:
								# Verificar que cuando un Proyectil enemigo choque con el del jugador los dos se eliminen
			#					for disparo in jugador.listaDisparo:
			#						if x.rect.colliderect(disparo.rect):
			#							jugador.listaDisparo.remove(disparo)
			#							enemigo.listaDisparo.remove(x)

			# Se establece en el menu que boton se hizo click
			self.menuItemsLaberinto[self.activeFocus].applyFocus(self.screen)
			self.menuItemsLaberinto[self.lastActiveFocus].removeFocus()
			self.menuItemsLaberinto[self.secondActiveFocus].removeFocus()
			self.menuItemsLaberinto[self.thirdActiveFocus].removeFocus()

			# Se muestra el menú de la Interfaz del Menu de Juegos
			for item in self.menuItemsLaberinto:
				self.screen.blit(item.label, (item.xpos, item.ypos))

			#  Se ejecuta la acción de click del mouse (Parte principal)
			if mpos[1] < self.scrHeight / 4:
				self.activeFocus = 0
				self.lastActiveFocus = 1
				self.secondActiveFocus = 2
				self.thirdActiveFocus = 3
			elif mpos[1] < self.scrHeight / 2:
				self.activeFocus = 1
				self.lastActiveFocus = 0
				self.secondActiveFocus = 2
				self.thirdActiveFocus = 3
			elif mpos[1] < (self.scrHeight / 4 + self.scrHeight/2):
				self.activeFocus = 2
				self.lastActiveFocus = 0
				self.secondActiveFocus = 1
				self.thirdActiveFocus = 3
			else:
				self.activeFocus = 3
				self.lastActiveFocus = 0
				self.secondActiveFocus = 1
				self.thirdActiveFocus = 2

			for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
				pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
			for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
				pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
				centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
				pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
				pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

				for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
					pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

			# Elimina la profundidad --> opencv problema de memoria
			del depth
			# Da vuelta la pantalla para que sea una pantalla de espejo
			screenFlipped = pygame.transform.flip(screen,1,0)
			# Actualiza la pantalla principal -> pantalla
			screen.blit(screenFlipped,(0,0))
			# Actualiza todo en la ventana
			pygame.display.flip()

			# Declaracion de prueba de mouse
			try:
				centroidX = blobData.centroid[0][0]
				centroidY = blobData.centroid[0][1]
				if dummy:
					# Obtiene los atributos actuales del mouse
					mousePtr = display.Display().screen().root.query_pointer()._data
					# Encuentra el cambio en X
					dX = centroidX - strX
					# Encuentra el cambio en Y
					dY = strY - centroidY
					minChange = 3
					# Si hubo un cambio en X mayor que minChange ...
					if abs(dX) > minChange:
						# Nueva coordenada X del mouse
						mouseX = mousePtr["root_x"] - 2*dX
						if mouseX < 0:
							mouseX = 0
						elif mouseX > self.scrWidth:
							mouseX = self.scrWidth
					# Si hubo un cambio en Y mayor que minChange ...
					if abs(dY) > minChange:
						# Nueva coordenada Y del mouse
						mouseY = mousePtr["root_y"] - 2*dY
						if mouseY < 0:
							mouseY = 0
						elif mouseY > self.scrHeight:
							mouseY = self.scrHeight
					print mouseX, mouseY
					# Mueve el mouse a una nueva ubicación
					move_mouse(mouseX, mouseY)
					# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
					strX = centroidX
					# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
					strY = centroidY
					# Normaliza (elimina el ruido) en el area convexa del casco
					cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
					# Normaliza la relacion entre el area del contorno y el area convexa del casco
					areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
					print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
					# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
					if cArea < 25000 and areaRatio > 0.82:
						click_down(1)
					else:
						click_up(1)
				else:
					# Inicializa la X inicial
					strX = centroidX
					# Inicializa el inicio Y
					strY = centroidY
					# Permite que la función continue en la primera parte de la sentencia if
					dummy = True
			except:
				# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
				# Espera un nuevo punto de partida
				dummy = False

	# Juego de Labarinto (Arriba, Abajo, Derecha, Izquierda)
	def JuegoLaberintoTomJerry(self):
		global done
		global identidad
		screenloop = True
		(depth,_) = get_depth()
		# Lista de cache en blanco para el area convexa del casco
		cHullAreaCache = constList(5,12000)
		# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
		areaRatioCache = constList(5,1)
		# Iniciar lista de centroides
		centroidList = list()
		screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
		# Iterator boolean -> Indica a programa cuando finalizar
		# Muy importante bool para la manipulacion del raton
		dummy = False
		# Cargar sonido principal
		# pygame.mixer.music.load('Sonidos/Intro.mp3')
		# pygame.mixer.music.play(3)
		# Instancia del Objeto Raton y Gato
		imagenRatonContento = Raton.imagenRatonContento(50,200)
		imagenGatoContento = Gato.imagenGatoContento(50,500)

		grupoimagenRatonContento = pygame.sprite.RenderUpdates(imagenRatonContento)
		grupoimagenGatoContento = pygame.sprite.RenderUpdates(imagenGatoContento)

		nivel = mapa.Mapa('Imagenes/mapa.txt')

		#jugador = Player.Kate((self.scrWidth/2,self.scrHeight/2))
		# Instancia del Objeto Nave Espacial
		# jugador = Protagonista(self.scrWidth,self.scrHeight)
		# Instancia del objeto Invasor
		# enemigo = Enemigo(100,100)
		# self.cargarEnemigos()
		# Instancia del Objeto Proyectil para el Jugador
		# DemoProyectil = Proyectil(self.scrWidth/2,self.scrHeight-80,"../Imagenes/bala.png", True)
		# Instancia del Objeto Proyectil para el enemigo
		# ProyectilInvasor = Proyectil(self.scrWidth/4,self.scrHeight-700,"../Imagenes/disparob.jpg", False)
		# Verificar si un jugador gano o perdio
		enJuego = True
		# Construye el Menu Principal si done = False
		if not done:
			self.buildMenuLaberinto()

		while screenloop:
			# Cuando se crea el Proyectil del Jugador se empieza a mover
			# DemoProyectil.trayectoria()
			# Cuando se crea el Proyectil del enemigo se empieza a mover
			# ProyectilInvasor.trayectoria()
			# Regulamos los frames por segundo
			self.clock.tick(30)
			# Obtenemos el tiempo del Juego
			tiempo = pygame.time.get_ticks()/1000
			# Obtenga la profundidad del kinect
			(depth,_) = get_depth()
			old_depth = depth
			depth = cv2.resize(old_depth, (1024, 768))
			# Convierta la profundidad en un flotador de 32 bits
			depth = depth.astype(np.float32)
			# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
			_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
			# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
			_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
			# Crea el objeto blobData usando la clase BlobAnalysis
			blobData = BlobAnalysis(depthThresh)
			# Crea el objeto blobDataBack usando la clase BlobAnalysis
			blobDataBack = BlobAnalysis(back)

			mpos = pygame.mouse.get_pos()

			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					screenloop = False
					pygame.quit()
					sys.exit()
				# Controlamos que cliqueo con el mouse
				if enJuego == True:
					if e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsLaberinto[self.itemNamesLaberinto[self.activeFocus]]()
						# Verificar cual de los botones se ha pulsado
						if identidad == "arriba":
							imagenRatonContento.dy = -2
							#jugador.update('up')
							# Movimiento del Jugador a la Izquierda
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "abajo":
							imagenRatonContento.dy = 2
							#jugador.update('down')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						else:
							imagenRatonContento.dy = 0

						if identidad == "derecha":
							imagenRatonContento.dx = -2
							#jugador.update('right')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "izquierda":
							imagenRatonContento.dx = 2
							#jugador.update('left')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						else:
							imagenRatonContento.dx = 0


			# Actualiza los movimientos del Raton
			grupoimagenRatonContento.update()

			# Verifica las Colisiones del Raton con el Laberinto
			if pygame.sprite.spritecollide(imagenRatonContento, nivel.grupo, 0, pygame.sprite.collide_mask):
				imagenRatonContento.deshacer()

			# Se Realiza la actividad de comer los quesos por parte del Raton
			for pum in pygame.sprite.groupcollide(grupoimagenRatonContento, nivel.quesos, 0, 1):
				pass

			# Carga el Fondo del Juego
			self.screen.blit(self.bgImageLaberinto, (0, 0))
			# Actualiza el Nivel del Laberinto
			nivel.actualizar(screen)

			# Y luego el Sprite del Jugador
			grupoimagenRatonContento.draw(screen)
			grupoimagenGatoContento.draw(screen)

			# Se establece en el menu que boton se hizo click
			self.menuItemsLaberinto[self.activeFocus].applyFocus(self.screen)
			self.menuItemsLaberinto[self.lastActiveFocus].removeFocus()
			self.menuItemsLaberinto[self.secondActiveFocus].removeFocus()
			self.menuItemsLaberinto[self.thirdActiveFocus].removeFocus()

			# Se muestra el menú de la Interfaz del Menu de Juegos
			for item in self.menuItemsLaberinto:
				self.screen.blit(item.label, (item.xpos, item.ypos))

			#  Se ejecuta la acción de click del mouse (Parte principal)
			if mpos[1] < self.scrHeight / 4:
				self.activeFocus = 0
				self.lastActiveFocus = 1
				self.secondActiveFocus = 2
				self.thirdActiveFocus = 3
			elif mpos[1] < self.scrHeight / 2:
				self.activeFocus = 1
				self.lastActiveFocus = 0
				self.secondActiveFocus = 2
				self.thirdActiveFocus = 3
			elif mpos[1] < (self.scrHeight / 4 + self.scrHeight/2):
				self.activeFocus = 2
				self.lastActiveFocus = 0
				self.secondActiveFocus = 1
				self.thirdActiveFocus = 3
			else:
				self.activeFocus = 3
				self.lastActiveFocus = 0
				self.secondActiveFocus = 1
				self.thirdActiveFocus = 2

			for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
				pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
			for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
				pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
				centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
				pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
				pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

				for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
					pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

			# Elimina la profundidad --> opencv problema de memoria
			del depth
			# Da vuelta la pantalla para que sea una pantalla de espejo
			screenFlipped = pygame.transform.flip(screen,1,0)
			# Actualiza la pantalla principal -> pantalla
			screen.blit(screenFlipped,(0,0))
			# Actualiza todo en la ventana
			pygame.display.flip()

			# Declaracion de prueba de mouse
			try:
				centroidX = blobData.centroid[0][0]
				centroidY = blobData.centroid[0][1]
				if dummy:
					# Obtiene los atributos actuales del mouse
					mousePtr = display.Display().screen().root.query_pointer()._data
					# Encuentra el cambio en X
					dX = centroidX - strX
					# Encuentra el cambio en Y
					dY = strY - centroidY
					minChange = 3
					# Si hubo un cambio en X mayor que minChange ...
					if abs(dX) > minChange:
						# Nueva coordenada X del mouse
						mouseX = mousePtr["root_x"] - 2*dX
						if mouseX < 0:
							mouseX = 0
						elif mouseX > self.scrWidth:
							mouseX = self.scrWidth
					# Si hubo un cambio en Y mayor que minChange ...
					if abs(dY) > minChange:
						# Nueva coordenada Y del mouse
						mouseY = mousePtr["root_y"] - 2*dY
						if mouseY < 0:
							mouseY = 0
						elif mouseY > self.scrHeight:
							mouseY = self.scrHeight
					print mouseX, mouseY
					# Mueve el mouse a una nueva ubicación
					move_mouse(mouseX, mouseY)
					# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
					strX = centroidX
					# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
					strY = centroidY
					# Normaliza (elimina el ruido) en el area convexa del casco
					cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
					# Normaliza la relacion entre el area del contorno y el area convexa del casco
					areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
					print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
					# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
					if cArea < 25000 and areaRatio > 0.82:
						click_down(1)
					else:
						click_up(1)
				else:
					# Inicializa la X inicial
					strX = centroidX
					# Inicializa el inicio Y
					strY = centroidY
					# Permite que la función continue en la primera parte de la sentencia if
					dummy = True
			except:
				# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
				# Espera un nuevo punto de partida
				dummy = False

	# Pantalla De Introuccion
	def introduccion(self):
			global done
			screenloop = True
			(depth,_) = get_depth()
			# Lista de cache en blanco para el area convexa del casco
			cHullAreaCache = constList(5,12000)
			# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
			areaRatioCache = constList(5,1)
			# Iniciar lista de centroides
			centroidList = list()
			screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
			# Iterator boolean -> Indica a programa cuando finalizar
			# Muy importante bool para la manipulacion del raton
			dummy = False
			if not done:
				self.buildMenuIntro() #Construye el Menu Principal

			while screenloop:
				self.clock.tick(30)
				# Obtenga la profundidad del kinect
				(depth,_) = get_depth()
				old_depth = depth
				depth = cv2.resize(old_depth, (1024, 768))
				# Convierta la profundidad en un flotador de 32 bits
				depth = depth.astype(np.float32)
				# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
				_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
				# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
				_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
				# Crea el objeto blobData usando la clase BlobAnalysis
				blobData = BlobAnalysis(depthThresh)
				# Crea el objeto blobDataBack usando la clase BlobAnalysis
				blobDataBack = BlobAnalysis(back)

				mpos = pygame.mouse.get_pos()

				for e in pygame.event.get():
					if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
						screenloop = False
						pygame.quit()
						sys.exit()
					elif e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsIntro[self.itemNamesIntro[self.activeFocus]]()
						break;

				# Se Carga el fondo de la Imagen de Introduccion
				self.screen.blit(self.bgImageIntro, (0, 0))
				# Se usa para que aparezca las imagenes que dan la vuelta
				self.floatingPicture()
				# Se establece en el menu que boton se hizo click
				self.menuItemsIntro[self.activeFocus].applyFocus(self.screen)
				self.menuItemsIntro[self.lastActiveFocus].removeFocus()

				# Se muestra el menú de la Interfaz de Introduccion
				for item in self.menuItemsIntro:
					self.screen.blit(item.label, (item.xpos, item.ypos))

				#  2 lazy 2 hacen algo hermoso y universal (Parte principal)
				if mpos[1] > self.scrHeight / 2:
					self.activeFocus = 1
					self.lastActiveFocus = 0
				else:
					self.activeFocus = 0
					self.lastActiveFocus = 1

				for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
					pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
				for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
					pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
					centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
					pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
					pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

					for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
						pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

				# Elimina la profundidad --> opencv problema de memoria
				del depth
				# Da vuelta la pantalla para que sea una pantalla de espejo
				screenFlipped = pygame.transform.flip(screen,1,0)
				# Actualiza la pantalla principal -> pantalla
				screen.blit(screenFlipped,(0,0))
				# Actualiza todo en la ventana
				pygame.display.flip()

				# Declaracion de prueba de mouse
				try:
					centroidX = blobData.centroid[0][0]
					centroidY = blobData.centroid[0][1]
					if dummy:
						# Obtiene los atributos actuales del mouse
						mousePtr = display.Display().screen().root.query_pointer()._data
						# Encuentra el cambio en X
						dX = centroidX - strX
						# Encuentra el cambio en Y
						dY = strY - centroidY
						minChange = 3
						# Si hubo un cambio en X mayor que minChange ...
						if abs(dX) > minChange:
							# Nueva coordenada X del mouse
							mouseX = mousePtr["root_x"] - 2*dX
							if mouseX < 0:
								mouseX = 0
							elif mouseX > self.scrWidth:
								mouseX = self.scrWidth
						# Si hubo un cambio en Y mayor que minChange ...
						if abs(dY) > minChange:
							# Nueva coordenada Y del mouse
							mouseY = mousePtr["root_y"] - 2*dY
							if mouseY < 0:
								mouseY = 0
							elif mouseY > self.scrHeight:
								mouseY = self.scrHeight
						print mouseX, mouseY
						# Mueve el mouse a una nueva ubicación
						move_mouse(mouseX, mouseY)
						# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
						strX = centroidX
						# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
						strY = centroidY
						# Normaliza (elimina el ruido) en el area convexa del casco
						cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
						# Normaliza la relacion entre el area del contorno y el area convexa del casco
						areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
						print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
						# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
						if cArea < 25000 and areaRatio > 0.82:
							click_down(1)
						else:
							click_up(1)
					else:
						# Inicializa la X inicial
						strX = centroidX
						# Inicializa el inicio Y
						strY = centroidY
						# Permite que la función continue en la primera parte de la sentencia if
						dummy = True
				except:
					# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
					# Espera un nuevo punto de partida
					dummy = False

	# Pantalla Del Menu de los Juegos
	def MenuJuegos(self):
			global done
			screenloop = True
			(depth,_) = get_depth()
			# Lista de cache en blanco para el area convexa del casco
			cHullAreaCache = constList(5,12000)
			# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
			areaRatioCache = constList(5,1)
			# Iniciar lista de centroides
			centroidList = list()
			screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
			# Iterator boolean -> Indica a programa cuando finalizar
			# Muy importante bool para la manipulacion del raton
			dummy = False
			if not done:
				self.buildMenuJuegos() #Construye el Menu Principal

			while screenloop:
				self.clock.tick(30)
				# Obtenga la profundidad del kinect
				(depth,_) = get_depth()
				old_depth = depth
				depth = cv2.resize(old_depth, (1024, 768))
				# Convierta la profundidad en un flotador de 32 bits
				depth = depth.astype(np.float32)
				# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
				_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
				# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
				_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
				# Crea el objeto blobData usando la clase BlobAnalysis
				blobData = BlobAnalysis(depthThresh)
				# Crea el objeto blobDataBack usando la clase BlobAnalysis
				blobDataBack = BlobAnalysis(back)

				mpos = pygame.mouse.get_pos()

				for e in pygame.event.get():
					if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
						screenloop = False
						pygame.quit()
						sys.exit()
					elif e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsMenuJuegos[self.itemNamesMenuJuegos[self.activeFocus]]()
						break;

				# Se Carga el fondo de la Imagen de Introduccion
				self.screen.blit(self.bgImageMenuJuegos, (0, 0))
				# Se usa para que aparezca las imagenes que dan la vuelta
				self.floatingPicture()
				# Se establece en el menu que boton se hizo click
				self.menuItemsMenuJuegos[self.activeFocus].applyFocus(self.screen)
				self.menuItemsMenuJuegos[self.lastActiveFocus].removeFocus()
				self.menuItemsMenuJuegos[self.secondActiveFocus].removeFocus()
				self.menuItemsMenuJuegos[self.thirdActiveFocus].removeFocus()

				# Se muestra el menú de la Interfaz del Menu de Juegos
				for item in self.menuItemsMenuJuegos:
					self.screen.blit(item.label, (item.xpos, item.ypos))

				#  Se ejecuta la acción de click del mouse (Parte principal)
				if mpos[1] < self.scrHeight / 4:
					self.activeFocus = 0
					self.lastActiveFocus = 1
					self.secondActiveFocus = 2
					self.thirdActiveFocus = 3
				elif mpos[1] < self.scrHeight / 2:
					self.activeFocus = 1
					self.lastActiveFocus = 0
					self.secondActiveFocus = 2
					self.thirdActiveFocus = 3
				elif mpos[1] < (self.scrHeight / 4 + self.scrHeight/2):
					self.activeFocus = 2
					self.lastActiveFocus = 0
					self.secondActiveFocus = 1
					self.thirdActiveFocus = 3
				else:
					self.activeFocus = 3
					self.lastActiveFocus = 0
					self.secondActiveFocus = 1
					self.thirdActiveFocus = 2

				for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
					pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
				for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
					pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
					centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
					pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
					pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

					for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
						pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

				# Elimina la profundidad --> opencv problema de memoria
				del depth
				# Da vuelta la pantalla para que sea una pantalla de espejo
				screenFlipped = pygame.transform.flip(screen,1,0)
				# Actualiza la pantalla principal -> pantalla
				screen.blit(screenFlipped,(0,0))
				# Actualiza todo en la ventana
				pygame.display.flip()

				# Declaracion de prueba de mouse
				try:
					centroidX = blobData.centroid[0][0]
					centroidY = blobData.centroid[0][1]
					if dummy:
						# Obtiene los atributos actuales del mouse
						mousePtr = display.Display().screen().root.query_pointer()._data
						# Encuentra el cambio en X
						dX = centroidX - strX
						# Encuentra el cambio en Y
						dY = strY - centroidY
						minChange = 3
						# Si hubo un cambio en X mayor que minChange ...
						if abs(dX) > minChange:
							# Nueva coordenada X del mouse
							mouseX = mousePtr["root_x"] - 2*dX
							if mouseX < 0:
								mouseX = 0
							elif mouseX > self.scrWidth:
								mouseX = self.scrWidth
						# Si hubo un cambio en Y mayor que minChange ...
						if abs(dY) > minChange:
							# Nueva coordenada Y del mouse
							mouseY = mousePtr["root_y"] - 2*dY
							if mouseY < 0:
								mouseY = 0
							elif mouseY > self.scrHeight:
								mouseY = self.scrHeight
						print mouseX, mouseY
						# Mueve el mouse a una nueva ubicación
						move_mouse(mouseX, mouseY)
						# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
						strX = centroidX
						# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
						strY = centroidY
						# Normaliza (elimina el ruido) en el area convexa del casco
						cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
						# Normaliza la relacion entre el area del contorno y el area convexa del casco
						areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
						print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
						# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
						if cArea < 25000 and areaRatio > 0.82:
							click_down(1)
						else:
							click_up(1)
					else:
						# Inicializa la X inicial
						strX = centroidX
						# Inicializa el inicio Y
						strY = centroidY
						# Permite que la función continue en la primera parte de la sentencia if
						dummy = True
				except:
					# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
					# Espera un nuevo punto de partida
					dummy = False

	# Pantalla De Fin del Juego
	def FinJuego(self, puntos, NroJuego):
			global done
			screenloop = True
			(depth,_) = get_depth()
			# Lista de cache en blanco para el area convexa del casco
			cHullAreaCache = constList(5,12000)
			# Lista de cache en blanco para la relacion de area del area de contorno al area de casco convexo
			areaRatioCache = constList(5,1)
			# Iniciar lista de centroides
			centroidList = list()
			screenFlipped = pygame.display.set_mode((self.scrWidth, self.scrHeight), pygame.FULLSCREEN)
			# Cargar la Palaba de Fin del Juego
			if NroJuego == 1:
				juego = "Izquierda, Derecha"
			elif NroJuego == 2:
				juego = "Arriba, Abajo"
			elif NroJuego == 3:
				juego = "Mover Objetos"
			else:
				juego = "Laberinto"
			Texto = pygame.transform.flip(self.fontFinJuego.render("Fin del Juego " + str(juego), 1, (255, 14, 0)), 1, 0)
			# Carga el Puntaje Obtenido en el JUEGO
			Marcador = pygame.transform.flip(self.fontPuntaje.render("Puntaje Obtenido: " + str(puntos), 1, (255,120,100)), 1, 0)
			# Iterator boolean -> Indica a programa cuando finalizar
			# Muy importante bool para la manipulacion del raton
			dummy = False
			if not done:
				self.buildFinJuego() #Construye el Menu Principal

			while screenloop:
				self.clock.tick(30)
				# Obtenga la profundidad del kinect
				(depth,_) = get_depth()
				old_depth = depth
				depth = cv2.resize(old_depth, (1024, 768))
				# Convierta la profundidad en un flotador de 32 bits
				depth = depth.astype(np.float32)
				# Umbral de la profundidad de una imagen binaria. Umbral en 600 unidades arbitrarias
				_,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV)
				# Umbral del fondo para tener un fondo delineado y un primer plano segmentado
				_,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
				# Crea el objeto blobData usando la clase BlobAnalysis
				blobData = BlobAnalysis(depthThresh)
				# Crea el objeto blobDataBack usando la clase BlobAnalysis
				blobDataBack = BlobAnalysis(back)

				mpos = pygame.mouse.get_pos()

				for e in pygame.event.get():
					if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
						screenloop = False
						pygame.quit()
						sys.exit()
					elif e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsFinJuego[self.itemNamesFinJuego[self.activeFocus]]()
						break;

				# Se Carga el fondo de la Imagen de Introduccion
				self.screen.blit(self.bgImageFinJuego, (0, 0))
				# Aparece El Texto de Fin del Juego
				screen.blit(Texto,(200,50))
				# Muestra el Puntaje Obtenido por el Jugador
				screen.blit(Marcador,(300,180))
				# Se usa para que aparezca las imagenes que dan la vuelta
				self.floatingPicture()
				# Se establece en el menu que boton se hizo click
				self.menuItemsFinJuego[self.activeFocus].applyFocus(self.screen)
				self.menuItemsFinJuego[self.lastActiveFocus].removeFocus()
				self.menuItemsFinJuego[self.secondActiveFocus].removeFocus()

				# Se muestra el menú de la Interfaz del Menu de Juegos
				for item in self.menuItemsFinJuego:
					self.screen.blit(item.label, (item.xpos, item.ypos))

				#  Se ejecuta la acción de click del mouse (Parte principal)
				if mpos[1] < self.scrHeight / 3:
					self.activeFocus = 0
					self.lastActiveFocus = 1
					self.secondActiveFocus = 2
				elif mpos[1] < (self.scrHeight - self.scrHeight/3):
					self.activeFocus = 1
					self.lastActiveFocus = 0
					self.secondActiveFocus = 2
				else:
					self.activeFocus = 2
					self.lastActiveFocus = 0
					self.secondActiveFocus = 1

				for cont in blobDataBack.contours: #Itera a traves de contornos en el fondo
					pygame.draw.lines(screen,(255,255,0),True,cont,3) #Colorea los limites binarios del fondo amarillo
				for i in range(blobData.counter): #Itera de 0 a la cantidad de blobs menos 1
					pygame.draw.circle(screen,(0,0,255),blobData.centroid[i],10) #Dibuja un circulo azul en cada centroide
					centroidList.append(blobData.centroid[i]) #Agrega la tupla centroide al centroidList -> utilizado para el dibujo
					pygame.draw.lines(screen,(255,0,0),True,blobData.cHull[i],3) #Dibuja el casco convexo para cada blob
					pygame.draw.lines(screen,(0,255,0),True,blobData.contours[i],3) #Dibuja el contorno de cada blob

					for tips in blobData.cHull[i]: #Itera a traves de los vertices del casco convexo para cada blob
						pygame.draw.circle(screen,(255,0,255),tips,5) #Dibuja los vertices purpura

				# Elimina la profundidad --> opencv problema de memoria
				del depth
				# Da vuelta la pantalla para que sea una pantalla de espejo
				screenFlipped = pygame.transform.flip(screen,1,0)
				# Actualiza la pantalla principal -> pantalla
				screen.blit(screenFlipped,(0,0))
				# Actualiza todo en la ventana
				pygame.display.flip()

				# Declaracion de prueba de mouse
				try:
					centroidX = blobData.centroid[0][0]
					centroidY = blobData.centroid[0][1]
					if dummy:
						# Obtiene los atributos actuales del mouse
						mousePtr = display.Display().screen().root.query_pointer()._data
						# Encuentra el cambio en X
						dX = centroidX - strX
						# Encuentra el cambio en Y
						dY = strY - centroidY
						minChange = 3
						# Si hubo un cambio en X mayor que minChange ...
						if abs(dX) > minChange:
							# Nueva coordenada X del mouse
							mouseX = mousePtr["root_x"] - 2*dX
							if mouseX < 0:
								mouseX = 0
							elif mouseX > self.scrWidth:
								mouseX = self.scrWidth
						# Si hubo un cambio en Y mayor que minChange ...
						if abs(dY) > minChange:
							# Nueva coordenada Y del mouse
							mouseY = mousePtr["root_y"] - 2*dY
							if mouseY < 0:
								mouseY = 0
							elif mouseY > self.scrHeight:
								mouseY = self.scrHeight
						print mouseX, mouseY
						# Mueve el mouse a una nueva ubicación
						move_mouse(mouseX, mouseY)
						# Hace que la nueva X inicial del mouse sea la X actual del centroide mas nuevo
						strX = centroidX
						# Hace que la nueva Y inicial del mouse sea la Y actual del centroide mas nuevo
						strY = centroidY
						# Normaliza (elimina el ruido) en el area convexa del casco
						cArea = cacheAppendMean(cHullAreaCache,blobData.cHullArea[0])
						# Normaliza la relacion entre el area del contorno y el area convexa del casco
						areaRatio = cacheAppendMean(areaRatioCache, blobData.contourArea[0]/cArea)
						print cArea, areaRatio, "(Must be: < 1000, > 0.82)"
						# Define lo que es un clic abajo. El area debe ser pequenia y la mano debe verse como un circulo binario (casi)
						if cArea < 25000 and areaRatio > 0.82:
							click_down(1)
						else:
							click_up(1)
					else:
						# Inicializa la X inicial
						strX = centroidX
						# Inicializa el inicio Y
						strY = centroidY
						# Permite que la función continue en la primera parte de la sentencia if
						dummy = True
				except:
					# No puede haber centroides y, por lo tanto, blobData.centroid [0] estará fuera de rango
					# Espera un nuevo punto de partida
					dummy = False

	# Maneja, crea y actualiza animales flotando / rebotando en la pantalla del menú
	def floatingPicture(self):
			self.animalAct = None
			self.animalPos = [[0, 0], [1024, 0]]
			if self.animalImgs == []:
				for i in range(0, 2):
					self.animalAct = self.animalPictures.pop(random.randrange(len(self.animalPictures)))
					self.animalImgs.append(BouncingSprite("Imagenes/" + self.animalAct, self.scrWidth, self.scrHeight,
						self.animalPos[i][0], self.animalPos[i][1], [3, 3]))
			else:
				for img in self.animalImgs:
					img.update()

			for img in self.animalImgs:
				img.draw(self.screen)

"""
Esta clase es una forma menos extensa de regionprops () desarrollada por MATLAB.
Encuentra propiedades de contornos y los establece en campos
"""
class BlobAnalysis:
	# Constructor. BW es una imagen binaria en forma de una matriz numpy
	def __init__(self,BW):
		self.BW = BW
		# Encuentra los contornos
		cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL)
		counter = 0
		"""
		Estas son listas dinamicas usadas para almacenar variables
		"""
		centroid = list()
		cHull = list()
		contours = list()
		cHullArea = list()
		contourArea = list()
		# Iterar a traves de CvSeq, cs.
		while cs:
			# Filtra contornos de menos de 2500 pixeles en el area
			if abs(cv.ContourArea(cs)) > 2000:
				# Se agrega contourArea con el area de contorno mas reciente
				contourArea.append(cv.ContourArea(cs))
				# Encuentra todos los momentos del contorno filtrado
				m = cv.Moments(cs)
				try:
					# Momento espacial m10
					m10 = int(cv.GetSpatialMoment(m,1,0))
					# Momento espacial m00
					m00 = int(cv.GetSpatialMoment(m,0,0))
					# Momento espacial m01
					m01 = int(cv.GetSpatialMoment(m,0,1))
					# Aniade la lista de centroides con las coordenadas mas nuevas del centro de gravedad del contorno
					centroid.append((int(m10/m00), int(m01/m00)))
					# Encuentra el casco convexo de cs en el tipo CvSeq
					convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True)
					# Agrega el area del casco convexo a la lista cHullArea
					cHullArea.append(cv.ContourArea(convexHull))
					# Agrega la lista del casco convexo a la lista de cHull
					cHull.append(list(convexHull))
					# Agrega la forma de lista del contorno a la lista de contornos
					contours.append(list(cs))
					# Agrega al mostrador para ver cuantos blobs hay
					counter += 1
				except:
					pass
			# Pasa al siguiente contorno en cs CvSeq
			cs = cs.h_next()
		"""
		A continuacion, las variables se convierten en campos para hacer referencias posteriores
		"""
		self.centroid = centroid
		self.counter = counter
		self.cHull = cHull
		self.contours = contours
		self.cHullArea = cHullArea
		self.contourArea = contourArea

# Muestra la referencia para la manipulacion Xlib
d = display.Display()

# Mueve el mouse a (x, y). x y y son enteros
def move_mouse(x,y):
	print "Moving mouse to:", x, y
	s = d.screen()
	root = s.root
	root.warp_pointer(x,y)
	d.sync()

# Simula un clic hacia abajo. El boton es un int
def click_down(button):
	print "GOT CLICK DOWN"
	Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
	d.sync()

# Simula un clic arriba. El boton es un int
def click_up(button):
	# print "GOT CLICK UP"
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

if __name__ == "__main__":
	screen = pygame.display.set_mode((1024, 768), 0, 32)
	pygame.display.set_caption("JUEGO DE UBICACION ESPACIAL UBIC")
	idscr = IdleScreen(screen)
	try:
		idscr.introduccion()
	except Exception, e:
		print "Something's wrong: %s" % e
