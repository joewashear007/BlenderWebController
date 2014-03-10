import bpy
import math


#-------------- Create Text Files --------------------------
bpy.ops.text.new()
bpy.data.texts[-1].name = "StartServer"


#-------------- Add empty Controller ------------------------
bpy.ops.object.add(type='EMPTY')
bpy.context.active_object.name = "Controller"
bpy.data.objects["Controller"].location = (0.0, 0.0, 0.0)

bpy.ops.logic.sensor_add(type="DELAY", name="StartServer")
bpy.ops.logic.controller_add(type="PYTHON", name="Sever")
bpy.ops.logic.actuator_add(type="MOTION", name="RotateRight")
bpy.ops.logic.actuator_add(type="MOTION", name="RotateLeft")
bpy.ops.logic.actuator_add(type="MOTION", name="RotateUp")
bpy.ops.logic.actuator_add(type="MOTION", name="RotateDown")

bpy.data.objects["Controller"].game.sensors["StartServer"].use_repeat = True
c = bpy.data.objects['Controller'].game.controllers['Sever']
c.text = bpy.data.texts['StartServer']

bpy.data.objects['Controller'].game.sensors['StartServer'].link(c)
bpy.data.objects['Controller'].game.actuators['RotateRight'].link(c)
bpy.data.objects['Controller'].game.actuators['RotateLeft'].link(c)
bpy.data.objects['Controller'].game.actuators['RotateUp'].link(c)
bpy.data.objects['Controller'].game.actuators['RotateDown'].link(c)


#------------- Add Camera ----------------
bpy.ops.object.add(type='CAMERA')
bpy.context.active_object.name = "ControllerView"
bpy.data.objects["ControllerView"].location = (0.0, -5.0, 0.0)
bpy.data.objects["ControllerView"].rotation_euler = (math.radians(90),0.0,0.0)
bpy.data.objects["ControllerView"].parent = bpy.data.objects["Controller"]
con = bpy.data.objects["ControllerView"].constraints.new('DAMPED_TRACK')
con.name = "ViewLock"
con.target = bpy.data.objects["Controller"]
con.track_axis = 'TRACK_NEGATIVE_Z'

bpy.context.scene.camera = bpy.data.objects["ControllerView"]
bpy.context.scene.render.engine = 'BLENDER_GAME'

bpy.ops.logic.actuator_add(type="MOTION", name="ZoomOut")
bpy.ops.logic.actuator_add(type="MOTION", name="ZoomIn")
bpy.data.objects["ControllerView"].game.actuators["ZoomIn"].offset_location = (0.0,0.0,0.01)
bpy.data.objects["ControllerView"].game.actuators["ZoomOut"].offset_location = (0.0,0.0,-0.01)