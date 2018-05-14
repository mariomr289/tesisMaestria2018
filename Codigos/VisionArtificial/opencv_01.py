import numpy
import cv2


imagen= cv2.imread("image/carro.jpg")

cv2.imshow("Ventana de imagen", imagen)

cv2.waitKey(0)