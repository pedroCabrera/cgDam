# -*- coding: utf-8 -*-
"""
Documentation:
"""
import os
import re
import sys
import traceback
from pathlib import Path

from PySide2.QtWidgets import QMessageBox

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT, CgDamROOT.joinpath('src')]
for sysPath in sysPaths:
    if str(sysPath) not in sys.path:
        sys.path.append(str(sysPath))

from utils.dialogs import message
from utils.file_manager import FileManager
from utils.textures import texture_type_from_name


import substance_painter
from substance_painter.exception import ProjectError, ResourceNotFoundError, ServiceNotFoundError

# ---------------------------------


Settings = {
    "OpenGL": substance_painter.project.NormalMapFormat.OpenGL,
    "DirectX": substance_painter.project.NormalMapFormat.DirectX,
    # ProjectWorkflow
    "Default": substance_painter.project.ProjectWorkflow.Default,
    "TextureSetPerUVTile": substance_painter.project.ProjectWorkflow.TextureSetPerUVTile,  # legacy
    "UVTile": substance_painter.project.ProjectWorkflow.UVTile,  # Set per material containing multiple UV
    # Tangent space
    "PerVertex": substance_painter.project.TangentSpace.PerVertex,
    "PerFragment": substance_painter.project.TangentSpace.PerFragment,
    "default_texture_resolution": 1024

}

Default_Project_settings = {
    "import_cameras": False,
    "default_texture_resolution": 1024,
    "normal_map_format": Settings["OpenGL"],
    "project_workflow": Settings["UVTile"],
    "tangent_space_mode": Settings["PerVertex"]

}

fm = FileManager()


def info(msg):
    substance_painter.logging.log(substance_painter.logging.INFO, "cgDam", msg)


def error_(msg):
    substance_painter.logging.log(substance_painter.logging.ERROR, "cgDam", msg)


class JS:
    def __init__(self):
        pass

    def exe(self, cmd):
        try:
            result = substance_painter.js.evaluate(cmd)
            return result
        except RuntimeError:
            info(f'Can not evaluate the "{cmd}" command')
            return

    def export_mesh(self, path=None):
        """
        TO export the current mesh
        :param path: the mesh path, if None it will export at the same path of original file
        :return:
        """

        if path is None:
            path = "alg.project.lastImportedMeshUrl()"
        else:
            path = f'"file:///{path}"'
        cmd = f'alg.project.exportMesh({path})'
        return self.exe(cmd)

    def open_export_window(self, **kwargs):
        """
        TO open the export window
        kwargs:
            format = "png",
            path = "/path/to/export",
            preset= "preset_name"
        :return:
        """
        cmd = f'alg.mapexport.showExportDialog({kwargs})'
        return self.exe(cmd)

    def get_current_export_preset(self):
        cmd = 'alg.mapexport.getProjectExportPreset()'
        return self.exe(cmd)

    def get_current_export_option(self):
        cmd = 'alg.mapexport.getProjectExportOptions()'
        return self.exe(cmd)

    def set_export_preset_name(self, preset_name):
        cmd = f'alg.mapexport.setProjectExportPreset("{preset_name}")'
        return self.exe(cmd)

    def get_export_preset_name(self):
        cmd = f'alg.mapexport.getProjectExportPreset()'
        return self.exe(cmd)

    def get_export_path(self):
        cmd = 'alg.mapexport.exportPath()'
        return self.exe(cmd)

    def get_documentStructure(self):
        cmd = f'alg.mapexport.documentStructure()'
        return self.exe(cmd)

    def export_texture(self, preset, path, extension, **kwargs):
        cmd = f'alg.mapexport.exportDocumentMaps("{preset}", "{path}", "{extension}")'
        return self.exe(cmd)


def main_window():
    return substance_painter.ui.get_main_window()


def create_project(mesh_file, project_path=None, cfg=None):
    """
    To remotely create a new project
    :param mesh_file: (str) the mesh file path
    :param project_path: (str) the new project path
    :param cfg: (dict) the configuration of starting file
    :return:
    """

    if not cfg:
        settings = Default_Project_settings
    else:
        settings = {}
        settings["import_cameras"] = cfg["import_cameras"]
        settings["default_texture_resolution"] = cfg["default_texture_resolution"]
        settings["normal_map_format"] = Settings[cfg["normal_map_format"]]
        settings["project_workflow"] = Settings[cfg["project_workflow"]]
        settings["tangent_space_mode"] = Settings[cfg["tangent_space_mode"]]
    # open project
    if substance_painter.project.is_open():
        substance_painter.project.close()

    substance_painter.project.create(mesh_file_path=mesh_file, settings=substance_painter.project.Settings(**settings))
    if substance_painter.project.is_open():
        print("The project was successfully created.")

    # save project
    if project_path:
        substance_painter.project.save_as(project_path)
        if not substance_painter.project.needs_saving():
            print("As expected, there is nothing to save since this was just done.")


def reload_mesh(mesh_path):
    mesh_reloading_settings = substance_painter.project.MeshReloadingSettings(
        import_cameras=False,
        preserve_strokes=True)

    def on_mesh_reload(status):
        if status == substance_painter.project.ReloadMeshStatus.SUCCESS:
            info("The mesh was reloaded successfully.")
        else:
            error_("The mesh couldn't be reloaded.")

    substance_painter.project.reload_mesh(mesh_path, mesh_reloading_settings, on_mesh_reload)


def get_mesh_path():
    return substance_painter.project.last_imported_mesh_path()


