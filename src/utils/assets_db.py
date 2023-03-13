# -*- coding: utf-8 -*-
"""
Documentation:
"""

# ---------------------------------
# Import Libraries
import datetime
import json
import sqlite3
import sys
import os
import site
import traceback
from functools import wraps
from urllib.parse import unquote
os.environ['CgDamROOT'] = os.path.abspath("./cgDam")
sysPaths = [os.getenv("CgDamROOT"), os.getenv("CgDamROOT") + "/src"]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

from settings.settings import get_textures_patterns
from utils.generic import merge_dicts
# ---------------------------------
# Variables

from utils.file_manager import FileManager

fm = FileManager()


def connect(db_file):
    def connect_(query_func):
        @wraps(query_func)
        def connect_wrapper(*args, **kwargs):
            try:
                conn = sqlite3.connect(db_file)
                query_func(conn, *args, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                raise e
            else:
                conn.commit()
                conn.close()

        return connect_wrapper

    return connect_


class Connect(object):
    db_file = None

    def __init__(self, db_file=None):
        if db_file is None:
            db_file = fm.user_db
        Connect.db_file = db_file

    def db(query_func):
        @wraps(query_func)
        def connect_wrapper(*args, **kwargs):
            try:
                conn = sqlite3.connect(Connect.db_file)
                cur = conn.cursor()
                ret_data = query_func(*args, conn, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                raise e
            else:
                conn.commit()
                conn.close()
                return ret_data

        return connect_wrapper

    def set_db_file(self, db_file):
        Connect.db_file = db_file

    def get_db_file(self):
        return Connect.db_file

    db = staticmethod(db)


class AssetsDB(Connect):

    def __init__(self, db_file=None):
        super(AssetsDB, self).__init__(db_file)
        if db_file:
            if not os.path.isdir(os.path.dirname(db_file)):
                os.makedirs(os.path.dirname(db_file))
            Connect.db_file = db_file
        self.create_default_tables()

    @Connect.db
    def delete_table(self, conn, table_name):
        cur = conn.cursor()

        query = f'''DROP TABLE IF EXISTS {table_name}'''
        cur.execute(query)

    @Connect.db
    def delete_row(self, conn, table_name, col, value):
        cur = conn.cursor()

        query = f'''DELETE from {table_name} where {col} = {value}'''
        cur.execute(query)

    @Connect.db
    def create_asset_table(self, conn):
        table_name = "assets"
        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                asset_type_id INTEGER,
                asset_category_id INTEGER,
                creation_date DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                modification_date DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                uuid TEXT DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
                UNIQUE(name, asset_type_id, asset_category_id),
                FOREIGN KEY (asset_type_id) REFERENCES asset_types (id) ON DELETE SET DEFAULT
                );
        '''
        cur.execute(query)

    @Connect.db
    def create_geometry_table(self, conn):
        table_name = "geometry"

        # self.delete_table(table_name=table_name)
        default_data = {}
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id INTEGER NOT NULL,
                    obj_file TEXT,
                    usd_geo_file TEXT,
                    abc_file TEXT,
                    fbx_file TEXT,
                    source_file TEXT,
                    substance_file TEXT,
                    mesh_data TEXT DEFAULT "{default_data}",
                    FOREIGN KEY (asset_id) REFERENCES assets (id) ON DELETE CASCADE
                    UNIQUE(asset_id)
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_map_type_table(self, conn):
        table_name = "map_type"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    type TEXT,
                    UNIQUE(name)
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_texture_table(self, conn):
        table_name = "textures"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id INTEGER NOT NULL,
                    map_id INTEGER NOT NULL,
                    udim_num INTEGER,
                    texture_path TEXT,
                    material_name TEXT,
                    res INTEGER,

                    FOREIGN KEY (asset_id) REFERENCES assets (id) ON DELETE CASCADE,
                    FOREIGN KEY (map_id) REFERENCES map_type (id)
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_thumbnail_table(self, conn):
        table_name = "thumbnail"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id INTEGER NOT NULL,
                    thumb_path TEXT,
                    thumbnail BLOB,

                    FOREIGN KEY (asset_id) REFERENCES assets (id) ON DELETE CASCADE
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_projects_table(self, conn):
        table_name = "projects"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_asset_types_table(self, conn):
        table_name = "asset_types"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    UNIQUE(name)
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_category_table(self, conn):
        table_name = "categories"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    parent_id INTEGER,
                    asset_type_id INTEGER,
                    UNIQUE(name, parent_id, asset_type_id),
                    FOREIGN KEY (parent_id) REFERENCES categories (id) ON DELETE CASCADE
                    FOREIGN KEY (asset_type_id) REFERENCES asset_types (id) ON DELETE CASCADE
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_tags_table(self, conn):
        table_name = "tags"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_asset_tags_table(self, conn):
        table_name = "asset_tags"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id INTEGER,
                    tag_id INTEGER,
                    FOREIGN KEY (asset_id) REFERENCES assets (id) ON DELETE CASCADE
                    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
                    );
        '''
        cur.execute(query)

    @Connect.db
    def create_asset_projects_table(self, conn):
        table_name = "asset_projects"

        # self.delete_table(table_name=table_name)
        cur = conn.cursor()
        query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id INTEGER,
                    project_id INTEGER,
                    FOREIGN KEY (asset_id) REFERENCES assets (id) ON DELETE CASCADE
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                    );
        '''
        cur.execute(query)

    def create_default_tables(self):
        self.create_asset_table()
        self.create_map_type_table()
        self.create_projects_table()
        self.create_tags_table()
        self.create_asset_tags_table()
        self.create_asset_projects_table()

        self.create_geometry_table()
        self.create_texture_table()
        self.create_thumbnail_table()

        self.create_asset_types_table()
        self.create_category_table()

    @Connect.db
    def get_last_id(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT last_insert_rowid();")
        ids = cur.fetchall()
        return ids[0][0]

    @Connect.db
    def get_asset_id(self, conn, asset_name):
        cur = conn.cursor()
        cur.execute(f'SELECT id from assets WHERE name="{asset_name}"')
        ids = cur.fetchone()
        if ids:
            return ids[0]
        else:
            return 0
    
    @Connect.db
    def get_asset_uuid(self, conn, asset_name):
        cur = conn.cursor()
        cur.execute(f'SELECT uuid from assets WHERE name="{asset_name}"')
        uuids = cur.fetchone()
        if uuids:
            return uuids[0]
        else:
            raise Exception(f"Asset '{asset_name}' not found")
    
    @Connect.db
    def get_asset_name(self, conn, uuid):
        cur = conn.cursor()
        cur.execute(f'SELECT name from assets WHERE uuid="{uuid}"')
        names = cur.fetchone()
        if names:
            return names[0]
        else:
            return ""

    @Connect.db
    def get_latest_edit_asset_name(self, conn):
        cur = conn.cursor()
        query = f'''
                SELECT name FROM assets 
                ORDER BY modification_date DESC LIMIT 1
        '''
        cur.execute(query)
        data = cur.fetchall()
        if data:
            return data[0][0]

    @Connect.db
    def update_date(self, conn, asset_name):
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d, %H:%M:%S")
        cur = conn.cursor()
        query = f'''
                UPDATE assets 
                SET modification_date = "{current_date}"
                WHERE
                name = "{asset_name}"
        '''
        cur.execute(query)

    @Connect.db
    def update_texture_maps(self, conn):
        map_types = get_textures_patterns()

        for map_type in map_types:
            cur = conn.cursor()
            if 'color' in map_type:
                _type = 'color'
            else:
                _type = 'float'

            query = f'''
                    INSERT INTO map_type
                    (name, type) 
                    VALUES
                    ("{map_type}", "{_type}")
                    ON CONFLICT(name) 
                    DO NOTHING
            '''

            cur.execute(query)
 
    @Connect.db
    def add_asset_type(self, conn, asset_type_name):
        cur = conn.cursor()
        query = f'''
                INSERT INTO asset_types 
                (name)
                VALUES
                ("{asset_type_name}")
                ON CONFLICT(name) 
                DO NOTHING
                ;
        '''
        cur.execute(query)
    
    @Connect.db
    def get_category_from_tree(self, conn, asset_category, asset_type_name):
        cur = conn.cursor()
        category_tree = asset_category.split("/")
        asset_category_id = cur.execute(f'''SELECT id FROM categories 
                                            WHERE name="{category_tree[0]}" 
                                            AND asset_type_id = (SELECT id FROM asset_types WHERE name="{asset_type_name}");''').fetchone()[0]
        if len(category_tree)>1:
            for parent_category in category_tree[1:]:
                asset_category_id = cur.execute(f'''SELECT id FROM categories 
                                                WHERE name="{parent_category}" 
                                                AND 
                                                parent_id ="{asset_category_id}" 
                                                AND 
                                                asset_type_id = (SELECT id FROM asset_types WHERE name="{asset_type_name}");''').fetchone()[0]
        return asset_category_id
    
    @Connect.db
    def get_tree_from_category(self, conn, asset_category, asset_type_name):
        cur = conn.cursor()
        if isinstance(asset_category, str):
            asset_category_id = self.get_category_from_tree(asset_category=asset_category,asset_type_name=asset_type_name)
        elif isinstance(asset_category,int):
            asset_category_id = asset_category
        else:
            raise Exception("You must specify a valid asset_category or asset_category_id")
            return
        query = f'''
                WITH RECURSIVE parent_names AS (
                    SELECT id, name, parent_id
                    FROM categories
                    WHERE id = {asset_category_id}
                    AND
                    asset_type_id = (SELECT id FROM asset_types WHERE name="{asset_type_name}")
                    
                    UNION ALL
                    
                    SELECT at.id, at.name, at.parent_id
                    FROM categories at
                    JOIN parent_names pn ON at.id = pn.parent_id
                )
                SELECT name
                FROM parent_names;        
                '''
        categories = [x[0] for x in cur.execute(query).fetchall() if x]
        categories.reverse()
        return "/".join(categories)

    @Connect.db
    def get_all_children_categories(self, conn, asset_category,asset_type_name):
        cur = conn.cursor()
        asset_category_id = self.get_category_from_tree(asset_category = asset_category,asset_type_name= asset_type_name)
        query = f'''
                WITH RECURSIVE recursive_cte(id, name, parent_id, asset_type_id) AS (
                    SELECT id, name, parent_id, asset_type_id
                    FROM categories
                    WHERE id = {asset_category_id}
                    UNION ALL
                    SELECT t.id, t.name, t.parent_id, t.asset_type_id
                    FROM categories t
                    JOIN recursive_cte r ON t.parent_id = r.id
                )
                SELECT id
                FROM recursive_cte;        
                '''      
        return [x[0] for x in cur.execute(query).fetchall() if x]
    
    @Connect.db
    def add_typed_category(self, conn, category_name, asset_type_name, parent_category = None):
        cur = conn.cursor()
        asset_type_id = cur.execute(f'SELECT id FROM asset_types WHERE name="{asset_type_name}";').fetchone()
        if not asset_type_id:
            raise Exception("You must specify a valid asset type to register a category")
            return 
         
        parent_id = None
        if parent_category:
            parent_id = self.get_category_from_tree(asset_category = parent_category,asset_type_name= asset_type_name)
            if not parent_id:
                raise Exception("Specify a valid parent Category")
                return
            #parent_id = parent_id[0]       
        query = f'''
                INSERT INTO categories 
                (name, parent_id, asset_type_id)
                VALUES
                ("{category_name}", "{parent_id}", "{asset_type_id[0]}")
                ON CONFLICT(name, parent_id, asset_type_id) 
                DO NOTHING
                ;
        '''
        cur.execute(query)
    
    @Connect.db
    def add_asset(self, conn, asset_name, asset_type, asset_category):
        cur = conn.cursor()
        asset_type_id = cur.execute(f'SELECT id FROM asset_types WHERE name="{asset_type}";').fetchone()[0]
        if not asset_type_id:
            raise Exception("You must specify a valid asset type to register an asset")
            return
        asset_category_id = self.get_category_from_tree(asset_category= asset_category, asset_type_name= asset_type)      
        if not asset_category_id:
            raise Exception("You must specify a valid asset category to register an asset")
            return            
        now = datetime.datetime.now()
        current_date = now.strftime("%Y/%m/%d, %H:%M:%S")
        
        query = f'''
                INSERT INTO assets 
                (name, asset_type_id, asset_category_id, modification_date)
                VALUES
                ("{asset_name}", "{asset_type_id}", "{asset_category_id}", "{current_date}")
                ON CONFLICT(name, asset_type_id) 
                DO UPDATE
                SET modification_date = "{current_date}";
        '''
        cur.execute(query)

    @Connect.db
    def add_geometry(self, conn, asset_name, **kwargs):

        '''obj_file="", usd_geo_file="", abc_file="", fbx_file="", source_file="", substance_file="", mesh_data=""'''
        self.update_date(asset_name=asset_name)
        for col in kwargs:
            value = kwargs.get(col)
            # get mesh data
            if isinstance(value, dict):
                old_data = self.get_geometry(asset_name=asset_name, mesh_data="")
                if not old_data:
                    old_data = {}

                old_data = old_data.get("mesh_data", {})
                if not old_data:
                    old_data = {}

                new_data_dict = dict(merge_dicts(old_data, kwargs.get(col)))
                value = json.dumps(new_data_dict)   

            cur = conn.cursor()
            query = f'''
                    INSERT INTO geometry 
                    (asset_id, {col})
                    VALUES
                    ((SELECT id from assets WHERE name='{asset_name}'), '{value}')
                    ON CONFLICT(asset_id) 
                    DO UPDATE
                    SET {col} = '{value}';

            '''
            cur.execute(query)

    @Connect.db
    def get_geometry(self, conn, asset_name, **kwargs):

        cols = ", ".join(kwargs.keys())
        cur = conn.cursor()
        query = f'''
                SELECT {cols} FROM geometry 
                WHERE
                asset_id = (SELECT id from assets WHERE name="{asset_name}")
        '''
        cur.execute(query)
        data = cur.fetchall()
        if not data:
            return {}

        data = data[0]

        returned_dict = dict(zip(kwargs.keys(), data))
        if returned_dict.get('mesh_data'):
            returned_dict['mesh_data'] = json.loads(returned_dict['mesh_data'])
        return returned_dict

    @Connect.db
    def add_tag(self, conn, asset_name, tag_name):
        cur = conn.cursor()
        tag_id = cur.execute(f'SELECT id FROM tags WHERE name="{tag_name}";').fetchone()
        if tag_id:
            tag_id = tag_id[0]
        else:
            cur.execute(f'INSERT INTO tags (name) VALUES ("{tag_name}");')
            tag_id = cur.lastrowid

        cur.execute(f'''SELECT asset_id, tag_id FROM asset_tags
                        WHERE 
                        asset_id = (SELECT id FROM assets WHERE name = "{asset_name}")
                        AND
                        tag_id = {tag_id}''')

        if not cur.fetchall():
            query = f'''
                    INSERT INTO asset_tags (asset_id, tag_id) 
                    VALUES 
                    ((SELECT id from assets WHERE name="{asset_name}"), {tag_id});
            '''
            cur.execute(query)

    @Connect.db
    def add_project(self, conn, asset_name, project_name):
        cur = conn.cursor()
        project_id = cur.execute(f'SELECT id FROM projects WHERE name="{project_name}";').fetchone()
        if project_id:
            project_id = project_id[0]
        else:
            cur.execute(f'INSERT INTO projects (name) VALUES ("{project_name}");')
            project_id = cur.lastrowid

        cur.execute(f'''SELECT asset_id, project_id FROM asset_projects
                        WHERE 
                        asset_id = (SELECT id FROM assets WHERE name = "{asset_name}")
                        AND
                        project_id = {project_id}''')

        if not cur.fetchall():
            query = f'''
                    INSERT INTO asset_projects (asset_id, project_id) 
                    VALUES 
                    ((SELECT id from assets WHERE name="{asset_name}"), {project_id});
            '''
            cur.execute(query)

    @Connect.db
    def add_textures(self, conn, asset_name, map_type_name, texture_path, udim_num, material_name="", resolution=""):
        cur = conn.cursor()
        result = cur.execute(f'''SELECT texture_path FROM textures
                            WHERE
                            asset_id = (SELECT id from assets WHERE name="{asset_name}")
                            AND 
                            map_id = (SELECT id from map_type WHERE name="{map_type_name}")
                            AND
                            material_name = "{material_name}"
                            ''')

        old_tex_path = result.fetchone()

        if not old_tex_path:
            query = f'''
                    INSERT INTO textures (asset_id, map_id, texture_path, udim_num, material_name, res)
                    VALUES
                    (
                    (SELECT id from assets WHERE name="{asset_name}"),
                    (SELECT id from map_type WHERE name="{map_type_name}"),
                    "{texture_path}",
                    {udim_num},
                    "{material_name}",
                    "{resolution}")
                    ;
            '''
        else:
            query = f'''
                    UPDATE textures
                    SET
                    texture_path = "{texture_path}",
                    udim_num = {udim_num},
                    res = "{resolution}"
                    WHERE
                    asset_id = (SELECT id from assets WHERE name="{asset_name}")
                    AND
                    map_id = (SELECT id from map_type WHERE name="{map_type_name}")
                    AND
                    material_name = "{material_name}"
                    ;
            '''

        cur.execute(query)

    @Connect.db
    def get_textures(self, conn, uuid):

        materials = {}

        cur = conn.cursor()

        query = f'''
                        SELECT material_name FROM 
                        assets 
                        LEFT JOIN textures ON assets.id=textures.asset_id
                        WHERE
                        assets.uuid = '{uuid}'
                        GROUP BY textures.material_name
                '''
        cur.execute(query)

        for material_name in cur.fetchall():
            if not material_name:
                continue
            material_name = material_name[0]
            materials[material_name] = {}
            query = f'''
                            SELECT textures.texture_path, textures.udim_num, textures.res, map_type.name, map_type.type  FROM 
                            textures 
                            LEFT JOIN map_type ON textures.map_id=map_type.id
                            WHERE
                            textures.material_name = '{material_name}'
                    '''
            cur.execute(query)
            textures = cur.fetchall()
            for row in textures:
                texture_path, udim_num, res, name, type = row
                materials[material_name][name] = {}
                materials[material_name][name]["type"] = type
                materials[material_name][name]["texture_path"] = texture_path
                materials[material_name][name]["udim_num"] = udim_num
                materials[material_name][name]["res"] = res

        return materials

    @Connect.db
    def get_assets_data(self, conn, asset_type_name=None, asset_category=None, recursive_category = True):
        cur = conn.cursor()
        asset_type_text = ""
        if asset_type_name:
            asset_type_text = f'WHERE asset_type_id = (SELECT id from asset_types WHERE name="{asset_type_name}")'
        if asset_category:
            if not recursive_category:
                asset_category_id = self.get_category_from_tree(asset_category=asset_category,asset_type_name= asset_type_name)
                asset_type_text += f' AND asset_category_id = "{asset_category_id}"'
            else:
                asset_category_id_list = self.get_all_children_categories(asset_category=asset_category,asset_type_name=asset_type_name)
                asset_category_id_list = ",".join([str(x) for x in asset_category_id_list])
                asset_type_text += f' AND asset_category_id IN ({asset_category_id_list});'
        query = f'''
                SELECT a.id, a.name, at.name AS asset_type, a.asset_category_id, a.creation_date, a.modification_date, a.uuid, g.*
                FROM assets a
                INNER JOIN asset_types at ON a.asset_type_id = at.id
                LEFT JOIN geometry g ON a.id = g.asset_id
                {asset_type_text}
        '''
        cur.execute(query)
        data = cur.fetchall()

        return data

    @Connect.db
    def get_asset(self, conn, uuid):

        asset = {}
        asset_name = self.get_asset_name(uuid=uuid)
        geometries = self.get_geometry(asset_name=asset_name, obj_file='', usd_geo_file='', abc_file='', fbx_file='')
        asset_data = json.loads(self.get_geometry(asset_name=asset_name, mesh_data='')['mesh_data'])
        materials = self.get_textures(uuid=uuid)

        asset["name"] = asset_name
        asset["geo_paths"] = geometries
        asset["asset_data"] = asset_data
        asset["materials"] = materials

        return asset

    @Connect.db
    def get_tags(self, conn, asset_name):

        cur = conn.cursor()
        query = f'''
                SELECT name FROM tags
                WHERE
                id IN (
                    SELECT tag_id FROM 
                    asset_tags 
                    WHERE 
                    asset_id = (SELECT id from assets WHERE name="{asset_name}")
                )

        '''
        cur.execute(query)
        tags = cur.fetchall()

        return [x[0] for x in tags if x[0]]

    @Connect.db
    def get_projects(self, conn, asset_name):

        cur = conn.cursor()
        query = f'''
                SELECT name FROM projects
                WHERE
                id IN (
                    SELECT project_id FROM 
                    asset_projects 
                    WHERE 
                    asset_id = (SELECT id from assets WHERE name="{asset_name}")
                )

        '''
        cur.execute(query)
        projects = cur.fetchall()

        return [x[0] for x in projects if x[0]]

    @Connect.db
    def all_asset_types(self, conn):

        cur = conn.cursor()
        query = f'''
                SELECT name,id FROM asset_types
                ORDER BY 
                name
        '''
        cur.execute(query)
        tags = cur.fetchall()

        return tags#[x[0] for x in tags if x[0]]
    
    @Connect.db
    def all_tags(self, conn):

        cur = conn.cursor()
        query = f'''
                SELECT name FROM tags
                ORDER BY 
                name
        '''
        cur.execute(query)
        tags = cur.fetchall()

        return [x[0] for x in tags if x[0]]
    
    @Connect.db
    def all_categories(self, conn, asset_type=None):
        cur = conn.cursor()
        if asset_type== None:
            query = f'''
                    SELECT id, name, parent_id, asset_type_id FROM categories
                    ORDER BY 
                    id
            '''
        else:
            query = f'''
                    SELECT id, name, parent_id, asset_type_id FROM categories
                    WHERE 
                    asset_type_id=(SELECT id from asset_types WHERE name="{asset_type}")
                    ORDER BY 
                    id            
            '''
        cur.execute(query)
        tags = cur.fetchall()

        return tags#[x[0] for x in tags if x[0]] 

    @Connect.db
    def all_projects(self, conn):

        cur = conn.cursor()
        query = f'''
                SELECT name FROM projects
                ORDER BY 
                name
        '''
        cur.execute(query)
        projects = cur.fetchall()

        return [x[0] for x in projects if x[0]]

    def delete_asset_projects(self, asset_name=None, asset_id=None):
        if asset_id is None:
            asset_id = self.get_asset_id(asset_name=asset_name)
        self.delete_row(table_name="asset_projects", col="asset_id", value=asset_id)

    def delete_asset_tags(self, asset_name=None, asset_id=None):
        if asset_id is None:
            asset_id = self.get_asset_id(asset_name=asset_name)
        self.delete_row(table_name="asset_tags", col="asset_id", value=asset_id)

    @Connect.db
    def set_thumbnail(self, conn, asset_name=None, asset_id=None, thumb_path=""):
        if asset_id is None:
            asset_id = self.get_asset_id(asset_name=asset_name)

        if thumb_path == "":
            return
        else:
            thumb_path = unquote(thumb_path)

        cur = conn.cursor()
        query = f'''
                INSERT INTO thumbnail  
                (asset_id, thumb_path)
                VALUES
                ("{asset_id}", "{thumb_path}") 

        '''
        cur.execute(query)
        data = cur.fetchall()

        return data

    @Connect.db
    def get_thumbnail(self, conn, asset_name, latest=True):

        asset_id = self.get_asset_id(asset_name=asset_name)
        cur = conn.cursor()
        query = f'''
                SELECT thumb_path FROM 
                assets 
                LEFT JOIN thumbnail ON assets.id=thumbnail.asset_id
                WHERE assets.id={asset_id}

        '''
        cur.execute(query)
        data = cur.fetchall()
        if latest:
            return data[-1][0]
        else:
            return [x[0] for x in data]


# Main Function
def main():
    db = AssetsDB()
    
    db.add_asset_type(asset_type_name="3D Asset")
    db.add_asset_type(asset_type_name="Textures")
    db.add_asset_type(asset_type_name="Shaders")
    db.add_asset_type(asset_type_name="HDRI")
    """
    db.add_typed_category(category_name="muebles",asset_type_name="3D Asset")
    db.add_typed_category(category_name="sofas",asset_type_name="3D Asset",parent_category="muebles")
    db.add_typed_category(category_name="indor",asset_type_name="3D Asset",parent_category="muebles/sofas")
    db.add_typed_category(category_name="outdor",asset_type_name="3D Asset",parent_category="muebles/sofas")
    db.add_typed_category(category_name="mesas",asset_type_name="3D Asset",parent_category="muebles")
    db.add_typed_category(category_name="indor",asset_type_name="3D Asset",parent_category="muebles/mesas")
    db.add_typed_category(category_name="outdor",asset_type_name="3D Asset",parent_category="muebles/mesas")  
    
    db.add_asset(asset_name="sofa_exterior",asset_type="3D Asset",asset_category="muebles/sofas/outdor")
    db.add_asset(asset_name="mesa_interior",asset_type="3D Asset",asset_category="muebles/mesas/indor")
    

    #db.add_typed_category(category_name="random",asset_type_name="Textures")
    db.add_asset(asset_name="texture_test",asset_type="Textures",asset_category="random")
    """
    #print(db.get_all_children_categories(asset_category="muebles/sofas"))
    #print(db.get_tree_from_category(asset_category="muebles/sofas"))
    #print(db.get_tree_from_category(asset_category=7))
    print(db.get_assets_data())
    #for i in range(50):
    #    db.add_asset(asset_name=f"texture_new_{i}",asset_type="Textures")
    #print(db.all_asset_types())

    #data = {'foo': 'bar'}
    #db.add_geometry(asset_name="tv_table", mesh_data=data)
    # x = db.add_tag(asset_name="ABAGORA", tag_name="tag1")
    # x = db.get_assets_data()
    # print(db.get_tags(asset_name="ABAGORA"))

    # print(db.get_thumbnail(asset_name="tv_table"))
    # print(db.add_textures(asset_name="tv_table", map_type_name="_", texture_path="bar", udim_num=10, material_name="", resolution=""))
    # db.get_asset(uuid='a990d365-62f4-43ff-81bf-63422dc5cefb')


if __name__ == '__main__':
    main()
