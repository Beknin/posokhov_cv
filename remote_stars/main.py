import numpy as np
import socket
from skimage.measure import label
from scipy import ndimage

host = "84.237.21.36"
port = 5152

def recvall(sock, nbytes):
    data = bytearray()
    while len(data) < nbytes:
        packet = sock.recv(nbytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(b"124ras1")
    print(sock.recv(10))
    
    completed = b'nope'

    while completed == b'nope':
        sock.send(b'get')
        bts = recvall(sock, 40002)
        img = np.frombuffer(bts[2:40002], dtype="uint8")
        img = img.reshape(bts[0], bts[1])
        binary = img > 0
        labeled = label(binary)

        centers = []
        if 2 in labeled:
            for i in 1, 2:
                current = labeled == i
                centers += [ndimage.center_of_mass(current)]
            dist = ((centers[0][0] - centers[1][0])**2 + (centers[0][1] - centers[1][1])**2)**0.5
        else:
            dist = 0
        
        sock.send(str(round(dist, 1)).encode())
        print(sock.recv(10))
        sock.send(b'beat')
        completed = sock.recv(10)