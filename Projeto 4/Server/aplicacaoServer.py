#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import time
import numpy as np
from PIL import Image
import io
from fileManager import *
from ProtocoloServer import Server

#use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    main = True
    server = Server(serialName)
    retorno = []

    while main:
        try:
            server.constructDatagram(b'\x01', b'\x01', b'\x01')     

        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            server.com1.disable()
            main = False

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
