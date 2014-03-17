#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



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
import json
from io import StringIO
from string import Template


def writeWebsite(file, new_address):
    site = Template($WEBSITE).safe_substitute(address=new_address)
    html = open(file ,"w")
    html.write(site)
    html.close()


class QuiteCGIHandler(http.server.CGIHTTPRequestHandler):
    def log_message(self, format, *args):
        pass #Hides all messages for Request Handler

# Inherit this class to handle the websocket connection
class WebSocketHandler(socketserver.BaseRequestHandler):

#-------------- Over ride these  ----------------------------------------
    def on_message(self, msg):
        #msg is a array, decoded from JSON
        #Override this function to handle the input from webcontroller
        print(msg)
        #self.send_message("Got :" + ast.literal_eval(msg))
        
    def handle_message(self, msg):    
        #only the user with the lock can control
        if self._hasLock():
            msg_data = json.loads(msg)
            if "MASTER_REQUEST" in msg_data:
                if msg_data["MASTER_REQUEST"]:
                    WebSocketHandler.lock_id = threading.current_thread().ident
                    self.send_json(dict(MASTER_STATUS=True));
                    print("Locking to thread: " ,WebSocketHandler.lock_id, "   :   ", self.id)
                    self.broadcast_all(dict(SLAVE=True))
                else:
                    WebSocketHandler.lock_id = None
                    self.send_json(dict(MASTER_STATUS=False))
                    self.broadcast_all(dict(SLAVE=False))
            #elif "MESSAGE" in msg_data:
            #    self.on_message(msg["MESSAGE"])
            #else:
            #   print("Unknown CMD, trashing: ", msg_data)
            self.on_message(msg_data)
        else:
            self.send_json(dict(SLAVE=True));
            print("Locked, trashing: ", msg) 
            
    def on_close(self):
        print("Server: Closing Connection for ", self.client_address)
        self.send_message("Server: Closing Connection")
        
    def send_message(self, message):
        print("Sending: ", message)
        self.send_json(dict(MESSAGE=message))
        
    def send_json(self, data):
        #sends a python dict as a json object
        self.request.sendall(self._pack(json.dumps(data)))
        
    def broadcast_all(self, data):
        #send a araay converted into JSON to every thread
        for t in WebSocketHandler.connections:
            if t.id == self.id:
                continue
            t.send_json(data)
    
#-------------------------------------------------------------------

    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    lock_id = None
    connections = []

    def _hasLock(self):
        #there is no lock or the current thread has it
        return (not WebSocketHandler.lock_id) or (WebSocketHandler.lock_id == self.id)
    
    
    
    def setup(self):
        #Overwrtien function from socketserver
        #Init some varibles
        print("\nConnection Established", self.client_address)
        self.closeHandle = False
        self.id = threading.current_thread().ident
        self.alive = threading.Event()
        self.alive.set()
        WebSocketHandler.connections.append(self)
    
    def handle(self):
        #handles the handshake with the server
        #Overwrtien function from socketserver
        try:
            self.handshake()
        except:
            print("HANDSHAKE ERROR! - Try using FireFox")
            #return
           
    def run(self):
        #runs the handler in a thread
        while self.alive.isSet():
            msg = self.request.recv(2)
            if not msg or self.closeHandle or msg[0] == 136: 
                print("Received Closed")
                break
            length = msg[1] & 127
            if length == 126:
                length = struct.unpack(">H", self.request.recv(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self.request.recv(8))[0]
            masks = self.request.recv(4)
            decoded = ""
            for char in self.request.recv(length):
                decoded += chr(char ^ masks[len(decoded) % 4])
            self.handle_message(decoded)
            
            #WebSocketHandler.broadcast_all.wait(0.01)
            
        self.close()
        
    def close(self, message="Cxn Closed"):
        self.closeHandle = True
        self.request.sendall(self._pack(message, True))
        self.on_close()
    
    def handshake(self):
        key = None
        data = self.request.recv(1024).strip()
        for line in data.splitlines():
            if b'Upgrade:' in line:
                upgrade = line.split(b': ')[1]
                if not upgrade == b'websocket':
                    raise Exception("Upgrade is Not a websocket!", data)
            if b'Sec-WebSocket-Key:' in line:
                key = line.split(b': ')[1]
                break
        if key is None:
            raise Exception("Couldn't find the key?:", data)
        print('Handshaking...   ', end = '')
        digest = self._websocketHash(key)
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response.encode())
        print("Sending Connected Message...   ", end = '')
        if self.handshake_done:
            self.send_message("Connected!")
        print("Connected!\n")
        
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
    def __init__(self, address_info=('',0)):
        threading.Thread.__init__(self)
        self.httpd = None
        self._start_server( address_info )
           
    def _start_server(self, address_info):
        #Starts the server at object init
        try:
            #Using std CGI Handler
            self.httpd = http.server.HTTPServer(address_info, QuiteCGIHandler)
            print("HTTP Server on : ", self.get_address() )
        except Exception as e:
            print("The HTTP server could not be started")
    
    def get_address(self):
        #returns string of the servers address or None
        if self.httpd is not None:
            return 'http://{host}:{port}/'.format(host=socket.gethostbyname(self.httpd.server_name), port=self.httpd.server_port)
        else:
            return None

    def run(self):
        #Overwrtien from Threading.Thread
        if self.httpd is not None :
            self.httpd.serve_forever()
        else:
            print("Error! - HTTP Server is NULL")

    def stop(self):
        #Overwrtien from Threading.Thread
        print("Killing Http Server ...")
        if self.httpd is not None:
            self.httpd.shutdown()
        print("Done")

class WebSocketTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    #Added a list of current handlers so they can be closed
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.handlers = []
        self.daemon_threads = True
        
    def finish_request(self, request, client_address):
        #Finish one request by instantiating RequestHandlerClass
        print("launching a new request")
        t = self.RequestHandlerClass(request, client_address, self)
        print("Request:" , t)
        self.handlers.append(t)
        print("Num request:" ,len(self.handlers))
        t.run()
        
    # def process_request(self, request, client_address):
        # #Start a new thread to process the request
        # t = threading.Thread(target = self.process_request_thread, args = (request, client_address))
        # t.daemon = True
        # t.start() 
        
    def get_handlers(self):
        #returns the list of handlers
        return self.handlers
    
class WebsocketServer(threading.Thread):
    def __init__(self, handler, address_info=('',0)):
        threading.Thread.__init__(self)
        self.wsd = None
        self.handler = handler
        self._start_server(address_info)

    def _start_server(self, address_info):
        #Starts the server at object init
        try:
            self.wsd = WebSocketTCPServer( address_info, self.handler)
            print( self.get_address())
        except Exception as e:
            print("Error! - Websocket Server Not Started!", e)
            
    def get_address(self):
        #returns string of the servers address or None
        if self.wsd is not None:
            return 'ws://{host}:{port}/'.format(host=socket.gethostbyname(self.wsd.server_name), port=self.wsd.server_port)
        else:
            return None
            
    def run(self):
        if self.wsd is not None:
            self.wsd.serve_forever()
        else:
            print("The WebSocket Server is NULL")

    def stop(self):
        print("Killing WebSocket Server ...")
        if self.wsd is not None:
            for h in self.wsd.handlers:
                h.alive.clear()
                
            self.wsd.shutdown()
        print("Done")
        
    def get_handlers(self):
        #returns the list of handlers
        return self.wsd.get_handlers()
        
    def send(self, msg):
        for h in self.wsd.get_handlers():
            h.send_message(msg)
        
class WebSocketHttpServer():
    def __init__(self, handler_class = WebSocketHandler, http_address=('',0), ws_address=('',0) ):
        self.http_address = http_address
        self.ws_address = ws_address
        self.handler = handler_class
        self.httpServer = None
        self.wsServer = None

    def _clean_server_temp_dir(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tempdir)
        os.rmdir(self.tempdir)
        
    def _make_server_temp_dir(self):
        #make the new temp directory
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)
        print("New temp dir:", self.tempdir)
    
    def _make_webpage(self):
        writeWebsite(self.tempdir + "/index.html" , self.wsServer.get_address())
        
    def stop(self):
        try:
            self.httpServer.stop()
            self.wsServer.stop()
            self._clean_server_temp_dir()
        except Exception as e:
            print("The Servers were never started")
        
    def start(self):
        try:
            # make directory and copy files
            self._make_server_temp_dir()
            self.httpServer = HTTPServer(self.http_address)
            self.wsServer = WebsocketServer(self.handler, self.ws_address)
            if self.wsServer is not None and self.httpServer is not None:
                self.httpServer.start()
                self.wsServer.start()
                self._make_webpage()
                return True
            else:
                print("Error Starting The Servers, Something is not Initialized!")
                return False
        except Exception as e:
            print()
            print("Error!!!, There is some error!")
            print(e)
            print()
            return False
    
    def send(self, msg):
        self.wsServer.send(msg)
    
    def launch_webpage(self):
        #Copies all the resource over to the temp dir
        webbrowser.open(self.httpServer.get_address() + "index.html")
        
    def status(self):
        if self.wsServer is None or self.httpServer is None:
            return False
        else:
            return True
            
if __name__ == '__main__':
    print("No Main Program!")

