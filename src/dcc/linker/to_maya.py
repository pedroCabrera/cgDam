# -*- coding: utf-8 -*-
"""
Documentation:
"""

import re
import traceback

from settings.settings import get_dcc_cfg
from utils.dialogs import message
from utils.file_manager import FileManager
from utils.open_ports import OpenSocket

fm = FileManager()


def is_maya_connected(port_num=None):
    if not port_num:
        port_num = get_dcc_cfg("maya", 'configuration', "command_port")
    socket = OpenSocket(host='localhost', port=port_num)
    return socket


def send_to_maya(data, port_num=None):
    try:
        if not port_num:
            port_num = get_dcc_cfg("maya", 'configuration', "command_port")
        socket = OpenSocket(host='127.0.0.1', port=int(port_num))

        cmd_text = "## cgDam Tools ##\n\n"
        cmd_text += "print('## cgDam Tools ##')\n"
        cmd_text += "print('[cgDam] Start of receiving from Substance Painter')\n"
        cmd_text += "import sys, os, traceback\n"
        cmd_text += "sys.path.append(os.getenv('CgDamROOT') + '/src')\n"
        cmd_text += "try:\n"
        cmd_text += "\tfrom dcc.maya.plugins.load_asset import LoadAsset\n"
        cmd_text += "\tfrom dcc.linker.instance import create_instance\n"
        cmd_text += f"\tinstance = create_instance({data})\n"
        cmd_text += f"\tLoadAsset().process(instance)\n"
        cmd_text += f"except:\n"
        cmd_text += f"\tprint(traceback.format_exc())\n"
        cmd_text += "print('[cgDam] End of receiving from Substance Painter')\n"

        socket.send('''{}'''.format(cmd_text))

    except Exception as e:
        message(None, "Error", str(e) + '\n Make sure you open maya or maya command port is open.')


if __name__ == '__main__':
    print(__name__)
