# -*- coding: utf-8 -*-
"""
Documentation: 
"""


# ---------------------------------
# Import Libraries
import os
import sys
from pathlib import Path

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT, CgDamROOT.joinpath('src')]
for sysPath in sysPaths:
    if str(sysPath) not in sys.path:
        sys.path.append(str(sysPath))

from utils.spp_remote import RemotePainter

# ---------------------------------
# Variables


# ---------------------------------
# Start Here
def connect_spp():
    """
    To connect with the current substance painter session
    :return: substance painter object
    """
    try:
        sp = RemotePainter()
        sp.checkConnection()
        sp.execScript('import substance_painter', 'python')
        sp.execScript('[cgDam]', 'python')
        return sp
    except:
        pass
        # print(traceback.format_exc())
        # message(None, 'Error', 'Can not get the current session of substance painter.')

# Main Function
def main():
    pass


if __name__ == '__main__':
    main()
