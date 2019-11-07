import argparse
import sys
import random
import socket


def main():
    parser = argparse.ArgumentParser(description='Parse for URL and chainfile')
    parser.add_argument("URL", help="Enter a URL")
    parser.add_argument('-c', nargs='?')
    arguments = parser.parse_args()
    if arguments.c is None:
        arguments.c = "chaingang.txt"
    url = arguments.URL
    chainFile = readChainFile(arguments.c).split("\n")
    print('Request:', url)
    print('chainlist is:', chainFile[1:])
    connectFirstSteppingStone(chainFile)


def readChainFile(filename):
    try:
        return open(filename).read()
    except FileNotFoundError:
        print("Chainfile not found, exiting...")
        sys.exit()


def getAddrAndPortFirstSteppingStone(chainFile):
    random.seed(1)
    indexOfFirstSS = random.randint(1, int(chainFile[0]))
    addr, port = chainFile[indexOfFirstSS].split(" ")
    return addr, port


def connectFirstSteppingStone(chainFile):
    addr, port = getAddrAndPortFirstSteppingStone(chainFile)
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.connect((addr, int(port)))


def fileNameToSave(url):
    strings = url.split('/')
    return strings[-1]


if __name__ == '__main__':
    main()
