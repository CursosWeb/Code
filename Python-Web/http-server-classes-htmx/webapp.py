#!/usr/bin/env python3

#
# webApp class
# Root for hierarchy of classes implementing web applications
#
# Copyright Jesus M. Gonzalez-Barahona 2009-2020
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
#

import socket

class WebApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse (self, request):
        """Parse the received request, extracting the relevant information."""

        print("Parse: Not parsing anything")
        return None

    def process (self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        print("Process: Returning 200 OK")
        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__ (self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print(f"Waiting for connections (port: {port})")
            (recvSocket, address) = mySocket.accept()
            print("HTTP request received (going to parse and process):")
            request = recvSocket.recv(8*1024)
            print(request)
            parsedRequest = self.parse(request.decode('utf8'))
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print("Answering back...")
            response = "HTTP/1.1 " + returnCode + " \r\n\r\n" \
                       + htmlAnswer + "\r\n"
            recvSocket.send(response.encode('utf8'))
            recvSocket.close()

if __name__ == "__main__":
    app = WebApp("localhost", 1234)
