# Blender-Eigen Addon Template

An template for building Blender addons with C++ and Eigen based on [numpyeigen](https://github.com/fwilliams/numpyeigen). 

This template implements a simple Blender addon including a
C++ shared library, a Blender operator and a UI panel.
Additionally, a small utility addon is included to reload addons
during development.

## Overview
This template is based on the numpyeigen [example project](https://github.com/fwilliams/NumpyEigen-Example-Project), with example code
from the [libigl tutorial](https://libigl.github.io/#tutorial).
C++ sources are stored in the `src` dir while python sources go in
the `cppTemplate` dir. For a full introduction to Blender addons refer to
the official [Addon Tutorial](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html) and the [Blender Python API](https://docs.blender.org/api/current/info_quickstart.html) documentation.

## Building
You can build the project using CMake. From the project root run
```
mkdir build
cd build
cmake ..
make
```
This will generate the C++ shared library `build/libtemplate.*.so` 
which can be imported from Python as `import libtemplate`.
Additional C++ dependencies can simply be added to the `CMakeLists.txt` file.
Python dependencies can be installed using
```
/path/to/blender/python -m pip install myDependency
```
To find the location of Blender's python binary run `bpy.app.binary_path_python`
in the Blender python console.

## Installation
### Reloader Addon
It is recommended to use the provided Reloader addon to install and 
reload development addons. The Reloader addon can be installed by executing `reload_addons.py` file under Blender's python interpreter.
```
blender -b -P reload_addons.py
```
This addon provides two commands, "Reload All Addons" and 
"Reload Enabled Addons" which can be accessed from the Blender
menu in the topbar under System, or through the tool search bar.
This will search the user addons directory (default `~/src/Blender`,
configurable in Preferences -> Addons -> Reload Addons) for addon sources,
install them and reload them in Blender's interpreter.

The Reloader will call the shell script `package_addon.sh` before reloading.
This can be used to perform whatever build actions you may need.
By default it will recompile the C++ source and copy the library into the
`cppTemplate` directory.

### Manual Installation
You can also choose to install the addon manually. To do this copy the comiled
library from `build` to `cppTemplate`, then zip the cppTemplate directory and 
install it using in Blender under Preferences -> Addons -> Install.

## Utilities
In addition to the addon skeleton, the template includes a couple
of useful development utilities in the `cppTemplate/utils` directory.

### NumpyMesh
`NumpyMesh` is a context manager which handler transfering mesh
data between Numpy and Blender. Wrap your geometry code in
in a NumpyMesh context and it'll handle extracting the vertices
and faces into numpy `ndarray`s and putting them back into the
Blender mesh object when you're done
```
myMesh = bpy.data.meshes['Suzanne']
with NumpyMesh(myMesh) as mesh:
    V = mesh.V
    F = mesh.F
    
    (newV, newF) = libtemplate.my_cool_geometry_function(V, F)
    
    mesh.V = V
    mesh.F = F
```

### SharedLib
During development it's helpful to be able to recompile and reload
your addon without restarting Blender. Unfortunately, Python does not
support "hot-reloading" external C++ modules. However, this can be circumvented
using the `SharedLib` wrapper. Use this wrapper instead of the normal module import
to executes each function call in a separate process which imports a fresh version
of the library.
```
class MyOperator(bpy.types.Operator):
    def execute(self, context):
        libtemplate = SharedLib('libtemplate')
        I = libtemplate.eye(3)
```
Note that if the library is imported normally this will override the wrapper's
version and the module will not be updated. You will need to restart Blender to
allow the new version to be imported.
