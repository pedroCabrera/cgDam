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
import ast
from collections import OrderedDict

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

CgDamROOT = os.getenv("CgDamROOT")


# ---------------------------------
# Variables


# ---------------------------------
# Start Here

class TextFiled(QWidget):
    name = 'input_text'

    def __init__(self, parent=None):
        super(TextFiled, self).__init__(parent)

        h_layout = QHBoxLayout(self)
        self.setLayout(h_layout)
        self.label = QLabel(self)
        self.label.setFixedWidth(155)
        self.label.setAlignment(Qt.AlignRight)
        self.line_edit = QLineEdit(self)

        h_layout.addWidget(self.label)
        h_layout.addWidget(self.line_edit)
        # h_layout.addItem(QSpacerItem(100, 2, QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

    def set_name(self, name):
        # name = ' '.join(str(name).split('_')).title()
        self.label.setText(name)

    def set_default_value(self, value):
        self.line_edit.setText(str(value))

    def set_value(self, value):
        self.line_edit.setText(str(value))

    def set_tooltip(self, text):
        self.setToolTip(text)

    def set_placeholder(self, text):
        self.line_edit.setPlaceholderText(text)

    def get_value(self):
        return self.line_edit.text()

    def get_name(self):
        return self.label.text()

class IntFiled(QWidget):
    name = 'input_number'

    def __init__(self, parent=None):
        super(IntFiled, self).__init__(parent)

        h_layout = QHBoxLayout(self)
        self.setLayout(h_layout)
        self.label = QLabel(self)
        self.label.setFixedWidth(155)
        self.label.setAlignment(Qt.AlignRight)

        self.spin_box = QSpinBox(self)
        self.spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_box.setMaximum(99999999)

        h_layout.addWidget(self.label)
        h_layout.addWidget(self.spin_box)
        # h_layout.addItem(QSpacerItem(100, 2, QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

    def set_name(self, name):
        # name = ' '.join(str(name).split('_')).title()
        self.label.setText(name)

    def set_default_value(self, value):
        self.spin_box.setText(value)

    def set_value(self, value):
        self.spin_box.setValue(value)

    def set_tooltip(self, text):
        self.setToolTip(text)

    def get_value(self):
        return self.spin_box.value()

    def get_name(self):
        return self.label.text()

class MultiTextFiled(QWidget):
    def __init__(self, parent=None, num=2):
        super(MultiTextFiled, self).__init__(parent)

        h_layout = QHBoxLayout(self)
        self.setLayout(h_layout)

        self.line_edits = {}
        for i in range(num):
            label = QLabel(self)
            line_edit = QLineEdit(self)
            self.line_edits[i] = {
                'label': label,
                'lineedit': line_edit
            }

            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
        # h_layout.addItem(QSpacerItem(100, 2, QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

    def set_name(self, name, num=0):
        # name = ' '.join(str(name).split('_')).title()
        self.line_edits[num]['label'].setText(name)

    def set_default_value(self, value, num=1):
        self.line_edits[num]['lineedit'].setText(value)

    def set_tooltip(self, text, num=0):
        self.line_edits[num]['lineedit'].setToolTip(text)

    def set_placeholder(self, text, num=0):
        self.line_edits[num]['lineedit'].setPlaceholderText(text)


class ToggleBox(QWidget):
    name = 'toggle_box'

    def __init__(self, parent=None):
        super(ToggleBox, self).__init__(parent)

        h_layout = QHBoxLayout(self)
        self.setLayout(h_layout)
        self.label = QLabel(self)
        self.label.setFixedWidth(155)
        self.label.setAlignment(Qt.AlignRight)
        self.check_box = QCheckBox(self)

        h_layout.addWidget(self.label)
        h_layout.addWidget(self.check_box)
        # h_layout.addItem(QSpacerItem(100, 2, QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

    def set_name(self, name):
        # name = ' '.join(str(name).split('_')).title()
        self.label.setText(name)

    def set_default_value(self, value):
        self.check_box.setChecked(bool(value))

    def set_tooltip(self, text):
        self.setToolTip(text)

    def set_value(self, value):
        self.check_box.setChecked(bool(value))

    def get_value(self):
        return self.check_box.isChecked()

    def get_name(self):
        return self.label.text()


