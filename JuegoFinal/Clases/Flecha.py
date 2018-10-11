#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase para las flechas
class Flechita(pygame.sprite.Sprite):
    def __init__(self, posx, posy, imagenFlecha):
        pygame.sprite.Sprite.__init__(self)

        self.imagenFlechita = pygame.image.load(imagenFlecha)
        self.rect = self.imagenFlechita.get_rect()

        self.rect.top = posy
        self.rect.left = posx

    def dibujar(self, screen):
        screen.blit(self.imagenFlechita, self.rect)
