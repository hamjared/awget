import urllib.request
import threading
from _thread import *
import socket

clientLock = threading.Lock()

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
        addr, port = ssSocket.accept()
        clientLock.acquire()
        print("Connected to ", addr, ":", port)


if __name__ == '__main__':
    main()
