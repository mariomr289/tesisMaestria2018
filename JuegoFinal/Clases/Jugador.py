#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase Para la Nena de la Canasta
class NenaCanasta(pygame.sprite.Sprite):
	def __init__(self, scrWidth, scrHeight):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNena = pygame.image.load('Imagenes/NenaCanasta.png')
		self.ImagenPerder = pygame.image.load('Imagenes/NenaPierde.png')
		self.rect = self.ImagenNena.get_rect()
		self.rect.centerx = scrWidth/2
		self.rect.centery = scrHeight-60

		self.listaDisparo = []
		self.Vida = True

		self.velocidad = 20

		self.sonidoPerder = pygame.mixer.Sound("Sonidos/endGame.wav")

	"""Nuevos Cambios (Metodos)"""
	def movimientoDerecha(self):
		self.rect.right -= self.velocidad
		self.__movimiento()

	def movimientoIzquierda(self):
		self.rect.left += self.velocidad
		self.__movimiento()

	# Identificar que la nena no se salga de la pantalla
	def __movimiento(self):
		if self.Vida == True:
			if self.rect.left <= 10:
				self.rect.left = 10
			elif self.rect.right > 1014:
				self.rect.right = 1014

	# Funcion para cuando pierda el juego
	def destruccion(self):
		self.sonidoPerder.play()
		self.Vida = False
		self.velocidad = 0
		self.ImagenNena = self.ImagenPerder

	def dibujar(self, screen):
		screen.blit(self.ImagenNena, self.rect)
