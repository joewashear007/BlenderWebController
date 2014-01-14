#! /usr/bin/env python3

# /*
 # * ----------------------------------------------------------------------------
 # * "THE BEER-WARE LICENSE" (Revision 42):
 # * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 # * can do whatever you want with this stuff. If we meet some day, and you think
 # * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 # * ----------------------------------------------------------------------------
 # */

import tempfile
import http.server
import threading
import os
import socket
import socketserver
import base64
import hashlib
import struct
import shutil
import webbrowser
from io import StringIO
from string import Template

#GLOBALS
httpServer = None
wsServer = None

# Inherit this class to handle the websocket connection
class WebSocketsHandler(socketserver.BaseRequestHandler):

#-------------- Over ride these  ----------------------------------------
    def on_message(self, msg):
        #Override this function to handle the input from webcontroller
        print(msg)
        self.send_message("Got :" + msg)
        
    def send_message(self, message):
        self.request.sendall(self._pack(message))
#-------------------------------------------------------------------

    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def setup(self):
        #Overwrtien function from socketserver
        #Init some varibles
        #socketserver.StreamRequestHandler.setup(self)
        print("connection established", self.client_address)
        self.closeHandle = False
        self.handshake_done = False
    
    def handle(self):
        #handles the handshake with the server
        #Overwrtien function from socketserver
        while not self.handshake_done:
            self.handshake()
            
        #runs the handler in a thread
        while 1:
            print("Reading")
            msg = self.request.recv(2)
            if msg[0] == 136 or not msg or self.closeHandle: 
                print("Received Closed")
                break
            length = msg[1] & 127
            if length == 126:
                #length = struct.unpack(">H", self.request.recv(2))[0]
                length = struct.unpack(">H", self.request.recv(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self.request.recv(8))[0]
            masks = self.request.recv(4)
            decoded = ""
            for char in self.request.recv(length):
                decoded += chr(char ^ masks[len(decoded) % 4])
            self.on_message(decoded)
        self.close()
        
    def close(self, message="Cxn Closed"):
        self.closeHandle = True
        print("Server: Closing Connection")
        self.send_message("Server: Closing Connection")
        self.request.sendall(self._pack(message, True))
    
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
            raise Exception("Couldn't find the key?:", data)
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
        
    def _websocketHash(self, key):
        result_string = key + self.magic
        sha1_digest = hashlib.sha1(result_string).digest()
        response_data = base64.encodestring(sha1_digest).strip()
        response_string = response_data.decode('utf8')
        return response_string

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
            #Using srd CGU Handler
            self.httpd = http.server.HTTPServer(("", self.port), http.server.CGIHTTPRequestHandler)
            #self.httpd = http.server.HTTPServer(("", self.port), CGIExtHTTPRequestHandler)
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

class WebSocketTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    #Added a list of current handlers so they can be closed
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.handlers = []
        self.daemon_threads = False
        
    def finish_request(self, request, client_address):
        #Finish one request by instantiating RequestHandlerClass
        self.RequestHandlerClass(request, client_address, self)
        
    def process_request(self, request, client_address):
        #Start a new thread to process the request
        t = threading.Thread(target = self.process_request_thread, args = (request, client_address))
        t.daemon = True
        t.start()
        self.handlers.append(t)
        
    def get_handlers(self):
        #returns the list of handlers
        return self.handlers
    
class WebsocketServer(threading.Thread):
    def __init__(self, WebsocketPort, handler):
        threading.Thread.__init__(self)
        self.port = WebsocketPort
        self.wsd = None
        self.handler = handler
        self.host = socket.gethostbyname(socket.gethostname())
        self._start_server()

    def _start_server(self):
        #Starts the server at object init
        try:
            print("Starting Websocket Server ... ")
            self.wsd = WebSocketTCPServer(("", self.port), self.handler)
            print('Done! Serving on ' , self.host , ":" , self.port)
        except Exception as e:
            print("Error! - Server Not Started!", e)
            
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
        
    def get_handlers(self):
        #returns the list of handlers
        return self.wsd.get_handlers()
        
class WebSocketHttpServer():
    def __init__(self, http_port, websocket_port, handler_class):
        self.http_port = http_port
        self.websocket_port = websocket_port
        self.handler = handler_class
        self.httpServer = None
        self.wsServer = None

    def _make_server_temp_dir(self):
        #make the new temp directory
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)
        print("Changed Directory to: " + self.tempdir)
        #copy the files over
    
    def _make_webpage(self):
        shutil.copytree( self.cwd+"\\res\\", self.tempdir+"\\res\\")
        html = open(self.tempdir + "\\index.html" ,"w")
        temp = open(self.cwd + "\\index.temp", "r")
        content = temp.read()
        content_sub = Template(content).substitute(address=self.wsServer.get_address())
        html.write(content_sub)
        html.close()
        temp.close()
        
    def stop(self):
        try:
            self.httpServer.stop()
            self.wsServer.stop()
        except Exception as e:
            print("The Servers were never started")
        
    def start(self):
        try:
            # make directorys and copy files
            self._make_server_temp_dir()
            #launch the servers
            self.httpServer = HTTPServer(self.http_port)
            self.wsServer = WebsocketServer(self.websocket_port, self.handler)
            if self.wsServer is not None and self.httpServer is not None:
                self.httpServer.start()
                self.wsServer.start()
                self._make_webpage()
                return True
            else:
                print("Error Starting Webserver!")
                return False
        except Exception as e:
            print("Error, There is some error!")
            print(e)
            return False
            
    def launch_webpage(self):
        #Copies all the resource over to the temp dir
        webbrowser.open(self.httpServer.get_address() + "index.html")
        
    def server_status(self):
        return

if __name__ == '__main__':
    print("No Main Program!")

