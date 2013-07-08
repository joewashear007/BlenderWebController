import struct
import socketserver
import base64
import hashlib
from io import StringIO

class WebSocketsHandler(socketserver.StreamRequestHandler):
	magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
	def websocketHash(self, key):
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
		while True:
			if not self.handshake_done:
				self.handshake()
				print("handshaking")
			else:
				print("Reading")
				self.read_next_message()

	def read_next_message(self):
		try:
			length = self.rfile.read(2)[1] & 127
			if length == 126:
				length = struct.unpack(">H", self.rfile.read(2))[0]
			elif length == 127:
				length = struct.unpack(">Q", self.rfile.read(8))[0]
			masks = self.rfile.read(4)
			decoded = ""
			for char in self.rfile.read(length):
				decoded += chr(char ^ masks[len(decoded) % 4])
			self.on_message(decoded)
		except Exception as e:
			print("Exception when reading!")
		
	def pack(self, data):
		#pack bytes for sending to client
		frame_head = bytearray(2)

		# set final fragment & opcode 1 = text
		frame_head[0] = frame_head[0] | (1 << 7)
		frame_head[0] = frame_head[0] | (1 << 0)

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
		
	def send_message(self, message):
		print("Starting Send Msg")
		self.wfile.write(self.pack(message))

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
		digest = self.websocketHash(key)
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


if __name__ == "__main__":
	server = socketserver.TCPServer(
		("", 9999), WebSocketsHandler)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("Got ^C")
		server.server_close();
		print("bye!")
