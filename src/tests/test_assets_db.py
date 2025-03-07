# -*- coding: utf-8 -*-
"""
Documentation: 
"""

# ---------------------------------
# Import Libraries
import sys
import os
import re

import unittest


CgDamROOT = os.getenv('CgDamROOT')
utils_path = os.path.join(CgDamROOT, 'src')
sysPaths = [CgDamROOT, utils_path]

for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from utils.assets_db import AssetsDB, Connect

# ---------------------------------
# Variables
db_file = CgDamROOT + '/src/tests/data/cgDam.db'

db = AssetsDB(db_file)

# ---------------------------------
# Start Here
class TestDataBase(unittest.TestCase):

    @Connect.db
    def test_create_default_tables(self, conn):
        table_names = [
            "assets",
            "categories",
            "asset_types",
            "asset_projects",
            "asset_tags",
            "geometry",
            "map_type",
            "projects",
            "tags",
            "textures",
            "thumbnail",
        ]

        for table_name in table_names:
            cur = conn.cursor()
            cur.execute(f'SELECT name FROM sqlite_master WHERE name="{table_name}"')
            tables = cur.fetchall()
            self.assertTrue(tables)

    def test_add_asset_type_and_category(self):
        db.add_asset_type(asset_type_name="Test")

        db.add_typed_category(category_name="Category1",asset_type_name="Test")
        db.add_typed_category(category_name="subCategory1",asset_type_name="Test",parent_category="Category1")
        db.add_typed_category(category_name="subCategory2",asset_type_name="Test",parent_category="Category1/subCategory1")        
        
        self.assertTrue("Test" in [x[0] for x in db.all_asset_types() if x[0]])
        self.assertTrue("Category1" in [x[1] for x in db.all_categories() if x[1]])
        self.assertTrue("subCategory1" in [x[1] for x in db.all_categories(asset_type_name="Test") if x[1]])
        self.assertTrue(db.get_tree_from_category(asset_category=db.get_category_from_tree(asset_category="Category1/subCategory1/subCategory2",
                                                                                            asset_type_name="Test"),
                                                   asset_type_name="Test")
                         in ["Category1/subCategory1/subCategory2"])
        self.assertTrue(db.get_all_children_categories(asset_category="Category1/subCategory1",asset_type_name="Test") in [[2,3]])

    def test_add_asset(self):

        # add asset
        id,name =db.add_asset(asset_name="foo1",asset_category="Category1/subCategory1",asset_type_name="Test")

        # assert UUID
        asset_uuid = db.get_asset_uuid(asset_name="foo1",asset_category="Category1/subCategory1",asset_type_name="Test")

        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        self.assertTrue(
            re.match(
                uuid_pattern,
                str(asset_uuid)
            ),
            asset_uuid
        )

        # assert asset name
        self.assertEqual(
            db.get_asset_name(uuid=asset_uuid),
            "foo1"
        )

"""
    def test_add_geometry(self):

        # reset all
        db.delete_row(
            table_name='geometry',
            col='asset_id',
            value=1,
        )


        # add data
        db.add_geometry(
            asset_name='foo',
            obj_file='path/to/obj',
            usd_geo_file='path/to/usd',
            mesh_data={'sgs': {'mat01': {}}}
        )

        geo_data = db.get_geometry(asset_name='foo', obj_file='', usd_geo_file='', mesh_data='')

        self.assertEqual(geo_data.get('obj_file'), 'path/to/obj')
        self.assertEqual(geo_data.get('usd_geo_file'), 'path/to/usd')
        self.assertEqual(geo_data.get('mesh_data'), {'sgs': {'mat01': {}}})

        # update geometry
        db.add_geometry(
            asset_name='foo',
            obj_file='path/to/obj2',
            abc_file='path/to/abc',
            mesh_data={'sgs': {'mat02': {}}}
        )

        geo_data = db.get_geometry(asset_name='foo', obj_file='', abc_file='', mesh_data='')
        self.assertEqual(geo_data.get('obj_file'), 'path/to/obj2')
        self.assertEqual(geo_data.get('abc_file'), 'path/to/abc')
        self.assertEqual(geo_data.get('mesh_data'), {'sgs': {'mat01': {}, 'mat02': {}}})

    def test_add_tag(self):
        db.add_tag(asset_name='foo', tag_name='tag1')

        self.assertTrue('tag1' in db.get_tags(asset_name='foo'))

    def test_add_project(self):
        db.add_project(asset_name='foo', project_name='project1')

        self.assertTrue('project1' in db.get_projects(asset_name='foo'))
"""

# Main Function
def main():
    unittest.main()
    #db_file = Connect.db_file
    #print(db_file)
    pass


if __name__ == '__main__':
    main()
