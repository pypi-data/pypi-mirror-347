import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import socket

class EncryptedSocket:
    def __init__(self, sock, session_key):
        self.socket = sock
        self.session_key = session_key

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.session_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = iv + encryptor.update(data) + encryptor.finalize()
        self.socket.sendall(encrypted)

    def recv(self, bufsize):
        data = self.socket.recv(bufsize)
        if not data:
            return None
        iv, encrypted = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self.session_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted) + decryptor.finalize()

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()