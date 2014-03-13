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
from server import WebSocketHandler

def main():
    run = True
    print()
    print()
    print("*** Starting Websocket Server ***")
    print()
    print("Press Any Key To Quit...")
    print()
    server = WebSocketHttpServer(WebSocketHandler, http_address=('',8000))
    if server.start():
        print()
        server.launch_webpage()
    else:
        print("Error Starting Server")
    while run:
        i = input("Enter Command:")
        if i == "q":
            server.stop()
            run = False
        else:
            if i:
                server.send(i)
    print("Good Bye")

if __name__ == '__main__':
    main()
