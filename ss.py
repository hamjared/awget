import urllib.request
import threading
from _thread import *
import time
import pickle
import socket


def threadedSS(connection):
    print("in threaded function")
    allData = bytearray()
    while True:
        data = connection.recv(1024)
        allData = allData + data
        if not data:
            break
    print(allData)
    print(pickle.loads(allData))


def main():
    hostName = socket.gethostname()

    print(socket.gethostbyname_ex(hostName)[2])
    port = 6324
    host = ""
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.bind((host, port))
    ssSocket.listen(5)
    print("Socket listening on ", socket.gethostbyname_ex(hostName)[2], "port: ", port)

    while True:
        connection, addr = ssSocket.accept()
        print("Connected to ", addr[0], ":", addr[1])
        start_new_thread(threadedSS, (connection,))


if __name__ == '__main__':
    main()
