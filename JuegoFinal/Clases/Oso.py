#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
#Clase Osito para el JuegoMoverObjetos
class Osito(pygame.sprite.Sprite):
	def __init__(self, scrWidth, scrHeight, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenOso = pygame.image.load("Imagenes/mario.png")
		self.rect = self.ImagenOso.get_rect()
		self.click = False
		self.rect.centerx = posx
		self.rect.centery = scrHeight - posy
		# Posición en X del Oso en la pantalla invertida
		self.PosOsoX = scrWidth - self.rect.centerx

	def update(self,screen, scrWidth):
		if self.click:
			# Obtiene la posicion del Mouse
			self.rect.center = pygame.mouse.get_pos()
			# Obtener la posicion del Oso en la pantalla invertida
			self.PosOsoX = scrWidth - self.rect.centerx
		# dibuja el oso cada vez que se mueve el mouse
		screen.blit(self.ImagenOso, (self.PosOsoX - 100, self.rect.centery - 100))
