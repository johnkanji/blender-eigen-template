import math

import bpy
import mathutils
import numpy as np

from . import utils


class ExampleOperator(bpy.types.Operator):
    """Example Blender Operator using numpyeigen C++ wrapper"""
    bl_idname = "cpp_template.example"
    bl_label = "Rotate and Scale"
    bl_options = {'UNDO'}

    def execute(self, context):
        # During development shared libraries can be hot-reloaded by wrapping in SharedLib
        libtemplate = utils.SharedLib('libtemplate')

        if context.active_object is None or context.active_object.type != 'MESH':
            return {'CANCELLED'}

        settings = context.scene.cpp_template_settings

        angle = settings.angle * (180/math.pi)
        axis = settings.axis
        R = mathutils.Matrix.Rotation(angle, 4, axis).to_3x3()
        M = np.array(R)

        # NumpyMesh(bobj) handles transfering mesh data to/from blender datastructures.
        with utils.NumpyMesh() as mesh:
            V = mesh.V
            F = mesh.F

            V = libtemplate.igl_example(V, F, M)
            mesh.V = V

        return {'FINISHED'}
