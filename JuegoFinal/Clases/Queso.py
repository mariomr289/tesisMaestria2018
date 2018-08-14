#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame

class Quesito(pygame.sprite.Sprite):

    def __init__(self, imagen, pos):
        pygame.sprite.Sprite.__init__( self )
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect_colision = self.rect.inflate(-30, -10)
        self.delay = 0
        self.se_puede_comer = True
        self.rect.topleft = pos

    def update(self):
        pass

    def update_desaparecer(self):
        self.delay -= 1
        if self.delay < 1:
            self.kill()


    def comer(self):
        self.delay = 30
        self.update = self.update_desaparecer
        self.se_puede_comer = False
