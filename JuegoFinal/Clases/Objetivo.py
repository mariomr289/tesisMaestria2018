#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase Objetivo que es a donde debe mover el Jugador el Oso
class ObjetivoMover(pygame.sprite.Sprite):
	def __init__(self, posx, posy, imagenUno, imagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.imagenA = pygame.image.load(imagenUno)
		self.imagenB = pygame.image.load(imagenDos)

		self.listaImagenes = [self.imagenA, self.imagenB]
		self.posImagen = 0

		self.imagenObjetivo = self.listaImagenes[self.posImagen]
		self.rect = self.imagenObjetivo.get_rect()

		self.velocidad = 10
		self.rect.top = posy
		self.rect.left = posx

		self.tiempoCambio = 1

	def dibujar(self, screen):
		self.imagenObjetivo = self.listaImagenes[self.posImagen]
		screen.blit(self.imagenObjetivo, self.rect)

	def comportamiento(self, tiempo):
		# Animacion del Objetivo
		if self.tiempoCambio != tiempo:
			self.posImagen += 1
			self.tiempoCambio += 1

			if self.posImagen > len(self.listaImagenes)-1:
				self.posImagen = 0
