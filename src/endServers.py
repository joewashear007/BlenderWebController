import bge

cont = bge.logic.getCurrentController()
trueSensors = False
for s in cont.sensors:
    trueSensors = trueSensors or s.positive
    
if "Server" in bge.logic.globalDict and trueSensors:
        bge.logic.globalDict["Server"].stop()
        bge.logic.globalDict["Server"] = None
        cont.activate(cont.actuators["QuitGame"])