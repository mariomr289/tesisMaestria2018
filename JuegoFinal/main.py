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
from Clases import Estrella
# Importar la Clase de la Animacion Inicial de los Animales
from Clases import BouncingSprite
# Importar la Clase para crear el Menu
from Clases import MenuItem
# Importar la Clase para crear el Puntaje
from Clases import Puntaje
# Importar la Clase para crear el Temporizador
from Clases import Temporizador
# Importar las Clases del Juego Laberinto
from Clases import mapa
from Clases import Ardilla
from Clases import Arbolito
# Importar las Clases para el Juego de Adentro Afuera
from Clases import Oso
from Clases import Objetivo
# Importar la Clase de las Flechas
from Clases import Flecha
# Importar la Clases de los Botones
from Clases import Boton

# Da una lista de longitud del tamanio lleno con la variable val la longitud es una lista y val es dinamica
constList = lambda length, val: [val for _ in range(length)]
# Variable Auxiliar para crear el menu
done = False
# Variable para seleccionar que boton Seleciono (izquierda o derecha)
identidad = None
# Lista de Enemigos del Juego de IzqDerecha
listaEnemigo = []
# lista de Obstaculos del Juego Arriba Abajo
listaObstaculos = []
# Lista de Estrellas del Juego Arriba Abajo
listaEstrellas = []
# Imagen de la Nuez del Juego del Laberinto
imagenNuez = 'Imagenes/q.png'
# Lista de Puntuacion Juego Entrenamiento
listaPuntos = [0,0,0,0]
# Lista de Tiempo Juego Adentro Afuera
listaTiempo = [0,0,0,0]
# Clase Principal del Juego
class IdleScreen():
	def __init__(self, screen):
		pygame.init()
		self.screen = screen
		self.scrWidth = self.screen.get_rect().width
		self.scrHeight = self.screen.get_rect().height
		self.bgColor = (0, 0, 0)
		self.bgImage = pygame.transform.flip(pygame.image.load("Imagenes/FondoIzquierdaDerecha.jpg").convert(), 1, 0)
		self.bgImageArriba = pygame.transform.flip(pygame.image.load("Imagenes/FondoArribaAbajo.jpg").convert(), 1, 0)
		self.bgImageLaberinto = pygame.transform.flip(pygame.image.load("Imagenes/FondoLaberinto.jpg").convert(), 1, 0)
		self.bgImageIntro = pygame.transform.flip(pygame.image.load("Imagenes/FondoInicio.jpg").convert(), 1, 0)
		self.bgImageMenuJuegos = pygame.transform.flip(pygame.image.load("Imagenes/FondoMenu.jpg").convert(), 1, 0)
		self.bgImageFinJuego = pygame.transform.flip(pygame.image.load("Imagenes/FondoFinJuego.jpg").convert(), 1, 0)
		self.bgImageInstrucciones = pygame.transform.flip(pygame.image.load("Imagenes/FondoInstEntrenamiento.jpg").convert(), 1, 0)
		self.bgImageEntrenaIzquierda = pygame.transform.flip(pygame.image.load("Imagenes/EntrenaIzquierda.jpg").convert(), 1, 0)
		self.bgImageEntrenaDerecha = pygame.transform.flip(pygame.image.load("Imagenes/EntrenaDerecha.jpg").convert(), 1, 0)
		self.bgImageEntrenaArriba = pygame.transform.flip(pygame.image.load("Imagenes/EntrenaArriba.jpg").convert(), 1, 0)
		self.bgImageEntrenaAbajo = pygame.transform.flip(pygame.image.load("Imagenes/EntrenaAbajo.jpg").convert(), 1, 0)
		self.bgImageAdentro = pygame.transform.flip(pygame.image.load("Imagenes/FondoAdentro.jpg").convert(), 1, 0)
		self.bgImageAfuera = pygame.transform.flip(pygame.image.load("Imagenes/FondoAfuera.jpg").convert(), 1, 0)
		self.bgImageEncima = pygame.transform.flip(pygame.image.load("Imagenes/FondoEncima.jpg").convert(), 1, 0)
		self.bgImageDebajo = pygame.transform.flip(pygame.image.load("Imagenes/fondoDebajo.jpg").convert(), 1, 0)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("gaban", 55)
		self.fontLogro = pygame.font.SysFont("gaban", 80)
		self.fontPuntaje = pygame.font.SysFont("Answer", 35)
		self.fontTiempo = pygame.font.SysFont("Answer", 25)
		self.fontFinJuego = pygame.font.SysFont("RicksAmericanNF", 55)
		self.fontColor = (16, 4, 130)
		self.menuItems = list()
		self.menuItemsArriba = list()
		self.menuItemsLaberinto = list()
		self.menuItemsIntro = list()
		self.menuItemsMenuJuegos = list()
		self.menuItemsFinJuego = list()
		self.menuItemsInstrucciones = list()
		self.itemNames = ("Derecha", "Izquierda")
		self.menuFuncs = {"Derecha" : self.ClickDerecho,
						"Izquierda" : self.ClickIzquierdo}
		self.itemNamesArriba = ("Arriba", "Abajo")
		self.menuFuncsArriba = {"Arriba" : self.ClickArriba,
							"Abajo" : self.ClickAbajo}
		self.itemNamesIntro = ("Entrar", "Salir")
		self.menuFuncsIntro = {"Entrar" : self.ClickEntrar,
							"Salir" : self.ClickSalir}
		self.itemNamesMenuJuegos = ("Entrenamiento", "Izquierda Derecha", "Arriba Abajo", "Adentro Afuera", "Laberinto")
		self.menuFuncsMenuJuegos = {"Entrenamiento" : self.ClickEntrenamiento,
							"Izquierda Derecha" : self.ClickPrimerJuego,
							"Arriba Abajo" : self.ClickSegundoJuego,
							"Adentro Afuera" : self.ClickTercerJuego,
							"Laberinto" : self.ClickCuartoJuego}
		self.itemNamesFinJuego = ("Reiniciar Juego", "Menu Juegos", "Salir")
		self.menuFuncsFinJuego = {"Reiniciar Juego" : self.ClickReiniciar,
							"Menu Juegos" : self.ClickRegresar,
							"Salir" : self.ClickSalir2}
		self.itemNamesLaberinto = ("Arriba", "Izquierda", "Abajo", "Derecha")
		self.menuFuncsLaberinto = {"Arriba" : self.ClickArriba,
							"Izquierda" : self.ClickIzquierdo,
							"Abajo" : self.ClickAbajo,
							"Derecha" : self.ClickDerecho}
		self.itemNamesInstrucciones = ("Anterior", "Siguiente")
		self.menuFuncsInstrucciones = {"Anterior" : self.ClickAnterior,
							"Siguiente" : self.ClickSiguiente}
		self.animalImgs = []
		self.animalPictures = ["bison.png", "elephant.png", "giraffe.png", "goat.png", "lion.png",
								"monkey.png", "sheep.png"]
		self.activeFocus = 0
		self.lastActiveFocus = 1
		self.secondActiveFocus = 2
		self.thirdActiveFocus = 3
		self.FourActiveFocus = 4

	# Crea el menu de los Botones de la Interfaz del Juego Izquierda y Derecha
	def buildMenu(self):
		self.items = []
		while len(self.menuItems) > 0:
			for miIzqDer in self.menuItems:
				#Elimina los items del Menu
				self.menuItems.remove(miIzqDer)

		for index, item in enumerate(self.itemNames):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width + 30
			height = label.get_rect().height
			posx = (self.scrHeight) - (height)
			totalHeight  = len(self.itemNames) * height
			posy = (self.scrWidth)  + (index * height)

			miIzqDer = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItems.append(miIzqDer)

	# Crea el menu de los Botones de la Interfaz de Introduccion
	def buildMenuIntro(self):
		self.items = []
		while len(self.menuItemsIntro) > 0:
			for miMnIntro in self.menuItemsIntro:
				#Elimina los items del Menu
				self.menuItemsIntro.remove(miMnIntro)

		for index, item in enumerate(self.itemNamesIntro):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesIntro) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			miMnIntro = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsIntro.append(miMnIntro)

	# Crea el menu de los Botones de la Interfaz de Instrucciones
	def buildMenuInstrucciones(self):
		self.items = []
		while len(self.menuItemsInstrucciones) > 0:
			for mi in self.menuItemsInstrucciones:
				#Elimina los items del Menu
				self.menuItemsInstrucciones.remove(mi)

		for index, item in enumerate(self.itemNamesInstrucciones):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesInstrucciones) * height
			posy = (self.scrHeight) - (230) + (index * height)

			mi = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsInstrucciones.append(mi)

	# Crea el menu de los Botones de la Interfaz del Juego Arriba y Abajo
	def buildMenuArriba(self):
		self.items = []
		while len(self.menuItemsArriba) > 0:
			for miMnArriba in self.menuItemsArriba:
				#Elimina los items del Menu
				self.menuItemsArriba.remove(miMnArriba)

		for index, item in enumerate(self.itemNamesArriba):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width + 30
			height = label.get_rect().height
			posx = (self.scrHeight) - (height)
			totalHeight  = len(self.itemNamesArriba) * height
			posy = (self.scrWidth) + (index * height)

			miMnArriba = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsArriba.append(miMnArriba)

	# Crea el menu de los Botones de la Interfaz del Memu de los Juegos
	def buildMenuJuegos(self):
		self.items = []
		while len(self.menuItemsMenuJuegos) > 0:
			for miMenuJuegos in self.menuItemsMenuJuegos:
				#Elimina los items del Menu
				self.menuItemsMenuJuegos.remove(miMenuJuegos)

		for index, item in enumerate(self.itemNamesMenuJuegos):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 26
			posx = (self.scrWidth / 6) - (width / 6)
			totalHeight  = len(self.itemNamesMenuJuegos) * height
			posy = (self.scrHeight / 2) - (totalHeight / 2) + (index * height)

			miMenuJuegos = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsMenuJuegos.append(miMenuJuegos)

	# Crea el menu de los Botones de la Interfaz de Fin del Juego
	def buildFinJuego(self):
		self.items = []
		while len(self.menuItemsFinJuego) > 0:
			for miFinJuegos in self.menuItemsFinJuego:
				#Elimina los items del Menu
				self.menuItemsFinJuego.remove(miFinJuegos)

		for index, item in enumerate(self.itemNamesFinJuego):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrWidth / 2) - (width / 2)
			totalHeight  = len(self.itemNamesFinJuego) * height
			posy = (self.scrHeight) - (400) + (index * height)

			miFinJuegos = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsFinJuego.append(miFinJuegos)

	# Crea el menu de los Botones de JuegoLaberintoArdilla
	def buildMenuLaberinto(self):
		self.items = []
		while len(self.menuItemsLaberinto) > 0:
			for miMnLabe in self.menuItemsLaberinto:
				#Elimina los items del Menu
				self.menuItemsLaberinto.remove(miMnLabe)

		for index, item in enumerate(self.itemNamesLaberinto):
			label = pygame.transform.flip(self.font.render(item, 1, self.fontColor), 1, 0)
			width = label.get_rect().width
			height = label.get_rect().height + 30
			posx = (self.scrHeight) - (height)
			totalHeight  = len(self.itemNamesLaberinto) * height
			posy = (self.scrWidth) + (index * height)

			miMnLabe = MenuItem(item, posx, posy, width, height, self.font, self.fontColor)
			self.menuItemsLaberinto.append(miMnLabe)

	# Boton de entrar de la Pantalla de Introduccion
	def ClickEntrar(self):
		global done
		done = False
		print "ENTRAR"
		self.MenuJuegos()

	# Boton de Salir de la Pantalla de Introduccion
	def ClickSalir(self):
		global done
		done = False
		print "SALIR"
		#sys.exit(128)

	# Boton de Salir de la Pantalla de Introduccion
	def ClickSalir2(self, NroJuego):
		global done
		done = False
		print "SALIR"
		#sys.exit(128)

	# Boton de Anterior de la Pantalla de Instrucciones
	def ClickAnterior(self, NroJuego):
		global done
		done = False
		print "ANTERIOR"
		self.MenuJuegos()

	# Boton de Siguiente de la Pantalla de Instrucciones
	def ClickSiguiente(self, NroJuego):
		global done
		done = False
		print "SIGUIENTE " + str(NroJuego)
		if NroJuego == 1:
			self.Entrenamiento(1)
		elif NroJuego == 2:
			self.JuegoIzquierdaDerecha()
		elif NroJuego == 3:
			self.JuegoArribaAbajo()
		elif NroJuego == 4:
			self.JuegoAdentroAfuera("Adentro")
		else:
			self.JuegoLaberinto()

	# Boton de Reiniciar los VideoJuegos
	def ClickReiniciar(self, NroJuego):
		global done
		done = False
		print "REINICIAR"
		if NroJuego == 1:
			self.Entrenamiento(1)
		elif NroJuego == 2:
			self.JuegoIzquierdaDerecha()
		elif NroJuego == 3:
			self.JuegoArribaAbajo()
		elif NroJuego == 4:
			self.JuegoAdentroAfuera("Adentro")
		else:
			self.JuegoLaberinto()

	# Boton de Regresar al Menu de los Juegos
	def ClickRegresar(self, NroJuego):
		global done
		done = False
		print "REGRESAR"
		self.MenuJuegos()

	# Boton de Ingreso al Primer Juego
	def ClickPrimerJuego(self):
		global done
		done = False
		print "Primer Juego"
		self.Instrucciones(2)
		#self.JuegoDerIzq()

	# Boton de Ingreso al Segundo Juego
	def ClickSegundoJuego(self):
		global done
		done = False
		print "Segundo Juego"
		self.Instrucciones(3)
		#self.JuegoArribaAbajo()

	# Boton de Ingreso al Tercer Juego
	def ClickTercerJuego(self):
		global done
		done = False
		print "Tercer Juego"
		self.Instrucciones(4)
		#self.JuegoLaberinto()

	# Boton de Ingreso al Cuarto Juego
	def ClickCuartoJuego(self):
		global done
		done = False
		print "Cuarto Juego"
		self.Instrucciones(5)
		#self.JuegoLaberintoTomJerry()

	# Boton de Ingreso al Entrenamiento
	def ClickEntrenamiento(self):
		global done
		done = False
		print "Juego Entrenamiento"
		self.Instrucciones(1)

	# Menu del Juego Derecha e Izquierda
	def ClickDerecho(self):
		global done
		global identidad
		print "DERECHA"
		done = True
		identidad = "derecha"

	def ClickIzquierdo(self):
		global done
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
			#Elimina La galina de la pantalla
			listaEnemigo.remove(enemigo)

		enemigo.conquista = True

	# Funcion que detiene todo en el Juego Arriba Abajo
	def detenerTodoArrAba(self):
		while len(listaEstrellas) > 0:
			for Recompensa in listaEstrellas:
				#Elimina las estrellas de la lista
				listaEstrellas.remove(Recompensa)

		while len(listaObstaculos) > 0:
			for ObstaculoEne in listaObstaculos:
				#Elimina los obstaculos de la lista
				listaObstaculos.remove(ObstaculoEne)

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

	# Funcion para Cargar las Estrellas del Juegos Arriba Abajo
	def cargarEstrellas(self, posx):
		posy = 90
		for y in range(1,6):
			Recompensa = Estrella.Estrellita(posx,posy, 40, 'Imagenes/estrellita1.png', 'Imagenes/estrellita2.png')
			listaEstrellas.append(Recompensa)
			posy = posy + 135

	# Funcion para cargar los Obstaculos del Juego Arriba Abajo
	def cargarObstaculos(self):
		posx = -3500
		posEstrellaX = -3500
		# Establece el orden de como aparecen los Obstaculos
		listaUbicacion = [1,0,1,0,1,0,1,0,1,0]
		for x in range(1,10):
			#valor = np.random.randint(2, size=1)
			if listaUbicacion[x] == 1:
				# posicion Abajo de los Obstaculos
				posy = 0
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/ObstaculoArriba.png', 'Imagenes/ObstaculoArriba.png')
				listaObstaculos.append(ObstaculoEne)
				posy = posy + 680
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/ObstaculoAbajo.png', 'Imagenes/ObstaculoAbajo.png')
				listaObstaculos.append(ObstaculoEne)
				#Cargar Las Estrellas
				self.cargarEstrellas(posEstrellaX)
			else:
				# posicion Arriba de los Obstaculos
				posy = -400
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/ObstaculoArriba.png', 'Imagenes/ObstaculoArriba.png')
				listaObstaculos.append(ObstaculoEne)
				posy = 280
				ObstaculoEne = Obstaculo.Obstaculito(posx,posy,40,'Imagenes/ObstaculoAbajo.png', 'Imagenes/ObstaculoAbajo.png')
				listaObstaculos.append(ObstaculoEne)
				#Cargar Las Estrellas
				self.cargarEstrellas(posEstrellaX)

			posx = posx + 500
			posEstrellaX = posx + 250

	# Juego de La Galina y los Huevos (Derecha e Izquierda)
	def JuegoIzquierdaDerecha(self):
		global done
		global identidad
		SonidoMusica = "play"
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
		# Cargar Imagen de Flecha Izquierda pequenia
		FlechaIzquierdaChica = Flecha.Flechita(205,415,'Imagenes/Flecha-Izquierda-Chica.png')
		# Cargar Imagen de Flecha Izquierda Grande
		FlechaIzquierdaGrande = Flecha.Flechita(175,385,'Imagenes/Flecha-Izquierda.png')
		# Cargar Imagen de Flecha Derecha pequenia
		FlechaDerechaChica = Flecha.Flechita(730,415,'Imagenes/Flecha-Derecha-Chica.png')
		# Cargar Imagen de Flecha Derecha Grande
		FlechaDerechaGrande = Flecha.Flechita(695,385,'Imagenes/Flecha-Derecha.png')
		# Cargar Imagen de Volumen Play
		VolumenPlay = Boton.Botoncito(15,655,'Imagenes/VolumenSonido.png')
		# Cargar Imagen de Volumen Pausa
		VolumenPausa = Boton.Botoncito(15,655,'Imagenes/VolumenSilencio.png')
		# Cargar sonido principal
		pygame.mixer.music.load('Sonidos/DonkeyKongCountry3-JangleBells.mp3')
		pygame.mixer.music.play(3)
		# Cargar la Palaba de Fin del Juego
		Texto = pygame.transform.flip(self.font.render("Fin del Juego", 1, (255, 14, 0)), 1, 0)
		# Instancia del Objeto Jugador
		jugador = Jugador.NenaCanasta(self.scrWidth,self.scrHeight)
		# Instancia del objeto Gallina o Ebemigo
		#enemigo = Invasor(100,100)
		self.cargarEnemigos()
		# Cargar el Temporizador
		Tempo = Temporizador.Tiempito(self.fontPuntaje, (128, 55))
		# Instancia del Objeto Puntaje
		puntos = Puntaje.Score(self.fontPuntaje, (900, 55))
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
			# Llamar a la funcion que inicializa el tiempo
			Tempo.tiempo_sube()
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
					pygame.mixer.music.fadeout(2000)
					pygame.quit()
					sys.exit()
				if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
					pygame.mixer.music.pause()
					SonidoMusica = "pausa"
				if e.type == pygame.KEYDOWN and e.key == pygame.K_v:
					pygame.mixer.music.unpause()
					SonidoMusica = "play"
				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
					pygame.time.wait(5000)
				if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
					pygame.mixer.music.fadeout(1000)
					self.detenerTodo()
					self.MenuJuegos()
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
			# Se muestra el tiempo del VideoJuego
			Tempo.update(screen)
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
			# Mostrar el Volumen del SonidoMusica
			if SonidoMusica == "play":
				VolumenPlay.dibujar(screen)
			else:
				VolumenPausa.dibujar(screen)

			# Mostrar las Flechas pequenias
			FlechaDerechaChica.dibujar(screen)
			FlechaIzquierdaChica.dibujar(screen)
			# Mostrar las flechas de IZQUIERDA y DERECHA
			if identidad == "izquierda":
				FlechaDerechaGrande.dibujar(screen)
			if identidad == "derecha":
				FlechaIzquierdaGrande.dibujar(screen)
			# llamada a que se dibuje la nave espacial
			jugador.dibujar(screen)
			# Verificar que el Puntaje sea igual a 10 Huevos o el Tiempo Transcurrido sea igual al limite
			if puntos.score == 10 or Tempo.temporal == 4500:
				enJuego = False
				self.detenerTodo()
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
				pygame.mixer.music.fadeout(4000)
				screen.blit(Texto,(320,200))
				# Llamar a la pantalla de Fin del Juego
				done = False
				self.FinJuego(puntos.score, Tempo.segundos, 2)

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
	def JuegoArribaAbajo(self):
		global done
		global identidad
		SonidoMusica = "play"
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
		# Cargar Imagen de Flecha Arriba pequenia
		FlechaArribaChica = Flecha.Flechita(460,150,'Imagenes/Flecha-Arriba-Chica.png')
		# Cargar Imagen de Flecha Arriba Grande
		FlechaArribaGrande = Flecha.Flechita(440,120,'Imagenes/Flecha-Arriba.png')
		# Cargar Imagen de Flecha Abajo pequenia
		FlechaAbajoChica = Flecha.Flechita(460,530,'Imagenes/Flecha-Abajo-Chica.png')
		# Cargar Imagen de Flecha Abajo Grande
		FlechaAbajoGrande = Flecha.Flechita(440,500,'Imagenes/Flecha-Abajo.png')
		# Cargar Imagen de Volumen Play
		VolumenPlay = Boton.Botoncito(15,655,'Imagenes/VolumenSonido.png')
		# Cargar Imagen de Volumen Pausa
		VolumenPausa = Boton.Botoncito(15,655,'Imagenes/VolumenSilencio.png')
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
		# Cargar el Temporizador
		Tempo = Temporizador.Tiempito(self.fontPuntaje, (128, 55))
		# Instancia del Objeto Puntaje
		puntos = Puntaje.Score(self.fontPuntaje, (900, 55))
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
			# llamar a la funcion que inicializa el tiempo
			Tempo.tiempo_sube()
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
					pygame.mixer.music.fadeout(2000)
					pygame.quit()
					sys.exit()
				if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
					pygame.mixer.music.pause()
					SonidoMusica = "pausa"
				if e.type == pygame.KEYDOWN and e.key == pygame.K_v:
					pygame.mixer.music.unpause()
					SonidoMusica = "play"
				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
					pygame.time.wait(5000)
				if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
					pygame.mixer.music.fadeout(1000)
					self.detenerTodoArrAba()
					self.MenuJuegos()
				# Controlamos que cliqueo con el mouse
				if enJuego == True:
					if e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsArriba[self.itemNamesArriba[self.activeFocus]]()
						# break;
					# Verificar cual de los botones se ha pulsado
					if identidad == "arriba":
						# Movimiento del Jugador arriba
						jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
					elif identidad == "abajo":
						# Movimiento del Jugador abajo
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
			# Se muestra el tiempo del VideoJuego
			Tempo.update(screen)
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
			#enemigo.comportamiento(tiempo)
			if SonidoMusica == "play":
				VolumenPlay.dibujar(screen)
			else:
				VolumenPausa.dibujar(screen)

			# Mostrar las Flechas pequenias
			FlechaArribaChica.dibujar(screen)
			FlechaAbajoChica.dibujar(screen)
			# Mostrar las Flechas Grandes
			if identidad == "arriba":
				FlechaArribaGrande.dibujar(screen)
			if identidad == "abajo":
				FlechaAbajoGrande.dibujar(screen)
			# llamada a que se dibuje la nave espacial
			jugador.dibujar(screen)
			# Verifica que el jugador ha recolectado 20 Estrellas o que el Tiempo Transcurrido sea el límite de 3000
			if puntos.score == 20 or Tempo.temporal == 4800:
				enJuego = False
				self.detenerTodoArrAba()
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

			# Cargar los Obstaculos
			if len(listaObstaculos) > 0:
				for ObstaculoEne in listaObstaculos:
					ObstaculoEne.comportamiento(tiempo)
					ObstaculoEne.dibujar(screen)
					# Verificar que el Obstaculo choco con el jugador
					if ObstaculoEne.rect.colliderect(jugador.rect):
						jugador.destruccion()
						enJuego = False
						self.detenerTodoArrAba()

			if len(listaEstrellas) > 0:
				for Recompensa in listaEstrellas:
					Recompensa.comportamiento(tiempo)
					Recompensa.dibujar(screen)
					# Verificar cuando el jugador choque con las Estrellas
					if Recompensa.rect.colliderect(jugador.rect):
						# Suma el puntaje las Estrellas que recoge el Jugador
						puntos.score_up()
						#Borrar de la Pantalla la Estrella recogida
						listaEstrellas.remove(Recompensa)
						enJuego = True

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
				self.FinJuego(puntos.score, Tempo.segundos, 3)

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

	# Juego de Laberinto (Arriba, Abajo, Derecha, Izquierda)
	def JuegoLaberinto(self):
		global done
		global identidad
		SonidoMusica = "play"
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
		# Cargar Imagen de Flecha Arriba pequenia
		FlechaArribaChica = Flecha.Flechita(715,125,'Imagenes/Flecha-Arriba-Chica.png')
		# Cargar Imagen de Flecha Arriba Grande
		FlechaArribaGrande = Flecha.Flechita(695,95,'Imagenes/Flecha-Arriba.png')
		# Cargar Imagen de Flecha Abajo pequenia
		FlechaAbajoChica = Flecha.Flechita(200,130,'Imagenes/Flecha-Abajo-Chica.png')
		# Cargar Imagen de Flecha Abajo Grande
		FlechaAbajoGrande = Flecha.Flechita(175,95,'Imagenes/Flecha-Abajo.png')
		# Cargar Imagen de Flecha Izquierda pequenia
		FlechaIzquierdaChica = Flecha.Flechita(205,515,'Imagenes/Flecha-Izquierda-Chica.png')
		# Cargar Imagen de Flecha Izquierda Grande
		FlechaIzquierdaGrande = Flecha.Flechita(175,485,'Imagenes/Flecha-Izquierda.png')
		# Cargar Imagen de Flecha Derecha pequenia
		FlechaDerechaChica = Flecha.Flechita(730,525,'Imagenes/Flecha-Derecha-Chica.png')
		# Cargar Imagen de Flecha Derecha Grande
		FlechaDerechaGrande = Flecha.Flechita(695,485,'Imagenes/Flecha-Derecha.png')
		# Cargar Imagen de Volumen Play
		VolumenPlay = Boton.Botoncito(15,655,'Imagenes/VolumenSonido.png')
		# Cargar Imagen de Volumen Pausa
		VolumenPausa = Boton.Botoncito(15,655,'Imagenes/VolumenSilencio.png')
		# Cargar sonido principal
		pygame.mixer.music.load('Sonidos/Intro.mp3')
		pygame.mixer.music.play(3)
		# Instancia del Objeto Raton y Gato
		imagenArdillita = Ardilla.imagenArdillita(30,30)
		imagenArbol = Arbolito.imagenArbol(910,670)

		grupoimagenArdillita = pygame.sprite.RenderUpdates(imagenArdillita)
		grupoimagenArbol = pygame.sprite.RenderUpdates(imagenArbol)

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
		# Cargar el Temporizador
		Tempo = Temporizador.Tiempito(self.fontPuntaje, (120, 65))
		# Instancia del Objeto Puntaje
		puntos = Puntaje.Score(self.fontPuntaje, (930, 65))
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
			# Llamar a la funcion que inicializa el tiempo
			Tempo.tiempo_sube()
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
				if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
					pygame.mixer.music.pause()
					SonidoMusica = "pausa"
				if e.type == pygame.KEYDOWN and e.key == pygame.K_v:
					pygame.mixer.music.unpause()
					SonidoMusica = "play"
				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
					pygame.time.wait(5000)
				if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
					pygame.mixer.music.fadeout(1000)
					self.MenuJuegos()
				# Controlamos que cliqueo con el mouse
				if enJuego == True:
					if e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsLaberinto[self.itemNamesLaberinto[self.activeFocus]]()
						# Verificar cual de los botones se ha pulsado
						if identidad == "arriba":
							imagenArdillita.dy = -2
							#jugador.update('up')
							# Movimiento del Jugador a la Izquierda
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "abajo":
							imagenArdillita.dy = 2
							#jugador.update('down')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						else:
							imagenArdillita.dy = 0

						if identidad == "derecha":
							imagenArdillita.dx = -2
							#jugador.update('right')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoArriba()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						elif identidad == "izquierda":
							imagenArdillita.dx = 2
							#jugador.update('left')
							# Movimiento del Jugador a la Derecha
							#jugador.movimientoAbajo()
							# Disparos del jugador
							#x,y = jugador.rect.center
							#jugador.disparar(x,y)
						else:
							imagenArdillita.dx = 0


			# Actualiza los movimientos de la Ardilla
			grupoimagenArdillita.update()

			# Verifica las Colisiones de la Ardilla con el Laberinto
			if pygame.sprite.spritecollide(imagenArdillita, nivel.grupo, 0, pygame.sprite.collide_mask):
				imagenArdillita.deshacer()

			# Se Realiza la actividad de comer las nueces por parte de la Ardilla
			for pum in pygame.sprite.groupcollide(grupoimagenArdillita, nivel.nueces, 0, 1):
				puntos.score_up()

			# Si Choca la Ardillla con el Arbol se Termina el JUEGO
			for pum in pygame.sprite.groupcollide(grupoimagenArdillita, grupoimagenArbol, 1, 0):
				imagenArdillita.destruccion()
				grupoimagenArdillita = pygame.sprite.RenderUpdates(imagenArdillita)
				enJuego = False

			# Carga el Fondo del Juego
			self.screen.blit(self.bgImageLaberinto, (0, 0))
			# Actualiza el Nivel del Laberinto, dibuja el Mapa
			nivel.actualizar(screen)
			# Se muestra el Tiempo del VideoJuego
			Tempo.update(screen)
			# Actualizar el Puntaje del JUEGO
			puntos.update(screen)
			# Mostrar el Volumen del SonidoMusica
			if SonidoMusica == "play":
				VolumenPlay.dibujar(screen)
			else:
				VolumenPausa.dibujar(screen)

			# Mostrar las Flechas pequenias
			FlechaArribaChica.dibujar(screen)
			FlechaAbajoChica.dibujar(screen)
			FlechaDerechaChica.dibujar(screen)
			FlechaIzquierdaChica.dibujar(screen)
			# Mostrar las Flechas Grandes
			if identidad == "arriba":
				FlechaArribaGrande.dibujar(screen)
			if identidad == "abajo":
				FlechaAbajoGrande.dibujar(screen)
			if identidad == "izquierda":
				FlechaDerechaGrande.dibujar(screen)
			if identidad == "derecha":
				FlechaIzquierdaGrande.dibujar(screen)

			# Y luego el Sprite del Jugador
			grupoimagenArdillita.draw(screen)
			grupoimagenArbol.draw(screen)

			if Tempo.temporal == 9000:
				enJuego = False

			if enJuego == False:
				pygame.mixer.music.fadeout(3000)
				done = False
				# Llamar a la pantalla de Fin de Juego
				self.FinJuego(puntos.score, Tempo.segundos, 5)

			# Se establece en el menu que boton se hizo click
			self.menuItemsLaberinto[self.activeFocus].applyFocus(self.screen)
			self.menuItemsLaberinto[self.lastActiveFocus].removeFocus()
			self.menuItemsLaberinto[self.secondActiveFocus].removeFocus()
			self.menuItemsLaberinto[self.thirdActiveFocus].removeFocus()

			# Se muestra el menú de la Interfaz del Menu de Juegos
			for item in self.menuItemsLaberinto:
				self.screen.blit(item.label, (item.xpos, item.ypos))

			#  Se ejecuta la acción de click del mouse (Parte principal)
			if mpos[0] <= self.scrWidth/2 and mpos[1] <= self.scrHeight/2:
				self.activeFocus = 0
				self.lastActiveFocus = 1
				self.secondActiveFocus = 2
				self.thirdActiveFocus = 3
			elif mpos[0] <= self.scrWidth/2 and mpos[1] > self.scrHeight/2:
				self.activeFocus = 1
				self.lastActiveFocus = 0
				self.secondActiveFocus = 2
				self.thirdActiveFocus = 3
			elif mpos[0] > self.scrWidth/2 and mpos[1] <= self.scrHeight/2:
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
			# Cargar Imagen del Boton Entrar pequenio
			BotonEntrarChico = Boton.Botoncito(480,350,'Imagenes/MarcianoA.jpg')
			# Cargar Imagen del Boton Entrar Grande
			BotonEntrarGrande = Boton.Botoncito(480,350,'Imagenes/MarcianoB.jpg')

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

	# Pantalla Del Juego Adentro_Afuera
	def JuegoAdentroAfuera(self, actividad):
			global done
			screenloop = True
			SonidoMusica = "play"
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
			# Cargar Imagen de Volumen Play
			VolumenPlay = Boton.Botoncito(15,655,'Imagenes/VolumenSonido.png')
			# Cargar Imagen de Volumen Pausa
			VolumenPausa = Boton.Botoncito(15,655,'Imagenes/VolumenSilencio.png')
			#Cargar el sonido Principal
			pygame.mixer.music.load('Sonidos/DonkeyKongCountry3-JangleBells.mp3')
			pygame.mixer.music.play(3)
			# Cargar la Palabra de la actividad
			TxtActividad = pygame.transform.flip(self.font.render(actividad, 1, (0,0,255)), 1, 0)
			#Cargar la Palabra de Fin del JUEGO
			Texto = pygame.transform.flip(self.fontLogro.render("Lo lograste", 1, (56,130,194)), 1, 0)
			# Verificar Que actividad se esta ejecutando
			if actividad == "Adentro":
				posOsoX = 150
				posOsoY = 510
				posObjX = 240
				posObjY = 310
			elif actividad == "Afuera":
				posOsoX = 750
				posOsoY = 510
				posObjX = 800
				posObjY = 310
			elif actividad == "Encima":
				posOsoX = 150
				posOsoY = 510
				posObjX = 460
				posObjY = 170
			elif actividad == "Debajo":
				posOsoX = 150
				posOsoY = 510
				posObjX = 460
				posObjY = 320

			# Instancia del objeto Cuadro
			ObjJug = Oso.Osito(self.scrWidth, self.scrHeight, posOsoX, posOsoY)
			# Instancia del Objeto ObjetivoMover
			Lugar = Objetivo.ObjetivoMover(posObjX,posObjY,'Imagenes/Objetivo1.png','Imagenes/Objetivo2.png')

			# Instancia del Objeto Puntaje
			puntos = Puntaje.Score(self.fontPuntaje, (900,60))
			# Cargar el Temporizador de la Actividad
			Tempo = Temporizador.Tiempito(self.fontTiempo, (135,42))
			# Cargar el Temporizador de Ejecucion de la Actividad
			Tempo2 = Temporizador.Tiempito(self.fontTiempo, (130,72))
			# Verificar si el Jugador gano o perdio
			enJuego = True
			#if not done:
			#	self.buildMenuIntro() #Construye el Menu Principal

			while screenloop:
				self.clock.tick(30)
				# Obtenemos el tiempo del Juego
				tiempo = pygame.time.get_ticks()/1000
				# Llamar a la funcion que inicializa el tiempo
				Tempo2.tiempo_sube()
				if puntos.score < 1:
					Tempo.tiempo_sube()
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
					if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
						pygame.mixer.music.pause()
						SonidoMusica = "pausa"
					if e.type == pygame.KEYDOWN and e.key == pygame.K_v:
						pygame.mixer.music.unpause()
						SonidoMusica = "play"
					if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
						pygame.time.wait(5000)
					if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
						pygame.mixer.music.fadeout(1000)
						self.MenuJuegos()
					# Controlamos el clic del MOUSE
					if enJuego == True:
						if e.type == pygame.MOUSEBUTTONDOWN:
							screenloop = True
							print "Mouse Down"
							if ObjJug.rect.collidepoint(e.pos):
								ObjJug.click = True
						elif e.type == pygame.MOUSEBUTTONUP:
							ObjJug.click = False
							print "Mouse Up"

				# Se Carga el fondo de la Imagen de Mover Objetos
				if actividad == "Adentro":
					self.screen.blit(self.bgImageAdentro, (0, 0))
				elif actividad == "Afuera":
					self.screen.blit(self.bgImageAfuera, (0, 0))
				elif actividad == "Encima":
					self.screen.blit(self.bgImageEncima, (0, 0))
				elif actividad == "Debajo":
					self.screen.blit(self.bgImageDebajo, (0, 0))
				# Se Muestra la Actividad a Realizar
				screen.blit(TxtActividad, (400,10))
				# Se muestra el tiempo de la actividad
				Tempo.update_actividad(screen)
				Tempo2.update(screen)
				# Actualizar el Puntaje del JUEGO
				puntos.update(screen)
				# Mostrar el Volumen del SonidoMusica
				if SonidoMusica == "play":
					VolumenPlay.dibujar(screen)
				else:
					VolumenPausa.dibujar(screen)

				# Animacion del ObjetivoMover
				Lugar.comportamiento(tiempo)
				# Dibuja el Objetivo a Realizar
				Lugar.dibujar(screen)
				# Actualiza el Osito en la Pantalla
				ObjJug.update(screen, self.scrWidth)

				#Verificar Colision del Jugador con el Objetivo
				if ObjJug.rect.collidepoint(self.scrWidth - posObjX,posObjY):
					screen.blit(Texto, (530,350))
					puntos.score = 1
					print "Colisiono el Jugador"

				if Tempo2.temporal == 900:
					enJuego = False

				if enJuego == False and actividad == "Adentro":
					listaTiempo[0] = Tempo.segundos
					listaPuntos[0] = puntos.score
					done = False
					self.JuegoAdentroAfuera("Afuera")
				elif enJuego == False and actividad == "Afuera":
					listaTiempo[1] = Tempo.segundos
					listaPuntos[1] = puntos.score
					done = False
					self.JuegoAdentroAfuera("Encima")
				elif enJuego == False and actividad == "Encima":
					listaTiempo[2] = Tempo.segundos
					listaPuntos[2] = puntos.score
					done = False
					self.JuegoAdentroAfuera("Debajo")
				elif enJuego == False and actividad == "Debajo":
					listaTiempo[3] = Tempo.segundos
					listaPuntos[3] = puntos.score
					done = False
					pygame.mixer.music.fadeout(2000)
					# Llamar a la pantalla de Fin de JUEGO
					self.FinJuego(listaPuntos[0], listaTiempo[0], 4)

				# Se establece en el menu que boton se hizo click
				#self.menuItemsIntro[self.activeFocus].applyFocus(self.screen)
				#self.menuItemsIntro[self.lastActiveFocus].removeFocus()

				# Se muestra el menú de la Interfaz de Introduccion
				#for item in self.menuItemsIntro:
				#	self.screen.blit(item.label, (item.xpos, item.ypos))

				#  2 lazy 2 hacen algo hermoso y universal (Parte principal)
				#if mpos[1] > self.scrHeight / 2:
				#	self.activeFocus = 1
				#	self.lastActiveFocus = 0
				#else:
				#	self.activeFocus = 0
				#	self.lastActiveFocus = 1

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

	# Pantalla De Entrenamiento Izquierda, Derecha, Arriba, Abajo
	def Entrenamiento(self, actividad):
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
			# Cargar Imagen de Carita Feliz
			CaritaFeliz = pygame.image.load("Imagenes/CaritaFeliz.png")
			spriteFeliz = pygame.sprite.Sprite()
			spriteFeliz.image = CaritaFeliz
			spriteFeliz.rect = CaritaFeliz.get_rect()
			# Cargar Imagen de Carita Triste
			CaritaTriste = pygame.image.load("Imagenes/CaritaTriste.png")
			spriteTriste = pygame.sprite.Sprite()
			spriteTriste.image = CaritaTriste
			spriteTriste.rect = CaritaTriste.get_rect()
			# Cargar la Palabra de Correcto
			TxtCorrecto = pygame.transform.flip(self.font.render("Correcto", 1, (100, 0, 255)), 1, 0)
			# Cargar la Palabra de Incorrecto
			TxtIncorrecto = pygame.transform.flip(self.font.render("Incorrecto", 1, (100, 0, 255)), 1, 0)
			# Cargar el Temporizador
			Tempo = Temporizador.Tiempito(self.fontPuntaje, (128, 67))
			# Instancia del Objeto Puntaje
			puntos = Puntaje.Score(self.fontPuntaje, (890, 67))
			# Verificar que el jugador gano o perdio
			enJuego = True
			#Construye el Menu Principal Izquierda Derecha
			if actividad == 1 or actividad == 2:
				if not done:
					self.buildMenu()
			elif actividad == 3 or actividad == 4:
				if not done:
					self.buildMenuArriba()

			while screenloop:
				# Regulamos los frames por segundo
				self.clock.tick(30)
				# Obtenemos el tiempo del Juego en Milisegundos
				tiempo = pygame.time.get_ticks()/1000
				#print "Tiempo actual: " + str(tiempo)
				# Llamar a la funcion que inicializa el tiempo
				Tempo.tiempo_sube()
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
					if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
						pygame.time.wait(5000)
					if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
						self.MenuJuegos()
					# Controlamos el cliqueo del mouse
					if actividad == 1 or actividad == 2:
						if enJuego == True:
							if e.type == pygame.MOUSEBUTTONDOWN:
								screenloop = True
								opcion = self.menuFuncs[self.itemNames[self.activeFocus]]()
								# Verificar cual de los botones se ha pulsado
								if identidad == "izquierda" and actividad == 1:
									puntos.score_up()
									#screen.blit(Texto, (320,300))
								if identidad == "derecha" and actividad == 2:
									puntos.score_up()

					# Controlamos el cliqueo del mouse
					if actividad == 3 or actividad == 4:
						if enJuego == True:
							if e.type == pygame.MOUSEBUTTONDOWN:
								screenloop = True
								opcion = self.menuFuncsArriba[self.itemNamesArriba[self.activeFocus]]()
								# Verificar cual de los botones se ha pulsado
								if identidad == "arriba" and actividad == 3:
									puntos.score_up()
								if identidad == "abajo" and actividad == 4:
									puntos.score_up()

				# Se Carga el fondo de la Imagen de Entrenamiento
				if actividad == 1:
					self.screen.blit(self.bgImageEntrenaIzquierda, (0, 0))
				elif actividad == 2:
					self.screen.blit(self.bgImageEntrenaDerecha, (0,0))
				elif actividad == 3:
					self.screen.blit(self.bgImageEntrenaArriba, (0,0))
				elif actividad == 4:
					self.screen.blit(self.bgImageEntrenaAbajo, (0,0))
				# Se muestra el tiempo de la actividad
				Tempo.update(screen)
				# Actualizar el Puntaje del jugador
				puntos.update(screen)
				# Mostrar las Caritas Feliz o Triste y la Palabra Correcta e Incorrecta
				# Actividad 1
				if identidad == "izquierda" and actividad == 1:
					self.screen.blit(TxtCorrecto, (670,320))
					self.screen.blit(spriteFeliz.image, (670,450))
				if identidad == "derecha" and actividad == 1:
					self.screen.blit(TxtIncorrecto, (120,320))
					self.screen.blit(spriteTriste.image, (150,450))
				# Actividad 2
				if identidad == "izquierda" and actividad == 2:
					self.screen.blit(TxtIncorrecto, (620,320))
					self.screen.blit(spriteTriste.image, (650,450))
				if identidad == "derecha" and actividad == 2:
					self.screen.blit(TxtCorrecto, (120,320))
					self.screen.blit(spriteFeliz.image, (120,450))
				# Actividad 3
				if identidad == "arriba" and actividad == 3:
					self.screen.blit(TxtCorrecto, (700,250))
					self.screen.blit(spriteFeliz.image, (80,150))
				if identidad == "abajo" and actividad == 3:
					self.screen.blit(TxtIncorrecto, (670,500))
					self.screen.blit(spriteTriste.image, (80,450))
				# Actividad 4
				if identidad == "arriba" and actividad == 4:
					self.screen.blit(TxtIncorrecto, (670,250))
					self.screen.blit(spriteTriste.image, (80,150))
				if identidad == "abajo" and actividad == 4:
					self.screen.blit(TxtCorrecto, (700,500))
					self.screen.blit(spriteFeliz.image, (80,450))
				# Verificar el Tiempo Transcurrido
				if Tempo.temporal == 450:
					enJuego = False

				# LLama a la Pantalla de Fin de Juego
				if enJuego == False and actividad == 1:
					listaPuntos[0] = puntos.score
					done = False
					self.Entrenamiento(2)
				elif enJuego == False and actividad == 2:
					listaPuntos[1] = puntos.score
					done = False
					self.Entrenamiento(3)
				elif enJuego == False and actividad == 3:
					listaPuntos[2] = puntos.score
					done = False
					self.Entrenamiento(4)
				elif enJuego == False and actividad == 4:
					listaPuntos[3] = puntos.score
					done = False
					self.FinJuego(listaPuntos[0],500,1)

				if actividad == 1 or actividad == 2:
					# Se establece en el menu que boton se hizo click
					self.menuItems[self.activeFocus].applyFocus(self.screen)
					self.menuItems[self.lastActiveFocus].removeFocus()

					# Se muestra el menú de la Interfaz de Entrenamiento Izquierda y Derecha
					#for item in self.menuItems:
					#	self.screen.blit(item.label, (item.xpos, item.ypos))

					#  2 lazy 2 hacen algo hermoso y universal (Parte principal)
					if mpos[0] > self.scrWidth / 2:
						self.activeFocus = 0
						self.lastActiveFocus = 1
					else:
						self.activeFocus = 1
						self.lastActiveFocus = 0

				if actividad == 3 or actividad == 4:
					# Se establece en el menu que boton se hizo click
					self.menuItemsArriba[self.activeFocus].applyFocus(self.screen)
					self.menuItemsArriba[self.lastActiveFocus].removeFocus()

					# Se muestra el menú de la Interfaz de Entrenamiento Arriba y Abajo
					#for item in self.menuItemsArriba:
					#	self.screen.blit(item.label, (item.xpos, item.ypos))

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
				self.menuItemsMenuJuegos[self.FourActiveFocus].removeFocus()

				# Se muestra el menú de la Interfaz del Menu de Juegos
				for item in self.menuItemsMenuJuegos:
					self.screen.blit(item.label, (item.xpos, item.ypos))

				#  Se ejecuta la acción de click del mouse (Parte principal)
				if mpos[1] < self.scrHeight / 5:
					self.activeFocus = 0
					self.lastActiveFocus = 1
					self.secondActiveFocus = 2
					self.thirdActiveFocus = 3
					self.FourActiveFocus = 4
				elif mpos[1] < (2*self.scrHeight) / 5:
					self.activeFocus = 1
					self.lastActiveFocus = 0
					self.secondActiveFocus = 2
					self.thirdActiveFocus = 3
					self.FourActiveFocus = 4
				elif mpos[1] < (3*self.scrHeight) /5:
					self.activeFocus = 2
					self.lastActiveFocus = 0
					self.secondActiveFocus = 1
					self.thirdActiveFocus = 3
					self.FourActiveFocus = 4
				elif mpos[1] < (4*self.scrHeight)/5:
					self.activeFocus = 3
					self.lastActiveFocus = 0
					self.secondActiveFocus = 1
					self.thirdActiveFocus = 2
					self.FourActiveFocus = 4
				else:
					self.activeFocus = 4
					self.lastActiveFocus = 0
					self.secondActiveFocus = 1
					self.thirdActiveFocus = 2
					self.FourActiveFocus = 3

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
	def FinJuego(self, puntos, TiempoJuego, NroJuego):
			global done
			global PuntajeTotal
			global TiempoTotal
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
				juego = "Entrenamiento"
			elif NroJuego == 2:
				juego = "Izquierda-Derecha"
			elif NroJuego == 3:
				juego = "Arriba-Abajo"
			elif NroJuego == 4:
				juego = "Adentro-Afuera"
			else:
				juego = "Laberinto"
			Titulo = pygame.transform.flip(self.fontFinJuego.render("Fin del Juego " + str(juego), 1, (23, 131, 191)), 1, 0)
			# Carga el Puntaje Obtenido en el JUEGO
			Marcador = pygame.transform.flip(self.fontPuntaje.render("Puntaje Obtenido: " + str(puntos), 1, (143,31,130)), 1, 0)
			# Carga el Tiempo Obtenido en el JUEGO
			TiempoFinal = pygame.transform.flip(self.fontPuntaje.render("Tiempo: " + str(TiempoJuego), 1, (143,31,130)), 1, 0)
			# Iterator boolean -> Indica a programa cuando finalizar
			# Muy importante bool para la manipulacion del raton
			dummy = False
			if not done:
				self.buildFinJuego() #Construye el Menu Principal

			while screenloop:
				self.clock.tick(30)
				PuntajeTotal = 0
				TiempoTotal = 0
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
						opcion = self.menuFuncsFinJuego[self.itemNamesFinJuego[self.activeFocus]](NroJuego)
						break;

				# Se Carga el fondo de la Imagen de Introduccion
				self.screen.blit(self.bgImageFinJuego, (0, 0))
				# Aparece El Texto de Fin del Juego
				screen.blit(Titulo,(240,10))
				if NroJuego == 2 or NroJuego == 3 or NroJuego == 5:
					# Muestra el Puntaje Obtenido por el Jugador
					screen.blit(Marcador,(350,170))
					screen.blit(TiempoFinal,(410,230))
				elif NroJuego == 1:
					y = 115
					accion = "Izquierda"
					for item in listaPuntos:
						Marcador = pygame.transform.flip(self.fontPuntaje.render("Puntaje "+ accion +" : " + str(item), 1, (143,31,130)), 1, 0)
						screen.blit(Marcador,(520,y))
						TiempoFinal = pygame.transform.flip(self.fontPuntaje.render("Tiempo "+ accion +" : 15" , 1, (143,31,130)), 1, 0)
						screen.blit(TiempoFinal,(190,y))
						# Sumar el Puntaje Total
						PuntajeTotal = PuntajeTotal + item
						y += 45
						if y == 160:
							accion = "Derecha"
						elif y == 205:
							accion = "Arriba"
						elif y == 250:
							accion = "Abajo"
					# Imprimir el Puntaje Total
					PuntosTotales = pygame.transform.flip(self.fontPuntaje.render("Puntaje Total: " + str(PuntajeTotal), 1, (143,31,130)), 1, 0)
					screen.blit(PuntosTotales,(520,295))
					# Imprimir el Tiempo Total
					TiemposTotales = pygame.transform.flip(self.fontPuntaje.render("Tiempo Total: 60", 1, (143,31,130)), 1, 0)
					screen.blit(TiemposTotales,(190,295))
				elif NroJuego == 4:
					# Imprimir el Puntaje de Todas las Acciones
					y = 115
					accion = "Adentro"
					for item in listaPuntos:
						Marcador = pygame.transform.flip(self.fontPuntaje.render("Puntaje "+ accion +" : " + str(item), 1, (143,31,130)), 1, 0)
						screen.blit(Marcador,(520,y))
						# Sumar el Puntaje Total
						PuntajeTotal = PuntajeTotal + item
						y += 45
						if y == 160:
							accion = "Afuera"
						elif y == 205:
							accion = "Encima"
						elif y == 250:
							accion = "Debajo"
					# Imprimir el Puntaje Total
					PuntosTotales = pygame.transform.flip(self.fontPuntaje.render("Puntaje Total: " + str(PuntajeTotal), 1, (143,31,130)), 1, 0)
					screen.blit(PuntosTotales,(520,295))
					# Imprimir el Tiempo de Todas las Acciones
					y = 115
					accion = "Adentro"
					for item in listaTiempo:
						TiempoFinal = pygame.transform.flip(self.fontPuntaje.render("Tiempo "+ accion +" : " + str(item), 1, (143,31,130)), 1, 0)
						screen.blit(TiempoFinal,(190,y))
						# Sumar el Tiempo Total
						TiempoTotal = TiempoTotal + item
						y += 45
						if y == 160:
							accion = "Afuera"
						elif y == 205:
							accion = "Encima"
						elif y == 250:
							accion = "Debajo"
					# Imprimir el Tiempo Total
					TiemposTotales = pygame.transform.flip(self.fontPuntaje.render("Tiempo Total: " + str(TiempoTotal), 1, (143,31,130)), 1, 0)
					screen.blit(TiemposTotales,(190,295))

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

	# Pantalla De Instrucciones
	def Instrucciones(self, NroJuego):
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
			# Cargar el Nombre de Cada VideoJuego y el Fondo de las Instrucciones
			if NroJuego == 1:
				TituloJuego = "Entrenamiento"
				self.bgImageInstrucciones = pygame.transform.flip(pygame.image.load("Imagenes/FondoInstEntrenamiento.jpg").convert(), 1, 0)
			elif NroJuego == 2:
				TituloJuego = "Izquierda, Derecha"
				self.bgImageInstrucciones = pygame.transform.flip(pygame.image.load("Imagenes/FondoInstIzquierdaDerecha.jpg").convert(), 1, 0)
			elif NroJuego == 3:
				TituloJuego = "Arriba, Abajo"
				self.bgImageInstrucciones = pygame.transform.flip(pygame.image.load("Imagenes/FondoInstArribaAbajo.jpg").convert(), 1, 0)
			elif NroJuego == 4:
				TituloJuego = "Adentro Afuera"
				self.bgImageInstrucciones = pygame.transform.flip(pygame.image.load("Imagenes/FondoInstAdentroAfuera.jpg").convert(), 1, 0)
			else:
				TituloJuego = "Laberinto"
				self.bgImageInstrucciones = pygame.transform.flip(pygame.image.load("Imagenes/FondoInstLaberinto.jpg").convert(), 1, 0)
			# Carga el Titulo de las Instrucciones
			Titulo = pygame.transform.flip(self.fontFinJuego.render("Instrucciones del Juego: " + str(TituloJuego), 1, (0, 0, 255)), 1, 0)
			# Carga el Puntaje Obtenido en el JUEGO
			# Iterator boolean -> Indica a programa cuando finalizar
			# Muy importante bool para la manipulacion del raton
			dummy = False
			if not done:
				self.buildMenuInstrucciones() #Construye el Menu Principal

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
					if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
						pygame.mixer.music.fadeout(1000)
						self.MenuJuegos()

					elif e.type == pygame.MOUSEBUTTONDOWN:
						screenloop = True
						opcion = self.menuFuncsInstrucciones[self.itemNamesInstrucciones[self.activeFocus]](NroJuego)
						break;

				# Se Carga el fondo de la Imagen de Introduccion
				self.screen.blit(self.bgImageInstrucciones, (0, 0))
				# Aparece El Titulo de las Instrucciones
				screen.blit(Titulo,(150,10))
				# Se usa para que aparezca las imagenes que dan la vuelta
				self.floatingPicture()
				# Se establece en el menu que boton se hizo click (Aqui Aparece el error: List index out of range)
				try:
					self.menuItemsInstrucciones[self.activeFocus].applyFocus(self.screen)
					self.menuItemsInstrucciones[self.lastActiveFocus].removeFocus()
				except IndexError:
					print "Asignacion de Juego " + str(NroJuego)

				# Se muestra el menú de la Interfaz de Introduccion
				for item in self.menuItemsInstrucciones:
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
