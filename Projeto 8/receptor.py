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

# audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
# sd.wait()
# print("...     FIM")

file = sf.read("modulado.wav")
dados = file[0]
fs = file[1]

len_file = len(dados)
print(len_file)
#grave uma variavel com apenas a parte que interessa (dados)
# dados = []
# for i in audio:
#     for j in i:
#         dados.append(j)

x = np.linspace(0, 2, len_file)

plt.figure()
l = [0,0.01,-1, 1]
plt.axis(l)
plt.plot(x, dados, '.-')

X, Y = signal.calcFFT(dados,fs)
plt.figure()
plt.stem(X,np.abs(Y))
plt.xlim(9000, 19000)


freqC = 14000 # frequencia portadora
A   = 1.5
gain = 0.3
T   = math.ceil((len(dados))/fs)

x, y = signal.generateSin(freqC, A*gain, T, fs)
signalC = y[:len(dados)]

print("Demodulando")
demodulacao = dados*signalC

print("Filtrando")
filtrado = filtro(demodulacao, fs, 4000)
norm_audio = normalize(filtrado)

sd.play(norm_audio, fs)
sd.wait()

plt.show()