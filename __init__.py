bl_info = {
    "name": "cvELD_AutoSave",
    "author": "cvELD",
    "version": (1, 1),
    "blender": (3, 3, 0),
    "location": "Preferences",
    "description": "Activate the icon in the upper left corner of the viewport to enter auto save mode.",
    "warning": "",
    "doc_url": "https://cveld.net/?p=9219",
    "tracker_url": "https://twitter.com/cvELD_info",
    "category": "System",
}

import bpy
import datetime
from bpy.app.handlers import persistent
from .translation import translation

class AutoSavePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    auto_saving: bpy.props.BoolProperty(
        name="Enable auto save and reload timer settingstime setting.",
        default=False,
        description="Whether auto saving is currently enabled",
        update=lambda self, context: cvtimer_reset(self, context, self.auto_saving)
    )

    autosave_on_start: bpy.props.BoolProperty(
        name="Enable Autosave on Start",
        description="If enabled, Autosave will be turned on when Blender starts",
        default=False,
    )

    cvtimer: bpy.props.IntProperty(
        name="Auto Save Timer (in minutes)",
        default=5,
        min=1,
        description="Interval for autosaving the current file",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "cvtimer")
        layout.prop(self, "auto_saving")
        layout.prop(self, "autosave_on_start")

_handle = None

def auto_save():
    filepath = bpy.data.filepath

    if not filepath:
        print("The scene is not saved yet. Autosave will be stored in the cache folder.")
        now = datetime.datetime.now()  # Get current date and time
        filename = now.strftime('%Y%m%d%H%M%S') + '.blend'  # Format filename with date and time
        filepath = bpy.app.tempdir + filename  # Set filepath to Blender's temp directory
        bpy.ops.wm.save_as_mainfile(filepath=filepath)  # Save the file
    else:
        bpy.ops.wm.save_mainfile()

    print(f"Auto saving at {datetime.datetime.now()}", filepath)

    for img in bpy.data.images:
        if img.source == 'FILE':
            img.reload()

    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs.auto_saving:
        cvtimer_reset(prefs, bpy.context, True)  # Reset the timer if auto-saving is still enabled

def cvtimer_reset(self, context, auto_saving):
    global _handle
    if _handle:
        bpy.app.timers.remove(_handle)
        _handle = None
    if auto_saving:
        prefs = bpy.context.preferences.addons[__name__].preferences
        _handle = bpy.app.timers.register(auto_save, first_interval=prefs.cvtimer * 60)

@persistent
def turn_off_auto_saving(dummy):
    prefs = bpy.context.preferences.addons[__name__].preferences
    prefs.auto_saving = False

@persistent
def check_autosave_on_start(dummy):
    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs.autosave_on_start:
        prefs.auto_saving = True

def draw_func(self, context):
    prefs = bpy.context.preferences.addons[__name__].preferences
    layout = self.layout
    layout.prop(prefs, "auto_saving", text="", icon='FILE_TICK')

def register():
    bpy.utils.register_class(AutoSavePreferences)
    bpy.types.VIEW3D_HT_header.prepend(draw_func)
    bpy.app.handlers.load_post.append(turn_off_auto_saving)
    bpy.app.handlers.load_post.append(check_autosave_on_start)
    turn_off_auto_saving(None)  # Call this once to ensure auto_saving is False at startup
    translation.register()

def unregister():
    global _handle
    if _handle:
        bpy.app.timers.remove(_handle)
        _handle = None
    bpy.utils.unregister_class(AutoSavePreferences)
    bpy.types.VIEW3D_HT_header.remove(draw_func)
    bpy.app.handlers.load_post.remove(turn_off_auto_saving)
    translation.unregister()
