import bpy

class CppTemplatePanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_CppTemplate'
    bl_label = 'C++ Addon Template'   # The name that will show up in the properties panel
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        settings = bpy.context.scene.cpp_template_settings

        layout.prop(settings, "angle")
        layout.prop(settings, "axis")
        layout.operator("cpp_template.example")