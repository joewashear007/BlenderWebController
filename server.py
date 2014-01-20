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


class QuiteCGIHandler(http.server.CGIHTTPRequestHandler):
    def log_message(self, format, *args):
        pass #Hides all messages for Request Handler

# Inherit this class to handle the websocket connection
class WebSocketsHandler(socketserver.BaseRequestHandler):

#-------------- Over ride these  ----------------------------------------
    def on_message(self, msg):
        #Override this function to handle the input from webcontroller
        print(msg)
        self.send_message("Got :" + msg)
        
    def on_close(self):
        print("Server: Closing Connection for ", self.client_address)
        self.send_message("Server: Closing Connection")
        
    def send_message(self, message):
        self.request.sendall(self._pack(message))
#-------------------------------------------------------------------

    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def setup(self):
        #Overwrtien function from socketserver
        #Init some varibles
        print("\nConnection Established", self.client_address)
        self.closeHandle = False
    
    def handle(self):
        #handles the handshake with the server
        #Overwrtien function from socketserver
        try:
            self.handshake()
        except:
            print("HANDSHAKE ERROR! - Try using FireFox")
            return
            
        #runs the handler in a thread
        while 1:
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
            self.on_message(decoded)
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
        if self.httpd is not None:
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
            self.wsd.shutdown()
        print("Done")
        
    def get_handlers(self):
        #returns the list of handlers
        return self.wsd.get_handlers()
        
class WebSocketHttpServer():
    def __init__(self, handler_class, http_address=('',0), ws_address=('',0) ):
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
    
    def _make_webpage(self):
        shutil.copytree( self.cwd+"\\res\\", self.tempdir+"\\res\\")
        html = open(self.tempdir + "\\index.html" ,"w")
        for line in open(self.cwd + "\\index.temp", "r"):
            if line.find("$address") > 0 :
                line = Template(line).safe_substitute(address=self.wsServer.get_address())
            if line.find("__PYTHON_INSERT__") > 0:
                css = open(self.cwd + "\\res\\style.css", "r")
                js = open(self.cwd + "\\res\\controller.js", "r")
                html.write("<script>"+js.read()+"</script>")
                html.write("<style>"+css.read()+"</style>")
                js.close()
                css.close()
            html.write(line)
        html.close()
        
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

