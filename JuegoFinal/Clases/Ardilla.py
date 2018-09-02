#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame

class imagenArdillita( pygame.sprite.Sprite ):

    def __init__( self, posX, posY ):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('Imagenes/raton1.png').convert()
        self.imagePerder = pygame.image.load('Imagenes/menuico.png').convert()
        self.image.set_colorkey((255,255,255))
        self.imagePerder.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

        self.vida = True
        self.sonidoPerder = pygame.mixer.Sound("Sonidos/endGame.wav")

        # Aprovechando el constructor de la clase, situamos la posicion inicial
        # del sprite en las coordenadas posX y posY


        self.rect.topleft = (posX, posY)


         # dy y dx son las velocidades verticales del sprite. Inicialmente son 0.

        self.dy = 0
        self.dx = 0

    def update(self):

        # Cuando se mueve el sprite se usa esta funcion. Pero ahora hay que ir con
        # cuidado. Si se mueve el sprite y hay colision con la pared, en realidad
        # no se deberia poder mover. Asi que necesitamos una manera de deshacer
        # el movimiento y que no se muestre realmente en pantalla. ¿Cómo hacerlo?
        # Lo que hacemos es almacenar en la variable pos la posición del sprite
        # antes de que se mueva, así para deshacer el movimiento sólo hay que
        # volver a colocar el sprite en donde indica pos.



        if self.vida == True:
            self.pos = self.rect.topleft
            # Una vez hecho eso, ya podemos hacer la tentativa de mover el sprite.
            self.rect.move_ip(self.dx,self.dy)

    def deshacer(self):

        # Ésta es la función en la que deshacemos el movimiento, si hace falta.
        # Como hemos dicho, ponemos el srpite donde estaba antes, en pos.


        self.rect.topleft = self.pos

    # Funcion para cuando pierda el JUEGO
    def destruccion(self):
        self.sonidoPerder.play()
        self.vida = False
        self.image = self.imagePerder
