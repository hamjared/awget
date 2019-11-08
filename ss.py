import argparse
import urllib.request
import threading
from _thread import *
import time
import pickle
import socket
import struct
from helpers import getData, sendDataHeader, getAddrNextSteppingStone, recv_all, getLength


def threadedSS(connection: socket.socket):
    length = getLength(connection)
    allData = recv_all(connection, length)
    allData = pickle.loads(allData)
    needToVisit = allData['needToVisit']
    url = allData['url']
    print("Request: ", url)
    if len(needToVisit) == 0:
        # last stepping stone so get the file
        print("chainlist is empty")
        dataToSendBack = getData(allData['url'])
        dataToSendBack = pickle.dumps(dataToSendBack)
        sendDataHeader(connection, len(dataToSendBack))
        print("Relaying file ...")
        connection.sendall(dataToSendBack)
    else:
        # get the next stepping stone
        chainfile = needToVisit
        addr, port = getAddrNextSteppingStone(chainfile)
        allData = pickle.dumps(allData)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        sendDataHeader(s, len(allData))
        s.sendall(allData)
        length = getLength(s)
        print("waiting for file ...")
        data = recv_all(s, length)
        sendDataHeader(connection, len(data))
        print("Relaying file ...")
        connection.sendall(data)
        connection.close()
        print("Goodbye!")


def main():
    parser = argparse.ArgumentParser(description='Parse for port')
    parser.add_argument('-p', nargs='?')
    arguments = parser.parse_args()
    if arguments.p is None:
        port = 6324
    else:
        port = int(arguments.p)
    hostName = socket.gethostname()

    host = ""
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssSocket.bind((host, port))
    ssSocket.listen(100)
    print("Socket listening on ", socket.gethostbyname_ex(hostName)[2], "port: ", port)

    while True:
        connection, addr = ssSocket.accept()
        print("Connected to ", addr[0], ":", addr[1])
        start_new_thread(threadedSS, (connection,))


if __name__ == '__main__':
    main()
