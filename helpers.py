import random
import socket
import struct
import subprocess
import os


def getAddrNextSteppingStone(chainFile: list):
    random.seed(1)
    indexOfFirstSS = random.randint(0, len(chainFile) - 1)
    addr, port = chainFile[indexOfFirstSS].split(" ")
    del chainFile[indexOfFirstSS]
    return addr, int(port)


def getData(url):
    subprocess.run(["wget", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data = open(url.split("/")[-1], 'rb').read()
    os.remove(url.split("/")[-1])
    return data


def sendDataHeader(s: socket.socket, dataLength):
    s.sendall(struct.pack('L', dataLength))


def recv_all(s: socket.socket, length: int):
    allData = bytearray()
    while True:
        data = s.recv(1024)
        allData = allData + data
        if not data:
            break
        if len(allData) >= length:
            break
    return allData
