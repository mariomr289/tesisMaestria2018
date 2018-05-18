import cv2

# Cargamos la imagen del disco duro
imagen = cv2.imread("imagenes/robot.jpg")

# Mostramos ancho, alto y canales
print("ancho: {} pixels".format(imagen.shape[1]))
print("alto: {} pixels".format(imagen.shape[0]))
print("canales: {} pixels".format(imagen.shape[2]))

# Mostramos la imagen en la pantalla
cv2.imshow("visor", imagen)
cv2.waitKey(0)

# obtener el pixel(0,0)
(b, g, r) = imagen[0,0]
print("Pixel (0,0) => Roja {}, Verde {}, Azul {}".format(r,g,b))

# Cambiamos el color del pixel (0,0)
imagen[0,0] = (0,0,255)
(b, g, r) = imagen[0,0]
print("Pixel (0,0) => Roja {}, Verde {}, Azul {}".format(r,g,b))
