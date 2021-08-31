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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        print('Comunicação estabelecida. \nPort Open...')
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        '''
        PRIMEIRA ETAPA:
        recebendo a array de bytes que contém o tamanho da 
        próxima array de comandos. 
        '''

        print("Receiving...")
        receiving = True
        printTest = True

        while receiving:
            rxBuffer, nRx = com1.getData(1)
            if nRx != None and printTest:
                print("Comunicação estabelecida, aguarde o recebimento de Dados :)")
                txBuffer = b'\x45'
                com1.sendData(txBuffer)
                '''
                Note to self: Por algum motivo não conhecido pela humanidade, 
                o buffer do rx adicionava SEMPRE 7 bytes vazios b'\x00'. Perguntar
                para os professores por que fiquei muito confuso.
                Por isso também a linha abaixo chama a função 'clearBuffer'.
                '''
                com1.rx.clearBuffer()
                print(f'BufferRx: {com1.rx.buffer}')
                printTest = False
            receiving = False
        
        #Agora temos que converter o byte do tamanho para um int
        receptionSize = int.from_bytes(rxBuffer, "big")
        
        print("Número do buffer: {}".format(nRx))
        print("Tamanho da array dos comandos: {}".format(receptionSize))

        '''
        Agora podemos nos preparar para receber 
        o array de comandos
        '''
        
        print("\nRecebendo a array de Comandos...")
        receiving = True
        printTest = True

        while receiving:
            rxBuffer, nRx = com1.getData(receptionSize)
            if nRx != None and printTest:
                print("\nComunicação estabelecida, aguarde o recebimento dos COMANDOS \o-o/ \n")
                printTest = False
            receiving = False

        print("Número do buffer: {}".format(nRx))
        print("Array de Comandos: {}".format(rxBuffer))

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
