#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



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
