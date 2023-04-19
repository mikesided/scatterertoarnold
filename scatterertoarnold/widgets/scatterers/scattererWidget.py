#!/usr/bin/env python
"""
    Name:           scattererWidget.py
    Description:    Scatterer Widget
 
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
from scatterertoarnold.widgets.scatterers import scattererItemWidget

# ______________________________________________________________________________________________________________________

class ScattererWidget(QWidget):
    """Scatterer selection widget"""

    scatterers_changed = Signal(list)
    def __init__(self, parent, *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent
            
        """
        super(ScattererWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent

        # Attributes
        self.scatterer_widgets = []
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
        self.btn_reload = QPushButton(parent=self, text='Reload Scatterers')
        self.btn_reload.clicked.connect(self.update_scatterers)

        self.header_layout.addWidget(self.btn_select_all)
        self.header_layout.addWidget(self.btn_unselect_all)
        self.header_layout.addItem(base.Spacer(h_expand=True))
        self.header_layout.addWidget(self.cb_show_full_name)
        self.header_layout.addWidget(self.btn_reload)

        # SCROLL AREA
        self.scroll_layout = base.ScrollLayout(self, self.layout)

        self.spacer = base.Spacer(v_expand=True)
        self.update_scatterers()

    # __________________________________________________________________________________________________________________
    # Handlers

    
    def _exitHandler(self):
        """Exit Gracefully"""
        NotImplemented

    def _on_btn_select_all_clicked(self):
        """Select all scatterers"""
        for widget in self.scatterer_widgets:
            widget.blockSignals(True)
            widget.set_checked(True)
            widget.blockSignals(False)
        self.emit_scatters_changed()

    def _on_btn_unselect_all_clicked(self):
        """Unselect all scatterers"""
        for widget in self.scatterer_widgets:
            widget.blockSignals(True)
            widget.set_checked(False)
            widget.blockSignals(False)
        self.emit_scatters_changed()

    def _on_cb_show_full_name_changed(self, index):
        """Sets Sets the show_full_name based on the selection"""
        self.show_full_name = bool(index)
        for widget in self.scatterer_widgets:
            widget.set_name()

    # __________________________________________________________________________________________________________________
    # Widget Functionality

    def update_scatterers(self):
        """Updates the list of scatterers based on the source_context found in the panelwidget"""
        # Reset Widget
        self.scatterer_widgets = []
        base.empty_item(self.scroll_layout)
        self.scroll_layout.takeAt(0) # Remove Spacer

        # Get Scatterers
        scatterers = []
        source_context = self.parent.source_context
        scat_array = ix.api.OfObjectArray()

        ix.application.get_factory().get_all_objects('SceneObjectScatterer', scat_array)
        
        for scat_index in range(scat_array.get_count()):
            scatterer = scat_array[scat_index]
            scatterers.append(scatterer)

        # Create scatterer widgets
        for scatterer in scatterers:
            # Validate if the scatterer is part of our context
            if source_context:
                if not scatterer.get_full_name().startswith(source_context):
                    continue
            scatterer_widget = scattererItemWidget.ScattererItemWidget(self, scatterer=scatterer)
            scatterer_widget.state_changed.connect(self.emit_scatters_changed)
            self.scroll_layout.addWidget(scatterer_widget)
            self.scatterer_widgets.append(scatterer_widget)
        
        self.scroll_layout.addItem(self.spacer)

    def emit_scatters_changed(self, *args, **kwargs):
        """Emits the scatters_changed signal with the right list"""
        scatterers = self.get_selected_scatterers()
        self.scatterers_changed.emit(scatterers)
    
    # __________________________________________________________________________________________________________________
    # Getters

    def get_selected_scattererWidgets(self):
        """Returns all selected scattererWidgets
        
        ReturnsL
            list: List of ScattererItemWidget
            
        """
        return [w for w in self.scatterer_widgets if w.is_checked()]

    def get_selected_scatterers(self):
        """Returns all selected scatterers
        
        Returns:
            list: List of SceneObjectScatterers
            
        """
        selected_widgets = self.get_selected_scattererWidgets()
        return [w.scatterer for w in selected_widgets]

# ______________________________________________________________________________________________________________________
