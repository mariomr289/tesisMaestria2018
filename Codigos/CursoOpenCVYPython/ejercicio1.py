import cv2

# Cargar Imagen Original
image_path = 'examples/images/Super_Mario.png'
image = cv2.imread(image_path)

# Cargar Imagen en Escala de Grises
image_path = 'examples/images/Super_Mario.png'
image_gray = cv2.imread(image_path,0)

# Guardar la imagen en Escala de Grises
image_copy_path = 'examples/images/Super_Mario_Copia.png'
cv2.imwrite(image_copy_path, image_gray)

# Mostrar Imagen
cv2.imshow('Original', image)
cv2.imshow('Copia Escala de Grises', image_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
