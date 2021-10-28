
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:

    def __init__(self):
        self.init = 0
        self.freq_list = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]
        self.convertor = {
            "1": [self.freq_list[0][0], self.freq_list[1][0]],
            "2": [self.freq_list[0][0], self.freq_list[1][1]],
            "3": [self.freq_list[0][0], self.freq_list[1][2]],
            "A": [self.freq_list[0][0], self.freq_list[1][3]],
            "4": [self.freq_list[0][1], self.freq_list[1][0]],
            "5": [self.freq_list[0][1], self.freq_list[1][1]],
            "6": [self.freq_list[0][1], self.freq_list[1][2]],
            "B": [self.freq_list[0][1], self.freq_list[1][3]],
            "7": [self.freq_list[0][2], self.freq_list[1][0]],
            "8": [self.freq_list[0][2], self.freq_list[1][1]],
            "9": [self.freq_list[0][2], self.freq_list[1][2]],
            "C": [self.freq_list[0][2], self.freq_list[1][3]],
            "X": [self.freq_list[0][3], self.freq_list[1][0]],
            "0": [self.freq_list[0][3], self.freq_list[1][1]],
            "#": [self.freq_list[0][3], self.freq_list[1][2]],
            "D": [self.freq_list[0][3], self.freq_list[1][3]],
        }
        print(self.convertor["1"])

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
