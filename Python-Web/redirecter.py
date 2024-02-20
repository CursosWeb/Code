#!/usr/bin/python

"""Simple redirector application"""

import random
import socket

my_port = 1234

def process(request):
    next_resource = "/" + str(random.randint(0, 10000))
    response = "HTTP/1.1 301 Moved permanently\r\n"
    response += f"Location: {next_resource}\r\n"
    response += "\r\n"
    return response.encode('utf-8')

def main():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocket.bind(('', my_port))
    mySocket.listen(5)
    random.seed()

    try:
        while True:
            print(f"Waiting for connections (port: {my_port})")
            (recvSocket, address) = mySocket.accept()
            request = recvSocket.recv(8*1024)
            print("HTTP request received:")
            response = process(request)
            recvSocket.send(response)
            recvSocket.close()

    except KeyboardInterrupt:
        print("Closing binded socket")
        mySocket.close()

if __name__ == "__main__":
    main()
