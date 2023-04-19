#!/usr/bin/env python
"""
    Name:           geometryItemWidget.py
    Description:    Item Widget representing one geometry
 
"""
# System Imports
import os
import sys
import logging

# Third-Party Imports
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import qtawesome
import ix

# Local Imports
from scatterertoarnold.widgets.main import base
from scatterertoarnold.lib import libclarisse
from scatterertoarnold.configs import config

# ______________________________________________________________________________________________________________________

class GeometryItemWidget(QWidget):
    """Scatterer Item Widget"""

    def __init__(self, parent, geometry, instances, *args, **kwargs):
        """Constructor
        
        Args:
            parent: parent
            geometry (str): Geometry object
            instances (int): Number of times used in the selected scatterers
            
        """
        super(GeometryItemWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.geometry = geometry
        self.instances = instances

        # Main Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.layout)

        self.checkbox_export = QCheckBox(parent=self)
        self.checkbox_export.setChecked(True)
        self.lbl_geo_count = QLabel(parent=self, text='')
        self.lbl_geo_count.setMinimumWidth(25)
        self.lbl_name = QLabel(parent=self, text='')
        self.le_ass_file_path = QLineEdit(parent=self, placeholderText='Choose .ass file..')
        browse_dir_icon = qtawesome.icon('fa5s.folder-open', color='#5d7396')
        self.btn_browse_file = QPushButton(icon=browse_dir_icon, parent=self)
        self.btn_browse_file.setFixedSize(16, 16)
        self.btn_browse_file.setStyleSheet('background-color: transparent;')
        self.btn_browse_file.clicked.connect(self._browse_ass_file)

        self.layout.addWidget(self.checkbox_export)
        self.layout.addWidget(self.lbl_geo_count)
        self.layout.addWidget(self.lbl_name)
        self.layout.addItem(base.Spacer(w=20))
        self.layout.addWidget(self.le_ass_file_path)
        self.layout.addWidget(self.btn_browse_file)

        self.set_geo_count()
        self.set_name()
        self.set_default_ass_file()

    def _browse_ass_file(self):
        """Opens a file browse to select an ass file."""
        init_path = self.le_ass_file_path.text() or ix.application.get_current_project_filename()
        filepath, ext = QFileDialog.getOpenFileName(self, 'Select .ass file for geometry {}'.format(self.geometry.get_name()), init_path, 'Arnold Scene Source (*.ass)')

        if filepath:
            self.le_ass_file_path.setText(filepath)

    def set_geo_count(self):
        """Sets the geo count label"""
        self.lbl_geo_count.setText(f'({self.instances} points)')

    def set_name(self):
        """Sets the name label"""
        if self.parent.show_full_name:
            name = self.geometry.get_full_name()
        else:
            name = self.geometry.get_name()
        
        self.lbl_name.setText(name)

    def set_default_ass_file(self):
        """Sets the default ass file path based on the geo's attribute"""
        attr_value = libclarisse.get_str_attribute(item=self.geometry, attr_name=config.ATTR_ASS_FILE)
        if attr_value is not None:
            self.le_ass_file_path.setText(attr_value)
    
    def set_checked(self, value):
        """Sets the scatterer to be exported or not
        
        Args:
            value (bool): Checked?
            
        """
        self.checkbox_export.setChecked(value)

    def is_checked(self):
        """Returns wether the checkbox is checked or not
        
        Returns:
            bool: Checked?
            
        """
        return self.checkbox_export.isChecked()

    def save_ass_file_path(self):
        """Saves the ass file path to the geometry's custom attributes"""
        attr_exists = bool(libclarisse.get_str_attribute(item=self.geometry, attr_name=config.ATTR_ASS_FILE))
        filepath = self.le_ass_file_path.text()
        if filepath:
            if not attr_exists:
                libclarisse.create_custom_attribute(
                    item=self.geometry, 
                    attr_type=ix.api.OfAttr.TYPE_FILE, 
                    attr_name=config.ATTR_ASS_FILE)
        
        if (not filepath and attr_exists) or filepath:
            attr = libclarisse.get_attribute_object(item=self.geometry, attr_name=config.ATTR_ASS_FILE)
            libclarisse.set_str_attribute(attr=attr, value=filepath)
             
# ______________________________________________________________________________________________________________________
