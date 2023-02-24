# -*- coding: utf-8 -*-
"""
Documentation:
"""

# ---------------------------------
# Import Libraries
import os
import sys
from cx_Freeze import setup, Executable
from pathlib import Path

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT.as_posix(), CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from version import version

# ---------------------------------
# Variables

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("start.py", base=base, targetName="cgDam",
               icon=f"{CgDamROOT.as_posix()}/src/utils/resources/icons/djed.ico")
]

include_files = [
]

build_options = {
    "include_files": include_files,
    "packages": []
}

# ---------------------------------
# Start Here


setup(
    name="cgDam",
    version=version,
    description="cgDam tools for 3d asset management",
    options={"build_exe": build_options},
    executables=executables
)
