# Lyd ind fra mikrofon
# Ex hentet fra:
# https://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array/24985016
# KAN IKKE køre med Thonny da installation af pyaudio giver en fejl i manage packages på windows så
# der skal mere til. Altså for 'bøvlet' til vores brug selvom det lyder som det rigtige bibliotek (crossplatform)
#
import pyaudio
import numpy as np
from matplotlib import pyplot as plt

CHUNKSIZE = 1024 # fixed chunk size

# initialize portaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNKSIZE)

# do this as long as you want fresh samples
data = stream.read(CHUNKSIZE)
numpydata = np.frombuffer(data, dtype=np.int16)

# plot data
plt.plot(numpydata)
plt.show()

# close stream
stream.stop_stream()
stream.close()
p.terminate()