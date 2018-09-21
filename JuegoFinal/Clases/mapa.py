#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pygame
import Pared
import Nuez

# La clase Mapa representa el mapa del nivel de nuestro juego. El mapa se ha escrito
# previamente en un archivo de texto y se convierten los diferentes caracteres que
# se encuentran al leerlo en dibujos.

class Mapa:
    def __init__(self, archivo):

        # grupo contiene a todos los sprites de las paredes

        self.grupo = pygame.sprite.RenderUpdates()
        self.nueces = pygame.sprite.RenderUpdates()

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
                    self.grupo.add(Pared.Paredsita(self.h, (x,y)))
                elif c == '|':
                    self.grupo.add(Pared.Paredsita(self.v, (x,y)))
                elif c == '7':
                    self.grupo.add(Pared.Paredsita(self.sd, (x,y)))
                elif c == 'J':
                    self.grupo.add(Pared.Paredsita(self.id, (x,y)))
                elif c == 'L':
                    self.grupo.add(Pared.Paredsita(self.ii, (x,y)))
                elif c == 'T':
                    self.grupo.add(Pared.Paredsita(self.si, (x,y)))
                elif c == 'k':
					self.nueces.add(Nuez.Nuecesita(self.q, (x,y)))

    # La función actualizar dibuja en pantalla el nivel. Aunque nuestras paredes
    # son fijas, el caso más general es que éstas se movieran; así lo que se hace
    # es borrar la pantalla con color blanco, actualizar la posición de los
    # sprites y dibujarlos. Fíjate que la surface donde se ha de dibujar todo
    # se le pasa a la función como parámetro.



    def actualizar(self, visor):
        #visor.fill((255,255,255))
        self.grupo.update()
        self.grupo.draw(visor)
        self.nueces.update()
        self.nueces.draw(visor)

    # aPixel es una función que convierte las coordenadas de un sprite, fila y
    # columna, en los pixeles reales donde se situa en pantalla. Recuerda que
    # estamos trabajando con una pantalla de 800x600 pixeles y que nuestro mapa
    # tiene 20 columnas (20 caracteres por línea en el archivo) y 15 filas
    # (15 líneas en el archivo). Así, cada dibujo de los sprites es de 40x40
    # pixeles (40x20 = 800, 40x15 = 600)

    def aPixel(self, fila, columna):
        return (columna*32, fila*32)

    # aCuadricula hace lo contrario. Dada una posición en pixeles en Pantalla
    # averigua cuál es la fila y la columna correspondientes en el mapa.

    def aCuadricula(self, x, y):
        return (y/32, x/32)
