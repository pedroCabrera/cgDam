# -*- coding: utf-8 -*-
"""
Documentation:
"""
import os
import site
from pathlib import Path

CgDamROOT = Path(os.getenv('CgDamROOT'))

site.addsitedir(CgDamROOT.joinpath('venv/python39/Lib/site-packages').as_posix())

import pyblish.api

def create_instance(data):
    context = pyblish.api.Context()
    instance = context.create_instance(**data)
    return instance

if __name__ == '__main__':
    print(__name__)
