#!/usr/bin/env python
"""
    Name:           geometryWidget.py
    Description:    Geometry Widget
 
"""
# System Imports
import os
import sys

# Third-Party Imports
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import ix

# Local Imports
from scatterertoarnold.widgets.main import base
from scatterertoarnold.widgets.geometry import geometryItemWidget
from scatterertoarnold.lib import libclarisse

# ______________________________________________________________________________________________________________________

class GeometryWidget(QWidget):
    """Geometry selection widget"""

    def __init__(self, parent, scatterers=[], *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent
            scatterers (list): List of scatterers to init with
            
        """
        super(GeometryWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self._scatterers = scatterers

        # Attributes
        self._geometries = []
        self.geometry_widgets = []
        self.show_full_name = False

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        # Header Layout
        self.header_layout = QHBoxLayout(self)
        self.layout.addLayout(self.header_layout)

        self.btn_select_all = QPushButton(parent=self, text='Select All')
        self.btn_select_all.clicked.connect(self._on_btn_select_all_clicked)
        self.btn_unselect_all = QPushButton(parent=self, text='Unselect All')
        self.btn_unselect_all.clicked.connect(self._on_btn_unselect_all_clicked)
        self.cb_show_full_name = QComboBox(parent=self)
        self.cb_show_full_name.addItems(['Show Name', 'Show Path'])
        self.cb_show_full_name.currentIndexChanged.connect(self._on_cb_show_full_name_changed)
        self.btn_reload = QPushButton(parent=self, text='Reload Geometries')
        self.btn_reload.clicked.connect(self.load_geometries)

        self.header_layout.addWidget(self.btn_select_all)
        self.header_layout.addWidget(self.btn_unselect_all)
        self.header_layout.addItem(base.Spacer(h_expand=True))
        self.header_layout.addWidget(self.cb_show_full_name)
        self.header_layout.addWidget(self.btn_reload)

        # SCROLL AREA
        self.scroll_layout = base.ScrollLayout(self, self.layout)

        self.spacer = base.Spacer(v_expand=True)
        self.load_geometries()

    # __________________________________________________________________________________________________________________
    # Handlers


    def _exitHandler(self):
        """Exit Gracefully"""
        self.save_geometry_widgets()
    
    def _on_about_to_export(self):
        """Triggered when the user clicked the export button in the options panel"""
        self.save_geometry_widgets()

    def _on_btn_select_all_clicked(self):
        """Select all geometries"""
        for widget in self.geometry_widgets:
            widget.set_checked(True)

    def _on_btn_unselect_all_clicked(self):
        """Unselect all geometries"""
        for widget in self.geometry_widgets:
            widget.set_checked(False)

    def _on_cb_show_full_name_changed(self, index):
        """Sets Sets the show_full_name based on the selection"""
        self.show_full_name = bool(index)
        for widget in self.geometry_widgets:
            widget.set_name()

    # __________________________________________________________________________________________________________________
    # Widget Functionality

    def load_geometries(self, scatterers=None):
        """Loads the geometries from the given scatterers
        
        Args:
            scatterers (list): If specified, load these scatterers, else use the widget's cache
            
        """
        if isinstance(scatterers, list):
            self._scatterers = scatterers
            
        # Reset Widget
        self.geometry_widgets = []
        base.empty_item(self.scroll_layout)
        self.scroll_layout.takeAt(0) # Remove Spacer

        # Get all geometries
        geometries, instance_count = libclarisse.get_geometries_from_scatterers(self._scatterers, return_count=True)
        self._geometries = {x: y for x, y in zip(geometries, instance_count)}

        # Create a widget for each geo
        for geometry, instances in sorted(self._geometries.items(), key=lambda k: k[0].get_name()):
            geometry_widget = geometryItemWidget.GeometryItemWidget(self, geometry=geometry, instances=instances)
            self.scroll_layout.addWidget(geometry_widget)
            self.geometry_widgets.append(geometry_widget)


        self.scroll_layout.addItem(self.spacer)

    def save_geometry_widgets(self):
        """Save the user inputted info within the geometry widgets"""
        for widget in self.geometry_widgets:
            widget.save_ass_file_path()

    # __________________________________________________________________________________________________________________
    # Getters


    def get_selected_geometryWidgets(self):
        """Returns all selected geometryWidgets
        
        ReturnsL
            list: List of GeometryItemWidget
            
        """
        return [w for w in self.geometry_widgets if w.is_checked()]


    def get_selected_geometries(self):
        """Returns all selected geometries
        
        Returns:
            list: List of geometry objects
            
        """
        selected_widgets = self.get_selected_geometryWidgets()
        return [w.geometry for w in selected_widgets]

# ______________________________________________________________________________________________________________________
