# -*- coding: utf-8 -*-
import pygame

# La clase Pared es un sprite que representa cada uno de los dibujos que forman
# las paredes. Las imágenes son h.png, v.png, id.png, etc. A efectos de hacer
# las cosas bien y que encajen las piezas, todas las imágenes tienen 40x40 pixeles
# de tamaño. Las paredes tienen un grosor de 20 pixeles y el margen, en caso de
# que exista, es de 10 pixeles. Si te fijas en las imágenes, lo comprenderás.
# Las defino como sprites para poder detectar cuando choca el jugador con ellas
# y, por tanto, no puede pasar.

class Pared(pygame.sprite.Sprite):
    def __init__(self, imagen, pos):
        pygame.sprite.Sprite.__init__( self )
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Queso(pygame.sprite.Sprite):

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

# La clase Mapa representa el mapa del nivel de nuestro juego. El mapa se ha escrito
# previamente en un archivo de texto y se convierten los diferentes caracteres que
# se encuentran al leerlo en dibujos.

class Mapa:
    def __init__(self, archivo):

        # grupo contiene a todos los sprites de las paredes

        self.grupo = pygame.sprite.RenderUpdates()
        self.quesos = pygame.sprite.RenderUpdates()

        # Cargamos las diferentes imágenes de las piezas de las paredes

        self.h=pygame.image.load('Imagenes/h.png').convert_alpha()
        self.v=pygame.image.load('Imagenes/v.png').convert_alpha()
        self.sd=pygame.image.load('Imagenes/sd.png').convert_alpha()
        self.id=pygame.image.load('Imagenes/id.png').convert_alpha()
        self.ii=pygame.image.load('Imagenes/ii.png').convert_alpha()
        self.si=pygame.image.load('Imagenes/si.png').convert_alpha()
        self.q=pygame.image.load('Imagenes/q.png').convert_alpha()

        # En la variable textoMapa se almacenan las líneas del archivo que
        # continene el mapa.



        archivo = open(archivo)
        self.textoMapa = archivo.readlines()
        archivo.close()

        # Recorremos los caracteres, línea a línea, y generamos el sprite que
        # representa cada una de ellas, añadiéndolo al grupo de sprites.

        fila = -1
        for linea in self.textoMapa:
            fila += 1
            columna = -1
            for c in linea:
                columna += 1

                # Tenemos los valores de fila y columna donde va el sprite.
                # Los convertimos en pixeles para saber donde está su
                # situación real en pantalla.

                x,y = self.aPixel(fila,columna)

                # Cada carácter codifica un dibujo de pared distinto.

                if c == '-':
                    self.grupo.add(Pared(self.h, (x,y)))
                elif c == '|':
                    self.grupo.add(Pared(self.v, (x,y)))
                elif c == '7':
                    self.grupo.add(Pared(self.sd, (x,y)))
                elif c == 'J':
                    self.grupo.add(Pared(self.id, (x,y)))
                elif c == 'L':
                    self.grupo.add(Pared(self.ii, (x,y)))
                elif c == 'T':
                    self.grupo.add(Pared(self.si, (x,y)))
                elif c == 'k':
					self.quesos.add(Queso(self.q, (x,y)))

    # La función actualizar dibuja en pantalla el nivel. Aunque nuestras paredes
    # son fijas, el caso más general es que éstas se movieran; así lo que se hace
    # es borrar la pantalla con color blanco, actualizar la posición de los
    # sprites y dibujarlos. Fíjate que la surface donde se ha de dibujar todo
    # se le pasa a la función como parámetro.



    def actualizar(self, visor):
        #visor.fill((255,255,255))
        self.grupo.update()
        self.grupo.draw(visor)
        self.quesos.update()
        self.quesos.draw(visor)

    # aPixel es una función que convierte las coordenadas de un sprite, fila y
    # columna, en los pixeles reales donde se situa en pantalla. Recuerda que
    # estamos trabajando con una pantalla de 800x600 pixeles y que nuestro mapa
    # tiene 20 columnas (20 caracteres por línea en el archivo) y 15 filas
    # (15 líneas en el archivo). Así, cada dibujo de los sprites es de 40x40
    # pixeles (40x20 = 800, 40x15 = 600)

    def aPixel(self, fila, columna):
        return (columna*40, fila*40)

    # aCuadricula hace lo contrario. Dada una posición en pixeles en Pantalla
    # averigua cuál es la fila y la columna correspondientes en el mapa.

    def aCuadricula(self, x, y):
        return (y/40, x/40)
