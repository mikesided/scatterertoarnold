#!/usr/bin/env python
"""
    Name:           panelWidget.py
    Description:    Panel with a QStackedWidget with panel functionality
 
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
from scatterertoarnold.widgets.scatterers import scattererWidget
from scatterertoarnold.widgets.geometry import geometryWidget
from scatterertoarnold.widgets.selection import selectionBoxWidget
from scatterertoarnold.widgets.arnoldsettings import arnoldSettingsWidget

# ______________________________________________________________________________________________________________________

class PanelWidget(QWidget):
    """QStackedWidget with panel functionality"""

    def __init__(self, parent):
        super(PanelWidget, self).__init__(parent)
        self.parent = parent

        # Attributes
        self.source_context = ''

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Tabs Button Layout
        self.tabs_layout = QHBoxLayout(self)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(0)
        self.layout.addLayout(self.tabs_layout)
        self.tab_btns = []
        
        self.tab_widget = QTabWidget(self)
        self.tabs_layout.addWidget(self.tab_widget)

        # Init Panels
        self.scatterer_widget = scattererWidget.ScattererWidget(self)
        self.geometry_widget = geometryWidget.GeometryWidget(self, scatterers=self.scatterer_widget.get_selected_scatterers())
        self.selection_widget = selectionBoxWidget.SelectionBoxWidget(self)
        self.arnold_settings_widget = arnoldSettingsWidget.ArnoldSettingsWidget(self)
        self.tab_widget.addTab(self.scatterer_widget, 'Scatterers')
        self.tab_widget.addTab(self.geometry_widget, 'Geometry')
        self.tab_widget.addTab(self.selection_widget, 'Selection')
        self.tab_widget.addTab(self.arnold_settings_widget, 'Arnold Settings')

        # Connections
        self.scatterer_widget.scatterers_changed.connect(self.geometry_widget.load_geometries)

    def _exitHandler(self):
        """Exit Gracefully"""
        self.scatterer_widget._exitHandler()
        self.geometry_widget._exitHandler()

    def _on_about_to_export(self):
        """Triggered when the use is about to export"""
        self.geometry_widget._on_about_to_export()

    def set_source_context(self, source_context):
        """Sets a new source context
        
        Args:
            source_context (str): Source Context to set
            
        """
        self.source_context = source_context
        self.scatterer_widget.update_scatterers()
        self.scatterer_widget.emit_scatters_changed()

    def set_scatterers_to_exporter(self, exporter):
        """Set the selected scatterers to the given exporter
        
        Args:
            exporter: Instance to set scatterers to
            
        """
        scatterers = self.scatterer_widget.get_selected_scatterers()
        exporter.scatterers = scatterers


    def set_geometries_to_exporter(self, exporter):
        """Set the selected geometries to the given exporter
        
        Args:
            exporter: Instance to set geometries to
            
        """
        geometries = self.geometry_widget.get_selected_geometries()
        exporter.geometries = geometries

    def set_default_arnold_settings(self, exporter):
        """Set the default arnold settings to the given eexporter
        
        Args:
            exporter: Instance to set default arnold settings to
            
        """
        default_arnold_settings = self.arnold_settings_widget.get_arnold_settings()
        exporter.ASS_NODE_TYPES.update(default_arnold_settings)

    def set_selection_boxes(self, exporter):
        """Set the selection boxes to the given exporter
        
        Args:
            exporter: Instance to set the selection boxes to
            
        """
        selection_boxes = self.selection_widget.get_selection_boxes()
        exporter.selection_boxes = selection_boxes

# ______________________________________________________________________________________________________________________
