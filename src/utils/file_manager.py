# -*- coding: utf-8 -*-
"""
Documentation:
"""

# ---------------------------------
# import libraries
import subprocess
import sys
import os
import re
import json
from pathlib import Path

CgDamROOT = os.getenv('CgDamROOT')
utils_path = os.path.join(CgDamROOT, 'src')

sysPaths = [CgDamROOT, utils_path]

for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

# ---------------------------------

class FileManager:

    def resolve_path(self, source_path, **kwargs):
        """
        To resolve the given paths like relative path and $project
        :param source_path: the unresolved path
        :param kwargs: args to resolve with
        :return: resolved path
        """

        relatives_to = kwargs.get('relatives_to', '')

        resolved_path = Path(relatives_to)

        if source_path.count("../") > 0:
            resolved_path = resolved_path.parents[source_path.count("../") - 1]
            resolved_path = resolved_path.joinpath(source_path.rsplit("../", 1)[-1])
        else:
            resolved_path = source_path

        variables = kwargs.get('variables', {})
        for var in variables:
            resolved_path = str(resolved_path).replace(var, variables.get(var))

        return resolved_path.replace('\\', '/')

    def get_user_json(self, key, key1=None):
        json_path = self.user_documents.joinpath("cgDam.json")

        data = {}

        if not json_path.is_file():
            self.user_documents.mkdir(parents=True, exist_ok=True)
            self.write_json(json_path, data)

        user_data = self.read_json(json_path)
        returned_data = user_data.get(key)
        if key1 and returned_data:
            return returned_data.get(key1)

        return returned_data

    def set_user_json(self, **kwargs):
        json_path = self.user_documents.joinpath("cgDam.json")

        if json_path.is_file():
            data = self.read_json(json_path)
        else:
            data = {}
        for key in kwargs:
            data[key] = kwargs[key]

        self.write_json(json_path, data)

    def read_json(self, json_path):
        """
        To read json file
        :param json_path: the system path of json
        :return: (dict)
        """
        with open(json_path, 'r') as f:
            return json.load(f)

    def write_json(self, json_path, data):
        json_path = Path(str(json_path))
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w') as f:
            return json.dump(data, f, indent=4)

    @property
    def user_documents(self):
        user_dir = Path.home().joinpath('Documents', 'cgDam')
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    @property
    def user_db(self):
        return self.user_documents.joinpath('assets.db')

    def list_dirs(self, directory):
        return [x for x in os.listdir(directory) if os.path.isdir(os.path.join(directory, x))]

    def list_files(self, directory, ext=".*"):
        return [x for x in os.listdir(directory) if
                os.path.isfile(os.path.join(directory, x)) and re.search(ext + "$", x)]

    def make_dirs(self, path, *args):
        if not os.path.isdir(os.path.join(path, *args)):
            os.makedirs(os.path.join(path, *args))

        return os.path.join(path, *args).replace("\\", "/")

    def get_latest_folder_version(self, path, prefix='v', padding=4, ret_path=False):

        self.make_dirs(path)
        all_versions = os.listdir(path)
        if len(all_versions) < 1:
            version = prefix + "1".zfill(padding)
        else:
            all_versions = [x for x in all_versions if re.search(prefix + r"\d+", x)]
            if len(all_versions) <= 1:
                version = prefix + "1".zfill(padding)
            else:
                all_versions_ints = [int(re.findall(r"\d+", x)[0]) for x in all_versions]
                version = prefix + str(max(all_versions_ints)).zfill(padding)

        if ret_path:
            return os.path.join(path, version).replace("\\", "/")
        else:
            return version

    def get_latest_file_version(self, root, ext='.*', prefix='v', padding=4, ret_path=False):
        root = Path(root)

        files = root.glob(f'*{ext}')
        names = [x.name for x in files if re.search(prefix + r"\d+", x.name)]
        if len(names) < 1:
            return 0

        all_versions_ints = [int(re.findall(r"\d+", x)[0]) for x in names]
        max_version_num = max(all_versions_ints)
        latest_version = prefix + str(max_version_num).zfill(padding)

        file_name = re.sub(prefix + r"\d+", latest_version, names[0])
        if ret_path:
            return root.joinpath(file_name).as_posix(), max_version_num
        else:
            return file_name, max_version_num

    def version_folder_up(self, path, prefix='v', padding=4):
        self.make_dirs(path)
        increment = "1".zfill(padding)
        up_version = "{}{}".format(prefix, increment)
        all_versions = os.listdir(path)
        if len(all_versions) < 1:
            ret_path = os.path.join(path, up_version)
        else:
            latest_version = self.get_latest_folder_version(path, prefix=prefix, padding=padding, ret_path=False)

            num_str = re.findall(r"\d+", latest_version)
            if not num_str:
                ret_path = os.path.join(path, up_version)
            else:
                increment = str(int(num_str[0]) + 1).zfill(padding)
                up_version = "{}{}".format(prefix, increment)
                ret_path = os.path.join(path, up_version)
        return ret_path.replace("\\", "/"), up_version

    def version_file_up(self, file_path, prefix='v', padding=4):

        file_path = Path(str(file_path))
        ext = file_path.suffix
        file_dir = file_path.parent
        file_dir.mkdir(parents=True, exist_ok=True)

        files = file_dir.glob(f'*{ext}')

        names = [x.name for x in files if re.search(prefix + r'\d+', x.name)]
        if len(names) < 1:
            file_name = re.sub(prefix + r'\d+', prefix + '0001', file_path.name)
            return file_dir.joinpath(file_name).as_posix()

        latest_file, num = self.get_latest_file_version(file_dir, ext=ext, prefix=prefix, padding=padding,
                                                        ret_path=True)
        increment_file = re.sub(
            prefix + str(num).zfill(padding),
            prefix + str(num + 1).zfill(padding),
            latest_file
        )

        return increment_file

    def open_in_expoler(self, path):
        path = Path(str(path))

        if path.is_file():
            subprocess.Popen(f'explorer /select,"{path}"')

        elif path.is_dir():
            subprocess.Popen(f'explorer "{path}"')


# Main function
def main():
    pass


if __name__ == '__main__':
    main()
