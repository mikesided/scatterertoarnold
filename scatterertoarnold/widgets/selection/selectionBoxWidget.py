#!/usr/bin/env python
"""
    Name:           selectionBoxWidget.py
    Description:    Selection Box Widget
 
"""
# System Imports
import os
import sys
import logging

# Local Imports
from scatterertoarnold.widgets.main import base
from scatterertoarnold.lib import libclarisse

# Third-Party Imports
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import ix

# ______________________________________________________________________________________________________________________
SUPPORTED_TYPES = ['GeometryPolybox', 'GeometryVolumeBox', 'GeometryBox']

class SelectionBoxWidget(QWidget):
    """Geometry selection widget"""

    def __init__(self, parent, *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent
            
        """
        super(SelectionBoxWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent

        # Attributes
        self._items = []

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel(parent=self, text='Add Cube geos to "select" scatterer points'))

        # Header Layout
        self.header_layout = QHBoxLayout(self)
        self.layout.addLayout(self.header_layout)

        self.btn_add = QPushButton(parent=self, text='Add From Clarisse Selection')
        self.btn_add.clicked.connect(self._on_btn_add_clicked)
        self.btn_remove = QPushButton(parent=self, text='Remove Selected')
        self.btn_remove.clicked.connect(self._on_btn_remove_clicked)

        self.header_layout.addWidget(self.btn_add)
        self.header_layout.addWidget(self.btn_remove)

        self.selection_list_widget = QListWidget(self)
        self.selection_list_widget.setSelectionMode(QAbstractItemView.MultiSelection)

        # SCROLL AREA
        self.scroll_layout = base.ScrollLayout(self, self.layout)
        self.scroll_layout.addWidget(self.selection_list_widget)

    # __________________________________________________________________________________________________________________
    # Handlers

    def _on_btn_add_clicked(self):
        """Adds the selected geometries in clarisse to the listwidget"""
        selected_items = libclarisse.get_selected_objects()
        for item in selected_items:
            item_name = item.get_full_name()
            item_type = item.get_type()
            if item_type in SUPPORTED_TYPES:
                if not item in self._items:
                    itemN = QListWidgetItem()
                    itemN.setText(item_name)
                    itemN.setData(Qt.UserRole, item)
                    self.selection_list_widget.addItem(itemN)
                    self._items.append(item)
        
        self.selection_list_widget.sortItems(order=Qt.AscendingOrder)
        self.get_selection_boxes()

    def _on_btn_remove_clicked(self):
        """Remove the selected items in the listwidget"""
        for item in reversed(self.selection_list_widget.selectedItems()):
            data = item.data(Qt.UserRole)
            self._items.remove(data)
            index = self.selection_list_widget.indexFromItem(item)
            self.selection_list_widget.takeItem(index.row())

    def get_selection_boxes(self):
        """Returns the geometries selected by the user
        
        Returns:
            list: Geometries
            
        """
        geometries = []
        for i in range(self.selection_list_widget.count()):
            itemN = self.selection_list_widget.item(i)
            data = itemN.data(Qt.UserRole)
            geometries.append(data)

        return geometries

# ______________________________________________________________________________________________________________________
