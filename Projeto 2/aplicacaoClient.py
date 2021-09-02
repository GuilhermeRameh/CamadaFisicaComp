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
import struct

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
    byteList = b''
    i = 0
    sizeList = random.randint(10,30)
    print(sizeList)
    numberCommands = struct.pack('B', sizeList)
    while(i < sizeList):
        randIndex = random.randint(0,5)
        if len(commandList[randIndex]) == 2:
            byteList += b'\x11'
        byteList += commandList[randIndex]
        i +=1
    byteSize = len(byteList)
    return byteList, byteSize, numberCommands      

def main():
    sending = True
    receive = False
    txBuffer, bufferLen, nCommands = generateRandomBytes()
    while sending:
        try:
            #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
            #para declarar esse objeto é o nome da porta.
            com1 = enlace(serialName)


            # Ativa comunicacao. Inicia os threads e a comunicação seiral
            com1.enable()
            print('Comunication established. \nPort Open...')
            while not receive:
                print("\nComencing Transmission:...\nsending {}".format(bufferLen))
                com1.sendData(np.asarray(bufferLen))
                rxBuffer, nRx = com1.getData(1)
                print('\nReceiving Transmission:...\nreceiving {}'.format(rxBuffer))
                if rxBuffer == b'\x45':
                    receive = True

            print("\nComencing Transmission:...\nsending {}".format(txBuffer))

            com1.sendData(txBuffer)

            while receive:
                com1.rx.clearBuffer()
                rxBuffer, nRx = com1.getData(1)
                print("\nAwaiting response:...\nreceiving {}".format(rxBuffer))
                if rxBuffer == nCommands:
                    com1.sendData(b'\x35')
                    print("\nTamanho recebido correto")
                    # Encerra comunicação
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    com1.disable() 
                    sending = False
                    receive = False
                else:
                    print("\nMensagem enviada errada\nIniciando novo envio")
                    receive = False

        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
