########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#
#######################################

from enlace import *
import numpy as np
import struct
from fileManager import *

class Protocolo:

    def __init__(self, port):
        self.com1 = enlace(port)
        self.com1.enable()
        print("#################### Port Opened ####################")

        self.headSize = 10
        self.EOPSize = 4
        self.payloadMaxSize = 114

        self.extension = ''

        self.resendBit = b'\x01'
        self.contBit = b'\x01'

        self.eop = b'\xba\xba\xb0\xe1'

   # Note to self: a função que abre, le e fragmenta (monta os pacotes)
   # vai ser feito pelo Bernardo. Por enquanto posso assumit que vou trabalhar 
   # com uma lista, em que cada elemento da lista é um pacote com 114 bytes

    def constructDatagram(self, idPacote, pkgSize, pkgTotalSize, receiverId, resendBit, continueBit, formato, package):

        # To-Do: Completar função que monta o Datagrama. 

        # ############### Monta Head #################
        head = b'' + idPacote + pkgSize + pkgTotalSize + receiverId + resendBit + continueBit + formato

        txBuffer = b'' + head + package + self.eop

        return txBuffer

    def sendingLoop(self, packages, formato):
        pkgTotalSize = len(packages).to_bytes(2, 'big')
        reciverId = b'\x69'
        print(f"\n\nTotal de pacotes a serem enviados {len(packages)}")
        for i in range(len(packages)):
            while True:
                package = bytes(packages[i])
                idPacote = struct.pack('B', i)
                pkgSize = struct.pack('B', len(package))

                txBuffer = self.constructDatagram(idPacote, pkgSize, pkgTotalSize, reciverId, b'\x00', b'\x00', formato, package)          

                self.com1.sendData(txBuffer)
                time.sleep(0.01)

                responseBuffer, nResponseBuffer = self.com1.getData(14)
                repeatStatus = responseBuffer[5].to_bytes(1, 'big')
                contStatus = responseBuffer[6].to_bytes(1, 'big')
                if contStatus == self.contBit:
                    break
                elif i+1 == len(packages):
                    break
        self.com1.disable()
        print("\n\nLoop de Envio concluído com sucesso!")

    def receivingLoop(self):
        receiving = True
        receivedArray = []

        while receiving:
            print("\n\nGetting Head Data...")
            bufferHead, headSize = self.com1.getData(10)   

            payloadId = bufferHead[0].to_bytes(1,'big')
            payloadSize = bufferHead[1]
            nPacotes = bufferHead[2:3]
            if payloadId > nPacotes:
                receiving = False
            fileExtension = bufferHead[7:9].decode('utf-8')
            print(f'\n\nQuantidade de Pacotes: {nPacotes}\n')
            print("\n\nGetting Payload Data...")
            bufferPayload, payloadBufferSize = self.com1.getData(payloadSize)

            #To-Do: Implementar uma função de timeoout

            bufferEOP, nBufferEOP = self.com1.getData(4)
            if bufferEOP != self.eop:
                print("\n\nEOP Incorreto, enviando pedido para correção de pacote...")
                sendAgainBuffer = self.constructDatagram(payloadId, b'\x00', b'\x00\x00', b'\x42', self.resendBit, b'\x00', b'\x00\x00\x00', b'\x00')
                self.com1.sendData(sendAgainBuffer)
            else:
                print("\n\nEOP correto pedindo novo envio")
                self.extension = fileExtension
                receivedArray.append(bufferPayload)
                contBuffer = self.constructDatagram(payloadId, b'\x00', b'\x00\x00', b'\x42', b'\x00', self.contBit, b'\x00\x00\x00', b'\x00')
                self.com1.sendData(contBuffer)
        self.com1.disable()
        print("\n\nRecebimento concluído com sucesso")
        return receivedArray

    def sendHandshake(self):
        send = True
        handShake = self.constructDatagram(b'\x00', b'\x00', b'\x00\x00', b'\x69', b'\x00', b'\x00', b'\x00\x00\x00', b'')
        while send:
            print("\n\nIniciando Handshake")
            self.com1.sendData(handShake)
            time.sleep(0.05)
            receivedShake, nRx = self.com1.getData(14)
            if receivedShake == handShake:
                send = False
                print("\n\nReceptor está vivo, iniciando transmissão")
            elif(receivedShake == b'\x00'):
                print("\n\nServidor inativo.")
                reenviar = input("\n Deseja tentar novamente: S/N?\n")
                if reenviar == "N":
                    send = False

    def receiveHandShake(self):
        print("\n\nRecebendo handshake")
        receivedShake, nRx = self.com1.getData(14)
        self.com1.sendData(receivedShake)

