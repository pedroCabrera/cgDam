# >>>>>>>>>
# cgDam Tools
# Add self

import maya.cmds as cmds


def open_commandPort():
    if not cmds.commandPort(":4436", query=True):
        cmds.commandPort(name=":4436", sourceType="python")


def init_cgDam():
    import traceback
    import os
    import sys
    import site
    from pathlib import Path

    CgDamROOT = Path(os.getenv('CgDamROOT'))

    print('cgDam: ', CgDamROOT.as_posix())
    try:
        site.addsitedir(CgDamROOT.joinpath('venv/python39/Lib/site-packages').as_posix())
        sys.path.append(CgDamROOT.joinpath('src').as_posix())
        sys.path.append(CgDamROOT.joinpath('src/dcc/maya/hooks').as_posix())

        print('start cgDam')
        from dcc.maya import shelves
        shelves.main()
        open_commandPort()

        from dcc.maya.api.lib import set_project_event
        set_project_event()

    except:
        print(traceback.format_exc())

cmds.evalDeferred("init_cgDam()")
# <<<<<<<<<