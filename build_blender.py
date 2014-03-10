import bpy
import math

bpy.ops.object.add(type='EMPTY')
bpy.context.active_object.name = "Controller"
bpy.data.objects["Controller"].location = (0.0, 0.0, 0.0)

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