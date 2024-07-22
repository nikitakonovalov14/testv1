import socket


class Protocol:
    def __init__(self, local_addr, remote_addr):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.remote_addr = remote_addr
        self.local_addr = local_addr
        self.batch_size = 512
        self.conn = None

    def close(self):
        self.conn.close()

    def connect(self):
        self.socket.connect(self.remote_addr)

    def bind(self):
        self.socket.bind(self.local_addr)
        self.socket.listen()
        self.conn, addr = self.socket.accept()

    def send(self, data: bytes):
        return self.socket.send(data)

    def recv(self, n):
        msg, addr = self.conn.recvfrom(n)
        return msg


class Packet:
    def __init__(self, data: bytes):
        self.header_size = 8
        self.size = len(data)
        self.data = data
        self.assembled = b''
        self.assemble()

    def assemble(self):
        self.assembled = self.size.to_bytes(4, 'big') + \
                         self.header_size.to_bytes(4, 'big') + \
                         self.data

    def disassemble(self, header: bytes):
        self.size = int.from_bytes(header[0:4], 'big')

    def send(self, protocol: Protocol):
        size = 0
        while size < self.size:
            n = protocol.send(self.assembled[size:])
            if n is None:
                if size == self.size:
                    return
                else:
                    raise EOFError(f'connection closed before full message was sent')
            size += n

    def recv(self, protocol: Protocol) -> bool:  # false if connection closed
        header = protocol.recv(self.header_size)
        if len(header) != self.header_size:
            raise TypeError(f'bad header size expected: {self.header_size}, got: {len(header)}')
        self.disassemble(header)
        self.data = b''
        size = 0
        while size < self.size:
            msg = protocol.recv(min(protocol.batch_size, self.size - size))
            if msg is None:
                if size == self.size:
                    protocol.close()
                    return False
                else:
                    raise EOFError(f'connection closed before full message receive')
            size += len(msg)
            self.data += msg
        protocol.close()
        return True
