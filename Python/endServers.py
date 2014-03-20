import bge
if "Server" in bge.logic.globalDict:  
        bge.logic.globalDict["Server"].stop()
        cont = bge.logic.getCurrentController()
        cont.activate(cont.actuators["QuitGame"])