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
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
# HOST = input("HOST: ")
# PORT = int(input("PORT: "))
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65438  # The port used by the server
p = Protocol('', (HOST, PORT))
p.connect()
while True:
    frames = b''

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        data_array = np.fromstring(data, dtype='int16')
        frames += data_array[0::CHANNELS].tostring()

    pac = Packet(frames)
    try:
        asyncio.run(pac.send(p))
    except:
        break

stream.stop_stream()
stream.close()

