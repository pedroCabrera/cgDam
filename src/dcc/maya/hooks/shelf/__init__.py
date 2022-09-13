# -*- coding: utf-8 -*-
"""
Documentation: 
"""


# ---------------------------------
# import libraries
import importlib
import sys, os
from collections import OrderedDict
from pathlib import Path

import maya.cmds as cmds
import maya.mel as mel

# ---------------------------------
shelf_name = "Djed"
__python__ = sys.version_info[0]

DJED_ROOT = Path(os.getenv("DJED_ROOT"))
icons = DJED_ROOT.joinpath('src', 'utils', 'resources', 'icons')
modules = DJED_ROOT.joinpath( 'src/dcc/maya/hooks/shelf/btns')

sysPaths = [DJED_ROOT, modules]
for sysPath in sysPaths:
    sysPath = str(sysPath)
    if sysPath not in sys.path:
        sys.path.append(sysPath)

Shelf_Items = [["exportMesh"],
               ["send2spp", "updateSpp"],  # "updateSpp", "updateExitSpp"],
               ["send2clarisse"],
               ["importTexs", "createMtl"],
               ["setting"]
               ]


def delete_self():
    if cmds.shelfLayout(shelf_name, ex=True):
        # mel.eval('deleteShelfTab '+shelf_name)
        cmds.deleteUI(shelf_name)
        gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
        cmds.saveAllShelves(gShelfTopLevel)


def create_self():
    if os.path.isdir(modules):

        # Delete old shelf
        try:
            delete_self()
        except:
            pass

        shelftoplevel = mel.eval("$gShelfTopLevel = $gShelfTopLevel;")
        shelves = cmds.tabLayout(shelftoplevel, query=True, childArray=True)

        # Add new shelf
        if not (shelf_name in shelves):
            mel.eval("addNewShelfTab {};".format(shelf_name))

        try:
            for btn in cmds.shelfLayout(shelf_name, q=1, ca=1):
                cmds.deleteUI(btn)
        except:
            pass

        for shelf_btns in Shelf_Items:
            for _btn in shelf_btns:
                script_file = modules.joinpath(_btn + ".py")
                if not script_file.is_file():
                    continue

                cmd_text = "## Djed Tools ##\n\n"
                cmd_text += "import sys\n"
                cmd_text += f"sys.argv = [r'{script_file}']\n"
                cmd_text += f"with open(r'{script_file}', 'r') as f:\n"
                cmd_text += "\texec(f.read())\n"

                dc_cmd = "## Djed Tools ##\n\n"
                dc_cmd += "import sys\n"
                dc_cmd += f"sys.argv = [r'{script_file}', 'double']\n"
                dc_cmd += f"with open(r'{script_file}', 'r') as f:\n"
                dc_cmd += "\texec(f.read())\n"

                mod = importlib.import_module(_btn)

                btn_info = {
                    "parent": shelf_name,
                    "label": _btn,
                    "annotation": mod._annotation,
                    "image1": icons.joinpath(mod._icon).as_posix(),
                    "imageOverlayLabel": mod._imgLabel,
                    "overlayLabelColor": mod._color,
                    "overlayLabelBackColor": mod._backColor,
                    "command": cmd_text,
                    "doubleClickCommand": dc_cmd
                    # noDefaultPopup=True
                }

                new_shelf_button = cmds.shelfButton(**btn_info)

            cmds.setParent(shelf_name)
            cmds.separator(width=12, height=35, style='shelf', hr=0)
            cmds.setParent(shelf_name)

        cmds.saveAllShelves(shelftoplevel)

        # if popupMenus:
        #     popup_menu = cmds.popupMenu(parent=new_shelf_button, button=n)
        #     for pop in popupMenus:
        #         menu_command = cmds.menuItem(label=pop["label"], sourceType=pop["sourceType"],
        #                                      parent=popup_menu, command=pop["command"])


    else:
        # message
        cmds.confirmDialog(title='Djed Shelf Error',
                           message='Unable to scripts to Djed Shelf.\n Please check shelf path', button=['OK'])


# Main function
def main():
    create_self()


if __name__ == '__main__':
    
    main()
    