def get_file_path():
    try:
        filepath = substance_painter.project.file_path()
    except ProjectError:
        filepath = None
        pass
    if filepath:
        return filepath
    else:
        message(main_window(), "Error", "Please save the project first.")


def save_file(file_path):
    if not file_path.endswith('.spp'):
        error_('The substance painter file must endswith ".spp"')
    return substance_painter.project.save_as(file_path, substance_painter.project.ProjectSaveMode.Full)

def open_file(file_path):
    if Path(file_path).is_file():
        if substance_painter.project.is_open():
            if substance_painter.project.needs_saving():
                result = QMessageBox.question(
                    main_window(),
                    'Need to save',
                    'Do you want to save the current project?',
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel
                )
                if result == QMessageBox.Yes:
                    substance_painter.project.save(substance_painter.project.ProjectSaveMode.Incremental)
                elif result == QMessageBox.Cancel:
                    return

            substance_painter.project.close()

        substance_painter.project.open(file_path)


def save_copy(file_path):
    if not file_path.endswith('.spp'):
        error_('The substance painter file must endswith ".spp"')
    return substance_painter.project.save_as_copy(file_path)


def save_incremental(file_path):
    if not file_path.endswith('.spp'):
        error_('The substance painter file must endswith ".spp"')
    return substance_painter.project.save_as(file_path, substance_painter.project.ProjectSaveMode.Incremental)


def get_all_texture_sets():
    try:
        return [x.name() for x in substance_painter.textureset.all_texture_sets()]
    except ProjectError:
        pass


def get_resolutions():
    return 11

def get_preset_name_from_url(url):
    preset_id = substance_painter.resource.ResourceID.from_url(url)
    return preset_id.name

def export_texture(tex_dir=None):
    js = JS()

    if tex_dir is None:
        tex_dir = js.get_export_path()

    tex_dir, version = fm.version_folder_up(tex_dir)
    Path(tex_dir).mkdir(parents=True, exist_ok=True)

    try:
        # [Python] {'bitDepth': 0, 'dilation': 16, 'exportShaderParams': False, 'fileFormat': '', 'padding': 'Infinite'}

        # get substance export options
        current_option = js.get_current_export_option()

        # export preset
        export_preset = js.get_current_export_preset()

        if current_option.get("fileFormat", "png") == "":
            current_option["fileFormat"] = "png"


        export_options = {}
        export_options["exportPath"] = tex_dir
        export_options["exportShaderParams"] = current_option.get("exportShaderParams", True)
        export_options["format"] = current_option.get("fileFormat", "png")
        export_options["defaultExportPreset"] = export_preset

        # extension
        file_format = current_option.get("fileFormat", "png")

        # bit-depth
        bit_depth = current_option.get("bitDepth", 16)
        if bit_depth == 32:
            bit_depth = "32f"
        elif bit_depth == 0:
            bit_depth = "16"
        else:
            bit_depth = str(bit_depth)

        export_options["exportParameters"] = [{
            "parameters": {
                "fileFormat": file_format,
                "bitDepth": bit_depth,
                "dithering": True,
                "paddingAlgorithm": current_option.get("padding", "Infinite"),
                # "sizeLog2": get_resolutions(),  # to override all resolutions
                "dilationDistance": current_option.get("dilation", 16)
            }
        }]

        # texture sets
        all_texture_sets = get_all_texture_sets()
        # Create the list of Texture Sets to export.
        export_options["exportList"] = []
        for texture_set in all_texture_sets:
            export_options["exportList"].append({
                "rootPath": texture_set,
                "exportPreset": export_preset
            })

        result = substance_painter.export.export_project_textures(export_options)
        return on_export_texture_finished(result), version

    except Exception as e:
        error_(f"Export error: {e}")
        error_(f"Export error: {traceback.format_exc()}")


def on_export_texture_finished(result):
    if result.status != substance_painter.export.ExportStatus.Success:
        message(main_window(), "Error", result.message)

    textures_data = {}

    for key in result.textures:
        sg = key[0]
        mtl_name = re.sub(r"(?i)sg$", "MTL", sg)
        textures_data[sg] = {
            'materials': {
                mtl_name: {
                    'type': 'standard_surface',
                    'attrs': {},
                    'texs': {}
                }
            },
            'displacements': {}
        }
        info(sg)

        texture_set = substance_painter.textureset.TextureSet.from_name(sg)
        textures = result.textures.get(key)

        if texture_set.has_uv_tiles():
            uv_tiles = texture_set.all_uv_tiles()
            udim = len(uv_tiles)
            selected_textures = textures[:int(len(textures) / udim)]
        else:
            udim = 0
            selected_textures = textures

        for file_path in selected_textures:
            info(file_path)
            map_type = texture_type_from_name(os.path.basename(file_path))
            tex_name = f'{sg}_{map_type}'

            if map_type == 'height':
                textures_data[sg]['displacements'][f'{sg}_displacement'] = {
                    'type': 'displacement',
                    'texs': {
                        tex_name: {
                            'plugs': [map_type],
                            'filepath': file_path,
                            'udim': udim,
                            'type': 'file',
                        },
                    },
                    'attrs': {}
                }
                continue

            textures_data[sg]['materials'][mtl_name]['texs'][tex_name] = {
                'plugs': [map_type],
                'filepath': file_path,
                'udim': udim,
                'type': 'file',

            }
    return textures_data






if __name__ == '__main__':
    print(__name__)
    mesh_path =  r"C:/Users/michael/Documents/projects/dummy/scenes/Export/chair/chair_v0029.obj"
    create_project(mesh_file=mesh_path)
