#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame

class imagenArbol( pygame.sprite.Sprite ):

    def __init__( self, posX, posY ):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('Imagenes/arbol.png')
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

        self.rect.topleft = (posX, posY)

        self.dy = 0
        self.dx = 0

    def update(self):

        self.pos = self.rect.topleft

        self.rect.move_ip(self.dx,self.dy)

    def deshacer(self):

        self.rect.topleft = self.pos
