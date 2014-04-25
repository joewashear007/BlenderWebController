#
# This script is used to map the IPO curve of an object as it travels
# through frames of an animation. The algorithm follows:
#
# 1. Calculate number of steps needed to animate at given framerate.
# 2. Get the selected object.
# 3. Duplicate the selected object (which will hold the generated IPO).
# 4. Reset the duplicate object.
# 5. Loop over the number of frames at the calculated framerate.
# 6. Set the active frame.
# 7. Position the duplicate object to the same place as the selected one.
# 8. Copy the selected object's location and rotation into the duplicate's IPO.
#
# Usage:
# (1) Select the object that follows a curve.
# (2) Load this script in Blender's Text window.
# (3) Move the mouse to the Text window.
# (4) Press Alt-p.
#

import bpy 


#framesPerSecond = Scene.GetCurrent().getRenderingContext().fps
framesPerSecond = bpy.context.scene.render.fps
firstFrame      = bpy.data.scenes['Scene'].frame_start
lastFrame       = bpy.data.scenes['Scene'].frame_end
stepsPerFrame   = (lastFrame - firstFrame) // framesPerSecond
#stepsPerFrame   = D.scenes['Scene'].frame_step

selected = bpy.context.scene.objects.active 
bpy.ops.object.duplicate()
duplicate = bpy.context.scene.objects.active 
duplicate.parent = None
bpy.ops.object.constraints_clear()
bpy.ops.anim.keyframe_clear_v3d()

for frame in range( firstFrame, lastFrame, stepsPerFrame ):
  bpy.data.scenes['Scene'].frame_set(frame)
  duplicate.matrix_world = selected.matrix_world
  print(duplicate.matrix_world)
  bpy.ops.anim.keyframe_insert(type="Location")
  bpy.ops.anim.keyframe_insert(type="Rotation")

bpy.data.scenes['Scene'].frame_set(0)
