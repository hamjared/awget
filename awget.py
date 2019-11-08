import argparse
import sys
import socket
import pickle
import struct
import time

from helpers import getAddrNextSteppingStone, sendDataHeader, recv_all, getLength


def main():
    parser = argparse.ArgumentParser(description='Parse for URL and chainfile')
    parser.add_argument("URL", help="Enter a URL")
    parser.add_argument('-c', nargs='?')
    arguments = parser.parse_args()
    if arguments.c is None:
        arguments.c = "chaingang.txt"
    url = arguments.URL
    chainFile = readChainFile(arguments.c)
    try:
        chainFile.remove('')
    except ValueError:
        pass
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
    chainStack = []
    addr, port = getAddrNextSteppingStone(chainFile)
    allData = {}
    allData.update({'needToVisit': chainFile})
    allData.update({'url': url})
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = pickle.dumps(allData)
    ssSocket.connect((addr, int(port)))
    sendDataHeader(ssSocket, len(data))
    ssSocket.sendall(data)

    print("waiting for file ....")
    length = getLength(ssSocket)
    allData = recv_all(ssSocket, length)
    allData = pickle.loads(allData)
    file = open(url.split("/")[-1], 'wb')
    file.write(allData)
    file.close()

    print("Received file ", url.split("/")[-1])
    print("Goodbye!")


def fileNameToSave(url):
    strings = url.split('/')
    return strings[-1]


if __name__ == '__main__':
    main()
