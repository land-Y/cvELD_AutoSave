import os
import csv
import codecs
import bpy

def GetTranslation():
    dict = {}
    path = os.path.join(os.path.dirname(__file__), "translation.csv")
    if os.path.isfile(path):
        with codecs.open(path, "r", "utf-8") as f:
            reader = csv.reader(f)
            dict["ja_JP"] = {}
            for row in reader:
                for context in bpy.app.translations.contexts:
                    dict["ja_JP"][(context, row[1].replace("\\n", "\n"))] = row[0].replace("\\n", "\n")

    return dict

def register():
    translation = GetTranslation()
    if translation:
        bpy.app.translations.register("cvELD_AutoSave", translation)

def unregister():
    try:
        bpy.app.translations.unregister("cvELD_AutoSave")
    except:
        print("Untranslation failed.")