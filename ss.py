import argparse
import urllib.request
import threading
from _thread import *
import time
import pickle
import socket
import struct
from helpers import getData, sendDataHeader, getAddrNextSteppingStone, recv_all


def threadedSS(connection: socket.socket):
    length = connection.recv(1)
    length = struct.unpack('B', length)[0]
    allData = recv_all(connection, length)
    allData = pickle.loads(allData)
    print(allData)
    needToVisit = allData['needToVisit']
    if len(needToVisit) == 0:
        # last stepping stone so get the file
        print("sending data back")
        dataToSendBack = getData(allData['url'])
        dataToSendBack = pickle.dumps(dataToSendBack)
        sendDataHeader(connection, len(dataToSendBack))
        connection.sendall(dataToSendBack)
    else:
        # get the next stepping stone
        chainfile = needToVisit
        url = allData['url']
        addr, port = getAddrNextSteppingStone(chainfile)
        print("All data: ", allData)
        allData = pickle.dumps(allData)
        print("Next stepping stone: ", addr, ":", port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        sendDataHeader(s, len(allData))
        s.sendall(allData)
        length = s.recv(1)
        length = struct.unpack('B', length)[0]
        data = recv_all(s, length)
        sendDataHeader(connection, len(data))
        connection.sendall(data)
        connection.close()
        s.close()


def main():
    parser = argparse.ArgumentParser(description='Parse for port')
    parser.add_argument('-p', nargs='?')
    arguments = parser.parse_args()
    if arguments.p is None:
        port = 6324
    else:
        port = int(arguments.p)
    hostName = socket.gethostname()

    print(socket.gethostbyname_ex(hostName)[2])
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
