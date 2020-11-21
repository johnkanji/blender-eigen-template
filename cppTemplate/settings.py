import bpy

class CppTemplateSettings(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(
        name="Angle", 
        description="Rotation angle in degrees",
        default=90.0,
        min=-180, max=180
    )
    axis: bpy.props.EnumProperty(
        name="Axis",
        description="Axis around which to rotate",
        default="X",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")],
    )