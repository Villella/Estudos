import cv2
import numpy as np
import pytesseract
from PIL import Image
import urllib
from urllib.request import urlopen


req = urlopen("http://multas.detran.rj.gov.br/gaideweb2/captcha")
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)

kernel = np.ones((5,5), np.uint8)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#img = cv2.bitwise_not(img)

img = cv2.resize(img, None, fx = 2, fy = 2)

kernel = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
dilated = cv2.dilate(img, kernel, iterations= 1)

ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

ret2, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

blur = cv2.GaussianBlur(img, (5, 5), 0)
ret3, img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imwrite("otimizada.jpg", img)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

texto = pytesseract.image_to_string(img, config= '--psm 8 --dpi 300 --oem 0 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ').replace(" ", "").lower()
print(texto)