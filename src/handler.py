#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



import server
import bge
import json
from time import sleep

class BlenderHandler(server.WebSocketHandler):
    def on_message(self, msg):
        cont = bge.logic.getCurrentController()
        msg_info = msg
        if "Actuator" in msg_info:
            direction = msg_info["Actuator"]
            print("Moving:", direction)
            if "Speed" in msg_info:
                speed = msg_info["Speed"]
                print("Speed: ", speed)
                #get the curretn speed
                rot = cont.actuators[direction].dRot
                loc = cont.actuators[direction].dLoc
                #Normalize the speed back to 1
                #print(sum(rot))
                if sum(rot) != 0:
                    rot = [x/abs(sum(rot)) for x in rot]
                #print(sum(loc))
                if sum(loc) != 0:
                    loc = [x/abs(sum(loc)) for x in loc]
                #set teh new speed
                cont.actuators[direction].dLoc = [x*speed for x in loc]
                cont.actuators[direction].dRot = [x*speed for x in rot]
            cont.activate(cont.actuators[direction])
#        sleep(cont.owner.get("MoveTime"))
        if "Stop" in msg_info:
            for act in cont.actuators:
                cont.deactivate(act)
        if "Reset" in msg_info:
            try:
                cont.owner.worldOrientation = [[1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
                scene = bge.logic.getCurrentScene()
                scene.objects["ControllerView"].localPosition = (0.0, -2.5, 0.0)
            except e:
                print("Error: "+ e)

    def send_message(self, msg):
        pass
    