bl_info = {
    "name": "Render to 3DS MPO",
    "author": "Krzysztof Krystian Jankowski",
    "version": (0, 18),
    "blender": (2, 80, 0),
    "location": "Render Properties",
    "description": "Renders left and right eye images for Nintendo 3DS",
    "warning": "",
    "wiki_url": "https://github.com/w84death/render-to-3ds-mpo",
    "category": "Render",
}

import bpy

class RenderMPOOperator(bpy.types.Operator):
    bl_idname = "render.render_mpo"
    bl_label = "Render MPO for Nintendo 3DS"
    bl_description = "Render left and right eye images and combine them into an MPO file"
    
    def execute(self, context):
        
        output_path = bpy.path.abspath(context.scene.render.filepath)
                
        # Set render settings
        context.scene.render.image_settings.file_format = 'JPEG'
        context.scene.render.resolution_x = 640
        context.scene.render.resolution_y = 480
        bpy.context.scene.frame_set(1)

        # Render left eye
        self.report({'INFO'}, "Rendering left eye.")

        context.scene.camera = bpy.data.objects['Camera_Left']
        context.scene.render.filepath = output_path + '_l.jpg'
        bpy.ops.render.render(write_still=True)

        # Render right eye
        self.report({'INFO'}, "Rendering right eye.")
        context.scene.camera = bpy.data.objects['Camera_Right']
        context.scene.render.filepath = output_path + '_r.jpg'
        bpy.ops.render.render(write_still=True)

        # TODO: Combine left and right images into an MPO file

        self.report({'INFO'}, "Render complete. Please combine the images into an MPO file manually.")
        return {'FINISHED'}


def setup_cameras():
    # Create left camera
    bpy.ops.object.camera_add(location=(-0.0325, 0, 1.7), rotation=(1.5707963267948966,0,0))
    camera_left = bpy.context.object
    camera_left.name = 'Camera_Left'

    # Create right camera
    bpy.ops.object.camera_add(location=(0.0325, 0, 1.7), rotation=(1.5707963267948966,0,0))
    camera_right = bpy.context.object
    camera_right.name = 'Camera_Right'

    # Create Stereoscopic_Rig Empty object
    bpy.ops.object.empty_add(location=(0, 0, 0))
    empty_rig = bpy.context.object
    empty_rig.name = 'Stereoscopic_Rig'

    # Create Focus Empty object
    bpy.ops.object.empty_add(location=(0, 3, 1.7))
    empty_focus = bpy.context.object
    empty_focus.name = 'Focus'

    camera_left.data.dof.use_dof = True
    camera_left.data.dof.focus_object = empty_focus
    camera_left.data.dof.aperture_fstop = 2.8

    camera_right.data.dof.use_dof = True
    camera_right.data.dof.focus_object = empty_focus
    camera_right.data.dof.aperture_fstop = 2.8

    # Parent Focus empty to the Stereoscopic_Rig
    bpy.ops.object.select_all(action='DESELECT')
    empty_focus.select_set(True)
    empty_rig.select_set(True)
    bpy.context.view_layer.objects.active = empty_rig
    bpy.ops.object.parent_set(type='OBJECT')

    # Parent cameras to the Stereoscopic_Rig
    bpy.ops.object.select_all(action='DESELECT')
    camera_left.select_set(True)
    camera_right.select_set(True)
    empty_rig.select_set(True)
    bpy.context.view_layer.objects.active = empty_rig
    bpy.ops.object.parent_set(type='OBJECT')

    # Add Track To constraint to cameras targeting the Focus empty
    for camera in [camera_left, camera_right]:
        constraint = camera.constraints.new('TRACK_TO')
        constraint.target = empty_focus
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'


class StereoscopicCameraOperator(bpy.types.Operator):
    bl_idname = "object.stereoscopic_camera_setup"
    bl_label = "Add Stereoscopic Camera (3Ds)"
    bl_description = "Add two cameras parented to an empty for stereoscopic rendering"

    def execute(self, context):
        setup_cameras()
        self.report({'INFO'}, "Stereoscopic cameras added to the scene.")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(StereoscopicCameraOperator.bl_idname, icon='CAMERA_DATA')

def register():
    bpy.utils.register_class(StereoscopicCameraOperator)
    bpy.utils.register_class(RenderMPOOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(StereoscopicCameraOperator)
    bpy.utils.unregister_class(RenderMPOOperator)
    bpy.types.VIEW3D_MT_add.remove(menu_func)

if __name__ == "__main__":
    register()
