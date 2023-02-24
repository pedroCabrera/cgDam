# -*- coding: utf-8 -*-
"""
Documentation:
"""
import os

CgDamROOT = os.getenv("CgDamROOT")


def get_stylesheet():
    return open(f"{CgDamROOT}/src/utils/resources/stylesheet.qss").read()


if __name__ == '__main__':
    print(__name__)
