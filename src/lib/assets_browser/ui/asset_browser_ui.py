# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_browser_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import os
import sys

CgDamROOT = os.getenv("CgDamROOT")
sysPaths = [CgDamROOT, f"{CgDamROOT}/src"]
for sysPath in sysPaths:
    if sysPath not in sys.path:
        sys.path.append(sysPath)
        
from lib.assets_browser.ui.promoted_widgets import ListView


class Ui_AssetBrowserWindow(object):
    def setupUi(self, AssetBrowserWindow):
        AssetBrowserWindow.resize(1204, 644)
        self.centralwidget = QSplitter(AssetBrowserWindow)
        self.layoutWidget = QWidget(self.centralwidget)

        self.splitter_main = QSplitter(self.layoutWidget)
        self.splitter_main.setLineWidth(3)
        self.splitter_main.setOpaqueResize(True)
        self.splitter_main.setHandleWidth(7)

        self.vertical_main_layout = QVBoxLayout(self.layoutWidget)
        self.vertical_main_layout.setSpacing(6)
        self.horizontal_filter_layout = QHBoxLayout()
        self.horizontal_filter_layout.setSpacing(6)

        self.verticlal_widget_categories = QWidget()
        self.verticla_layout_categories = QVBoxLayout(self.verticlal_widget_categories)
        self.verticla_layout_categories.setSpacing(6)
        self.asset_type_selector = QComboBox()
        self.asset_type_selector.setMinimumWidth(150)
        self.verticla_layout_categories.addWidget(self.asset_type_selector)
        self.splitter_main.addWidget(self.verticlal_widget_categories)


        spacerItem = QSpacerItem(50, 2, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        self.horizontal_filter_layout.addItem(spacerItem)
        self.pushButton_sortItems = QPushButton(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_sortItems.sizePolicy().hasHeightForWidth())
        self.pushButton_sortItems.setSizePolicy(sizePolicy)
        self.pushButton_sortItems.setMinimumSize(QSize(0, 20))
        self.pushButton_sortItems.setMaximumSize(QSize(40, 25))
        self.pushButton_sortItems.setStyleSheet("background-color:none;\n"
"                       border:none;\n"
"                       padding: 2px 2px 2px 2px;\n"
"                   ")
        self.pushButton_sortItems.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/ui/icon/images/sort.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_sortItems.setIcon(icon)
        self.horizontal_filter_layout.addWidget(self.pushButton_sortItems)
        self.pushButton_refreshView = QPushButton(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_refreshView.sizePolicy().hasHeightForWidth())
        self.pushButton_refreshView.setSizePolicy(sizePolicy)
        self.pushButton_refreshView.setMinimumSize(QSize(0, 20))
        self.pushButton_refreshView.setMaximumSize(QSize(40, 25))
        self.pushButton_refreshView.setStyleSheet("background-color:none;\n"
"                             border:none;\n"
"                             padding: 2px 2px 2px 2px;\n"
"                         ")
        self.pushButton_refreshView.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/reload.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_refreshView.setIcon(icon1)
        self.pushButton_refreshView.setIconSize(QSize(20, 20))
        self.horizontal_filter_layout.addWidget(self.pushButton_refreshView)
        self.pushButton_filterItems = QPushButton(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_filterItems.sizePolicy().hasHeightForWidth())
        self.pushButton_filterItems.setSizePolicy(sizePolicy)
        self.pushButton_filterItems.setMinimumSize(QSize(0, 25))
        self.pushButton_filterItems.setMaximumSize(QSize(40, 25))
        self.pushButton_filterItems.setStyleSheet("background-color:none;\n"
"                       border:none;\n"
"                       padding: 2px 2px 2px 2px;\n"
"                   ")
        self.pushButton_filterItems.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/icons/filter.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_filterItems.setIcon(icon2)
        self.horizontal_filter_layout.addWidget(self.pushButton_filterItems)
        self.le_search = QLineEdit(self.layoutWidget)
        self.le_search.setMinimumSize(QSize(150, 0))
        self.le_search.setMaximumSize(QSize(170, 16777215))
        self.le_search.setStyleSheet("")
        self.horizontal_filter_layout.addWidget(self.le_search)
        

        
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.verticla_layout_categories.addWidget(self.treeView)
                
        self.lw_assets = ListView(self.splitter_main)
        self.lw_assets.setMinimumSize(QSize(300, 0))
        #self.verticla_layout_categories.addWidget(self.lw_assets)

        self.splitter_main.setStretchFactor(0, 2)
        self.splitter_main.setStretchFactor(1, 8)        
        

        self.horizontal_scale_Layout = QHBoxLayout()
        self.horizontal_scale_Layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontal_scale_Layout.setSpacing(0)
        self.asset_num = QLabel(self.layoutWidget)
        self.horizontal_scale_Layout.addWidget(self.asset_num)
        spacerItem1 = QSpacerItem(120, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontal_scale_Layout.addItem(spacerItem1)
        self.horizontalSlider = QSlider(self.layoutWidget)
        self.horizontalSlider.setMaximumSize(QSize(150, 16777215))
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.horizontal_scale_Layout.addWidget(self.horizontalSlider)

        self.vertical_main_layout.addLayout(self.horizontal_filter_layout)
        self.vertical_main_layout.addWidget(self.splitter_main)
        self.vertical_main_layout.addLayout(self.horizontal_scale_Layout)

        self.splitter_vertical = QSplitter(self.centralwidget)
        self.splitter_vertical.setLineWidth(3)
        self.splitter_vertical.setOrientation(Qt.Orientation.Vertical)
        self.splitter_vertical.setOpaqueResize(True)
        self.splitter_vertical.setHandleWidth(7)

        self.layoutWidget_3 = QWidget(self.splitter_vertical)
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget_3)
        self.tabWidget_2 = QTabWidget(self.layoutWidget_3)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setMinimumSize(QSize(265, 265))
        self.tab_2 = QWidget()
        self.gridLayout_6 = QGridLayout(self.tab_2)
        self.verticalLayout_7 = QVBoxLayout()
        self.frame_3d = QFrame(self.tab_2)
        self.frame_3d.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3d.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3d)
        self.verticalLayout_7.addWidget(self.frame_3d)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.verticalLayout_7.addItem(spacerItem2)
        self.gridLayout_6.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setMaximumSize(QSize(1000, 1000))
        self.gridLayout_5 = QGridLayout(self.tab_3)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_11 = QVBoxLayout()
        self.horizontalLayout_4 = QHBoxLayout()
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.label_preview0 = QLabel(self.tab_3)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_preview0.sizePolicy().hasHeightForWidth())
        self.label_preview0.setSizePolicy(sizePolicy)
        self.label_preview0.setMinimumSize(QSize(128, 128))
        self.label_preview0.setMaximumSize(QSize(512, 512))
        self.label_preview0.setText("")
        self.horizontalLayout_4.addWidget(self.label_preview0)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_11.addLayout(self.horizontalLayout_4)
        self.verticalLayout_10.addLayout(self.verticalLayout_11)
        self.horizontalLayout_6 = QHBoxLayout()
        self.verticalLayout_10.addLayout(self.horizontalLayout_6)
        self.verticalLayout_8.addLayout(self.verticalLayout_10)
        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.verticalLayout_8.addItem(spacerItem5)
        self.gridLayout_5.addLayout(self.verticalLayout_8, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.verticalLayout_5.addWidget(self.tabWidget_2)
        self.gridLayoutWidget = QWidget(self.splitter_vertical)
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.table_data = QTreeWidget(self.gridLayoutWidget)
        self.table_data.headerItem().setText(0, "1")
        self.gridLayout_2.addWidget(self.table_data, 0, 0, 1, 1)
        AssetBrowserWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(AssetBrowserWindow)
        self.menubar.setGeometry(QRect(0, 0, 1204, 22))
        AssetBrowserWindow.setMenuBar(self.menubar)

        self.retranslateUi(AssetBrowserWindow)
        self.tabWidget_2.setCurrentIndex(1)
        QMetaObject.connectSlotsByName(AssetBrowserWindow)

    def retranslateUi(self, AssetBrowserWindow):
        _translate = QCoreApplication.translate
        AssetBrowserWindow.setWindowTitle(_translate("AssetBrowserWindow", "MainWindow"))
        self.pushButton_sortItems.setToolTip(_translate("AssetBrowserWindow", "Sort Items"))
        self.pushButton_refreshView.setToolTip(_translate("AssetBrowserWindow", "Sort Items"))
        self.pushButton_filterItems.setToolTip(_translate("AssetBrowserWindow", "Filter Items"))
        self.le_search.setToolTip(_translate("AssetBrowserWindow", "Search Items"))
        self.le_search.setPlaceholderText(_translate("AssetBrowserWindow", "Search"))
        self.asset_num.setText(_translate("AssetBrowserWindow", "0 Asset"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("AssetBrowserWindow", "3D"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("AssetBrowserWindow", "Image"))



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    AssetBrowserWindow = QMainWindow()
    ui = Ui_AssetBrowserWindow()
    ui.setupUi(AssetBrowserWindow)
    AssetBrowserWindow.show()
    sys.exit(app.exec_())
