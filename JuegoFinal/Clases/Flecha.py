#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase para las Flechas de dirección
class Flechita(pygame.sprite.Sprite):
	def __init__(self, scrWidth, scrHeight):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenPez = pygame.image.load('Imagenes/PECESITA2.png')
		self.ImagenPerder = pygame.image.load('Imagenes/explosion.jpg')
		self.rect = self.ImagenPez.get_rect()
		self.rect.centerx = scrWidth - 100
		self.rect.centery = scrHeight/2