class DropMenu(QWidget):
    name = 'drop_menu'

    def __init__(self, parent=None):
        super(DropMenu, self).__init__(parent)

        h_layout = QHBoxLayout(self)
        self.setLayout(h_layout)
        self.label = QLabel(self)
        self.label.setFixedWidth(155)
        self.label.setAlignment(Qt.AlignRight)
        self.combo_box = QComboBox(self)

        h_layout.addWidget(self.label)
        h_layout.addWidget(self.combo_box)
        h_layout.addItem(QSpacerItem(100, 2, QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

    def set_name(self, name):
        # name = ' '.join(str(name).split('_')).title()
        self.label.setText(name)

    def set_menu_items(self, item_list):
        self.combo_box.addItems(item_list)

    def set_default_value(self, value):
        self.combo_box.setCurrentText(str(value))

    def set_tooltip(self, text):
        self.setToolTip(text)

    def set_value(self, value):
        self.combo_box.setCurrentText(str(value))

    def get_value(self):
        return str(self.combo_box.currentText())

    def get_name(self):
        return self.label.text()


class TableField(QWidget):
    name = 'table_field'

    def __init__(self, parent=None):
        super(TableField, self).__init__(parent=parent)

        g_layout = QGridLayout(self)
        self.setLayout(g_layout)

        self.table = QTableWidget()
        # self.table.setAlternatingRowColors(True)
        self.table.setCornerButtonEnabled(False)
        self.table.setFrameStyle(QFrame.NoFrame)

        g_layout.addWidget(self.table)

    def set_data(self, data):
        hor_headers = []

        self.table.setRowCount(len(data))
        for r, item_data in enumerate(data):
            vert_headers = []
            hor_headers.append(item_data.get('label'))

            self.table.setColumnCount(len(item_data.get('value', {})))

            c = 0
            for col, value in item_data.get('value', {}).items():
                if isinstance(value, list):
                    value = str(json.dumps(value))
                value = str(value)
                vert_headers.append(col)
                new_item = QTableWidgetItem(value)
                new_item.setToolTip(value)
                self.table.setItem(r, c, new_item)
                c += 1

            self.table.setHorizontalHeaderLabels(vert_headers)

        self.table.setVerticalHeaderLabels(hor_headers)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        #
        # self.adjustSize()

        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # +++

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_values(self):
        values = []
        for row in range(self.table.rowCount()):
            header_label = self.table.verticalHeaderItem(row).text()
            header_name = header_label.lower().replace(' ', '_')

            value = {"name": "", "type": "", "plug": "", "inbetween": ""}
            for col, key in enumerate(value):
                it = self.table.item(row, col)
                text = it.text() if it is not None else ""
                value[key] = text
                if key == 'inbetween':
                    value[key] = ast.literal_eval(text)
            values.append({'name': header_name, 'label': header_label, 'value': value})

        return values


class TreeItemWidget(QWidget):
    def __init__(self, widgets_data, parent=None):
        super(TreeItemWidget, self).__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.widgets = {}
        self.all_widgets()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        if not widgets_data:
            return

        if isinstance(widgets_data, dict):
            widgets_data = [widgets_data]

        for item in widgets_data:
            if not isinstance(item, dict):
                continue

            widget_type = item.get("type")
            if not widget_type:
                return

            widget_class = self.widgets.get(widget_type)
            if not widget_class:
                continue

            if 'multi' in widget_type:
                widget = QWidget(self)
                h_layout = QHBoxLayout(self)
                widget.setLayout(h_layout)

                for i in range(len(item.get("label"))):
                    in_widget = self.widgets.get(widget_type)(self)
                    in_widget.set_name(item.get("label")[i])

                    in_widget.set_default_value(str(item.get("default_value")[i]))
                    in_widget.set_placeholder(str(item.get("placeholder")[i]))
                    in_widget.set_tooltip(str(item.get("tooltip")[i]))
                    h_layout.addWidget(in_widget)

            elif 'table_field' in widget_type:
                widget = self.widgets.get(widget_type)(self)
                widget.set_data(item.get('data', []))
                widget.set_name(item.get('label'))

            else:

                widget = self.widgets.get(widget_type)(self)
                widget.set_name(item.get("label"))

                if hasattr(widget, 'set_menu_items'):
                    widget.set_menu_items(item.get("menu_items"))

                # widget.set_default_value(str(item.get("default_value")))
                widget.set_value(item.get("value"))
                widget.set_tooltip(str(item.get("tooltip")))

                if hasattr(widget, 'set_placeholder'):
                    widget.set_placeholder(str(item.get("placeholder")))

            self.main_layout.addWidget(widget)

    def all_widgets(self):
        # input text
        self.widgets["input_text"] = TextFiled
        self.widgets["input_number"] = IntFiled
        self.widgets["multi_input_text"] = TextFiled
        self.widgets["table_field"] = TableField
        self.widgets["toggle_box"] = ToggleBox
        self.widgets["drop_menu"] = DropMenu


class ItemRoles():
    TapName = Qt.UserRole + 10
    SettingName = Qt.UserRole + 11
    SettingFields = Qt.UserRole + 12
    Widget = Qt.UserRole + 13


class StyledItemDelegate(QStyledItemDelegate):
    def __init__(self, _index=None, item=None, parent=None):
        super(StyledItemDelegate, self).__init__(parent)
        self._index = _index
        self.item = item

    def paint(self, painter, option, index):
        if (index == self._index):
            if isinstance(option.widget, QAbstractItemView):
                option.widget.openPersistentEditor(index)
        else:
            super(StyledItemDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if (index == self._index):
            tap_name = index.parent().data(ItemRoles.TapName)
            ui_fields = index.data(ItemRoles.SettingFields)

            editor = TreeItemWidget(ui_fields, parent=parent)
            self.item.setData(editor, ItemRoles.Widget)

            editor.installEventFilter(self)
            return editor
        return super(StyledItemDelegate, self).createEditor(parent, option, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setContentsMargins(0, 0, 0, 0)
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        s = super(StyledItemDelegate, self).sizeHint(option, index)
        s.setHeight(s.height() * 1.5)
        return s


class SettingsTree(QTreeView):
    def __init__(self, parent=None):
        super(SettingsTree, self).__init__(parent)
        self.data_model = QStandardItemModel(0, 1)
        self.header().hide()
        self.setModel(self.data_model)

    def has_childrens(self, data):
        for item in data:
            if 'children' in item:
                return True
        return False

    def populate_row(self, widgets_data, parent_item):
        widgets_item = QStandardItem()
        parent_item.appendRow([widgets_item])
        widgets_item.setData(widgets_data, ItemRoles.SettingFields)
        if widgets_data:
            widgets_item.setData(widgets_data[0].get('label'), ItemRoles.TapName)
        self.set_item_widget(parent_item, row=0)

    def populate_rows(self, data, row_item, row=None):
        if not self.has_childrens(data):
            self.populate_row(data, row_item)

        for child_data in data:
            if 'children' in child_data:
                child_item = QStandardItem()
                child_item.setText(child_data.get('label'))
                child_item.setData(child_data.get('label'), ItemRoles.TapName)
                child_item.setData(child_data, ItemRoles.SettingFields)
                if row:
                    row_item.insertRow(row, [child_item])
                else:
                    row_item.appendRow([child_item])
                self.populate_rows( child_data.get('children'), child_item)

    def add_rows(self, items_data):
        for row_data in items_data:
            row_item = QStandardItem()
            label = row_data.get('label')
            row_item.setText(label)
            row_item.setData(row_data.get('name'), ItemRoles.TapName)
            row_item.setData(row_data, ItemRoles.SettingFields)
            children_data = row_data.get('children', [])
            self.populate_rows(children_data, row_item)
            self.data_model.appendRow(row_item)
            self.set_item_widget(row_item, row=0)

    def set_item_widget(self, item, row=0):
        index = self.data_model.index(row, 0, self.data_model.indexFromItem(item))
        self.setItemDelegate(StyledItemDelegate(_index=index, item=item))
        self.openPersistentEditor(index)
