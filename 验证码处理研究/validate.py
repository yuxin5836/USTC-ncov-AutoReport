import pytesseract
from PIL import Image, ImageDraw
import numpy as np
import cv2
image=cv2.imread('t.png')
kernel = np.ones((3,3),np.uint8)
image = cv2.dilate(image,kernel,iterations = 1)
image = Image.fromarray(image)
image.show()
text=pytesseract.image_to_string(image)
print(text)

