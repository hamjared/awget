import random
import socket
import struct


def getAddrNextSteppingStone(chainFile):
    random.seed(1)
    indexOfFirstSS = random.randint(0, len(chainFile) - 1)
    addr, port = chainFile[indexOfFirstSS].split(" ")
    del chainFile[indexOfFirstSS]
    return addr, int(port)


def getData(url):
    return "Fake Data"


def sendDataHeader(s: socket.socket, dataLength):
    s.sendall(struct.pack('B', dataLength))




def recv_all(s: socket.socket, length: int):
    allData = bytearray()
    while True:
        data = s.recv(1024)
        print(data)
        allData = allData + data
        if not data:
            break
        if len(allData) >= length:
            break
    return allData
