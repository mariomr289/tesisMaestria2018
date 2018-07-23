import pygame
from random import randint
import Huevo
# Clase para la Gallina que es el Enemigo
class Gallina(pygame.sprite.Sprite):
	def __init__(self, posx, posy, distancia, imagenUno, imagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.imagenA = pygame.image.load(imagenUno)
		self.imagenB = pygame.image.load(imagenDos)

		self.listaImagenes = [self.imagenA, self.imagenB]
		self.posImagen = 0

		self.imagenGallina = self.listaImagenes[self.posImagen]
		self.rect = self.imagenGallina.get_rect()

		self.listaDisparo = []
		self.velocidad = 10
		self.rect.top = posy
		self.rect.left = posx

		self.rangoDisparo = 2
		self.tiempoCambio = 1

		self.derecha = True
		self.contador = 0
		self.Maxdescenso = self.rect.top + 40

		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx - distancia

	def dibujar(self, screen):
		self.imagenGallina = self.listaImagenes[self.posImagen]
		screen.blit(self.imagenGallina, self.rect)

	def comportamiento(self, tiempo):
		# algoritmo de comportamiento
		self.__movimientos()

		self.__ataque()
		# Animacion de la Gallina
		if self.tiempoCambio != tiempo:
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaImagenes)-1:
				self.posImagen = 0

	def __movimientos(self):
		#if self.contador < 3:
			self.__movimientoLateral()
		#else:
		#	self.__descenso()

	def __descenso(self):
		if self.Maxdescenso == self.rect.top:
			self.contador = 0
			self.Maxdescenso = self.rect.top + 40
		else:
			self.rect.top += 1

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left = self.rect.left + self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False

				self.contador += 1
		else:
			self.rect.left = self.rect.left - self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True

	def __ataque(self):
		# Numero de Huevos que Pone la gallina
		if (randint(0,150) < self.rangoDisparo):
			self.__disparo()

	def __disparo(self):
		x,y = self.rect.center
		miHuevo = Huevo.Huevo(x,y,"Imagenes/HuevoFinal.png", False)
		self.listaDisparo.append(miHuevo)
