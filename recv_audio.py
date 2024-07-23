import math
import random

import pyaudio
from matplotlib.animation import FuncAnimation

from protocol import *
import socket
import time
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1
DATALEN = int(RATE / CHUNK * RECORD_SECONDS) * CHUNK
interval = 100


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_port(HOST):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for PORT in range(8080, 9090):
        try:
            s.bind((HOST, PORT))
            s.listen(5)
            s.close()
            return PORT
        except:
            continue
    raise Exception('no available port found')


HOST = get_ip()
PORT = get_port('127.0.0.1')
print(f'HOST: {HOST}\nPORT: {PORT}')
p = Protocol((HOST, PORT), '')
p.bind()
pac = Packet(b'')
pac.recv(p)
info = np.frombuffer(pac.data, dtype=np.int16)

xdata, data = np.zeros(100), np.zeros(RATE * 5)
fig, ax = plt.subplots(figsize=(8, 4))
ln, = ax.plot(data, color=(0, 1, 0.29))
shift = math.ceil(DATALEN * interval / 1000) + 1500
ax.set_facecolor((0, 0, 0))
ax.set_yticks([0])
ax.yaxis.grid(True)


def init():
    ax.set_ylim(-32768, 32767)
    return ln,


def update(frame):
    global data, info
    if p.can_recv() or len(info) < shift:
        if (len(info) > shift):
            print(f'!!!!TRAILING DATA len:{len(info)}')
        pac.recv(p)
        info = np.frombuffer(pac.data, dtype=np.int16)
    data = np.roll(data, -shift, axis=0)
    data[-shift:] = info[:shift]
    info = info[shift:]
    ln.set_ydata(data)
    return ln,


ani = FuncAnimation(fig, update, #frames=10000000,
                    interval=interval,
                    init_func=init, blit=True)
plt.show()
