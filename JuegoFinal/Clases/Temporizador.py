import pygame
# Clase para el Puntaje de los Juegos
class Tiempito(pygame.sprite.Sprite):
    def __init__(self, font, pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.pos = pos
        self.temporal = 0
        self.image = self.font.render(str(self.temporal),0,(255,255,255))
        self.rect = self.image.get_rect(center = self.pos)

    def tiempo_sube(self):
        self.temporal += 1

    def update(self, screen):
        self.image = pygame.transform.flip(self.font.render("Tiempo: " + str(self.temporal), 1, (46, 255, 246)), 1, 0)
        self.rect = self.image.get_rect(center = self.pos)
        screen.blit(self.image, self.rect)
