import socket
import struct
import os , json

import time
import mimetypes

CHUNK = 64 * 1024


def send_msg(sock, data: bytes):
    sock.sendall(struct.pack("!I", len(data)) + data)


def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError
        data += chunk
    return data


def recv_msg(sock):
    length = struct.unpack("!I", recv_exact(sock, 4))[0]
    return recv_exact(sock, length)

"100.77.10.89"
sock = socket.create_connection(("192.168.1.3",  29763))
print("connected")
# /set_upload_url http://192.168.1.2:5000/api/upload

### 
while True:
    print("Type Query along with comms eg: /set_volume 0.7")
    comms = input()

    send_msg(sock, comms.encode())
    # print(recv_msg(sock).decode())

