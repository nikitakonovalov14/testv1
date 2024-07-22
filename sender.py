from protocol import *

HOST = input("HOST: ")
PORT = int(input("PORT: "))
p = Protocol('', (HOST, PORT))
p.connect()
message = input("message: ")
pac = Packet(message.encode('utf-8'))
pac.send(p)
