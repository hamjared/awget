import socket, threading


class SteppingStone(threading.Thread):
    def __init__(self, url, chainFile, client):
        threading.Thread.__init__(self)
