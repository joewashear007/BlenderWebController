#! /usr/bin/env python3

import http.server
import threading
import os
import socket
import socketserver
import base64
import hashlib
import struct
import select
from io import StringIO


#### GLOBAL ####
ServerRun = True

################

#### FUNCS #####
def callback(data):
	print("Received: ", data)
################
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

class HTTPServer(threading.Thread):
	def __init__(self, HttpPort):
		threading.Thread.__init__(self)
		self.HttpPort = HttpPort
		self.httpd = None
		self.host = socket.gethostbyname(socket.gethostname())

	def run(self):
		if 0 < os.getcwd().count(' '): 
			print("ERROR!!! - The cwd path contains blanks! Can't Start Servers")
		else:
			print("Starting HTTP Server ...")
			server_addr = ("", self.HttpPort)
			self.httpd = http.server.HTTPServer(server_addr, CGIExtHTTPRequestHandler)
			print('Done! Serving on ' , self.host + ":" , self.HttpPort)
			self.httpd.serve_forever()
		
	def stop(self):
		print("Killing Http Server ...")
		self.httpd.shutdown()
		print("Done")
		
class Websocket(object):
	def __init__(self, port, new_client_callback=None):
		self.port = int(port)
		self.callback = new_client_callback

	def calculate_websocket_hash(self, key):
		magic_websocket_string = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
		result_string = key + magic_websocket_string
		sha1_digest = hashlib.sha1(result_string).digest()
		response_data = base64.encodestring(sha1_digest).strip()
		response_string = response_data.decode('utf8')
		return response_string

	def set_bit(self, int_type, offset):
		#set_bit(2, 0) : 3
		return int_type | (1 << offset)

	def bytes_to_int(self, data):
		#Convert a bytes/str/list to int.
		return int.from_bytes(data, byteorder='big')

	def int_to_bytes(self, number, bytesize):
		#Convert an integer to a bytearray. 
		#The integer is represented as an array of bytesize. An OverflowError 
		#is raised if the integer is not representable with the given number
		#of bytes.
			return bytearray(number.to_bytes(bytesize, byteorder='big'))

	def pack(self, data):
		#pack bytes for sending to client
		frame_head = bytearray(2)
		# set final fragment
		frame_head[0] = set_bit(frame_head[0], 7)
		# set opcode 1 = text
		frame_head[0] = set_bit(frame_head[0], 0)
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
		# add data
		frame = frame_head + data.encode('utf-8')
		#print(list(hex(b) for b in frame))
		return frame

	def receive(self):
		#blocking call to receive data from client    
		# read the first two bytes
		frame_head = self.s.recv(2)
		#On severed connection
		if frame_head == '' or frame_head == b'':
			return
		# length of payload
		# 7 bits, or 16 bits, 64 bits
		payload_length = frame_head[1] & 0x7F
		if payload_length == 126:
			raw = self.s.recv(2)
			payload_length = bytes_to_int(raw)
		elif payload_length == 127:
			raw = self.s.recv(8)
			payload_length = bytes_to_int(raw)
		#masking key
		#All frames sent from the client to the server are masked by a
		#32-bit nounce value that is contained within the frame
		#print("mask: ", masking_key, bytes_to_int(masking_key))
		
		# finally get the payload data:
		bytes_received = 0
		masked_data_in = bytearray(payload_length)
		while bytes_received < payload_length:
			data_in = bytearray(self.s.recv(payload_length))
			#print "Received {} bytes".format(len(data_in))
			masked_data_in[bytes_received:bytes_received+len(data_in)] = data_in
			bytes_received += len(data_in)
		data = bytearray(payload_length)
		# The ith byte is the XOR of byte i of the data with
		# masking_key[i % 4]
		for i, b in enumerate(masked_data_in):
			data[i] = b ^ masking_key[i%4]
		return data

	def serve_forever(self, end=None):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('', int(self.port)))
		self.s.listen(1)
		while True:
			r, w, e = select.select((self.s,), (), (), 1)
			for l in r:
				t, address = self.s.accept()
				print("Accepting connection from {}:{}".format(*address))
				self.handle_connection()
			else:
				# should we quit?
				if end is not None and end:
					return
					

	def transmit(self, msg_str):
		self.s.send(self.pack(msg_str))

	def handle_connection(self):
		client_request = self.s.recv(4096)
		key = None
		# get to the key
		for line in client_request.splitlines():
			#print(line.strip())
			if b'Sec-WebSocket-Key:' in line:
				key = line.split(b': ')[1]
				break
		if key is None:
			raise IOError("Couldn't find the key?\n\n", client_request)
		response_string = self.calculate_websocket_hash(key)
		header = 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n'
		header += 'Connection: Upgrade\r\nSec-WebSocket-Accept: {}\r\n\r\n'
		header = header.format(response_string)
		self.s.send(header.encode())
		if self.callback is not None:
			self.callback(self.receive())

	def __del__(self):
		self.s.close()
		
class WebsocketServer(threading.Thread):
	def __init__(self, Port):
		threading.Thread.__init__(self)
		self.wsPort = Port
		self.wsd = None
		self.host = socket.gethostbyname(socket.gethostname())

	def run(self):
		print("Starting Websocket Server ...")
		self.wsd = Websocket(self.wsPort, callback)
		print('Done! Serving on ' , self.host + ":" , self.wsPort)
		self.wsd.serve_forever(ServerRun)

	def stop(self):
		print("Killing Websocket Server ...")
		self.wsd.shutdown()
		print("Done")





def main():
	quit = False
	ServerRun = False
	while( not quit):
		c = input("Enter input [s,k,q]: ")
		if c == "s" and  not ServerRun:
			httpServer = HTTPServer(8000)
			wsServer = WebsocketServer(9999)
			httpServer.start()
			wsServer.start()
			ServerRun = True
		if c == "k" and ServerRun:
			ServerRun = False
			httpServer.stop()
			wsServer.stop()
		if c == "q":
			if ServerRun :
				httpServer.stop()
				wsServer.stop()
			quit = True

if __name__ == '__main__':
	main()
