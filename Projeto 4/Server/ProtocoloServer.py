########################################
# Arquivo para a criação da Classe 
#            PROTOCOLO
#
#######################################

import os
import sys
from pathlib import Path
from enlace import *
import numpy as np
import struct
from fileManager import *

sys.path.insert(1, os.path.realpath(os.path.pardir))
from Protocolo import Protocolo

class Server(Protocolo):

    def __init__(self, port):
        self.com1 = enlace(port)
        self.com1.enable()
        self.main = True
        self.id_do_server = b'\x66'
        print("#################### Port Opened ####################")
        super().__init__()
        
        

    ''' 
    TODO: 
        Precisamos construir uma nova lógica de envio. Assim, vamos reescrever 
        em arquivos diferentes (ProtocoloServer e ProtocoloClient) cada uma das lógicas 
        do zero. A ideia é dividir a lógica principal em algumas classes, e juntá-las em um 
        loop que construa a logica corretamente, sendo esse loop a função chamada 
        "logicaPrincipal". Recomendo olhar a classe Protocolo para nos baseármos no código que
        já escrevemos.
    '''

    def logicaPrincipal(self):
        print("Esperando Mensagem")

        ###################### ENTRA NO PRIMEIRO LOOP ######################
        ######################### ESTADO = OCIOSO ##########################
        self.estadoOcioso()

        print("Na escuta!")

        self.sendHandshake()

        ###################### ENTRA NO SEGUNDO LOOP ######################
        ##################### ESTADO = PEGANDO PACOTES ####################
        checkResult =  self.estadoPegandoPacotes()
        if checkResult=="SHUTDOWN":
            print(":-(")
        else:
            print("SUCCESS!")
            

        print(self.receivedArray)

    def estadoOcioso(self):
        ocioso = True
        while ocioso:
            
            msgt1, nMsgt1 = self.com1.getData(14)
            id_do_servidor = msgt1[2].to_bytes(1, "big")
            self.id_do_sensor = msgt1[1].to_bytes(1, "big")
            tipo_da_mensagem = msgt1[0].to_bytes(1, "big")
            
            if id_do_servidor == self.id_do_server and tipo_da_mensagem == b'\x01':
                print("Recebi uma mensagem para mim!")
                ocioso = False
                self.com1.rx.inOcioso = False
            
            time.sleep(1)

    def sendHandshake(self):
        txBuffer = self.constructDatagram(b'\x02', self.id_do_sensor, self.id_do_server)
        self.msgt2 = txBuffer
        self.com1.sendData(self.msgt2)

    def estadoPegandoPacotes(self):
        cont = 1
        pacotes_total = b'\xFF' # NOTE: Esse valor é arbitrário, apenas para iniciar o loop
        self.receivedArray = []
        
        previousId = 0

        while cont <= int.from_bytes(pacotes_total, "big"):

            print("\nGetting Head Data...")
            self.com1.rx.timer1Bool = True

            while self.com1.rx.timer1Bool:

                bufferHead, nBufferHead = self.com1.getData(10)

                if self.com1.rx.timer1>2:
                    self.com1.sendData(self.msgt2)

                if self.com1.rx.timer2 > 20:
                    print("\nTimeout [2]: 20 segundos sem resposta.")
                    print("Desligando comunicação")
                    txBuffer = self.constructDatagram(b'\x05', self.id_do_sensor, self.id_do_server)
                    self.com1.sendData(txBuffer)
                    self.com1.disable()
                    return "SHUTDOWN"

                if nBufferHead != 0:
                    tipo_da_mensagem = bufferHead[0].to_bytes(1, "big")
                    if tipo_da_mensagem == b'\x03':
                        self.com1.rx.timer1Bool = False
                        self.com1.rx.timer2Bool = True
                    
                    time.sleep(1)

            if tipo_da_mensagem==b'\x03':
                print("A mensagem é do tipo DADOS")

                pacotes_total = bufferHead[3].to_bytes(1, "big")
                id_pacote = bufferHead[4].to_bytes(1, "big")
                tamanho_pacote = bufferHead[5].to_bytes(1, "big")

                print(f"\nID do pacote a receber: {int.from_bytes(id_pacote, byteorder='big')}")
                print(f"Tamanho do pacote a receber: {int.from_bytes(tamanho_pacote, byteorder='big')}")
                print("\nGetting Payload...")

                bufferPacote, nPacoteBuffer = self.com1.getData(int.from_bytes(tamanho_pacote, "big"))

                print("\nGetting EOP...")
                bufferEOP, nBufferEOP = self.com1.getData(4)


                print(f'\nMensagem Inteira: {bufferHead+bufferPacote+bufferEOP}')
                print(f'Contagem: {cont}, ID: {id_pacote}\n')

                if bufferEOP == self.eop and int.from_bytes(id_pacote, "big") == cont:
                    print("EOP correto. ID do pacote correto. \nEnviando *msgt4* para confirmação de recebimento.")
                    self.receivedArray.append(bufferPacote)
                    cont += 1
                    previousId = id_pacote
                    txBuffer = self.constructDatagram(b'\x04', self.id_do_sensor, self.id_do_server, ultimo_pacote_recebido=id_pacote)
                    self.com1.sendData(txBuffer)
                else:
                    print("EOP incorreto ou ID do pacote incorreto. \nEnviando *msgt6* para reenvio de pacote.")
                    if previousId == 0:
                        txBuffer = self.msgt2
                    else:
                        txBuffer = self.constructDatagram(b'\x06', self.id_do_sensor, self.id_do_server, pacote_recomeco=previousId)
                    self.com1.sendData(txBuffer)

        self.com1.disable()
        return "SUCCESS"

    def flushPortTX(self):
        self.com1.tx.fisica.flush()
        time.sleep(1)
        self.com1.sendData(b'\x69')
        time.sleep(1)
