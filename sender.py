import asyncio

from protocol import *

HOST = input("HOST: ")
PORT = int(input("PORT: "))
protocol = Protocol('', (HOST, PORT))
protocol.connect()
message = input("message: ")
package = Packet(message.encode('utf-8'))
asyncio.run(package.send(protocol))
