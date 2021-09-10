########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#
#######################################

import os
from pathlib import Path
import time
import numpy as np
import struct

class Protocolo:

    def __init__(self):
        self.headSize = 10
        self.EOPSize = 4
        self.payloadMaxSize = 114

        self.extension = ''

        self.resendBit = b'\x01'
        self.contBit = b'\x01'
        self.endBit = b'\x01'

        self.eop = b'\xFF\xAA\xFF\xAA'

        self.fileNumber = 1
        self.erro = True

    def constructDatagram(self, tipo_da_mensagem, id_do_sensor, id_do_servidor, pacotes_total=b'\x00', id_pacote=b'\x00', id_do_arquivo=b'\x00', tamanho_pacote=b'\x00', pacote_recomeco=b'\x00', ultimo_pacote_recebido=b'\x00', pacote=b'', h8=b'\x00', h9=b'\x00'):
        ############### Monta Head #################
        
        if tipo_da_mensagem==b'\x01':
            h5 = id_do_arquivo
        elif tipo_da_mensagem==b'\x02':
            h5 = tamanho_pacote

        head = b'' + tipo_da_mensagem + id_do_sensor + id_do_servidor + pacotes_total + id_pacote + h5 + pacote_recomeco + ultimo_pacote_recebido + h8 + h9

        txBuffer = b'' + head + pacote + self.eop

        return txBuffer

    def sendingLoop(self, packages):
        pkgTotalSize = (len(packages)-1).to_bytes(2, 'big')
        receiverId = b'\x69'
        endStatus = b'\x00'
        print(f"Total de pacotes a serem enviados {len(packages)}")
        for i in range(len(packages)):
            if endStatus == self.endBit:
                break
            while True:
                print(f"\nIniciando envio do pacote de ID {i}")
                package = bytes(packages[i])
                idPacote = struct.pack('B', i)
                if i ==1 and self.erro:
                    idPacote = struct.pack('B', 0)
                    self.erro = False
                pkgSize = struct.pack('B', len(package))

                txBuffer = self.constructDatagram(idPacote, receiverId, package, pkgSize=pkgSize, pkgTotalSize=pkgTotalSize)          

                self.com1.sendData(txBuffer)

                responseBuffer, nResponseBuffer = self.com1.getData(14)
                time.sleep(0.01)
                repeatStatus = responseBuffer[5].to_bytes(1, 'big')
                contStatus = responseBuffer[6].to_bytes(1, 'big')
                endStatus = responseBuffer[7].to_bytes(1, 'big')
                if contStatus == self.contBit and repeatStatus != self.resendBit:
                    print("Nada de errado na transmição enviando próximo pacote.")
                    break
                else:
                    print(f"Algo deu errado reiniciando envio do pacote de ID {i}")
        self.com1.disable()
        print("\n\n\nLoop de Envio concluído com sucesso!")

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
            
            print(f'Quantidade de Pacotes: {int.from_bytes(nPacotes, "big")}')
            print(f'ID do Pacote: {bufferHead[0]}')
            print("\nGetting Payload Data...")
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

            if (b'\x00'+payloadId) == nPacotes:
                print("\n\n\nRecebi todos os pacotes")
                receiving = False

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
        verify = True
        while verify:
            if os.path.exists(filepath):
                fileNum = str(self.fileNumber)
                fileNum = "("+fileNum+")."
                if self.fileNumber > 1:
                    filepath = filepath.replace("("+str(self.fileNumber - 1)+").", fileNum)
                    self.fileNumber += 1
                else:
                    filepath = filepath.replace(".", fileNum)
                    self.fileNumber += 1


                
            else:
                verify = False
        print(f'O novo arquivo será encontrado em: {filepath}')
        newFile = open(filepath, 'wb')
        for content in self.receivedArray:
            newFile.write(content)
        newFile.close()

