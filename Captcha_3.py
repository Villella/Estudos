#chamando as bibliotecas necessárias
import cv2
import numpy as np
import pytesseract
from PIL import Image
import urllib
from urllib.request import urlopen

#chamando a imagem da URL utilizando a urllib / urlopen
req = urlopen("https://publicodetran.es.gov.br/captcha.asp")
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)

#preparando o kernel para rodar o comando de dilatação mais à frente
kernel = np.ones((5,5), np.uint8)

#colocando a imagem da url na coloração preto e branco com a escala cinza do OpenCV
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"""linha de código colocada como comentário pois não foi necessário inverter a coloração para negativa"""
#img = cv2.bitwise_not(img)

#aumentando o tamanho da imagem
img = cv2.resize(img, None, fx = 2, fy = 2)

#rodando o comando de dilatação da imagem para facilitar a leitura do pytesseract
kernel = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
dilated = cv2.dilate(img, kernel, iterations= 1)

#removendo a coloração cinza do fundo da imagem
ret, img = cv2.threshold(img, 135, 255, cv2.THRESH_BINARY)

#otimizando a imagem para facilitar a leitura pelo pytesseract
ret2, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#colocando efeito para melhorar a qualidade da imagem (desembaçamento), facilitando leitura do pytesseract
blur = cv2.GaussianBlur(img, (1, 1), 0)
ret3, img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#criando um arquivo no diretório após a aplicação de todas as camadas de aperfeiçoamento da imagem, mostrando em tela até que algo seja pressionado e o programa extraia o texto.
cv2.imwrite("otimizada.jpg", img)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#tesseract puxa a imagem trabalhada, com algumas configurações definidas para que facilite o entendimento do texto, deixando explicito quais caracteres poderão ser utilizados, removendo os espaços entre caracteres e colocando tudo em minúsculo.
texto = pytesseract.image_to_string(img, config= '--psm 8 --dpi 300 --oem 0 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ').replace(" ", "").lower()
#apresentação do texto após OpenCV e Pytesseract
print(texto)