import pygame
# Clase para un elemento de menu (welp, en realidad tenemos dos elementos de menu, pero lo que sea)
class MenuItem(pygame.font.Font):
	def __init__(self, name, xpos, ypos, width, height, font, fontColor):
		self.name = name
		self.xpos = xpos
		self.ypos = ypos
		self.width = width
		self.height = height
		self.font = font
		self.fontColor = fontColor
		self.label = pygame.transform.flip(self.font.render(self.name, 1, self.fontColor), 1, 0)
		self.itemImage = pygame.image.load("Imagenes/menuico.png").convert()
		self.itemImage.set_colorkey((255, 255, 255))

	# Controles, si las coordenadas dadas estan en el marco del objeto
	def isMouseSelect(self, (xpos, ypos)):
		if(xpos >= self.xpos and xpos <= self.xpos + self.width) and \
			(ypos >= self.ypos and ypos <= self.ypos + self.height):
				return True

		return False

	# Se aplica el foco en el elemento de menu real
	def applyFocus(self, screen):
		self.label = pygame.transform.flip(self.font.render(self.name, 1, (255, 0, 0)), 1, 0)
		self.label = pygame.transform.smoothscale(self.label, (self.width + 25, self.height + 25))
		screen.blit(self.itemImage, (self.xpos - 70, self.ypos + 25))

	# Elimina el foco del elemento de menu real
	def removeFocus(self):
		self.label = pygame.transform.flip(self.font.render(self.name, 1, self.fontColor), 1, 0)
		self.label = pygame.transform.smoothscale(self.label, (self.width, self.height))
