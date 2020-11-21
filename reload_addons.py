import bpy
import os
import subprocess
import sys
from pathlib import Path

bl_info = {
    "name": "Reload Addons",
    "author": "John Kanji",
    "version": (1, 0, 0),
    "blender": (2, 90, 1),
    "location": "SpaceBar Search -> Reload All Addons",
    "category": "Development",
}


def reload_addons(only_enabled=True):
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__name__].preferences
    user_addons_path = addon_prefs.source_dir

    blender_addons_path = Path(bpy.utils.script_path_user())/'addons'

    enabled_addons = [a.module for a in bpy.context.preferences.addons]
    addons = next(os.walk(user_addons_path))[1]
    addons = [a for a in addons if a[0] != '_']

    if only_enabled:
        addons = [a for a in addons if a in enabled_addons]

    cwd = os.getcwd()
    for a in addons:
        print(f'reloading {a}')
        adir = os.path.join(user_addons_path, a)
        os.chdir(adir)
        if 'package_addon.sh' in os.listdir(adir):
            subprocess.run([os.path.join(adir, 'package_addon.sh')])
        subprocess.run(['rsync', '-avh', os.path.join(adir, a), blender_addons_path])

        if a in enabled_addons:
            bpy.ops.preferences.addon_disable(module=a)
        mods = []
        for mod_name, mod in sys.modules.items():
            if a in mod_name:
                mods.append(mod_name)
        for mod in mods:
            del sys.modules[mod]
        bpy.ops.preferences.addon_enable(module=a)
    os.chdir(cwd)


class ReloadEnabledAddons(bpy.types.Operator):
    """Reload Addons"""
    bl_idname = "reload_addons.enabled"
    bl_label = "Reload Enabled Addons"

    def execute(self, context):
        reload_addons()
        return {'FINISHED'}


class LoadAddons(bpy.types.Operator):
    """Reload Addons"""
    bl_idname = "reload_addons.load"
    bl_label = "Reload All Addons"

    def execute(self, context):
        reload_addons(only_enabled=False)
        return {'FINISHED'}


class ReloadAddonsPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    source_dir: bpy.props.StringProperty(
        name="Source Dir",
        subtype="FILE_PATH",
        default=str(Path.home()/'src'/'Blender')
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Choose the directory to be scanned for addons.")
        layout.prop(self, "source_dir")


def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(ReloadEnabledAddons.bl_idname, text=ReloadEnabledAddons.bl_label)
    layout.operator(LoadAddons.bl_idname, text=LoadAddons.bl_label)

def register():
    bpy.utils.register_class(ReloadEnabledAddons)
    bpy.utils.register_class(LoadAddons)
    bpy.utils.register_class(ReloadAddonsPrefs)
    bpy.types.TOPBAR_MT_app_system.append(draw_menu)


def unregister():
    bpy.utils.unregister_class(ReloadEnabledAddons)
    bpy.utils.unregister_class(LoadAddons)
    bpy.utils.unregister_class(ReloadAddonsPrefs)
    bpy.types.TOPBAR_MT_app_system.remove(draw_menu)


if __name__ == "__main__":
    import shutil

    script_path = Path(__file__)
    addons_path = Path(bpy.utils.script_path_user()) / 'addons'
    addons_path.mkdir(exist_ok=True)
    shutil.copy2(script_path, addons_path)
    print(f'Installed reload_addons script into {addons_path}')
