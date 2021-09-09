########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#
#######################################

import os
from pathlib import Path
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
        self.endBit = b'\x01'

        self.eop = b'\xba\xba\xb0\xe1'

        self.fileNumber = 1

   # Note to self: a função que abre, le e fragmenta (monta os pacotes)
   # vai ser feito pelo Bernardo. Por enquanto posso assumit que vou trabalhar 
   # com uma lista, em que cada elemento da lista é um pacote com 114 bytes

    def constructDatagram(self, idPacote, receiverId, package, pkgSize=b'\x00', pkgTotalSize=b'\x00\x00', resendBit=b'\x00', continueBit=b'\x00', endBit = b'\x00',freebits=b'\x00\x00'):

        # To-Do: Completar função que monta o Datagrama. 

        # ############### Monta Head #################
        head = b'' + idPacote + pkgSize + pkgTotalSize + receiverId + resendBit + continueBit + endBit + freebits

        txBuffer = b'' + head + package + self.eop

        return txBuffer

    def sendingLoop(self, packages):
        pkgTotalSize = (len(packages)-1).to_bytes(2, 'big')
        receiverId = b'\x69'
        endStatus = b'\x00'
        print(f"\n\nTotal de pacotes a serem enviados {len(packages)}")
        for i in range(len(packages)):
            if endStatus == self.endBit:
                break
            while True:
                package = bytes(packages[i])
                idPacote = struct.pack('B', i)
                pkgSize = struct.pack('B', len(package))

                txBuffer = self.constructDatagram(idPacote, receiverId, package, pkgSize=pkgSize, pkgTotalSize=pkgTotalSize)          

                self.com1.sendData(txBuffer)

                responseBuffer, nResponseBuffer = self.com1.getData(14)
                time.sleep(0.01)
                repeatStatus = responseBuffer[5].to_bytes(1, 'big')
                contStatus = responseBuffer[6].to_bytes(1, 'big')
                endStatus = responseBuffer[7].to_bytes(1, 'big')
                if contStatus == self.contBit and repeatStatus != self.resendBit:
                    break
        self.com1.disable()
        print("\n\nLoop de Envio concluído com sucesso!")

    def receivingLoop(self):
        receiving = True
        self.receivedArray = []
        previousId = b''

        while receiving:
            print("\n\nGetting Head Data...")
            bufferHead, headSize = self.com1.getData(10)   

            payloadId = bufferHead[0].to_bytes(1,'big')
            payloadSize = bufferHead[1]
            nPacotes = bufferHead[2:4]
            if (b'\x00'+payloadId) == nPacotes:
                print("\n\n\nrecebi todos os pacotes")
                receiving = False
            print(f'\n\nQuantidade de Pacotes: {nPacotes}\n')
            print("\n\nGetting Payload Data...")
            bufferPayload, payloadBufferSize = self.com1.getData(payloadSize)

            #To-Do: Implementar uma função de timeoout

            bufferEOP, nBufferEOP = self.com1.getData(4)
            if bufferEOP != self.eop or previousId == payloadId:
                print("\n\nEnvio Incorreto, enviando pedido para correção de pacote...")
                sendAgainBuffer = self.constructDatagram(payloadId, b'\x42', b'', resendBit=self.resendBit)
                self.com1.sendData(sendAgainBuffer)
            else:
                print("\n\nEOP correto pedindo novo envio")
                self.receivedArray.append(bufferPayload)
                contBuffer = self.constructDatagram(payloadId, b'\x42', b'', continueBit=self.contBit)
                self.com1.sendData(contBuffer)
            previousId = payloadId
        print('\n\nenviando mensagem de fim')
        endBuffer = self.constructDatagram(b'\x00', b'\x42', b'', endBit=self.endBit)
        self.com1.sendData(endBuffer)
        self.com1.disable()
        print("\n\nRecebimento concluído com sucesso")
        return self.receivedArray

    def sendHandshake(self):
        send = True
        handShake = self.constructDatagram(b'\x00', b'\x00', b'')
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

    def reconstructMessage(self):
        curPath = Path(__file__).parent.resolve()
        filepath = self.receivedArray[0].decode('utf-8')
        filepath = str(curPath) + '/' + filepath
        del self.receivedArray[0]
        if os.path.exists(filepath):
            fileNum = str(self.fileNumber)
            fileNum += "."
            filepath = filepath.replace(".", fileNum)
            self.fileNumber += 1
        print(f'o novo arquivo será encontrado em: {filepath}')
        newFile = open(filepath, 'wb')
        for content in self.receivedArray:
            newFile.write(content)
        newFile.close()

