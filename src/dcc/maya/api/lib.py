# -*- coding: utf-8 -*-
"""
Documentation:
"""
import importlib
import os
import sys

import maya.cmds as cmds

CgDamROOT = os.getenv("CgDamROOT")
scripts_path = os.path.join(CgDamROOT, "src")

sysPaths = [CgDamROOT, scripts_path]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from utils.file_manager import FileManager
from dcc.maya.api.cmds import Maya

fm = FileManager()
ma = Maya()


def on_set_project():
    general = fm.get_user_json('general')
    general['project'] = ma.get_project_dir()
    fm.set_user_json(general=general)


def set_project_event():
    on_set_project()
    cmds.scriptJob(event=["workspaceChanged", on_set_project])


if __name__ == '__main__':
    print(__name__)
