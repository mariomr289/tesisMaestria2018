#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase para las flechas
class Botoncito(pygame.sprite.Sprite):
    def __init__(self, posx, posy, imagenBoton):
        pygame.sprite.Sprite.__init__(self)

        self.imagenBotoncito = pygame.image.load(imagenBoton)
        self.rect = self.imagenBotoncito.get_rect()

        self.rect.top = posy
        self.rect.left = posx

    def dibujar(self, screen):
        screen.blit(self.imagenBotoncito, self.rect)
