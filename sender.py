from protocol import *
import time

HOST = "127.0.0.1"
PORT = 65445
p = Protocol('', (HOST,PORT))
p.connect()
pac = Packet(("f"*1000000).encode('utf-8'))
pac.send(p)
