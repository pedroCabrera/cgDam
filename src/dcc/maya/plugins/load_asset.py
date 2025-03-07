# -*- coding: utf-8 -*-
"""
Documentation: 
"""

# ---------------------------------
# Import Libraries
import os
import sys
from pathlib import Path
import re

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

###############################
import importlib
import utils.generic
import dcc.maya.api.cmds
import utils.file_manager

importlib.reload(utils.generic)
importlib.reload(dcc.maya.api.cmds)
importlib.reload(utils.file_manager)

################################

import pyblish.api
from dcc.maya.api.cmds import Maya
from settings.settings import material_attrs_conversion, shading_nodes_conversion, get_material_attrs
from utils.file_manager import FileManager

import maya.cmds as cmds
import maya.mel as mel


# ---------------------------------
# Variables

# ---------------------------------
# Start Here
class LoadAsset(pyblish.api.InstancePlugin):
    label = "import and set the asset"
    order = pyblish.api.ExtractorOrder
    hosts = ["maya"]
    families = ["asset"]

    def process(self, instance):

        ma = Maya()
        fm = FileManager()
        asset_name = instance.name
        data = instance.data

        # import geo
        geo_type = data.get('geometry_type', '')
        import_type = data.get('import_type', '<none>')
        geo_paths = data.get('geo_paths', {})
        colorspace = data.get('colorspace')

        geo_path = geo_paths.get(geo_type)
        if geo_path:
            if import_type == 'Import Geometry':
                ma.import_geo(geo_path)

        # host
        source_host = data.get('host', 'standard')
        if source_host == 'spp':
            source_host = 'standard'
        host = 'maya'

        # renderer
        to_renderer = data.get('to_renderer')
        source_renderer = data.get('source_renderer', 'standard')

        # conversions
        if source_host == 'standard' or source_renderer == 'standard':
            # standard material
            plugs_conversion = get_material_attrs(host, to_renderer)
        else:
            plugs_conversion = material_attrs_conversion(source_host, source_renderer, host, to_renderer)
            nodes_conversion = shading_nodes_conversion(source_host, source_renderer, host, to_renderer)

        asset_data = data.get('asset_data')
        for sg in asset_data:
            # materials
            materials = asset_data.get(sg, {}).get('materials', {})
            for mtl in materials:
                mtl_name = re.sub(r'(?i)sg', 'MTL', sg)
                if not cmds.objExists(sg):
                    mtl_name, sg = ma.create_material(name=mtl_name, sg=sg)
                else:
                    exist_materials = ma.get_materials_from_sg(sg, 'material')
                    if exist_materials and mtl_name in exist_materials:
                        mtl_name = exist_materials[0]
                    else:
                        mtl_name, sg = ma.create_material(name=mtl, sg=sg)

                # attributes
                attrs = materials[mtl].get('attrs')
                for attr in attrs:
                    to_attr = plugs_conversion.get(attr).get('name')
                    value = attrs.get(attr)
                    cmds.setAttr(f'{mtl_name}.{to_attr}', value)

                # create textures
                textures = materials[mtl].get('texs')
                for tex_name, tex_dict in textures.items():
                    plug_name = tex_dict.get('plugs')[0]
                    if not plug_name:
                        continue
                    tex_type = tex_dict.get('type')
                    to_plug = plugs_conversion.get(plug_name)
                    if not to_plug:
                        continue
                    plug_type = to_plug.get('type')  # float color, vector

                    if colorspace is None:
                        colorspace = tex_dict.get('colorspace', 'aces')
                    # create texture
                    tex_node = ma.import_texture(
                        tex_dict.get('filepath'),
                        tex_dict.get('udim'),
                        colorspace,
                        plug_type == 'color',
                        tex_name

                    )

                    if plug_type == 'float':
                        tex_plug = 'outColor.outColorR'
                        cmds.setAttr(tex_node + ".alphaIsLuminance", 1)
                    else:
                        tex_plug = 'outColor'
                        mel.eval(f'generateUvTilePreview {tex_node};')

                    # inbetween nodes
                    connected_node = tex_node
                    connected_plug = tex_plug
                    for inbetween_dict in to_plug.get("inbetween"):
                        if inbetween_dict == [{}] or not inbetween_dict:
                            continue
                        inbetween_node = mtl + inbetween_dict.get('name')
                        if not cmds.objExists(inbetween_node):
                            inbetween_node = ma.create_util_node(inbetween_dict.get('type'), inbetween_node)
                        ma.connect_attr(
                            f'{connected_node}.{connected_plug}',
                            f'{inbetween_node}.{inbetween_dict.get("inplug")}'
                        )
                        connected_node = inbetween_node
                        connected_plug = inbetween_dict.get("outplug")

                    ma.connect_attr(
                        f'{connected_node}.{connected_plug}',
                        f'{mtl_name}.{to_plug.get("name")}')

            # displacement
            displacements = asset_data.get(sg, {}).get('displacements', {})
            for displacement, displacement_dict in displacements.items():
                # create displacement
                displacement_node = displacement
                tex_name = displacement.replace('displacement', 'height')
                if not cmds.objExists(displacement_node):
                    displacement_node = cmds.shadingNode('displacementShader', n=displacement_node, asShader=1)

                for tex_name, tex_dict in displacement_dict.get('texs', {}).items():
                    # create texture
                    if colorspace is None:
                        colorspace = tex_dict.get('colorspace', 'aces')
                    tex_node = ma.import_texture(
                        tex_dict.get('filepath'),
                        tex_dict.get('udim'),
                        colorspace,
                        False,
                        tex_name
                    )
                    if not tex_node:
                        continue
                    cmds.connectAttr(f'{tex_node}.outColor.outColorR', displacement_node + '.displacement', f=1)
                    cmds.connectAttr(displacement_node + '.displacement', f'{sg}.displacementShader', f=1)

            # assign materials
            if not geo_path:
                continue
            meshes = asset_data.get(sg, {}).get('meshes', {}).get('shape', {})
            for mesh_path in meshes:
                try:
                    mesh_path = '*' + mesh_path.split('|', 2)[-1]
                    ma.assign_material(cmds.ls(mesh_path), sg_name=sg)
                except:
                    pass

        # ma.arrangeHypershade()


# Main Function
def main():
    pyblish.api.register_host("maya")
    pyblish.api.register_plugin(LoadAsset)

    context = pyblish.util.collect()

    LoadAsset().process(context[0])
    instance = pyblish.util.extract(context)


if __name__ == '__main__':
    main()
