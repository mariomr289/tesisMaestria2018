#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase Pez Juego Arriba Abajo
class Pececito(pygame.sprite.Sprite):
	def __init__(self, scrWidth, scrHeight):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenPez = pygame.image.load('Imagenes/PECESITA2.png')
		self.ImagenPerder = pygame.image.load('Imagenes/PECESITA2.png')
		self.rect = self.ImagenPez.get_rect()
		self.rect.centerx = scrWidth - 100
		self.rect.centery = scrHeight/2

		self.Vida = True

		self.velocidad = 20

		self.sonidoPerder = pygame.mixer.Sound("Sonidos/endGame.wav")

	"""Nuevos Cambios (Metodos)"""
	def movimientoArriba(self):
		self.rect.top -= self.velocidad
		self.__movimiento()

	def movimientoAbajo(self):
		self.rect.bottom += self.velocidad
		self.__movimiento()

	# Identificar que la nave no se salga de la pantalla
	def __movimiento(self):
		if self.Vida == True:
			if self.rect.top <= 110:
				self.rect.top = 110
			elif self.rect.bottom > 668:
				self.rect.bottom = 668

	# Funcion para cuando pierda el juego
	def destruccion(self):
		self.sonidoPerder.play()
		self.Vida = False
		self.velocidad = 0
		self.ImagenPez = self.ImagenPerder

	def dibujar(self, screen):
		screen.blit(self.ImagenPez, self.rect)
