#!/usr/bin/env python
"""
    Name:           __init__.py
    Description:    Entry Point for the clarisse2ass tool
 
"""
# System Imports
import os
import logging
import sys

# Local Imports
from scatterertoarnold import pkginfo
from scatterertoarnold.style import stylesheet
from scatterertoarnold.widgets.main import scattererToArnoldWidget

# Third-Party Imports
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqt_clarisse

# ______________________________________________________________________________________________________________________

def launch():
    """Launch the tool"""
    app = None
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    app.setStyleSheet(stylesheet.base_stylesheet)

    app.processEvents()
    window = ScattererToArnoldWindow()
    window.show()
    pyqt_clarisse.exec_(app)


class AboutWindow(QMainWindow):
    """Loading Window"""
    __windowtitle = pkginfo.display_name
    def __init__(self, *args, **kwargs):
        super(AboutWindow, self).__init__(*args, **kwargs)
        flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        self.setWindowFlags(flags)
        self.setMinimumWidth(300)
        self.setMinimumHeight(120)

        # Main Widget
        self.widget = QWidget()
        self.widget.setObjectName('framelesswindow')
        self.widget.setStyleSheet('QWidget#framelesswindow { border: 2px outset #1c2029; }')
        self.setCentralWidget(self.widget)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)
        self.centralWidget().setLayout(self.main_layout)

        about_lbl = QLabel(parent=self, text='  About')
        about_lbl.setStyleSheet('font-size: 18px;')
        self.main_layout.addWidget(about_lbl)
        lbl = QLabel(parent=self, text=f'{pkginfo.display_name} v{pkginfo.version}')
        lbl.setStyleSheet('font-size: 12px;')
        self.main_layout.addWidget(lbl)

        # ADD EDITOR WITH ALL INFO TO COPY PASTE
        editor = QTextEdit(parent=self)
        editor.setReadOnly(True)
        editor.setPlainText(
            f'Package: {pkginfo.pretty_print_name}\n'
            f'Developer: {pkginfo.developer}\n'
            f'Version: {pkginfo.version}\n'
            f'URL: {pkginfo.url}\n\n'
            f'Description: {pkginfo.description}\n'
        )

        self.main_layout.addWidget(editor)

        close_btn = QPushButton('Ok', parent=self)
        close_btn.clicked.connect(self.close)
        self.main_layout.addWidget(close_btn)


class ScattererToArnoldWindow(QMainWindow):
    """Main Window"""
    __windowtitle = '{} v{}'.format(pkginfo.display_name, pkginfo.version)
    def __init__(self, *args, **kwargs):
        super(ScattererToArnoldWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(self.__windowtitle)
        flags = Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setMinimumWidth(750)
        self.setMinimumHeight(600)
        # Main Widget
        self.widget = scattererToArnoldWidget.ScattererToArnoldWidget(mainwindow=self)
        self.setCentralWidget(self.widget)

        self.widget.close_app.connect(self.close)

        # Nav menu
        self.menu_bar = self.menuBar()
        self.menu_bar.setObjectName('mainMenu')
        file_menu = self.menu_bar.addMenu('File')
        help_menu = self.menu_bar.addMenu('Help')
        about_action = QAction(text='About', parent=self)
        about_action.triggered.connect(self._on_about_action_triggered)
        help_menu.addAction(about_action)

        self.setStyleSheet(stylesheet.base_stylesheet)
    
    def closeEvent(self, event):
        """Override close event to allow exit handlers"""
        self.widget._exitHandler()

    def _on_about_action_triggered(self):
        """Opens the about window"""
        self.about_window = AboutWindow()
        self.about_window.show()
        

if __name__ == '__main__':
    launch()
        
# ______________________________________________________________________________________________________________________
