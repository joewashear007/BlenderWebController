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
from Handler import BlenderHandler
import threading


def run_server():
    if "Running" in bge.logic.globalDict:
        return
    if "Server" in bge.logic.globalDict:  
        if not bge.logic.globalDict["Server"].status():
            print()
            print()
            print("*** Starting Websocket Server ***")
            print()
            print("Press Any Key To Quit...")
            print()
            if bge.logic.globalDict["Server"].start():
                print()
                bge.logic.globalDict["Server"].launch_webpage()
                bge.logic.globalDict["Running"] = True
            else:
                print("Error Starting Server")
    else:
        print("Server Not Defined!")

def main():
    cont = bge.logic.getCurrentController()
    scene = bge.logic.getCurrentScene()
    scene.active_camera = scene.objects['ControllerView']
    bge.logic.globalDict["Server"] = WebSocketHttpServer(BlenderHandler, http_address=('',8000))
    run_server()

if __name__ == '__main__':
	main()
