########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#
#######################################

from enlace import *
import numpy as np
import struct

class Protocolo:

    def __init__(self, port):
        self.com1 = enlace(port)
        self.com1.enable()
        print("#################### Port Opened ####################")

        self.headSize = 10
        self.EOPSize = 4
        self.payloadMaxSize = 114

    def montaHead(self, data):
        if len(data) != self.headSize:
            print("[ERRO] O tamanho do HEAD é inválido.")

        # To-Do: Completar função para montar o Head do Datagrama
        return 

    def montaEOP(self):

        # To-Do: Completar função para montar o EOP
        return b'\xba\xba\xb0\xe1'

   # Note to self: a função que abre, le e fragmenta (monta os pacotes)
   # vai ser feito pelo Bernardo. Por enquanto posso assumit que vou trabalhar 
   # com uma lista, em que cada elemento da lista é um pacote com 114 bytes

    def montaDatagrama(self, dataHead, dataEOP, package):

        # To-Do: Completar função que monta o Datagrama. 
        # Dependências: funções montaHead, montaEOP, montaPayload

        head = self.montaHead(dataHead)
        eop = self.montaEOP(dataEOP)
        

        txBuffer = b'' + head + package + eop

        return txBuffer

    def sendingLoop(self, packages):
        for package in packages:
            txBuffer = self.montaDatagrama(package)
            self.sendData(txBuffer)
            time.sleep(0.005)

    def sendData(self, txBuffer):
        return self.com1.sendData(txBuffer)

    def getData(self, nRxBuffer):
        return self.com1.getData(nRxBuffer)

