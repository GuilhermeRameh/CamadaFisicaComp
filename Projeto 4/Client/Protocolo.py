########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#
#######################################

import os
from pathlib import Path
import time
from datetime import datetime
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

        self.msgType1 = b'\x01' 
        self.msgType2 = b'\x02'
        self.msgType3 = b'\x03'
        self.msgType4 = b'\x04'
        self.msgType5 = b'\x05'
        self.msgType6 = b'\x06'

        self.eop = b'\xFF\xAA\xFF\xAA'

        self.fileNumber = 1
        self.erro = True

    def constructDatagram(self, tipo_da_mensagem, id_do_sensor, id_do_servidor, pacotes_total=b'\x00', id_pacote=b'\x00', id_do_arquivo=b'\x00', tamanho_pacote=b'\x00', pacote_recomeco=b'\x00', ultimo_pacote_recebido=b'\x00', pacote=b'', h8=b'\x00', h9=b'\x00'):
        ############### Monta Head #################
        
        if tipo_da_mensagem==b'\x01' or tipo_da_mensagem==b'\x02':
            h5 = id_do_arquivo
        elif tipo_da_mensagem==b'\x03':
            h5 = tamanho_pacote
        else: 
            h5 = b'\x00'

        head = b'' + tipo_da_mensagem + id_do_sensor + id_do_servidor + pacotes_total + id_pacote + h5 + pacote_recomeco + ultimo_pacote_recebido + h8 + h9

        txBuffer = b'' + head + pacote + self.eop

        return txBuffer

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

    def cleanLog(self):
        fp = open('Projeto 4/Client/log.txt', 'w')
        fp.close()

    def logger(self, sendReceive, msgType, totalBytes, msgId=None, totalMsgs=None, crc=''):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logData = currentTime
        msgTypeStr = str(int.from_bytes(msgType, 'big'))
        totalBytesStr = str(int.from_bytes(totalBytes, 'big')) 
        if msgTypeStr == '3':
            msgIdStr = str(int.from_bytes(msgId, 'big'))
            totalMsgsStr = str(int.from_bytes(totalMsgs, 'big'))
            crcStr = crc.decode('utf-8')
            logData += " / " + sendReceive + " / " + msgTypeStr + " / " + totalBytesStr + " / " + msgIdStr + " / " + totalMsgsStr + " / " + crcStr + '\n'
            fp = open('Projeto 4/Client/log.txt', 'a')
            fp.write(logData)
            fp.close()
        else:
            logData += " / " + sendReceive + " / " + msgTypeStr + " / " + totalBytesStr + '\n'
            fp = open('Projeto 4/Client/log.txt', 'a')
            fp.write(logData)
            fp.close()
    

