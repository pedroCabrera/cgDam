# -*- coding: utf-8 -*-
"""
Documentation: 
"""


# ---------------------------------
# Import Libraries
import sys
import os
import platform

import unittest


CgDamROOT = os.getenv('CgDamROOT')
utils_path = os.path.join(CgDamROOT, 'src')
sysPaths = [CgDamROOT, utils_path]

for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from utils.file_manager import FileManager

# ---------------------------------
# Variables
fm = FileManager()

# ---------------------------------
# Start Here
class TestFileManager(unittest.TestCase):

    def test_user_documents(self):

        user_document_dir = fm.user_documents.as_posix()

        if platform.system() == 'Windows':

            self.assertEqual(
                user_document_dir,
                f"C:/Users/{os.environ['USERNAME']}/Documents/cgDam"
            )

    def test_resolve_path(self):
        resolved_path = fm.resolve_path(
            '../path/to/$version/$asset_name',
            relatives_to='/root/dir/file.ext',
            variables={'$version': 'v10', '$asset_name': 'Foo'}
        )

        self.assertEqual(resolved_path, '/root/dir/path/to/v10/Foo')

    def test_user_json(self):
        fm.set_user_json(foo='bar')
        self.assertEqual(fm.get_user_json('foo'), 'bar')



# Main Function
def main():
    unittest.main()
    pass


if __name__ == '__main__':
    main()
