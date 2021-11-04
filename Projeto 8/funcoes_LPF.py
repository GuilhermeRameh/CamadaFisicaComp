from scipy import signal as sg
from scipy.signal.filter_design import normalize

def filtro(y, samplerate, cutoff_hz):
  # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = sg.kaiserord(ripple_db, width)
    taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = sg.lfilter(taps, 1.0, y)
    return yFiltrado

def LPF(signal, cutoff_hz, fs):
  #####################
  # Filtro
  #####################
  # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
  nyq_rate = fs/2
  width = 5.0/nyq_rate
  ripple_db = 60.0 #dB
  N , beta = sg.kaiserord(ripple_db, width)
  taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
  return( sg.lfilter(taps, 1.0, signal))

def normalize(signal):
  max_nbr = max(abs(signal))
  normalize = signal/max_nbr
  return normalize