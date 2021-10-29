#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import peakutils
import sys
import time


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida) 
    signal = signalMeu()   
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duration = 2 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    print("A captação começara em 0.5s")
    time.sleep(0.5)
    #use um time.sleep para a espera
   
    #faca um print informando que a gravacao foi inicializada
    print("Gravação inicializada")
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = fs * duration
    freqDeAmostragem = fs

    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    print(len(audio))
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = []
    for i in audio:
        for j in i:
            dados.append(j)

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    inicio = 0
    fim  = 1
    numPontos = 44100 *duration
    t = np.linspace(inicio,fim,numPontos)

    # plot do grafico  áudio vs tempo!
    plt.figure("Audio")
    plt.plot(t, dados)   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, fs)
    print(yf)
    print(len(yf))
    plt.figure("F(y)")
    plt.plot(xf,np.abs(yf))
    plt.xlim(0, 1800)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(np.abs(yf), thres=0.1, min_dist=40)

    #printe os picos encontrados! 
    print("index de picos {}" .format(index))
    frequencia_num = []
    for freq in xf[index]:
        if freq > 600:
            print("freq de pico sao {}" .format(freq))
            frequencia_num.append(freq)
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    for key,values in signal.convertor.items():
        freq1Achada = False
        freq2Achada = False
        for freq in frequencia_num:
            dif1 = values[0] - freq
            dif2 = values[1] - freq
            if abs(dif1) < 2:
                freq1Achada = True
            elif abs(dif2) < 2:
                freq2Achada = True
        if freq1Achada and freq2Achada:
            print(f"O número é {key}")
            break
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
