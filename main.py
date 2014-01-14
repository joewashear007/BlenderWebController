#! /usr/bin/env python3

# /*
 # * ----------------------------------------------------------------------------
 # * "THE BEER-WARE LICENSE" (Revision 42):
 # * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 # * can do whatever you want with this stuff. If we meet some day, and you think
 # * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 # * ----------------------------------------------------------------------------
 # */
 
from server import WebSocketHttpServer
from server import WebSocketsHandler
import threading

def main():
	print()
	print()
	print("*** Starting Websocket Server ***")
    print()
    print("Press Any Key To Quit...")
    print()
	server = WebSocketHttpServer(8000, 9999, WebSocketsHandler)
	if server.start():
		print("Server Started on:" + server.httpServer.get_address())
		print("Launching Website")
		server.launch_webpage()
	else:
		print("Error Starting Server")
	i = input("Press any key to quit!")
	server.stop()
	print("Good Bye")

if __name__ == '__main__':
	main()
