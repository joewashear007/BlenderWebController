import server
import bge
import json
from time import sleep
class BlenderHandler(server.WebSocketHandler):
 def on_message(self,msg):
  cont=bge.logic.getCurrentController();msg_info=msg
  if 'Actuator' in msg_info:
   direction=msg_info['Actuator'];print('Moving:',direction)
   if 'Speed' in msg_info:
    speed=msg_info['Speed'];print('Speed: ',speed);rot=cont.actuators[direction].dRot;loc=cont.actuators[direction].dLoc;print(sum(rot))
    if sum(rot)!=0:rot=[x/abs(sum(rot)) for x in rot]
    print(sum(loc))
    if sum(loc)!=0:loc=[x/abs(sum(loc)) for x in loc]
    cont.actuators[direction].dLoc=[x*speed for x in loc];cont.actuators[direction].dRot=[x*speed for x in rot]
   cont.activate(cont.actuators[direction])
  if 'Stop' in msg_info:
   for act in cont.actuators:cont.deactivate(act)
  if 'Reset' in msg_info:
   try:cont.owner.worldOrientation=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]];scene=bge.logic.getCurrentScene();scene.objects['ControllerView'].localPosition=0.,-2.5,0.
   except e:print('Error: '+e)
 def send_message(self,msg):pass
 def on_close(self):cont=bge.logic.getCurrentController();cont.activate(cont.actuators['QuitMsg'])
