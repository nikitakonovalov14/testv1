import numpy as np

from protocol import *
import pyaudio
import wave
import asyncio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
HOST = input("HOST: ")
PORT = int(input("PORT: "))
protocol = Protocol('', (HOST, PORT))
protocol.connect()
while True:
    frames = b''

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        data_array = np.fromstring(data, dtype='int16')
        frames += data_array[0::CHANNELS].tostring()

    package = Packet(frames)
    try:
        asyncio.run(package.send(protocol))
    except:
        break

stream.stop_stream()
stream.close()

