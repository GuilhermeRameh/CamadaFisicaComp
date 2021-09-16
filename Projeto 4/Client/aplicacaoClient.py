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
from ProtocoloClient import Client

#use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    main = True
    client = Client(serialName)
    retorno = []

    while main:
        try:
            client.flushPortTX()

            txBuffer = client.constructDatagram(b'\x01', b'\x01', b'\x66')
            client.com1.sendData(txBuffer)
            print(txBuffer)
            main = False
            client.com1.disable()

        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            client.com1.disable()
            main = False

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
