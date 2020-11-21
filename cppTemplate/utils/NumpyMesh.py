import bpy
import numpy as np

class NumpyMesh:
    """Context manager for transfering mesh data between Blender and Numpy.
    Assumes the input mesh is triangulated.
    
    Attributes:
        mesh: reference to Blender mesh object
        V: [#Vx3] numpy float64 array of vertex positions
        F: [#Fx3] number int32 array of vertex indices

    """

    def __init__(self, obj=None):
        """Initialize a new NumpyMesh handler from the given Blender
        object or the active object.

        Args:
            obj: [optional] the Blender mesh object
        """
        if obj is None:
            obj = bpy.context.active_object
        if type(obj) is bpy.types.Mesh:
            self.mesh = obj
        elif type(obj) is bpy.types.Object and obj.type == "MESH":
            self.mesh = obj.data
        else:
            raise ValueError("Not a mesh")

        self._initial_mode = bpy.context.object.mode
    
    def __enter__(self):
        # Changes made in edit mode will be overwritten so switch to object mode first
        bpy.ops.object.mode_set(mode='OBJECT')
        
        V = np.empty(len(self.mesh.vertices) * 3, dtype=np.float64)
        self.mesh.vertices.foreach_get("co", V)
        V.shape = (len(self.mesh.vertices), 3)
        self.V = V  # corresponds to Eigen::MatrixXd
        
        F = np.empty(len(self.mesh.polygons) * 3, dtype=np.int64)
        self.mesh.polygons.foreach_get("vertices", F)
        F.shape = (len(self.mesh.polygons), 3)
        self.F = F.astype(np.int32)  # corresponds to Eigen::MatrixXi

        return self
        
    def __exit__(self, *args):
        self.mesh.vertices.foreach_set('co', self.V.astype(np.float64).flatten())
        self.mesh.polygons.foreach_set('vertices', self.F.astype(np.int64).flatten())
        
        # Entering edit mode triggers Blender to update mesh data
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode=self._initial_mode)
