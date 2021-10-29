from suaBibSignal import *
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys
import soundfile as sf

#importe as bibliotecas

signal = signalMeu()


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

    fs = 44100   # taxa de amostagem (sample rate)
    sd.default.samplerate = fs
    sd.default.channels = 1  # pontos por segundo (frequência de amostragem)
    A   = 1.5   # Amplitude
    F   = 440     # Hz
    T   = 1    # Tempo em que o seno será gerado
    t   = np.linspace(-T/2,T/2,T*fs)
    
    
    duration = 1 #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    dict_tons = {}

    for key in signal.convertor.keys():
        freqs = signal.convertor[key]
        # char = signal.convertor[]

        x1, y1 = signal.generateSin(freqs[0], A*gainX, T, fs)
        x2, y2 = signal.generateSin(freqs[1], A*gainX, T, fs)

        tone = y1+y2

        dict_tons[key] = tone

    print("Gerando Tons base")

    while True:
        try:
            NUM = input("Digite caracter:")
            #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
            #use para isso sua biblioteca (cedida)
            #obtenha o vetor tempo tb.
            #deixe tudo como array

            plt.close('all')
            tone = dict_tons[NUM]

            #printe a mensagem para o usuario teclar um numero de 0 a 9. 
            #nao aceite outro valor de entrada.
            print("Gerando Tom referente ao símbolo : {}".format(NUM))

            #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
                
            plt.figure()
            l = [0,0.01,-1, 1]
            plt.axis(l)
            plt.plot(x1, tone, '.-')

            X, Y = signal.calcFFT(tone,fs)
            plt.figure()
            plt.stem(X,np.abs(Y))
            plt.xlim(600, 1700)

            #printe o grafico no tempo do sinal a ser reproduzido
            # reproduz o som
            sd.play(tone, fs)
            sf.write(f'4 Semestre\Camada Física da computação\CamadaFisicaComp\Projeto 7\GravacoesGeradas/freqNbr{NUM}.wav', tone, fs)
            # Exibe gráficos
            plt.show(block=False)
            # aguarda fim do audio
            sd.wait()
            

        except KeyboardInterrupt:
            print(KeyboardInterrupt)


if __name__ == "__main__":
    main()
