import socket, threading


class SteppingStone(threading.Thread):
    def __init__(self, url, chainFile):
        threading.Thread.__init__(self)
