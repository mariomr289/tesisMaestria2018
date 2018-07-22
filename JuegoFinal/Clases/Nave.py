import pygame
import Proyectil
# Clase Para las Naves
class naveEspacial(pygame.sprite.Sprite):
	def __init__(self, scrWidth, scrHeight):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load('Imagenes/NenaCanasta.png')
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = scrWidth/2
		self.rect.centery = scrHeight-80

		self.listaDisparo = []
		self.Vida = True

		self.velocidad = 20

		self.sonidoDisparo = pygame.mixer.Sound("Sonidos/laserSpace.wav")

	"""Nuevos Cambios (Metodos)"""
	def movimientoDerecha(self):
		self.rect.right -= self.velocidad
		self.__movimiento()

	def movimientoIzquierda(self):
		self.rect.left += self.velocidad
		self.__movimiento()

	# Identificar que la nave no se salga de la pantalla
	def __movimiento(self):
		if self.Vida == True:
			if self.rect.left <= 22:
				self.rect.left = 22
			elif self.rect.right > 1002:
				self.rect.right = 1002

	def disparar(self,x,y):
		miProyectil = Proyectil.Proyectil(x,y,"Imagenes/bala.png", True)
		self.listaDisparo.append(miProyectil)
		self.sonidoDisparo.play()

	def dibujar(self, screen):
		screen.blit(self.ImagenNave, self.rect)
