########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#             Cliente
#######################################

import os
import sys
from pathlib import Path
from enlace import *
import numpy as np
import struct
from fileManager import *
from Protocolo import Protocolo

class Client(Protocolo):

    def __init__(self, port, idServer, fileId, packages):
        super().__init__()
        self.com1 = enlace(port)
        self.com1.enable()
        print("#################### Port Opened ####################")
        self.id = b'\x50'
        self.idServer = idServer
        self.fileId = fileId
        self.packages = packages
        self.numPackages = len(packages)
        self.inicia = False
        self.msgError = False
        self.cont = 0

        self.refFiveSec = 0.0
        self.refTwentySec = 0.0
        self.fiveSecTimer = 0.0
        self.twentySecTimer = 0.0

    def mainLoop(self):
        self.handShake()
        while self.cont <= self.numPackages:
            self.sendPackage()
            if (self.fiveSecTimer) < 5 or self.msgError:
                    self.refTwentySec = time.time()
            self.refFiveSec = time.time()        
            self.fiveSecTimer = time.time() - self.refFiveSec
            self.twentySecTimer = time.time() - self.refTwentySec
            self.receiveResponse()
            if self.twentySecTimer >= 20:
                self.sendTimeoutMessage()
                break
        print("\n\n\nEncerrando Transmissão.")
        self.com1.disable()

    def handShake(self):
        print("Iniciando handShake.")
        while not self.inicia:
            txBuffer = super().constructDatagram(self.msgType1, self.id, self.idServer, id_do_arquivo=self.fileId)
            self.com1.sendData(txBuffer)
            print("Esperando resposta do handshake.")
            rxBuffer, nRx = self.com1.getData(14, self.msgType1)
            msgType = rxBuffer[0]
            eop = rxBuffer[10:14]
            print(f"Recebi mensagem do tipo {type(msgType)}, eop {eop}")
            if msgType.to_bytes(1, 'big') == self.msgType2 and eop == self.eop:
                self.inicia = True
                self.cont = 1
                break

    def sendPackage(self):
        package = self.packages[self.cont-1]
        totalPackages = self.numPackages.to_bytes(1,'big')
        packageId = self.cont.to_bytes(1,'big')
        packageSize = len(package)
        packageSizeBytes = packageSize.to_bytes(1,'big')
        txBuffer = super().constructDatagram(self.msgType3, self.id, self.idServer, pacotes_total=totalPackages, id_pacote=packageId, id_do_arquivo=self.fileId, tamanho_pacote=packageSizeBytes, pacote=package)
        print(f"\n\nEnviando o Pacote n°{self.cont}, de tamanho: {packageSize}.")
        self.com1.sendData(txBuffer)
    
    def receiveResponse(self):
        print("Esperando resposta do Server")
        rxBuffer, nRx = self.com1.getData(14, msgType=self.msgType3, refFiveSec=self.refFiveSec, refTwentySec=self.refTwentySec)
        print(f"Recebi a mensagem {rxBuffer}")
        msgType = rxBuffer[0].to_bytes(1,'big')
        eop = rxBuffer[10:14]
        if msgType == self.msgType4 and eop == self.eop:
            self.msgError = False
            print(f"\nO server Falou que tudo estava ok com o pacote n°{self.cont}, seguindo para o próximo.")
            self.cont += 1
        elif msgType == self.msgType6 and eop == self.eop:
            packageToResend = rxBuffer[6]
            self.cont = packageToResend
            self.msgError = True
            print(f"\n\nRecebi mensagem de erro, re-enviando pacote defeituoso de n°{self.cont}.")
        elif rxBuffer == b'\xFF':
            self.fiveSecTimer = time.time() - self.refFiveSec
            self.twentySecTimer = 20
            print("Enviando mensagem de timeout para Server.")
        elif rxBuffer == b'\x00':
            self.fiveSecTimer = time.time() - self.refFiveSec
            self.twentySecTimer = time.time() - self.refTwentySec
            print("re-enviando mensagem.")
        
    def sendTimeoutMessage(self):
        txBuffer = super().constructDatagram(self.msgType6, self.id, self.idServer)
        self.com1.sendData(txBuffer)
                
    def flushPortTX(self):
        self.com1.tx.fisica.flush()
        time.sleep(1)
        self.com1.sendData(b'\x01')
        time.sleep(1)