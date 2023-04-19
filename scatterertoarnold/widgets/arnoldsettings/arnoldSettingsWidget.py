#!/usr/bin/env python
"""
    Name:           arnoldSettingsWidget.py
    Description:    Arnold Settings Widget
 
"""
# System Imports
import os
import sys
import logging
import functools

# Third-Party Imports
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import ix

# Local Imports
from scatterertoarnold.widgets.main import base
from scatterertoarnold.lib import libclarisse
from scatterertoarnold.core import ass_generator

# ______________________________________________________________________________________________________________________

class ArnoldSettingsWidget(QWidget):
    """Arnold Settings selection widget"""

    def __init__(self, parent, *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent
            
        """
        super(ArnoldSettingsWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent

        # Attributes
        self.arnold_settings = {}

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        # Header Layout
        self.header_layout = QHBoxLayout(self)
        self.layout.addLayout(self.header_layout)
        self.title_lbl = QLabel(parent=self, text="Update any of the default arnold node's values")
        self.header_layout.addWidget(self.title_lbl)

        # SCROLL AREA
        self.scroll_layout = base.ScrollLayout(self, self.layout)
        self.build_settings_list()

        self.spacer = base.Spacer(v_expand=True)
        self.scroll_layout.addItem(self.spacer)

    # __________________________________________________________________________________________________________________
    # Handlers

    def _exitHandler(self):
        """Exit Gracefully"""
        self.save_geometry_widgets()

    # __________________________________________________________________________________________________________________
    # Widget Functionality

    def build_settings_list(self):
        """Builds the settings list"""
        self.arnold_settings = ass_generator.ASS_NODE_TYPES.copy()
        for node_type, node_dict in self.arnold_settings.items():
            gb = QGroupBox(node_type, parent=self)
            self.scroll_layout.addWidget(gb)

            layout = QGridLayout(self)
            gb.setLayout(layout)

            for key, value in node_dict.items():
                lbl = QLabel(parent=self, text=key)
                lineedit = QLineEdit(value, parent=self)
                lineedit.textChanged.connect(
                    functools.partial(
                        self._on_lineedit_textChanged, 
                        node_type=node_type, 
                        key=key
                        )
                    )
                layout.addWidget(lbl, list(node_dict.keys()).index(key), 0)
                layout.addWidget(lineedit, list(node_dict.keys()).index(key), 1)
                    
    def get_arnold_settings(self):
        """Returns the arnold settings
        
        Returns:
            dict: ass_generator.ASS_NODE_TYPES copy with user-entered values
            
        """
        return self.arnold_settings

    def _on_lineedit_textChanged(self, value, node_type, key):
        """Triggered when a lineedit has changed, update the arnold settings dict
        
        Args:
            node_type (str) Node type in the arnold_settings dict
            key (str) Key in the node_type dict
            lineedit (QLineEdit): Updated lineedit
            
        """
        self.arnold_settings[node_type][key] = value

# ______________________________________________________________________________________________________________________
