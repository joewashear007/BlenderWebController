import bge
import time
if "Server" in bge.logic.globalDict:  
        bge.logic.globalDict["Server"].stop()
        time.sleep(1)
        cont = bge.logic.getCurrentController()
        cont.activate(cont.actuators["QuitGame"])