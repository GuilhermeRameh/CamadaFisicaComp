
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window




class signalMeu:

    def __init__(self):
        self.init = 0
        self.freq_list = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]
        self.freq_port = 14000
#
    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')


    
    def sans(self):
        
        duration = 1 #tempo em segundos que ira emitir o sinal acustico 
        
        gainX  = 0.3
        gainY  = 0.3

        fs = 44100   # taxqa de amostagem (sample rate)
        sd.default.samplerate = fs
        sd.default.channels = 1  # pontos por segundo (frequência de amostragem)
        A   = 1.5   # Amplitude
        F   = 440     # Hz
        T   = 1    # Tempo em que o seno será gerado
        t   = np.linspace(-T/2,T/2,T*fs)

        x, y = self.generateSin(148.1,5*gainX,T,fs)
        x, y2 = self.generateSin(296.2,5*gainX,T,fs)
        x, y3 = self.generateSin(222.02,5*gainX,T,fs)
        x, y4 = self.generateSin(209.48,5*gainX,T,fs)
        x, y5 = self.generateSin(197.74,5*gainX,T,fs)
        x, y6 = self.generateSin(176.22,5*gainX,T,fs)
        #printe a mensagem para o usuario teclar um numero de 0 a 9. 
        #nao aceite outro valor de entrada.
        #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides

        list = [1, 1, 2, 3, 4, 5, 6, 1, 6, 5]
        list_2 = []

        for j in range(len(list)):
            i = list[j]
            if i == 1:
                list_2.append(y[:(round(len(y)/8))])
            elif i == 2:
                if j == 2:
                    list_2.append(y2[:(round(len(y)/4))])
                else:
                    list_2.append(y2[:(round(len(y)/8))])
            elif i == 3:
                list_2.append(y3[:(round(len(y)*3/8))])
            elif i == 4:
                if j == 4:
                    list_2.append(y4[:(round(len(y)/4))])
                else:
                    list_2.append(y4[:(round(len(y)/8))])
            elif i == 5:
                if j == 5:
                    list_2.append(y5[:(round(len(y)/4))])
                else:
                    list_2.append(y5[:(round(len(y)/8))])
            elif i == 6:
                if j == 6:
                    list_2.append(y6[:(round(len(y)/4))])
                else:
                    list_2.append(y6[:(round(len(y)/8))])
        #printe o grafico no tempo do sinal a ser reproduzido
        # reproduz o som

        flat_list = [item for sublist in list_2 for item in sublist]

        return flat_list
