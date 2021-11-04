from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import math
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys
import soundfile as sf
from funcoes_LPF import filtro, LPF, normalize

signal = signalMeu()
audio_file = sf.read('freqNbrSANS.wav')

audio_array = audio_file[0]
fs = audio_file[1] # Sample Rate

# Nomalizando para o intervalo de [-1, 1]
print("Normalizing audio")
norm_audio = normalize(audio_array)

# Filtrando freqs acima de 4kHz
print("Filtering audio")
filtered_audio = filtro(norm_audio, fs, 4000)

sd.play(filtered_audio, fs)
sd.wait()

freqC = 14000 # frequencia portadora
A   = 1.5
gain = 0.3
T   = math.ceil((len(filtered_audio))/fs)

x, y = signal.generateSin(freqC, A*gain, T, fs)
signalC = y[:len(filtered_audio)]

AM_audio = abs(1+filtered_audio)*signalC
input('Continue to transmission?')
sd.play(AM_audio, fs)
sd.wait()