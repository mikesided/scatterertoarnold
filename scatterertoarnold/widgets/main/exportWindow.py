#!/usr/bin/env python
"""
    Name:           exportWindow.py
    Description:    Window to show current process of the export
 
"""
# System Imports
import os
import sys
import logging
import functools
import webbrowser

# Third-Party Imports
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import qtawesome
import ix

# Local Imports
from scatterertoarnold.widgets.main import base
from scatterertoarnold.core import clarisse_exporter
from scatterertoarnold.configs import config
from scatterertoarnold.lib import libclarisse
from scatterertoarnold.style import stylesheet

# ______________________________________________________________________________________________________________________

class ScattererToAssExportWindow(QMainWindow):
    """Export Window"""

    __window_title = 'Scatterer to .ass Export'
    def __init__(self, parent, exporter):
        """Constructor
        
        Args:
            parent: Parent widget
            exporter (ScattererToAss): exporter instance
            
        """
        super(ScattererToAssExportWindow, self).__init__()
        self.parent = parent
        self.exporter = exporter
        self.setWindowTitle(self.__window_title)
        flags = Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setWindowModality(Qt.ApplicationModal)
        self.setCentralWidget(QWidget())
        self.setMinimumWidth(650)
        self.setMinimumHeight(350)
        self.setStyleSheet(stylesheet.base_stylesheet)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFormat('')
        self.progress_bar.setFixedWidth(400)

        self.export_finished = False

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)
        self.centralWidget().setLayout(self.layout)
       
        self.title_lbl = QLabel(parent=self, text='Scatterer Export Process')
        self.title_lbl.setObjectName('title')
        self.title_lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_lbl)

        progress_bar_layout = QHBoxLayout()
        progress_bar_layout.setAlignment(Qt.AlignCenter)
        progress_bar_layout.addWidget(self.progress_bar)
        self.layout.addLayout(progress_bar_layout)

        # Body layout
        self.scroll_layout = base.ScrollLayout(parent=self, layout=self.layout)
        self.body_layout = QGridLayout()
        self.body_layout.setContentsMargins(10, 10, 10, 10)
        self.body_layout.setSpacing(8)
        self.scroll_layout.addLayout(self.body_layout)
        self.scroll_layout.addItem(base.Spacer(v_expand=True))

        # Warning row
        self.warning_icon = qtawesome.icon('fa5s.exclamation-triangle', color='#bda13e')
        self.warning_lbl = QLabel(parent=self, text='')
        self.warning_layout = QGridLayout(self)
        self.body_layout.addWidget(self.warning_lbl, 0, 0, 1, 3)
        self.body_layout.addItem(base.Spacer(h_expand=True), 0, 2)
        self.body_layout.addLayout(self.warning_layout, 1, 0, 1, 3)

        self.body_layout.addItem(base.Spacer(h=20), 2, 0)

        # Error row
        self.error_icon = qtawesome.icon('fa5s.exclamation-circle', color='#c43535')
        self.error_lbl = QLabel(parent=self, text='')
        self.error_layout = QGridLayout(self)
        self.body_layout.addWidget(self.error_lbl, 3, 0, 1, 3)
        self.body_layout.addItem(base.Spacer(h_expand=True), 3, 2)
        self.body_layout.addLayout(self.error_layout, 4, 0, 1, 3)

        # Input Row
        self.input_layout = QHBoxLayout()
        self.input_label = QLabel(parent=self, text='')
        self.input_layout.addWidget(self.input_label)
        self.layout.addLayout(self.input_layout)

        self.layout.addItem(base.Spacer(h=20))

        # Footer layout
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(5)
        self.layout.addLayout(self.footer_layout)
        
        self.btn_abort = QPushButton(parent=self, text='Abort')
        self.btn_abort.setFixedWidth(150)
        self.btn_abort.clicked.connect(self._on_btn_abort_clicked)
        self.btn_continue = QPushButton(parent=self, text='Continue')
        self.btn_continue.setFixedWidth(150)
        self.btn_continue.setVisible(False)
        self.btn_continue.clicked.connect(self._on_btn_continue_clicked)
        self.footer_layout.addWidget(self.btn_abort)
        self.footer_layout.addWidget(self.btn_continue)
        self.footer_layout.addItem(base.Spacer(h_expand=True))
        self.btn_open_dir = QPushButton(parent=self, text=' Open Export Directory ')
        self.btn_open_dir.clicked.connect(self._on_btn_open_dir_clicked)
        self.footer_layout.addWidget(self.btn_open_dir)
        self.btn_close = QPushButton(parent=self, text='Close')
        self.btn_close.setEnabled(False)
        self.btn_close.clicked.connect(self.close)
        self.footer_layout.addWidget(self.btn_close)

        # Exporter connections    
        self.exporter.export_started.connect(lambda: self.progress_bar.setValue(0))
        self.exporter.pre_validation_started.connect(lambda: self.progress_bar.setFormat('Running Pre Validation'))
        self.exporter.pre_validation_finished.connect(self._on_pre_validation_finished)
        self.exporter.export_progress.connect(self._set_progress)
        self.exporter.export_finished.connect(self._on_export_finished)

        # Start export
        self.export()

    def closeEvent(self, event):
        """Override close event to allow exit handlers"""
        if not self.export_finished:
            msgbox = QMessageBox(self)
            msgbox.setStyleSheet(stylesheet.base_stylesheet)
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle(self.__window_title)
            msgbox.setText('Are you sure you want to abort the export?')
            msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msgbox.exec_()
            if result == QMessageBox.Yes:
                self.exporter.abort_export()
            else:
                event.ignore()

    def export(self):
        """Start the export process"""
        self.exporter.export()

    def _set_progress(self, current, total):
        """Sets the current progress to the progress bar
        
        Args:
            current (int): Current point
            max (int): Total number of points
            
        """
        percent = current/total*100
        self.progress_bar.setValue(percent)
        self.progress_bar.setFormat('{} / {}'.format(current, total))

    def _on_btn_abort_clicked(self):
        """Abort the export"""
        self.exporter.abort_export()
        self.btn_continue.setVisible(False)

        self.title_lbl.setText('-- Export Aborted! --')
        self.title_lbl.setStyleSheet('color: #bda13e;')

    def _on_btn_continue_clicked(self):
        """Accept the warnings"""
        self.exporter._warning_event.set()
        self.input_label.setText('')
        self.btn_continue.setVisible(False)

    def _on_btn_open_dir_clicked(self):
        """Opens the exporter's export dir"""
        export_dir = self.exporter.export_dir
        webbrowser.open('file:///' + export_dir)

    def _on_pre_validation_finished(self, errors, warnings):
        """Triggered when the pre validation is finished
        
        Args:
            errors (list): List of error strings
            warnings (list): List of warning strings
            
        """
        self.warning_lbl.setText('-> ' + str(len(warnings)) + ' warning{} found'.format('' if len(warnings) == 1 else 's'))
        self.error_lbl.setText('-> ' + str(len(errors)) + ' error{} found'.format('' if len(errors) == 1 else 's'))

        # Write errors to widget
        for error in errors:
            index = errors.index(error)
            widget_error = qtawesome.IconWidget()
            widget_error.setIcon(self.error_icon)
            self.error_layout.addWidget(widget_error, index, 0)
            self.error_layout.addWidget(QLabel(parent=self, text=error), index, 1)
            self.error_layout.addItem(base.Spacer(h_expand=True), index, 2)

        # Write warnings to widget
        for warning in warnings:
            index = warnings.index(warning)
            widget_warning = qtawesome.IconWidget()
            widget_warning.setIcon(self.warning_icon)
            self.warning_layout.addWidget(widget_warning, index, 0)
            self.warning_layout.addWidget(QLabel(parent=self, text=warning), index, 1)
            self.warning_layout.addItem(base.Spacer(h_expand=True), index, 2)

        # On error, export is cancelled
        if errors:
            self.input_label.setText('--> Cannot export with errors.')

        # On warning, we query user to continue or not
        elif warnings and self.exporter.request_user_input_on_warning:
            self.input_label.setText('--> Continue despite warnings?')
            self.btn_continue.setVisible(True)

    def _on_export_finished(self, result):
        """Triggered when export is finished
        
        Args:
            result (bool): Success?
            
        """
        self.export_finished = True
        self.btn_close.setEnabled(True)
        self.btn_abort.setEnabled(False)

        if result:
            self.title_lbl.setText('-- Export Complete! --')
            self.title_lbl.setStyleSheet('color: #66bf4b;')
        else:
            if not 'abort' in self.title_lbl.text().lower():
                self.title_lbl.setText('-- Export Failed! --')
                self.title_lbl.setStyleSheet('color: #c43535;')

# ______________________________________________________________________________________________________________________
