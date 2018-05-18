import cv2

# Cargamos la imagenes
imagen = cv2.imread("imagenes/robot.jpg")

# Obtener region cuadrada
region = imagen[0:150,0:150]
cv2.imshow("region", region)
cv2.waitKey(0)

# Cambiar el color de una region
imagen[50:180,30:250]=(255,0,0)
cv2.imshow("imagen",imagen)
cv2.waitKey(0)
