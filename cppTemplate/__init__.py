# flake8: noqa: F821, F722

bl_info = {
    "name": "C++ Addon Template",
    "blender": (2, 90, 1),
    "category": "Development",
}

import os
import sys

mpath = os.path.dirname(os.path.realpath(__file__))
if not any(mpath in v for v in sys.path):
    sys.path.insert(0, mpath)

if 'bpy' in locals():
    import importlib
    importlib.reload(operators)
    importlib.reload(settings)
    importlib.reload(ui)
else:
    import bpy
    from . import (operators, settings, ui)


classes = (
    settings.CppTemplateSettings,
    operators.ExampleOperator,
    ui.CppTemplatePanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cpp_template_settings = bpy.props.PointerProperty(type=settings.CppTemplateSettings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cpp_template_settings
