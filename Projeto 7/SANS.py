from suaBibSignal import *
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys

import math
#importe as bibliotecas


bruh = signalMeu()

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
     #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = 1 #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    fs = 44100   # taxqa de amostagem (sample rate)
    sd.default.samplerate = fs
    sd.default.channels = 1  # pontos por segundo (frequência de amostragem)
    A   = 1.5   # Amplitude
    F   = 440     # Hz
    T   = 1    # Tempo em que o seno será gerado
    t   = np.linspace(-T/2,T/2,T*fs)

    x, y = bruh.generateSin(148.1,5*gainX,T,fs)
    x, y2 = bruh.generateSin(296.2,5*gainX,T,fs)
    x, y3 = bruh.generateSin(222.02,5*gainX,T,fs)
    x, y4 = bruh.generateSin(209.48,5*gainX,T,fs)
    x, y5 = bruh.generateSin(197.74,5*gainX,T,fs)
    x, y6 = bruh.generateSin(176.22,5*gainX,T,fs)
    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    NUM = 5
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides

    # list = [1, 1, 2, 3, 4, 5, 6, 1, 6, 5]
    # list_2 = []

    # for i in list:
    #     if i == 1:
    #         list_2.append(y[:(round(len(y)/8))])
    #     elif i == 2:
    #         list_2.append(y2[:(round(len(y)/8))])
    #     elif i == 3:
    #         list_2.append(y3[:(round(len(y)/8))])
    #     elif i == 4:
    #         list_2.append(y4[:(round(len(y)/8))])
    #     elif i == 5:
    #         list_2.append(y5[:(round(len(y)/8))])
    #     elif i == 6:
    #         list_2.append(y6[:(round(len(y)/8))])
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som

    sd.play(y[:(math.ceil(len(y)/8))], fs)
    sd.wait(0.1)
    sd.play(y[:(math.ceil(len(y)/8))], fs)
    sd.wait(0.1)
    sd.play(y2[:(math.ceil(len(y)/4))], fs)
    sd.wait(0.1)
    sd.play(y3[:(math.ceil(len(y)*3/8))], fs)
    sd.wait(0.1)
    sd.play(y4[:(math.ceil(len(y)/4))], fs)
    sd.wait(0.1)
    sd.play(y5[:(math.ceil(len(y)/4))], fs)
    sd.wait(0.1)
    sd.play(y6[:(math.ceil(len(y)/4))], fs)
    sd.wait(0.1)
    sd.play(y[:(math.ceil(len(y)/8))], fs)
    sd.wait(0.1)
    sd.play(y6[:(math.ceil(len(y)/8))], fs)
    sd.wait(0.1)
    sd.play(y5[:(math.ceil(len(y)/8))], fs)
    

    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
