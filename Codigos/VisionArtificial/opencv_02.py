import numpy
import cv2
from matplotlib import pyplot as plt


def main():


    #Cargar Imagen
    img= cv2.imread("image/carro.jpg")

    #Cargar Imagen a escala de grises
    img= cv2.imread("image/carro.jpg",cv2.IMREAD_GRAYSCALE)

    #Guardar una Imagen
    cv2.imwrite('carro2.png',img)


    #Mostrar La imagen, esperar tecla para cerrar y destruir ventanas
    cv2.imshow('imagen carro',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    matplotlib()
    
    return

def matplotlib():

    img = cv2.imread('image/carro.jpg')
    plt.imshow(img)
    plt.xticks([]), plt.yticks([])
    plt.show()


    return





if __name__ == '__main__':
    main()
