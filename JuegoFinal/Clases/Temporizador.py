#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
# Clase para el Puntaje de los Juegos
class Tiempito(pygame.sprite.Sprite):
    def __init__(self, font, pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.pos = pos
        self.temporal = 0
        self.segundos = 0
        self.image = self.font.render(str(self.temporal),0,(255,255,255))
        self.rect = self.image.get_rect(center = self.pos)

    def tiempo_sube(self):
        self.temporal += 1
        self.segundos = self.temporal / 30

    def update(self, screen):
        self.image = pygame.transform.flip(self.font.render("Tiempo: " + str(self.segundos), 1, (255, 255, 255)), 1, 0)
        self.rect = self.image.get_rect(center = self.pos)
        screen.blit(self.image, self.rect)

    def update_actividad(self, screen):
        self.image = pygame.transform.flip(self.font.render("Tiempo Actividad: " + str(self.segundos), 1, (255, 255, 255)), 1, 0)
        self.rect = self.image.get_rect(center = self.pos)
        screen.blit(self.image, self.rect)
