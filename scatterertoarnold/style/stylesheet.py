#!/usr/bin/env python
"""
    Name:           stylesheet.py
    Description:    Stylesheet file
 
"""
# System Imports
import os
import sys
import logging

# Third-Party Imports

# Local Imports

# ______________________________________________________________________________________________________________________

base_stylesheet = """

/*
TEXT: #e3e3e3
TEXT-HOVER: white
TEXT-PRESSED: #7d7d7d
TEXT-DISABLED: #878787
BUTTON: #343b42 
BG-DISABLED: #202020

DEFAULT BACKGROUND #101d36
DEFAULT BORDER #242833
DEFAULT INSET BACKGROUND #1e2430
DEFAULT INPUT COLOR #393f4d

QTAWESOME BUTTON COLOR #5d7396
*/


/* 
Base Style _____________________________________________________________________________________________________
*/

QWidget {
    color: #e3e3e3;
}


/* 
Main Window Style ______________________________________________________________________________________________________
*/

QMainWindow {
    background-color: #101d36;
}

QMenuBar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0c162b, stop:1 #060d1c);
    spacing: 3px;
    border-bottom: 1px inset #242833;
}

QMenuBar::item {
    padding: 1px 4px;
    background: transparent;
}

QMenuBar::item:selected {
    color: white;
}

QMenuBar::item:pressed {
    color: #7d7d7d;
}

QMenu {
    background: #1e2430;
}

QMenu::item {
    color: #e3e3e3;
}

QMenu::item::selected {
    background: #393f4d;
}



/* 
Base Widgets Style _____________________________________________________________________________________________________
*/



QDialog, QMessageBox {
    background: #101d36;
}

QScrollArea {
    background: transparent;
}

QScrollArea > QWidget > QWidget { 
    background: transparent;
}

QScrollArea > QWidget > QScrollBar {
    background: transparent;
}

QPushButton {
    background-color: #343b42;
}

QPushButton:hover {
    color: white;
}

QPushButton:disabled {
    color: #6b6b6b;
    background-color: #202020;
}

QGroupBox {
    background-color: transparent;
    border: 2px groove #242833;
    border-radius: 5px;
    margin-top: 6px;
    padding: 5 0px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 20px;
    background-color: transparent;
}

QLineEdit {
    background-color: transparent;
    border: none;
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-bottom-color: #393f4d;
}

QComboBox {
    border: 1px solid #242833;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}

QComboBox:editable {
    background: #393f4d;
}

QComboBox:!editable, QComboBox::drop-down:editable {
    background: #393f4d;
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: #393f4d;
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 0px;
    border-left-color: #202020;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}

QComboBox::hover {
    color: white;
}

QComboBox QAbstractItemView {
    selection-background-color: #5d6575;
    background-color: transparent;
}


QTabWidget::pane {
    border: 2px groove #242833;
    background-color: #1e2430;
    border-radius: 5px;
    top: -2px;
}

QTabWidget::tab-bar {
    left: 10px;
    border: 2px groove #242833;
}

QTabBar::tab {
    background: transparent;
    border: none;
    border-bottom-color: #242833; /* same as the pane border color */
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    min-width: 25ex;
    padding: 2px;
}

QTabBar::tab:selected {
    background: #1e2430;
    border: 2px groove #242833; /* same as the pane border color */
    margin-bottom: -2px;
    border-color: #242424;
    padding-left: -4px;
    padding-right: -4px
}


QTabBar::tab:hover {
    background: #1e2430;
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}

QProgressBar {
    color: #e3e3e3;
    border: 2px solid #242833;
    background-color: #1e2430;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #5d7396;
}

QListWidget {
    background: transparent;
    border: 2px inset #242833;
    border-radius: 5px;
}

QTextEdit {
    background: #1e2430;
    color: #e3e3e3;
}

/* 
Named Widgets Style ____________________________________________________________________________________________________
*/

QLabel#title {
    font-size: 12px;
    color: white;
    font-weight: bold;
}

QPushButton#tab {
    background-color: #262626;
    border: none;
}

QPushButton#tab:checked{
    background-color: #262626;
    border: none;
    border-bottom: 1px solid #408be6};
}

QPushButton#tab:pressed {
    background-color: #262626;
    border: none;
    border-bottom: 1px solid #88b4eb;
}

QPushButton#tab:hover {
    background-color: #262626;
    border: none;
    border-bottom: 1px solid #404040;
}


QFrame#line {
    background-color: #242833;
}

"""
