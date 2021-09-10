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
        print("#################### Port Opened ####################")
        super().__init__(port)
        self.id = b'\x66'

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
        ocioso = True

        while ocioso:
            self.estadoOcioso()

        print("Na escuta!")

        self.sendHandshake()
        cont = 1

        

        return

    def estadoOcioso(self):
        msgt1, nMsgt1 = self.com1.getData(14)
        id_do_servidor = msgt1[2]

        if id_do_servidor == self.id:
            ocioso = False
        
        time.sleep(0.1)

    def sendHandshake(self):
        return