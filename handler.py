#! /usr/bin/env python3

# /*
 # * ----------------------------------------------------------------------------
 # * "THE BEER-WARE LICENSE" (Revision 42):
 # * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 # * can do whatever you want with this stuff. If we meet some day, and you think
 # * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 # * ----------------------------------------------------------------------------
 # */

import server
import bge
import json
from time import sleep

class BlenderHandler(server.WebSocketHandler):
    def on_message(self, msg):
        cont = bge.logic.getCurrentController()
        #msg_info = json.loads(msg)
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
                print(sum(rot))
                if sum(rot) != 0:
                    rot = [x/abs(sum(rot)) for x in rot]
                print(sum(loc))
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
    
    def on_close(self):
        cont = bge.logic.getCurrentController()
        cont.activate(cont.actuators["QuitMsg"])