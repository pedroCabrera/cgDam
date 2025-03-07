# -*- coding: utf-8 -*-
"""
Documentation: 
"""

# ---------------------------------
# Import Libraries
import os
import sys
import site
from pathlib import Path

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

#site.addsitedir(CgDamROOT.joinpath('venv', 'python39', 'Lib', 'site-packages').as_posix())
site.addsitedir(CgDamROOT.joinpath('../.conda/Lib/site-packages').as_posix())

import pyblish.api
import pyblish.util

from dcc.maya.api.cmds import Maya, maya_main_window
from utils.assets_db import AssetsDB
from utils.dialogs import message

import maya.cmds as cmds

# ---------------------------------
# Variables
db = AssetsDB()


# ---------------------------------
# Start Here
class CreateAsset(pyblish.api.ContextPlugin):
    label = "Get current asset info"
    order = pyblish.api.CollectorOrder
    hosts = ["maya"]
    families = ["asset"]

    def process(self, context):
        ma = Maya()
        selection = ma.selection()

        if len(selection) != 1:
            message(maya_main_window(), "Warring", "You should select the asset main group only.")
            raise
        if '.' in selection[0]:
            message(maya_main_window(), "Warring", "You should select the asset main group only.")
            raise
        asset_name = selection[0]

        # export mesh
        cmds.select(selection, r=1)
        geo_paths = ma.export_selection(asset_dir=None, asset_name=asset_name, export_type=["obj", "abc", "usd"],
                                        _message=False)
        geo_paths = db.get_geometry(asset_name=asset_name, obj_file="", usd_geo_file="", abc_file="", fbx_file="",
                                    source_file="")
        cmds.select(selection, r=1)

        instance = context.create_instance(
            name=asset_name,
            family="asset",
            file_color_space=ma.get_file_colorspace(),
            renderer=ma.get_renderer(),
            host="maya",
            geo_paths=geo_paths,
            asset_data=ma.get_asset_data(asset_name)
        )


# Main Function
def main():
    pyblish.api.register_host("maya")
    pyblish.api.register_plugin(CreateAsset)

    instance = pyblish.util.collect()[0]

    # pyblish.util.publish()


if __name__ == '__main__':
    main()
