import pygame
# Clase para el Huevo de la Gallina
class Huevo(pygame.sprite.Sprite):
	def __init__(self, posx, posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)

		self.imageHuevo = pygame.image.load(ruta)

		self.rect = self.imageHuevo.get_rect()

		self.velocidadDisparo = 2

		self.rect.top = posy
		self.rect.left = posx

		self.disparoPersonaje = personaje

	def trayectoria(self):
		if self.disparoPersonaje == True:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def dibujar(self, screen):
		screen.blit(self.imageHuevo, self.rect)
