#chamando as bibliotecas necessárias
import cv2
import numpy as np
import pytesseract
from PIL import Image
import urllib
from urllib.request import urlopen

#chamando a imagem da URL utilizando a urllib / urlopen
req = urlopen("https://www.e-crvsp.sp.gov.br/gever/jcaptcha")
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)

#colocando a imagem da url na coloração preto e branco com a escala cinza do OpenCV
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#jogando a imagem com coloração negativa para que as letras brancas ficassem pretas
img = cv2.bitwise_not(img)

#aumentando o tamanho da imagem
img = cv2.resize(img, None, fx = 2, fy = 2)

#removendo a coloração cinza do fundo da imagem
ret, img = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)

#otimizando a imagem para facilitar a leitura pelo pytesseract
ret2, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

"""linha de código colocada como comentário pois o mesmo código foi modificado apenas algumas linhas para os próximos captchas
#blur = cv2.GaussianBlur(img, (5,5), 0)
#ret3, img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)"""

#criando um arquivo no diretório após a aplicação de todas as camadas de aperfeiçoamento da imagem, mostrando em tela até que algo seja pressionado e o programa extraia o texto.
cv2.imwrite("otimizada.jpg", img)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#tesseract puxa a imagem trabalhada, com algumas configurações definidas para que facilite o entendimento do texto, deixando explicito quais caracteres poderão ser utilizados, removendo os espaços entre caracteres e colocando tudo em minúsculo.
texto = pytesseract.image_to_string(img, config= '--psm 8 --dpi 300 --oem 0 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ').replace(" ", "").lower()
#apresentação do texto após OpenCV e Pytesseract
print(texto)