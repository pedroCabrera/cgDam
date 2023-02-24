# -*- coding: utf-8 -*-
"""
Documentation:
"""
import os
from pathlib import Path

CgDamROOT = Path(os.getenv('CgDamROOT'))

from dcc.spp.api.remote_connect import connect_spp
from utils.dialogs import message
from utils.file_manager import FileManager

import pyblish.api

fm = FileManager()


class UpdateAsset(pyblish.api.InstancePlugin):
    label = "update asset inside substance painter"
    order = pyblish.api.ExtractorOrder
    hosts = ["spp"]
    families = ["asset"]


    def process(self, instance):
        asset_name = instance.name
        data = instance.data

        colorspace = data.get("colorspace", "aces")
        mesh_path = data.get('mesh_path', '')


        sp = connect_spp()

        if sp:
            current_sbp_path = eval(sp.execScript('substance_painter.project.file_path()', 'python'))
        else:
            message(None, 'Error', 'Can not get the current session of substance painter.')
            return

        cmd_text = "print('## cgDam Tools ##')\n"
        cmd_text += "import os\n"
        cmd_text += "import sys\n"
        cmd_text += "sys.path.append(os.path.join(os.getenv('CgDamROOT'), 'src'))\n"
        cmd_text += "from dcc.spp.api.pipeline import reload_mesh\n"
        cmd_text += f'reload_mesh("{mesh_path}")\n'

        sp.execScript(cmd_text, 'python')

if __name__ == '__main__':
    print(__name__)
