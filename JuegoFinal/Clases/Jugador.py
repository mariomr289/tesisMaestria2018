import pygame
# import Proyectil
# Clase Para la Nena de la Canasta
class NenaCanasta(pygame.sprite.Sprite):
	def __init__(self, scrWidth, scrHeight):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNena = pygame.image.load('Imagenes/NenaCanasta.png')
		self.ImagenExplosion = pygame.image.load('Imagenes/NenaPierde.png')
		self.rect = self.ImagenNena.get_rect()
		self.rect.centerx = scrWidth/2
		self.rect.centery = scrHeight-60

		self.listaDisparo = []
		self.Vida = True

		self.velocidad = 20

		#self.sonidoDisparo = pygame.mixer.Sound("Sonidos/laserSpace.wav")
		self.sonidoExplosion = pygame.mixer.Sound("Sonidos/short-egg-cracking.mp3")

	"""Nuevos Cambios (Metodos)"""
	def movimientoDerecha(self):
		self.rect.right -= self.velocidad
		self.__movimiento()

	def movimientoIzquierda(self):
		self.rect.left += self.velocidad
		self.__movimiento()

	# Identificar que la nena no se salga de la pantalla
	def __movimiento(self):
		if self.Vida == True:
			if self.rect.left <= 10:
				self.rect.left = 10
			elif self.rect.right > 1014:
				self.rect.right = 1014

	#def disparar(self,x,y):
	#	miProyectil = Proyectil.Proyectil(x,y,"Imagenes/bala.png", True)
	#	self.listaDisparo.append(miProyectil)
	#	self.sonidoDisparo.play()

	# Funcion para cuando pierda el juego
	def destruccion(self):
		self.sonidoExplosion.play()
		self.Vida = False
		self.velocidad = 0
		self.ImagenNena = self.ImagenExplosion

	def dibujar(self, screen):
		screen.blit(self.ImagenNena, self.rect)
