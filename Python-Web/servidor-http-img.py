#!/usr/bin/python

#
# Simple HTTP Server
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2010
# September 2009
# Febraury 2022
# February 2025

import socket

# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTLM page
#  (in a loop)

try:
    while True:
        print("Waiting for connections")
        (recvSocket, address) = mySocket.accept()
        print("HTTP request received:")
        request = recvSocket.recv(2048)
        print(request)
        request_parts = request.decode('utf-8').split(' ',2)
        resource = request_parts[1]
        if resource == '/':
            response = (b"HTTP/1.1 200 OK\r\n"
                + b"Content-Type: text/html; charset=UTF-8\r\n\r\n") \
                + b"<html><body>" \
                + b"<h1>Hello world with image</h1>" \
                + b"<img src='/image'/></body></html>"
        elif resource == '/image':
            image = open('image.jpg', 'rb').read()
            response = (b"HTTP/1.1 200 OK\r\n"
                + b"Content-Type: image/jpeg\r\n\r\n") \
                + image
        else:
            response = (b"HTTP/1.1 404 Not Found\r\n"
                + b"Content-Type: text/html; charset=UTF-8\r\n\r\n") \
                + b"<html><body>" \
                + b"<h1>Not Found</h1>" \
                + b"</body></html>"
        recvSocket.send(response)
        recvSocket.close()

except KeyboardInterrupt:
	print("Closing binded socket")
	mySocket.close()
