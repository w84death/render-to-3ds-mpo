bl_info = {
    "name": "Render to 3DS MPO",
    "author": "Krzysztof Krystian Jankowski",
    "version": (0, 4),
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
        context.scene.render.filepath = output_path + 'left_eye.jpg'
        bpy.ops.render.render(write_still=True)

        # Render right eye
        self.report({'INFO'}, "Rendering right eye.")
        context.scene.camera = bpy.data.objects['Camera_Right']
        context.scene.render.filepath = output_path + 'right_eye.jpg'
        bpy.ops.render.render(write_still=True)

        # TODO: Combine left and right images into an MPO file

        self.report({'INFO'}, "Render complete. Please combine the images into an MPO file manually.")
        return {'FINISHED'}

class RenderMPORenderPanel(bpy.types.Panel):
    bl_label = "Render MPO"
    bl_idname = "RENDER_PT_mpo"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        layout = self.layout

        # Add the operator button
        layout.operator("render.render_mpo")

def register():
    bpy.utils.register_class(RenderMPOOperator)
    bpy.utils.register_class(RenderMPORenderPanel)

def unregister():
    bpy.utils.unregister_class(RenderMPOOperator)
    bpy.utils.unregister_class(RenderMPORenderPanel)

if __name__ == "__main__":
    register()
