#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Documentation:
"""

# ---------------------------------
# Import Libraries
import os
import re
import sys
import json
from collections import OrderedDict
import copy

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

CgDamROOT = os.getenv("CgDamROOT")
sysPaths = [CgDamROOT, f"{CgDamROOT}/src"]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)

#from utils.assets_db import AssetsDB
from utils.file_manager import FileManager
from utils.dialogs import message
from settings.widgets import *
from settings.settings import *

from utils.resources.stylesheet import get_stylesheet
from utils.resources.style_rc import *

# ---------------------------------
# Variables
#db = AssetsDB()
fm = FileManager()

user_settings = fm.user_documents.joinpath('settings')
user_settings.mkdir(parents=True, exist_ok=True)


# ---------------------------------
# Start Here
class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.init_win()
        self.color()

        self.connect_events()

        # self.setting_tree.expandAll()

    def connect_events(self):

        self.save_btn.clicked.connect(self.on_save)

        self.setting_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setting_tree.customContextMenuRequested.connect(self.on_right_click)

        self.mousePressEvent = self.showEvent

    def init_win(self):
        title = "cgDam Settings"

        Size_object = QGuiApplication.primaryScreen().availableGeometry()
        screen_height = Size_object.height()
        screen_width = Size_object.width()

        self.setWindowIcon(QIcon(":icons/settings.png"))
        self.setWindowTitle(title)
        self.setMinimumSize(screen_width * 0.45, screen_height * 0.5)

        self.setStyleSheet(get_stylesheet())

        # Update table
        ui_data = json.loads(json.dumps(get_settings_data()),object_pairs_hook=OrderedDict)
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)

        self.main_layout = QVBoxLayout()
        self.cw.setLayout(self.main_layout)

        # tree widget
        self.setting_tree = SettingsTree()
        self.setting_tree.add_rows(ui_data)

        # buttons
        l_btn = QHBoxLayout(self.cw)
        self.save_btn = QPushButton("Save")

        l_btn.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        l_btn.addWidget(self.save_btn)

        self.main_layout.addWidget(self.setting_tree)
        self.main_layout.addLayout(l_btn)

    def color(self):
        darkPalette = QPalette()
        color = QColor(45, 45, 45)
        display_color = QColor(127, 127, 127)
        darkPalette.setColor(QPalette.Window, color)

        self.setPalette(darkPalette)

    def on_right_click(self, point):

        index = self.setting_tree.indexAt(point)

        if not index.isValid():
            return

        # We build the menu.
        menu = QMenu(self)
        print_action = menu.addAction("Print Data")
        print_action.triggered.connect(lambda: self.on_print_data(index))

        menu.exec_(self.setting_tree.mapToGlobal(point))

    def on_print_data(self, index):

        item = self.setting_tree.data_model.itemFromIndex(index)
        item_data = index.data(ItemRoles.SettingFields)
        parent_data = index.parent().data(ItemRoles.SettingFields)

        print('item data : ', json.dumps(item_data,indent=4))
        print('parent data : ', json.dumps(parent_data,indent=4))

    def on_save(self):

        all_data = []
        self.parent_data = None

        root = self.setting_tree.data_model.invisibleRootItem()
        self.iterItems(root)

        for row in range(root.rowCount()):
            row_item = root.child(row, 0)
            name, row_data = row_item.data(ItemRoles.TapName), row_item.data(ItemRoles.SettingFields)
            #self.subscribe_data_with_variable(row_data)
            all_data.append(row_data)
        print(json.dumps(all_data,indent=4))
        save_encoded_cfg_data(all_data,path=user_settings)
        #fm.write_json(user_settings.joinpath(f'settings.json'), OrderedDict([('items', all_data)]))

    def subscribe_data_with_variable(self, data):
        # TO replace the dictionary with its file name

        if "$" in data:
            file_name = data.split('$')[-1]
            cfg_path_rel = f"src/settings/cfg/{file_name}.json"
            cfg_path = os.path.join(CgDamROOT, cfg_path_rel)

            if os.path.isfile(cfg_path):
                ...
            cfg_path = os.path.abspath(cfg_path).replace('\\', '/')
            with open(cfg_path) as f:
                data = json.load(f, object_pairs_hook=OrderedDict)
                data['reference'] = {'$' + file_name: f'$CgDamROOT/{cfg_path_rel}'}

        children = data.get('children', [])
        for i, child_data in enumerate(children):
            if 'reference' in child_data:
                reference_dict = child_data['reference']
                key = list(reference_dict.keys())[0]
                children[i] = f'${key}'
            else:
                #print(child_data)
                self.subscribe_data_with_variable(child_data)

    def get_data(self, item):

        widget = item.parent().data(ItemRoles.Widget)
        parent_data = item.parent().data(ItemRoles.SettingFields)
        data_list = item.data(ItemRoles.SettingFields)

        tap_name = item.parent().text()

        parent_data['name'] = tap_name.lower().strip().replace(' ', '_')
        parent_data['label'] = tap_name

        # add condition of tap name
        for child in widget.children():
            if isinstance(child, QVBoxLayout):
                continue

            if isinstance(child, TableField):
                label = child.get_name()
                values = child.get_values()
                for child_dict in data_list:
                    if child_dict.get('label') == label:
                        child_dict["data"] = values

            else:
                label = child.get_name()
                value = child.get_value()

                for child_dict in data_list:
                    if child_dict.get('label') == label:
                        child_dict['value'] = value

        # reference json
        #if 'path' in parent_data:
        #    ref_name = f'{parent_data.get("path")}/{parent_data.get("name")}'
        #    parent_data['reference'] = {
        #        f'{ref_name}': f'$CgDamROOT/src/settings/cfg/{ref_name}.json'
        #    }
        #    #fm.write_json(user_settings.joinpath(f'{ref_name}.json'), parent_data)

        item.parent().setData(parent_data, ItemRoles.SettingFields)

    def iterItems(self, root):
        if root is not None:
            for row in range(root.rowCount()):
                row_item = root.child(row, 0)
                if row_item.hasChildren():
                    self.iterItems(row_item)
                else:
                    self.get_data(row_item)

    def showEvent(self, event):
        self.show

    def closeEvent(self, event):
        self.destroy()

    def mousePressEvent(self, event):
        pass


# Main Function
def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    win = SettingsWindow()
    print(win)
    win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
