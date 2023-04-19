#!/usr/bin/env python
"""
    Name:           scattererItemWidget.py
    Description:    Item Widget representing one scatterer
 
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
import ix

# Local Imports
from scatterertoarnold.widgets.main import base

# ______________________________________________________________________________________________________________________

class ScattererItemWidget(QWidget):
    """Scatterer Item Widget"""

    state_changed = Signal(bool)
    def __init__(self, parent, scatterer, *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent
            scatterer: Scatterer to represent
            
        """
        super(ScattererItemWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.scatterer = scatterer

        # Main Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.layout)

        self.checkbox_export = QCheckBox(parent=self)
        self.checkbox_export.setChecked(True)
        self.checkbox_export.stateChanged.connect(self.state_changed.emit)
        self.lbl_geo_count = QLabel(parent=self, text='')
        self.lbl_geo_count.setMinimumWidth(50)
        self.lbl_name = QLabel(parent=self, text='')

        self.layout.addWidget(self.checkbox_export)
        self.layout.addWidget(self.lbl_geo_count)
        self.layout.addWidget(self.lbl_name)
        self.layout.addItem(base.Spacer(h_expand=True))

        self.set_geo_count()
        self.set_name()

    def set_geo_count(self):
        """Sets the geo count label"""
        geos = self.scatterer.get_attribute('geometry')
        num_geos = geos.get_value_count() + 1
        self.lbl_geo_count.setText(f'({num_geos} geos)')

    def set_name(self):
        """Sets the name label"""
        if self.parent.show_full_name:
            name = self.scatterer.get_full_name()
        else:
            name = self.scatterer.get_name()
        
        self.lbl_name.setText(name)
    
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

# ______________________________________________________________________________________________________________________
