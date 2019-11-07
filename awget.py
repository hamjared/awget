import argparse
import sys
import random
import socket
import pickle
import struct
from helpers import getAddrNextSteppingStone, sendDataHeader, recv_all


def main():
    parser = argparse.ArgumentParser(description='Parse for URL and chainfile')
    parser.add_argument("URL", help="Enter a URL")
    parser.add_argument('-c', nargs='?')
    arguments = parser.parse_args()
    if arguments.c is None:
        arguments.c = "chaingang.txt"
    url = arguments.URL
    chainFile = readChainFile(arguments.c)
    print('Request:', url)
    print('chainlist is:', chainFile)
    connectFirstSteppingStone(chainFile, url)


def readChainFile(filename):
    try:
        chainFile = open(filename).read().split("\n")
        del chainFile[0]
        return chainFile
    except FileNotFoundError:
        print("Chainfile not found, exiting...")
        sys.exit()


def connectFirstSteppingStone(chainFile, url):
    addr, port = getAddrNextSteppingStone(chainFile)
    print(addr, ":", port)
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chainFile.append(url)
    data = pickle.dumps(chainFile)
    print(data)
    ssSocket.connect((addr, int(port)))
    sendDataHeader(ssSocket, len(data))
    print("Sent chainfile: ", chainFile)
    ssSocket.sendall(data)
    allData = bytearray()
    length = ssSocket.recv(1)
    length = struct.unpack('B', length)[0]
    allData = recv_all(ssSocket, length)
    print(pickle.loads(allData))


def fileNameToSave(url):
    strings = url.split('/')
    return strings[-1]


if __name__ == '__main__':
    main()
