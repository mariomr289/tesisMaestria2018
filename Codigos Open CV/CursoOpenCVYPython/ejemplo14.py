import cv2
from matplotlib import pyplot as plt

# Load
image_path = 'examples/images/rabbit.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Histogram & plot
plt.hist(image.ravel(), 256, [0, 255]);
plt.xlim([0, 255])
plt.show()
