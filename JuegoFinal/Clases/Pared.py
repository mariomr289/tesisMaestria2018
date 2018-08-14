#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame

# La clase Pared es un sprite que representa cada uno de los dibujos que forman
# las paredes. Las imágenes son h.png, v.png, id.png, etc. A efectos de hacer
# las cosas bien y que encajen las piezas, todas las imágenes tienen 40x40 pixeles
# de tamaño. Las paredes tienen un grosor de 20 pixeles y el margen, en caso de
# que exista, es de 10 pixeles. Si te fijas en las imágenes, lo comprenderás.
# Las defino como sprites para poder detectar cuando choca el jugador con ellas
# y, por tanto, no puede pasar.

class Paredsita(pygame.sprite.Sprite):
    def __init__(self, imagen, pos):
        pygame.sprite.Sprite.__init__( self )
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
