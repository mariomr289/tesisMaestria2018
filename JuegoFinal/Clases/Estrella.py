#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase Moneda que son las Estrellas que recoge el Juego Arriba Abajo
class Estrellita(pygame.sprite.Sprite):
	def __init__(self, posx, posy, distancia, imagenUno, imagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.imagenA = pygame.image.load(imagenUno)
		self.imagenB = pygame.image.load(imagenDos)

		self.listaImagenes = [self.imagenA, self.imagenB]
		self.posImagen = 0

		self.imagenMoneda = self.listaImagenes[self.posImagen]
		self.rect = self.imagenMoneda.get_rect()

		self.velocidad = 10
		self.rect.top = posy
		self.rect.left = posx

		self.tiempoCambio = 1

		self.conquista = False

		self.MaxDerecha = self.rect.left + 40

	def dibujar(self, screen):
		self.imagenMoneda = self.listaImagenes[self.posImagen]
		screen.blit(self.imagenMoneda, self.rect)

	def comportamiento(self, tiempo):
		if self.conquista == False:
			self.__Moviderecha()
			# Animacion del Enemigo
		if self.tiempoCambio != tiempo:
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaImagenes)-1:
				self.posImagen = 0

	def __Moviderecha(self):
		if self.MaxDerecha == self.rect.left:
			self.MaxDerecha = self.rect.left + 40
		else:
			self.rect.left += 1
