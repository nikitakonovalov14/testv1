from protocol import *

HOST = "127.0.0.1"
PORT = 65445
p = Protocol((HOST,PORT), '')
p.bind()

pac = Packet(b'')
pac.recv(p)
print(len(pac.data.decode('utf-8')))
