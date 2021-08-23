import requests
from io import BytesIO
import pytesseract
from PIL import Image, ImageDraw
import numpy as np
import cv2
text=requests.get('https://passport.ustc.edu.cn/validatecode.jsp?type=login',stream=True).content
image=Image.open(BytesIO(text))
image=cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
kernel = np.ones((3,3),np.uint8)
image = cv2.dilate(image,kernel,iterations = 1)
image = cv2.erode(image,kernel,iterations = 1)
image = Image.fromarray(image)
image.show()
text=pytesseract.image_to_string(image)
print(text[:4])
