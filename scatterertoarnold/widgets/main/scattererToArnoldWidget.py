#!/usr/bin/env python
"""
    Name:           scattererToArnoldWidget.py
    Description:    Main Widget File
 
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
from scatterertoarnold.widgets.main import panelWidget
from scatterertoarnold.widgets.options import optionsWidget

# ______________________________________________________________________________________________________________________

class ScattererToArnoldWidget(QWidget):
    """Main Widget"""

    close_app = Signal()
    def __init__(self, mainwindow, *args, **kwargs):
        """Constructor
        
        Args:
            mainwindow (QMainWindow): Main Window instance
            
        """
        super(ScattererToArnoldWidget, self).__init__(mainwindow, *args, **kwargs)
        self.mainwindow = mainwindow

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        self.panels_layout = QHBoxLayout(self)
        self.layout.addLayout(self.panels_layout)

        # Stacked Widget with various panels
        self.panel_widget = panelWidget.PanelWidget(self)
        self.panels_layout.addWidget(self.panel_widget)
        
        # Main Options widget
        self.options_widget = optionsWidget.OptionsWidget(self)
        self.panels_layout.addWidget(self.options_widget)

        # Connections
        self.options_widget.source_context_changed.connect(self._on_source_context_changed)
        self.options_widget.request_scatterers.connect(self._on_request_scatterers_triggered)
        self.options_widget.request_geometries.connect(self._on_request_geometries_triggered)
        self.options_widget.request_arnold_settings.connect(self._on_request_arnold_settings_triggered)
        self.options_widget.request_selection_boxes.connect(self._on_request_selection_boxes_triggered)
        self.options_widget.about_to_export.connect(self._on_about_to_export_triggered)
        
    # __________________________________________________________________________________________________________________
    # Handlers

    def _exitHandler(self):
        """Exit gracefully"""
        self.panel_widget._exitHandler()
        self.options_widget._exitHandler()

    def _on_source_context_changed(self, new_context):
        """Triggered when source context has been changed
        
        Args:
            new_context (str): New context chosen
            
        """
        self.panel_widget.set_source_context(new_context)

    def _on_request_scatterers_triggered(self, exporter):
        """Ask the panel widget to set the selected scatterers to the exporter
        
        Args:
            exporter: Instance to set the scatterers to
            
        """
        self.panel_widget.set_scatterers_to_exporter(exporter)

    def _on_request_geometries_triggered(self, exporter):
        """Ask the panel widget to set the selected geometries to the exporter
        
        Args:
            exporter: Instance to set the scatterers to
            
        """
        self.panel_widget.set_geometries_to_exporter(exporter)
        
    def _on_request_arnold_settings_triggered(self, exporter):
        """Ask the panel widget to set the default arnold settings to the exporter
        
        Args:
            exporter: Instance to set the default arnold settings to
            
        """
        self.panel_widget.set_default_arnold_settings(exporter)

    def _on_request_selection_boxes_triggered(self, exporter):
        """Ask the panel widget to set the selection boxes to the exporter
        
        Args:
            exporter: Instance to set the selection boxes to
            
        """
        self.panel_widget.set_selection_boxes(exporter)

    def _on_about_to_export_triggered(self):
        """Prepare the tool to export"""
        self.panel_widget._on_about_to_export()

# ______________________________________________________________________________________________________________________
