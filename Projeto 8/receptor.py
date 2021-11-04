from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import math
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys
import time
import soundfile as sf
from funcoes_LPF import filtro, LPF, normalize

signal = signalMeu()

fs = 44100
sd.default.samplerate = fs #taxa de amostragem
sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
duration = 3 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

time.sleep(1)

numAmostras = fs * duration
freqDeAmostragem = fs

audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
sd.wait()
print("...     FIM")

freqC = 14000 # frequencia portadora
A   = 1.5
gain = 0.3
T   = math.ceil((len(audio))/fs)

x, y = signal.generateSin(freqC, A*gain, T, fs)
signalC = y[:len(audio)]

demodulacao = audio*signalC

filtrado = filtro(demodulacao, fs, 4000)

sd.play(filtrado, fs)
sd.wait()