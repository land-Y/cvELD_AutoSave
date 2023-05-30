bl_info = {
    "name": "cvELD_AutoSave",
    "author": "cvELD",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "Preferences",
    "description": "Autosave will not work unless saved as .blend",
    "warning": "",
    "doc_url": "https://cveld.net/?p=9219",
    "tracker_url": "https://twitter.com/cvELD_info",
    "category": "System",
}

import bpy
from .translation import translation

class AutoSavePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    timer : bpy.props.IntProperty(
        name="Auto Save Timer (in minutes)",
        default=5,  # default to 5 minutes
        min=1,
        description="Interval for autosaving the current file",
        update=lambda self, context: timer_reset()
    )

    def draw(self, context):
        self.layout.prop(self, "timer")

_handle = None

def auto_save():
    filepath = bpy.data.filepath
    if filepath:
        bpy.ops.wm.save_mainfile()
        print("Auto saved file: ", filepath)
    else:
        print("Autosave will not work unless saved as .blend.")

def timer_reset():
    global _handle
    if _handle:
        bpy.app.timers.remove(_handle)
        _handle = None
    prefs = bpy.context.preferences.addons[__name__].preferences
    _handle = bpy.app.timers.register(auto_save, first_interval=prefs.timer * 60)  # convert minutes to seconds

def register():
    bpy.utils.register_class(AutoSavePreferences)
    translation.register()
    timer_reset()

def unregister():
    global _handle
    if _handle:
        bpy.app.timers.remove(_handle)
        _handle = None
    bpy.utils.unregister_class(AutoSavePreferences)
    translation.unregister()

if __name__ == "__main__":
    register()
