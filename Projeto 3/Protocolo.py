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

        self.eop = b'\xba\xba\xb0\xe1'

   # Note to self: a função que abre, le e fragmenta (monta os pacotes)
   # vai ser feito pelo Bernardo. Por enquanto posso assumit que vou trabalhar 
   # com uma lista, em que cada elemento da lista é um pacote com 114 bytes

    def montaDatagrama(self, idPacote, pkgSize, pkgTotalSize, receiverId, formato, package):

        # To-Do: Completar função que monta o Datagrama. 

        # ############### Monta Head #################
        head = b'' + idPacote + pkgSize + pkgTotalSize + receiverId + b'\x00\x00' + formato

        txBuffer = b'' + head + package + self.eop

        return txBuffer

    def sendingLoop(self, packages, formato):
        pkgTotalSize = len(packages).to_bytes(2, 'big')
        reciverId = b'\x69'
        
        for i in range(len(packages)):
            package = packages[i]

            idPacote = struct.pack('B', i)
            pkgSize = struct.pack('B', len(package))

            txBuffer = self.montaDatagrama(idPacote, pkgSize, pkgTotalSize, reciverId, formato, package)
            self.sendData(txBuffer)
            time.sleep(0.005)
        print("Loop de Envio concluído!")

    def receivingLoop(self):
        receiving = True

        while receiving:
            print("Getting Head Data...")
            bufferHead, headSize = self.getData(10)
            payloadSize = bufferHead[5 - 1]
            nPacotes = bufferHead[6-1:7-1]
            print(f'\nQuantidade de Pacotes: {nPacotes}\n')
            print("Getting Payload Data...")
            bufferPayload, payloadBufferSize = self.getData(payloadSize)





    def sendData(self, txBuffer):
        return self.com1.sendData(txBuffer)

    def getData(self, nRxBuffer):
        return self.com1.getData(nRxBuffer)

