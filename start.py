# -*- coding: utf-8 -*-
"""
Documentation:
"""
import os
import sys
from pathlib import Path

from PySide2.QtWidgets import *
from PySide2.QtGui import *

os.environ['CgDamROOT'] = os.path.abspath("./cgDam")

CgDamROOT = Path(os.getenv('CgDamROOT'))
sysPaths = [CgDamROOT.as_posix(), CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from startup.system_tray import cgDamTray
from utils.resources.style_rc import *


def run_tray():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    parent = QWidget()
    tray = cgDamTray(QIcon(":/icons/djed.png"), parent)

    sys.exit(app.exec_())


def main():
    run_tray()


if __name__ == '__main__':
    print("Starting cgDam")
    main()
