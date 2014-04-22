# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



bl_info = {
    "name": "Blender Web Controller",
    "category": "Game Engine",
}

import bpy
import math

class BlenderWebController_pl(bpy.types.Panel):
    bl_idname = "game.panel.webcontroller"
    bl_label = "Web Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()
        row.operator('game.webcontroller')



class BlenderWebController_op(bpy.types.Operator):
    """Launches a website to control a new BGE camera"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "game.webcontroller"        # unique identifier for buttons and menu items to reference.
    bl_label = "Setup Web Controller"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO' }
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    #when to show this add on
    @classmethod
    def poll(self, context):
        return True
    
    
    def execute(self, context):
        bpy.context.scene.render.engine = 'BLENDER_GAME'
        bpy.context.scene.game_settings.show_debug_properties = True
        #-------------- Create Text Files --------------------------   
        bpy.ops.text.new()
        bpy.data.texts[-1].name = 'StartServer'
        bpy.data.texts['StartServer'].from_string($_STARTSERVERS_PY)
        bpy.ops.text.new()
        bpy.data.texts[-1].name = "EndServer"
        bpy.data.texts["EndServer"].from_string($_ENDSERVERS_PY)
        bpy.ops.text.new()
        bpy.data.texts[-1].name = "handler.py"
        bpy.data.texts["handler.py"].use_module = True
        bpy.data.texts["handler.py"].from_string($_HANDLER_PY)
        bpy.ops.text.new()
        bpy.data.texts[-1].name = "server.py"
        bpy.data.texts["server.py"].use_module = True
        bpy.data.texts["server.py"].from_string($_SERVER_PY)
		bpy.ops.text.new()
        bpy.data.texts[-1].name = "customButtons.py"
        bpy.data.texts["customButtons.py"].use_module = True
        bpy.data.texts["customButtons.py"].from_string($_CUSTOMBUTTONS_PY)
        
        #-------------- Add empty Controller ------------------------
        bpy.ops.object.add(type='EMPTY')
        bpy.context.active_object.name = "Controller"
        bpy.ops.object.game_property_new(type="INT", name="Website Port")
        bpy.ops.object.game_property_new(type="INT", name="Socket Port")
        bpy.ops.object.game_property_new(type="STRING", name="Website Address")
        bpy.ops.object.game_property_new(type="STRING", name="Socket Address")
        bpy.data.objects["Controller"].location = (0.0, 0.0, 0.0)
        bpy.data.objects['Controller'].game.properties['Website Port'].value = 8000
        bpy.data.objects['Controller'].game.properties['Socket Port'].value = 0
        bpy.data.objects['Controller'].game.properties['Website Address'].show_debug = True
        bpy.data.objects['Controller'].game.properties['Socket Address'].show_debug = True
        
        bpy.ops.logic.sensor_add(       type="DELAY",       name="StartServer")
        bpy.ops.logic.sensor_add(       type="KEYBOARD",    name="QuitKey")
        bpy.ops.logic.sensor_add(       type="MESSAGE",     name="QuitMsg")
        bpy.ops.logic.controller_add(   type="PYTHON",      name="Sever")
        bpy.ops.logic.controller_add(   type="PYTHON",      name="QuitSever")
        bpy.ops.logic.actuator_add(     type="MOTION",      name="RotateRight")
        bpy.ops.logic.actuator_add(     type="MOTION",      name="RotateLeft")
        bpy.ops.logic.actuator_add(     type="MOTION",      name="RotateUp")
        bpy.ops.logic.actuator_add(     type="MOTION",      name="RotateDown")
        bpy.ops.logic.actuator_add(     type="MOTION",      name="ZRotateLeft")
        bpy.ops.logic.actuator_add(     type="MOTION",      name="ZRotateRight")
        bpy.ops.logic.actuator_add(     type="MESSAGE",     name="SendQuit")
        bpy.ops.logic.actuator_add(     type="GAME",        name="QuitGame")

        #------------- Add Camera ----------------
        bpy.ops.object.add(type='CAMERA')
        bpy.context.active_object.name = "ControllerView"
        bpy.data.objects["ControllerView"].location = (0.0, -5.0, 0.0)
        bpy.data.objects["ControllerView"].rotation_euler = (math.radians(90),0.0,0.0)
        bpy.data.objects["ControllerView"].parent = bpy.data.objects["Controller"]
        bpy.ops.logic.actuator_add(type="MOTION", name="ZoomOut")
        bpy.ops.logic.actuator_add(type="MOTION", name="ZoomIn")
        con = bpy.data.objects["ControllerView"].constraints.new('DAMPED_TRACK')
        con.name = "ViewLock"
        con.target = bpy.data.objects["Controller"]
        con.track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.scene.camera = bpy.data.objects["ControllerView"]

        #------------------ Add Logic Block Info -----------------------
        bpy.data.objects["Controller"].game.sensors["StartServer"].use_repeat           = True
        bpy.data.objects["Controller"].game.sensors["QuitKey"].key                      = "Q"
        bpy.data.objects["Controller"].game.sensors['QuitMsg'].subject                  = "QUIT"
        bpy.data.objects['Controller'].game.controllers['Sever'].use_priority           = True
        bpy.data.objects['Controller'].game.controllers['Sever'].text                   = bpy.data.texts['StartServer']
        bpy.data.objects['Controller'].game.controllers['QuitSever'].text               = bpy.data.texts['EndServer']
        bpy.data.objects['Controller'].game.actuators['QuitGame'].mode                  = "QUIT"
        bpy.data.objects["Controller"].game.actuators["RotateRight"].offset_rotation    = (0.0,     0.0,   math.radians(-1))
        bpy.data.objects["Controller"].game.actuators["RotateLeft"].offset_rotation     = (0.0,     0.0,    math.radians(1))
        bpy.data.objects["Controller"].game.actuators["RotateUp"].offset_rotation       = (math.radians(1),     0.0,    0.0)
        bpy.data.objects["Controller"].game.actuators["RotateDown"].offset_rotation     = (math.radians(-1),    0.0,    0.0)
        bpy.data.objects["Controller"].game.actuators["ZRotateLeft"].offset_rotation    = (0.0,     math.radians(1),    0.0)
        bpy.data.objects["Controller"].game.actuators["ZRotateRight"].offset_rotation   = (0.0,     math.radians(-1),   0.0)
        bpy.data.objects["ControllerView"].game.actuators["ZoomIn"].offset_location     = (0.0,     0.0,                0.01)
        bpy.data.objects["ControllerView"].game.actuators["ZoomOut"].offset_location    = (0.0,     0.0,                -0.01)
        bpy.data.objects['Controller'].game.actuators['SendQuit'].to_property = bpy.data.objects['Controller'].name

        c = bpy.data.objects['Controller'].game.controllers['Sever']
        d = bpy.data.objects['Controller'].game.controllers['QuitSever']
        bpy.data.objects['Controller'].game.sensors['StartServer'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateRight'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateLeft'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateUp'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateDown'].link(c)
        bpy.data.objects['Controller'].game.actuators['ZRotateLeft'].link(c)
        bpy.data.objects['Controller'].game.actuators['ZRotateRight'].link(c)
        bpy.data.objects['Controller'].game.actuators['SendQuit'].link(c)
        bpy.data.objects["ControllerView"].game.actuators["ZoomIn"].link(c)
        bpy.data.objects["ControllerView"].game.actuators["ZoomOut"].link(c)
        
        bpy.data.objects['Controller'].game.sensors['QuitKey'].link(d)
        bpy.data.objects['Controller'].game.sensors['QuitMsg'].link(d)
        bpy.data.objects['Controller'].game.actuators['QuitGame'].link(d)

        #Show collaspsed
        for s in bpy.data.objects["ControllerView"].game.sensors:
            s.show_expanded = False
        for s in bpy.data.objects["ControllerView"].game.actuators:
            s.show_expanded = False
        for s in bpy.data.objects["Controller"].game.sensors:
            s.show_expanded = False
        for s in bpy.data.objects["Controller"].game.actuators:
            s.show_expanded = False
        
        
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects['Controller'].select = True
        return {'FINISHED'}  

def register():
    bpy.utils.register_class(BlenderWebController_op)
    bpy.utils.register_class(BlenderWebController_pl)


def unregister():
    bpy.utils.unregister_class(BlenderWebController_op)
    bpy.utils.unregister_class(BlenderWebController_pl)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
