#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



from server import WebSocketHttpServer
from handler import BlenderHandler
import threading

def main():
    if 'Server' in bge.logic.globalDict:
        return
    else:
        print("\n\n------------------ BUILDING THE SERVER -----------------------")
        scene=bge.logic.getCurrentScene();
        scene.active_camera=scene.objects['ControllerView'];
        cont=bge.logic.getCurrentController()
        
        http_addr='',cont.owner['Website Port']
        ws_addr='',cont.owner['Socket Port']
        bge.logic.globalDict['Server'] = WebSocketHttpServer(BlenderHandler,http_address=http_addr,ws_address=ws_addr)
        if bge.logic.globalDict['Server'].start():
            cont.owner['Website Address'] = bge.logic.globalDict['Server'].httpServer.get_address();
            cont.owner['Socket Address']  = bge.logic.globalDict['Server'].wsServer.get_address();
            bge.logic.globalDict['Server'].launch_webpage();
        else:
            print('Error Starting Server')
           
if __name__=='__main__':
    main()