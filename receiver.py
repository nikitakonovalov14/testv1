from protocol import *
import socket
import time


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
print(f'Message: {pac.data.decode("utf-8")}')
time.sleep(10)
