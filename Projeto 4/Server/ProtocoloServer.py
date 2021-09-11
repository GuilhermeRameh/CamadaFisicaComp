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
        self.estadoPegandoPacotes()

        return

    def estadoOcioso(self):
        ocioso = True
        while ocioso:
                
            msgt1, nMsgt1 = self.com1.getData(14)
            id_do_servidor = msgt1[2]
            self.id_do_sensor = msgt1[1]

            if id_do_servidor == self.id:
                ocioso = False
            
            time.sleep(0.1)

    def sendHandshake(self):
        self.constructDatagram(b'\x02', self.id_do_sensor, self.id)

    def estadoPegandoPacotes(self):
        cont = 1
        pacotes_total = 100 # NOTE: Esse valor é arbitrário, apenas para iniciar o loop
        self.receivedArray = []
        previousId = b''

        while cont <= pacotes_total:
            print("\nGetting Head Data...")

            while self.com1.rx.timer1Bool:
                bufferHead, nBufferHead = self.com1.getData(10)
                time.sleep(0.05)
                if self.com1.rx.timer2 > 20:
                    print("\nTimeout [2]: 20 segundos sem resposta.")
                    print("Desligando comunicação")
                    txBuffer = self.constructDatagram(b'\x05', self.id_do_sensor, self.id_do_server)
                    self.com1.sendData(txBuffer)
                    self.com1.disable()
                    self.main = False
                    break

            
            tipo_da_mensagem = bufferHead[0]

            if tipo_da_mensagem==b'\x03':
                print("A mensagem é do tipo DADOS")

            pacotes_total = bufferHead[3]
            id_pacote = bufferHead[4]
            tamanho_pacote = bufferHead[5]

            print(f"\nID do pacote a receber: {id_pacote}")
            print(f"Tamanho do pacote a receber: {tamanho_pacote}")

            bufferPacote, nPacoteBuffer = self.com1.getData(tamanho_pacote)

            bufferEOP, nBufferEOP = self.com1.getData(4)



    def main(self):
        return self.main