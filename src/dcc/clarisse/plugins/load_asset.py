# -*- coding: utf-8 -*-
"""
Documentation:
"""

# ---------------------------------
# Import Libraries
import os
import re
import sys
import site
import traceback
from pathlib import Path

CgDamROOT = Path(os.getenv("CgDamROOT"))
sysPaths = [CgDamROOT.joinpath('src').as_posix()]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

#site.addsitedir(CgDamROOT.joinpath('venv', 'python39', 'Lib', 'site-packages').as_posix())
site.addsitedir(CgDamROOT.joinpath('../.conda/Lib/site-packages').as_posix())
############################################
import importlib
import dcc.clarisse.api.cmds
import utils.file_manager

importlib.reload(dcc.clarisse.api.cmds)
importlib.reload(utils.file_manager)

############################################

import pyblish.api

from settings.settings import get_dcc_cfg, material_attrs_conversion, shading_nodes_conversion, get_material_attrs, \
    get_shading_nodes

from dcc.clarisse.api.cmds import Clarisse

import ix


# ---------------------------------
# Variables

# ---------------------------------
# Start Here

def create_instance(data):
    context = pyblish.api.Context()
    instance = context.create_instance(**data)
    return instance


class LoadAsset(pyblish.api.InstancePlugin):
    label = "import and set the asset"
    order = pyblish.api.ExtractorOrder
    hosts = ["clarisse"]
    families = ["asset"]

    def process(self, instance):
        self.log.info("-initialize loading asset into clarisse")
        print('-initialize loading asset into clarisse')
        self.cl = Clarisse()

        asset_name = instance.name
        data = instance.data

        # colorspace
        colorspace = data.get('colorspace', 'aces')

        # host
        source_host = data.get('host', 'standard')
        if source_host == 'spp':
            source_host = 'standard'
        host = 'clarisse'

        # renderer
        to_renderer = data.get('to_renderer', 'standard_surface')  # clarisse
        source_renderer = data.get('renderer', 'standard')

        geo_paths = data.get('geo_paths')

        if geo_paths:
            # get the geometry types  ('Alembic Reference', 'Alembic Bundle', 'USD Reference', 'USD Bundle')
            geo_type = data.get('geometry_type', 'Alembic Bundle')

            if re.search(r'(?i)alembic', geo_type):
                geo_path = geo_paths.get('abc_file')
            elif re.search(r'(?i)usd', geo_type):
                geo_path = geo_paths.get('usd_geo_file')
            else:
                ix.ix.log_error(f"Invalid geometry_type, '{geo_type}' not supported.")
                return

            if not os.path.isfile(str(geo_path)):
                ix.ix.log_error(f"'{geo_path}' file does not exists")
                return
        else:
            geo_type = geo_paths = geo_path = None

        # create main contexts
        selected_ctx = data.get('context')  # if the working context is given
        if selected_ctx == 'selected':
            root_ctx = self.cl.get_selected_context()
            if not root_ctx:
                return
        else:
            root_ctx = get_dcc_cfg( 'clarisse', 'configuration', 'asset_root')
            root_ctx = root_ctx.replace("$assetName", asset_name)

        # get context cfg
        geo_ctx = get_dcc_cfg( 'clarisse', 'configuration', 'geometry_root')
        mtl_ctx = get_dcc_cfg( 'clarisse', 'configuration', 'material_root')
        tex_ctx = get_dcc_cfg( 'clarisse', 'configuration', 'texture_root')
        utils_ctx = get_dcc_cfg( 'clarisse', 'configuration', 'utils_root')

        # resolve and create contexts
        if selected_ctx != 'selected':
            geo_ctx = self.cl.create_context(geo_ctx.replace('..', root_ctx))
        mtl_ctx = self.cl.create_context(mtl_ctx.replace('..', root_ctx))
        tex_ctx = self.cl.create_context(tex_ctx.replace('..', root_ctx))
        utils_ctx = self.cl.create_context(utils_ctx.replace('..', root_ctx))

        # import geometry
        if geo_paths:
            geo_item = self.cl.import_geo(geo_path, asset_name, context=str(geo_ctx), geo_type=geo_type)
        else:
            geo_item = None

        # get asset data
        asset_data = data.get('asset_data')

        # convert material data to clarisse engines
        if source_host == 'standard' or source_renderer == 'standard':
            # standard material
            plugs_conversion = get_material_attrs(host, to_renderer)
            nodes_conversion = get_shading_nodes(host, to_renderer)
        else:
            plugs_conversion = material_attrs_conversion(source_host, source_renderer, host, to_renderer)
            nodes_conversion = shading_nodes_conversion(source_host, source_renderer, host, to_renderer)

        # materials data
        for sg in asset_data:
            # materials
            materials = asset_data.get(sg, {}).get('materials', {})
            material_items = []
            displacement_items = []
            for mtl in materials:
                from_renderer = materials[mtl].get('type')
                mtl_type = nodes_conversion.get(from_renderer)
                # create material
                mtl_item = self.cl.create_node(mtl, mtl_type, cntx=mtl_ctx)
                material_items.append(mtl_item)

                # attributes
                attrs = materials[mtl].get('attrs')
                for attr in attrs:
                    try:
                        to_attr = plugs_conversion.get(attr).get('name')
                        value = attrs.get(attr)
                        ix.cmds.SetValues([f'{mtl_item}.{to_attr}'], [f'{value}'])
                    except:
                        pass

                # create textures
                textures = materials[mtl].get('texs')
                for tex, tex_dict in textures.items():
                    plug_name = tex_dict.get('plugs')[0]
                    tex_type = tex_dict.get('type')

                    to_plug = plugs_conversion.get(plug_name)

                    if not to_plug:
                        continue

                    # create_ texture
                    tex_item = self.cl.import_texture(
                        tex_dict.get('filepath'),
                        tex_ctx,
                        tex_dict.get('udim'),
                        colorspace,  # tex_dict.get('colorspace'),
                        to_plug.get('type') == 'color'
                    )

                    tex_attr = mtl_item.get_attribute(to_plug.get('name'))

                    connected_item = tex_item
                    for inbetween_dict in to_plug.get("inbetween"):
                        if inbetween_dict == [{}] or not inbetween_dict:
                            continue

                        inbetween_node_name = mtl + inbetween_dict.get('name')
                        inbetween_item = self.cl.create_node(inbetween_node_name, inbetween_dict.get('type'),
                                                             cntx=utils_ctx)
                        if not inbetween_item:
                            inbetween_item = ix.get_item(str(utils_ctx) + "/" + inbetween_node_name)

                        inbetween_node_attr = inbetween_item.get_attribute(inbetween_dict.get('inplug'))
                        ix.cmds.SetTexture([str(inbetween_node_attr)], str(connected_item))
                        connected_item = inbetween_item

                    ix.cmds.SetTexture([str(tex_attr)], str(connected_item))

            displacements = asset_data.get(sg, {}).get('displacements', {})
            for displacement, displacement_dict in displacements.items():
                displacement_item = self.cl.create_node(displacement, material_type='Displacement', cntx=mtl_ctx)
                if not displacement_item:
                    displacement_item = ix.get_item(f'{mtl_ctx}/{displacement}')
                displacement_items.append(displacement_item)

                for tex_name, tex_dict in displacement_dict.get('texs', {}).items():
                    tex_item = self.cl.import_texture(
                        tex_dict.get('filepath'),
                        tex_ctx,
                        tex_dict.get('udim'),
                        colorspace,  # tex_dict.get('colorspace'),
                        False
                    )
                    # displacement_item.attrs.front_value = str(tex_item)
                    ix.cmds.SetTexture([f"{displacement_item}.front_value"], str(tex_item))
                    # turn off displacement
                    ix.cmds.SetValues([f"{displacement_item}.active"], ["0"])

            if not geo_item:
                continue

            # assign materials
            default_sgs = ['default', 'top', 'bottom', 'back', 'left', 'right', 'front', 'sides', 'subset']
            # - reference
            if re.search(r'(?i)reference', geo_type):

                if re.search(r'(?i)alembic', geo_type):
                    clarisse_geo_type = 'GeometryAbcMesh'
                elif re.search(r'(?i)usd', geo_type):
                    clarisse_geo_type = 'GeometryUsdMesh'
                else:
                    continue

                shape_items = self.cl.get_objects_by_type(clarisse_geo_type, str(geo_item))

                for mesh_shape_path in asset_data.get(sg, {}).get('meshes', {}).get('shape', {}):
                    for shape_item in shape_items:
                        shape_item_sgs = self.cl.get_shading_group(shape_item)

                        shape_item_name = str(shape_item.get_name())

                        if re.search(r'(?i)usd', geo_type):
                            mesh_path = mesh_shape_path.rsplit('|', 1)[0]
                        else:
                            mesh_path = mesh_shape_path

                        if mesh_path.endswith(shape_item_name):
                            for shape_item_sg, index in shape_item_sgs.items():
                                shape_sg = shape_item_sg.split('>')[-1]

                                if (shape_sg == sg) or (shape_sg in default_sgs):
                                    ix.cmds.SetValues(
                                        [str(shape_item) + f".materials[{index}]"],
                                        [str(material_items[0])])
                                    if displacement_items:
                                        ix.cmds.SetValues(
                                            [str(shape_item) + f".displacements[{index}]"],
                                            [str(displacement_items[0])])

            # - bundle
            elif re.search(r'(?i)bundle', geo_type):
                bundle_sgs = self.cl.get_shading_group(geo_item)

                for mesh_shape in asset_data.get(sg, {}).get('meshes', {}).get('shape', {}):
                    for shape_item_path, index in bundle_sgs.items():
                        shape_sg = shape_item_path.split('>')[-1]

                        if (shape_sg == sg) or (shape_sg in default_sgs):
                            clarisse_path_pattern = shape_item_path.split('>')[0].split('/', 2)[-1]

                            # source data pattern
                            source_path_pattern = mesh_shape.split('|')
                            if re.search(r'(?i)usd', geo_type):
                                # remove shape node because clarisse usd ignore the shape nodes
                                source_path_pattern.pop(-1)
                            else:
                                # remove transform node because clarisse abc ignore the transform nodes
                                source_path_pattern.pop(-2)

                            source_path_pattern = '/'.join(source_path_pattern)
                            # assign material
                            try:
                                print(clarisse_path_pattern, source_path_pattern, index, material_items)
                                if clarisse_path_pattern in source_path_pattern:
                                    ix.cmds.SetValues([str(geo_item) + f".materials[{index}]"],
                                                      [str(material_items[0])])

                                if displacement_items:
                                    ix.cmds.SetValues(
                                        [str(geo_item) + f".displacements[{index}]"],
                                        [str(displacement_items[0])])
                            except:
                                print(traceback.format_exc())


# Main Function
def main():
    import sys

    data = sys.argv[0]
    instance = create_instance(data)

    LoadAsset().process(instance)


if __name__ == '__main__':
    main()
