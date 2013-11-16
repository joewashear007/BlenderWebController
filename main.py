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

running = True

def run(server):
    server.start()
    while running:
        server.server_status()

def main():
    print()
    print()
    print("*** Starting Websocket Server ***")
    server = WebSocketHttpServer(8000, 9999, WebSocketsHandler)
    #start the server its only threading
    t = threading.Thread(target = run, args = (server,) )
    t.daemon = False
    t.start()
    print("Launching Website")
    server.launch_webpage()
    i = input("Press any key to quit!")
    running = False
    t.join()
    server.stop()
    print("Good Bye")

if __name__ == '__main__':
    main()
