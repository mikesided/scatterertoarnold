#!/usr/bin/env python
"""
    Name:           optionsWidget.py
    Description:    Options Widget with the main actions
 
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
import qtawesome
import ix

# Local Imports
from scatterertoarnold.widgets.main import base, exportWindow
from scatterertoarnold.core import clarisse_exporter
from scatterertoarnold.configs import config
from scatterertoarnold.lib import libclarisse

# ______________________________________________________________________________________________________________________

class OptionsWidget(QWidget):
    """Options Widget"""

    source_context_changed = Signal(str)
    request_scatterers = Signal(object)
    request_geometries = Signal(object)
    request_arnold_settings = Signal(object)
    request_selection_boxes = Signal(object)
    about_to_export = Signal()
    def __init__(self, parent, *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent
            
        """
        super(OptionsWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setMaximumWidth(300)

        self.exporter = None

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Scroll Area
        self.scroll_layout = base.ScrollLayout(self, self.layout)

        self.export_source_grpbox = QGroupBox('Export Source', parent=self)
        self.scroll_layout.addWidget(self.export_source_grpbox)

        self.options_grpbox = QGroupBox('Export Options', parent=self)
        self.scroll_layout.addWidget(self.options_grpbox)

        self.destination_grpbox = QGroupBox('Export Location', parent=self)
        self.scroll_layout.addWidget(self.destination_grpbox)

        self.scroll_layout.addItem(base.Spacer(v_expand=True))

        self.footer_layout = QHBoxLayout(self)
        self.layout.addLayout(self.footer_layout)

        # Inits
        self._init_export_source_groupbox()
        self._init_options_groupbox()
        self._init_destination_groupbox()
        self._init_footer_layout()

    # __________________________________________________________________________________________________________________
    # INITS

    def _init_footer_layout(self):
        """Init the footer layout"""
        _l = self.footer_layout

        self.btn_close = QPushButton(text='Close', parent=self)
        self.btn_close.clicked.connect(self.parent.close_app.emit)

        self.btn_export = QPushButton(text='Export', parent=self)
        self.btn_export.clicked.connect(self._on_btn_export_clicked)

        _l.addWidget(self.btn_close)
        _l.addItem(base.Spacer(h_expand=True))
        _l.addWidget(self.btn_export)

    def _init_export_source_groupbox(self):
        """Init the export_source_groupbox"""
        gb = self.export_source_grpbox
        layout = QGridLayout(self)

        # Root Context Selection
        self.le_source_context = QLineEdit(self)
        self.le_source_context.setPlaceholderText('Context Root')
        self.le_source_context.setReadOnly(True)
        #self.le_source_context.textChanged.emit(self.source_context_changed)
        self.btn_set_source_context = QPushButton(parent=self, text='Use Selected')
        self.btn_set_source_context.clicked.connect(self._on_btn_set_source_context_clicked)
        self.btn_set_source_context.clicked.connect(lambda: self.source_context_changed.emit(self.le_source_context.text()))

        layout.addWidget(self.le_source_context, 0, 0)
        layout.addWidget(self.btn_set_source_context, 0, 1)
        gb.setLayout(layout)

    def _init_destination_groupbox(self):
        """Init the destination_groupbox"""
        gb = self.destination_grpbox
        layout = QGridLayout(self)
        self.le_dest_directory = QLineEdit(self)
        self.le_dest_directory.setPlaceholderText(libclarisse.get_default_dir_path())
        self.le_dest_directory.textChanged.connect(self._on_le_dest_directory_textChanged)
        self._on_le_dest_directory_textChanged()

        browse_dir_icon = qtawesome.icon('fa5s.folder-open', color='#5d7396')

        self.btn_browse_dir = QPushButton(icon=browse_dir_icon, parent=self)
        self.btn_browse_dir.setFixedSize(24, 24)
        self.btn_browse_dir.setStyleSheet('background-color: transparent;')
        self.btn_browse_dir.clicked.connect(self._on_btn_browse_dir_clicked)
        self.le_dest_file_name = QLineEdit(self)
        self.le_dest_file_name.setPlaceholderText(libclarisse.get_default_file_name())
        self.le_dest_file_name.textChanged.connect(self._on_le_dest_file_name_textChanged)
        self._on_le_dest_file_name_textChanged()
        self.cb_dest_file_type = QComboBox(self)
        self.cb_dest_file_type.addItems(['Arnold Scene Source (*.ass)'])

        layout.addWidget(QLabel('Directory   '), 0, 0)
        layout.addWidget(self.le_dest_directory, 0, 1)
        layout.addWidget(self.btn_browse_dir, 0, 2)
        layout.addWidget(QLabel('File Name'), 1, 0)
        layout.addWidget(self.le_dest_file_name, 1, 1, 1, 2)
        layout.addWidget(QLabel('File Type'), 2, 0)
        layout.addWidget(self.cb_dest_file_type, 2, 1, 1, 2)
        gb.setLayout(layout)

    def _init_options_groupbox(self):
        """Init the options_groupbox"""
        gb = self.options_grpbox
        layout = QGridLayout(self)
        self.cb_grouping = QComboBox(self)
        self.cb_grouping.addItems(sorted(list(config.GROUPINGS.values())))
        self.cb_grouping.setCurrentText(config.GROUPINGS.get(config.DEFAULT_GROUPING))
        self.cb_selection_type = QComboBox(self)
        self.cb_selection_type.addItems(sorted(list(config.SELECTION_TYPES.values())))
        self.cb_selection_type.setCurrentText(config.SELECTION_TYPES.get(config.DEFAULT_SELECTION_TYPE))

        layout.addWidget(QLabel(parent=self, text='Grouping'), 0, 0)
        layout.addWidget(self.cb_grouping, 0, 1)
        layout.addWidget(QLabel(parent=self, text='Selection'), 1, 0)
        layout.addWidget(self.cb_selection_type, 1, 1)
        gb.setLayout(layout)

    # __________________________________________________________________________________________________________________
    # HANDLERS

    def _exitHandler(self):
        """Exit gracefully"""
        if self.exporter:
            self.exporter.abort_export()

    def _on_btn_set_source_context_clicked(self):
        """Sets the selected item to the appropriate lineedit"""
        context = ''
        for item in ix.selection:
            item = ix.selection[0]
            context = item.get_full_name()
            break

        self.le_source_context.setText(context)

    def _on_btn_browse_dir_clicked(self):
        """Opens a file browser to select the root folder for the export"""
        init_path = self.le_dest_directory.text() or os.path.dirname(ix.application.get_current_project_filename())
        init_dir = os.path.dirname(init_path) if os.path.isfile(init_path) else init_path
        dir_path = QFileDialog.getExistingDirectory(self, 'Select export directory', init_dir)

        if dir_path:
            self.le_dest_directory.setText(dir_path)

    def _on_le_dest_directory_textChanged(self):
        """Updates the line edit tooltip"""
        self.le_dest_directory.setToolTip(self.le_dest_directory.text() or self.le_dest_directory.placeholderText())

    def _on_le_dest_file_name_textChanged(self):
        """Updates the line edit tooltip"""
        self.le_dest_file_name.setToolTip(self.le_dest_file_name.text() or self.le_dest_file_name.placeholderText())

    def _on_btn_export_clicked(self):
        """Start the export process"""
        self.about_to_export.emit()
        self.export()

    # __________________________________________________________________________________________________________________
    # EXPORT
    
    def export(self):
        """
        Run the export. 
        Utilize the clarisse_exporter module by building the export class, setting it up and firing the export.
        """
        # Start the exporter
        exp = clarisse_exporter.ScattererToAss(request_user_input_on_warning=True)
        self.request_arnold_settings.emit(exp)

        # Set export path
        exp.export_dir = self.le_dest_directory.text() or libclarisse.get_default_dir_path()
        exp.export_file_name = self.le_dest_file_name.text() or libclarisse.get_default_file_name()

        # Set Selection type
        _reversed_dict = {v: k for k, v in config.SELECTION_TYPES.items()}
        exp.selection_type = _reversed_dict.get(self.cb_selection_type.currentText())

        # Set Grouping
        _reversed_dict = {v: k for k, v in config.GROUPINGS.items()}
        exp.grouping = _reversed_dict.get(self.cb_grouping.currentText())

        # Set Scatterers
        self.request_scatterers.emit(exp)

        # Set Geometries
        self.request_geometries.emit(exp)

        # Set Chosen selection boxes
        self.request_selection_boxes.emit(exp)

        self.set_exporter(exp=exp)
        self.exporter.export_finished.connect(lambda: self.set_exporter(exp=None))
        self.export_window = exportWindow.ScattererToAssExportWindow(parent=self, exporter=exp)
        self.export_window.show()

    def set_exporter(self, exp=None):
        """Set the exporter to the attributes
        
        Args:
            exp: (ScattererToAss): Export instance
            
        """
        self.exporter = exp
    

# ______________________________________________________________________________________________________________________
