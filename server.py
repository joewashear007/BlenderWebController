#! /usr/bin/env python3

import http.server
import threading
import os
import socket
import socketserver
import base64
import hashlib
import struct
from io import StringIO
from string import Template
import webbrowser

class CGIExtHTTPRequestHandler(http.server.CGIHTTPRequestHandler):
    def is_python(self, path):
        return path.lower().endswith('.cgi')

    def is_cgi(self):
        base = self.path
        query = ''
        i = base.find('?')
        if i != -1:
            query = base[i:]
            base = base[:i]
        if not base.lower().endswith('.cgi'):
            return False
        [parentDirs, script] = base.rsplit('/', 1)
        self.cgi_info = (parentDirs, script+query)
        return True

class WebSocketsHandler(socketserver.StreamRequestHandler):
    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def _websocketHash(self, key):
        result_string = key + self.magic
        sha1_digest = hashlib.sha1(result_string).digest()
        response_data = base64.encodestring(sha1_digest).strip()
        response_string = response_data.decode('utf8')
        return response_string

    def setup(self):
        socketserver.StreamRequestHandler.setup(self)
        print("connection established", self.client_address)
        self.handshake_done = False

    def handle(self):
        #Overwrtien function from socketserver
        while 1:
            if not self.handshake_done:
                print("handshaking")
                self.handshake()
            else:
                print("Reading")
                msg = self.request.recv(2)
                if msg[0] == 136 or not msg:
                    print("Received Closed")
                    break
                length = msg[1] & 127
                if length == 126:
                    #length = struct.unpack(">H", self.request.recv(2))[0]
                    length = struct.unpack(">H", self.rfile.read(2))[0]
                elif length == 127:
                    length = struct.unpack(">Q", self.rfile.read(8))[0]
                masks = self.rfile.read(4)
                decoded = ""
                for char in self.rfile.read(length):
                    decoded += chr(char ^ masks[len(decoded) % 4])
                self.on_message(decoded)
        self.close()
        
    def _get_framehead(self, close=False):
        #Gets the frame header for sending data, set final fragment & opcode
        frame_head = bytearray(2)
        frame_head[0] = frame_head[0] | (1 << 7)
        if close:
            # send the close connection frame
            frame_head[0] = frame_head[0] | (8 << 0)
        else:
            #send the default text frame
            frame_head[0] = frame_head[0] | (1 << 0)
        return frame_head
            
        
    def _pack(self, data ,close=False):
        #pack bytes for sending to client
        frame_head = self._get_framehead(close)        
        # payload length
        if len(data) < 126:
            frame_head[1] = len(data)
        elif len(data) < ((2**16) - 1):
            # First byte must be set to 126 to indicate the following 2 bytes
            # interpreted as a 16-bit unsigned integer are the payload length
            frame_head[1] = 126
            frame_head += int_to_bytes(len(data), 2)
        elif len(data) < (2**64) -1:
            # Use 8 bytes to encode the data length
            # First byte must be set to 127
            frame_head[1] = 127
            frame_head += int_to_bytes(len(data), 8)
        frame = frame_head + data.encode('utf-8')
        return frame
    
    def close(self, message="Cxn Closed"):
        print("Server: Closing Connection")
        self.send_message("Server: Closing Connection")
        self.wfile.write(self._pack(message, True))
    
    def send_message(self, message):
        print("Starting Send Msg")
        self.wfile.write(self._pack(message))

    def handshake(self):
        key = None
        data = self.request.recv(1024).strip()
        for line in data.splitlines():
            if b'Upgrade:' in line:
                upgrade = line.split(b': ')[1]
                if not upgrade == "websocket":
                    print("ERROR! - Upgrade is not websocket!")
                    return
            if b'Sec-WebSocket-Key:' in line:
                key = line.split(b': ')[1]
                break
        if key is None:
            raise IOError("Couldn't find the key?\n\n", data)
        print('Handshaking...')
        digest = self._websocketHash(key)
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response.encode())
        print("Done!")
        print("Sending Connected Message")
        if self.handshake_done:
            self.send_message("Connected!")
        print("Done!")

    def on_message(self, msg):
        print(msg)
        self.send_message("Got :" + msg)

class HTTPServer(threading.Thread):
    def __init__(self, HttpPort):
        threading.Thread.__init__(self)
        self.port = HttpPort
        self.httpd = None
        self.host = socket.gethostbyname(socket.gethostname())
        self._start_server()
        
    def _checkPath(self):
        #Checks the curretn path for an blanks
        if 0 < os.getcwd().count(' '):
            print("ERROR!!! - The cwd path contains blanks! Can't Start Servers")
            return False
        else:
            return True
            
    def _start_server(self):
        #Starts the server at object init
        if not self._checkPath():
            return
        try:
            print("Starting HTTP Server ...")
            self.httpd = http.server.HTTPServer(("", self.port), CGIExtHTTPRequestHandler)
            print('Done! Serving on ' , self.host + ":" , self.port)
        except Exception as e:
            print("There server could not be started")
    
    def get_address(self):
        #returns string of the servers address or None
        if self.httpd is not None:
            return 'http://{host}:{port}/'.format(host=self.host, port=self.port)
        else:
            return None

    def run(self):
        #Overwrtien from Threading.Thread
        if self.httpd is not None:
            self.httpd.serve_forever()
        else:
            print("Error! - Server Not Started!")

    def stop(self):
        #Overwrtien from Threading.Thread
        print("Killing Http Server ...")
        if self.httpd is not None:
            self.httpd.shutdown()
        print("Done")

class WebsocketServer(threading.Thread):
    def __init__(self, WebsocketPort):
        threading.Thread.__init__(self)
        self.port = WebsocketPort
        self.wsd = None
        self.host = socket.gethostbyname(socket.gethostname())
        self._start_server()

    def _start_server(self):
        #Starts the server at object init
        try:
            print("Starting Websocket Server ... ")
            self.wsd = socketserver.TCPServer(("", self.port), WebSocketsHandler)
            print('Done! Serving on ' , self.host , ":" , self.port)
        except Exception as e:
            print("Error! - Server Not Started!")
            
    def get_address(self):
        #returns string of the servers address or None
        if self.wsd is not None:
            return 'ws://{host}:{port}/'.format(host=self.host, port=self.port)
        else:
            return None
            
    def run(self):
        if self.wsd is not None:
            self.wsd.serve_forever()
        else:
            print("The server could not be started!")

    def stop(self):
        print("Killing WebSocket Server ...")
        if self.wsd is not None:
            self.wsd.shutdown()
        print("Done")

def launchUI(http_address, ws_address):
    html = open("index.html" ,"w")
    temp = open("index.temp", "r")
    html.write(Template(temp.read()).substitute(address=ws_address))
    html.close()
    temp.close()
    webbrowser.open(http_address+ "/index.html")
    
def main():
    quit = False
    while( not quit):
        c = input("Enter input [s,q]: ")
        if c == "s":
            httpServer = HTTPServer(8000)
            wsServer = WebsocketServer(9999)
            http_address = httpServer.get_address()
            ws_address = wsServer.get_address()
            if ws_address is not None and http_address is not None:
                launchUI(http_address, ws_address)
                httpServer.start()
                wsServer.start()
            else:
                print("Error Starting Webserver!")
            
        if c == "q":
            httpServer.stop()
            wsServer.stop()
            quit = True

if __name__ == '__main__':
    main()