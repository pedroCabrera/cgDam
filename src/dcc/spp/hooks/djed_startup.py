# -*- coding: utf-8 -*-
"""
Documentation:
"""

# ---------------------------------
# Import Libraries
import sys
import os
import importlib

import substance_painter_plugins

# ---------------------------------
# Variables
PLUGIN = None


# ---------------------------------PLUGIN
# Start Here
def start_plugin():
    CgDamROOT = os.getenv("CgDamROOT")
    spp_path = os.path.join(CgDamROOT, "src", "dcc", "spp")

    plugin_path = os.path.join(spp_path, "hooks", "plugins")

    sysPaths = [spp_path, plugin_path]
    for sysPath in sysPaths:
        if sysPath not in sys.path:
            sys.path.append(sysPath)
            substance_painter_plugins.path.append(sysPath)

    global PLUGIN
    PLUGIN = importlib.import_module("cgDam")

    # Start the Plugin if it wasn't already:
    if not substance_painter_plugins.is_plugin_started(PLUGIN):
        substance_painter_plugins.start_plugin(PLUGIN)

    substance_painter_plugins.update_sys_path()


def close_plugin():
    global PLUGIN
    substance_painter_plugins.close_all_plugins()
    del PLUGIN


# Main Function
def main():
    pass


if __name__ == '__main__':
    main()
