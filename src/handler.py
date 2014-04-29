
import server
import bge
import json

class BlenderHandler(server.WebSocketHandler):
    def on_message(self, msg):
        cont = bge.logic.getCurrentController()
        msg_info = msg
        if "Actuator" in msg_info:
            print("Acting: ", msg_info["Actuator"])
            action = msg_info["Actuator"]
            if "Speed" in msg_info:
                speed = msg_info["Speed"]
                print("   - Speed: ", speed)
                #get the curretn speed
                rot = cont.actuators[action].dRot
                loc = cont.actuators[action].dLoc
                #Normalize the speed back to 1
                #print(sum(rot))
                if sum(rot) != 0:
                    rot = [x/abs(sum(rot)) for x in rot]
                #print(sum(loc))
                if sum(loc) != 0:
                    loc = [x/abs(sum(loc)) for x in loc]
                #set teh new speed
                cont.actuators[action].dLoc = [x*speed for x in loc]
                cont.actuators[action].dRot = [x*speed for x in rot]
            cont.activate(cont.actuators[action])
        if "Stop" in msg_info:
            for act in cont.actuators:
                cont.deactivate(act)
        if "Reset" in msg_info:
            print("Resetting the scene!")
            try:
                print("Ornt: ", bge.logic.globalDict['Ctrl-Ornt'])
                print("Pos: ", bge.logic.globalDict["CtrlView-Pos"])
                cont.owner.worldOrientation = bge.logic.globalDict['Ctrl-Ornt']
                scene = bge.logic.getCurrentScene()
                scene.objects["ControllerView"].localPosition = bge.logic.globalDict["CtrlView-Pos"]
            except e:
                print("Error: "+ e)
        
    def send_message(self, msg):
        pass
    