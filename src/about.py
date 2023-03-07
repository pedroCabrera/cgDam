# -*- coding: utf-8 -*-
"""
Documentation:
"""
import sys
import os
from pathlib import Path

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT.as_posix(), CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)


from PySide2.QtWidgets import QMessageBox
from PySide2.QtGui import QPixmap, QIcon

from utils.resources.style_rc import *
from src.version import version

def message(parent=None):
    about = QMessageBox(parent)
    about.setWindowTitle("cgDam Tools")
    about.setWindowIcon(QIcon(":/icons/about.png"))
    about.setInformativeText(f'''
    <blockquote skip="true">
        <h2><strong>cgDam</strong></h2>
    </blockquote>
    <p>Open-source assets manager with workflow tools.</p>
    <p><a href="https://github.com/pedroCabrera/cgDam">https://github.com/pedroCabrera/cgDam</a></p>
    <pstyle="margin-left: 40px;">Version: {version}</p>
    <pre>2022 cgDam, All rights reserved</pre>
    <p><br></p>
        ''')
    pixmap = QPixmap(":/icons/djed.ico")
    pixmap.scaled(20, 20)

    about.setIconPixmap(pixmap)
    about.show()
    about.exec_()


if __name__ == '__main__': 
    message()
    print(__name__)
