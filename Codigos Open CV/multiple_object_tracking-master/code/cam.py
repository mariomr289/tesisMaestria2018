#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################
################## Detección de multiples objetos #####################
#######################################################################
# Desarrollado por:
#
# LED 		: https://www.youtube.com/c/LEDTurnOn
# Facebook	: https://www.facebook.com/ProyectosIE/
#
# 1. El programa tiene configuración manual del rango de detección.
# 2. El programa puede detectar multiples objetos.
#----------------------------------------------------------------------

# Importando OpenCV y Numpy
import cv2
import numpy as np

#----------------------------------------------------------------------
# paint(event, x, y, flags, param)
#	Dibujar un rectangulo indicando el área seleccionada.
#
# Valores de Iniciación:
down = False
xi, yi = 0, 0
xf, yf = 0, 0 
# event  : Detecta las acciones realizadas con el mouse y
#		   su valor es un número entero.
#
#	cv2.EVENT_LBUTTONDOWN --> 1
#	cv2.EVENT_MOUSEMOVE	  --> 0
# 	cv2.EVENT_LBUTTONUP   --> 4
#
# x, y   : Posición actual del mouse.
# xi, yi : Posición inicial del mouse.
# xf, yf : Posición final del mouse.
#
# variables globales: down,xi,yi,xf,yf,p
#	p   : Si se terminó de seleccionar procede con la función 'webcam'.	  	
# 	down: 
#		True : Si el botón izquierdo fue pulsado.
#		False: Si el botón izquierdo se dejo de pulsar.
#
# Puede ver el video 'Python & OpenCV: Pizarra Virtual'
# para comprender mejor cada linea de esta función.
# link --> 'https://youtu.be/Q9FrmJK7rMA'
#
#----------------------------------------------------------------------

def paint(event, x, y, flags, param):
	global down,xi,yi,xf,yf,p
	if event == cv2.EVENT_LBUTTONDOWN:
		xi, yi = x, y
		down = True

	elif event == cv2.EVENT_MOUSEMOVE and down == True:
		if down == True:
			board[:]=0
			cv2.rectangle(board,(xi,yi),(x,y),(0,255,0),3)
			xf, yf = x, y

	elif event == cv2.EVENT_LBUTTONUP:
			down = False
			p = True

#----------------------------------------------------------------------
# webcam(cam, color_avr)
#	Inicia la cámara y detecta el área de la imágen que se encuentra
#	dentro del rango de valores de detección.
#
# cam   	: Objeto 'VideoCapture' recibido desde la función 'main'
# color_avr : Color promedio del área seleccionada.
# 
# Puede ver el video 'Python | Detección de objetos con OpenCV'
# para comprender mejor cada linea de esta función.
# link --> 'https://youtu.be/CppgV8inf7g'
#
# add(m, num)
# 	Fija las reglas para la suma de un número(num) a todos los elementos 
# 	de una vector(m).
#	
# Si al sumar el número, el resultado excede a 255 se reemplaza por 255.
# Si al sumar el número, el resultado es negativo se reemplza por 0.
# 	
#----------------------------------------------------------------------

def webcam(cam,color_avr):
	kernel=np.ones((5,5),np.uint8)
	def add(m,num):
		output = np.array([0,0,0],np.uint8)
		for i,e in enumerate(m):
			q = e+num
			if q>=0 and q<=255: output[i] = q
			elif q>255: output[i]=255
			else: output[i] = 0
		return output
	rangomax = add(color_avr,15)
	rangomin = add(color_avr,-15)
	print 'color_avr:\t',color_avr
	print 'rangomin :\t',rangomin
	print 'rangomax :\t',rangomax
	while(True):
		ret,frame=cam.read()
		mascara=cv2.inRange(frame,rangomin,rangomax)
		opening=cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)
		contours,hierarchy = cv2.findContours(opening,1,2)
		for cnt in contours:
			if np.size(cnt) > 500:
				x,y,w,h=cv2.boundingRect(cnt)
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
				cv2.circle(frame,(x+w/2,y+h/2),5,(0,0,255),-1)
		cv2.imshow("cam",frame)
		k=cv2.waitKey(1) & 0xFF
		if k==27:
			break
	cam.release()
	cv2.destroyAllWindows()

#----------------------------------------------------------------------
# main: función principal
#	Genera la captura de imágenes para poder seleccionar el área a 
#	detectar.
#	
# variables globales: board, p
#
# cam	: Objeto 'VideoCapture', para la captura de imágenes.
# p 	: Si es verdadero(True) se procede con la función 'webcam'.
# board : Se genera una matriz de la misma dimension de imágenes
#		  capturadas.
#
#----------------------------------------------------------------------
def main():
	global board,p
	p = False
	cam = cv2.VideoCapture(0)
	board = np.zeros((int(cam.get(4)),int(cam.get(3)),3),dtype=np.uint8)
	while(True):
		ret,frame=cam.read()
		cv2.namedWindow('board')
		cv2.setMouseCallback('board', paint)
		dst = cv2.addWeighted(frame,1,board,1,0)
		cv2.imshow('board',dst)
		k=cv2.waitKey(1) & 0xFF
		if k==27 or p:
			break
	cv2.destroyAllWindows()
	if xi!=xf and yi!=yf:
		ext = frame[yi:yf,xi:xf] # ext: Se extrae frame  
								 #		desde (xi,yi) a (xf,yf).
		s=np.array([0,0,0])
		for i in range(np.shape(ext)[0]):
			for j in range(np.shape(ext)[1]):
				s+=ext[i][j]
		webcam(cam,s/((i+1)*(j+1)))

if __name__=='__main__':
	print 
	print "Comandos"
	print "======================"
	print
	print "Salir: \t\t\t[ESC]\n"
	main()
	
	
	
