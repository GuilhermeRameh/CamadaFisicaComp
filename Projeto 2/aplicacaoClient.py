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
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)

def generateRandomBytes():
    commandList = [b'\x00', b'\x0F', b'\xF0', b'\xFF', b'\x00\xFF', b'\xFF\x00']
    byteList = []
    i = 0
    sizeList = random.randint(10,30)
    while(i < sizeList):
        byteList.append(random.choice(commandList))
        i +=1
    return byteList      

def main():
    sending = True
    txBuffer = generateRandomBytes()
    bufferLen = len(txBuffer)
    while sending:
        try:
            #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
            #para declarar esse objeto é o nome da porta.
            com1 = enlace(serialName)


            # Ativa comunicacao. Inicia os threads e a comunicação seiral
            com1.enable()
            print('Comunication established. \nPort Open...')

            print("\n Enviando Tamanho da mensagem: {}".format(bufferLen))
            byteLen = (bufferLen).to_bytes(1,byteorder="big")
            com1.sendData(byteLen)

            print("\nComencing Transmission:...\nsending {}".format(txBuffer))

            print(type(txBuffer))
            com1.sendData(np.asarray(txBuffer))

            # Encerra comunicação
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            com1.disable() 
            sending = False

        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
