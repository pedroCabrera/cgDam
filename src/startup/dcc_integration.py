# -*- coding: utf-8 -*-
"""
Documentation:
"""
import os
import sys
from pathlib import Path

CgDamROOT = Path(os.getenv('CgDamROOT'))
sysPaths = [CgDamROOT.as_posix(), CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from dcc.maya.hooks.start import add_maya_module
from dcc.spp.hooks.start import add_spp_startup
from dcc.clarisse.hooks.start import add_clarisse_shelf


def add_cgDam_integration():
    msg = []
    msg.append(f'<p><span>Maya integration: </span> {add_maya_module()}</p>')
    msg.append(f'<p><span>Substance painter integration: </span> {add_spp_startup()}</p>')
    msg.append(f'<p><span>Clarisse integration: </span> {add_clarisse_shelf()}</p>')

    return '\n'.join(msg)


if __name__ == '__main__':
    print(__name__)
