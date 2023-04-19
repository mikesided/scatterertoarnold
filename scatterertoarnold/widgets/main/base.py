#!/usr/bin/env python
"""
    Name:           base.py
    Description:    Base UI Classes
 
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

# Local Imports

# ______________________________________________________________________________________________________________________

def empty_item(item):
    """Empties the given item of all widgets & layouts"""
    if hasattr(item, "layout"):
        if callable(item.layout):
            layout = item.layout()
    else:
        layout = None

    if hasattr(item, "widget"):
        if callable(item.widget):
            widget = item.widget()
    else:
        widget = None


    if widget:
        widget.setParent(None)
    elif layout:
        for i in reversed(range(layout.count())):
            empty_item(layout.itemAt(i))
        item.removeItem(layout)
        
class Spacer(QSpacerItem):
    """Spacer Item"""
    def __init__(self, w=1, h=1, h_expand=False, v_expand=False):
        """Constructor
        
        Args:
            w (int): width, defaults to 1
            h (int): height, defaults to 1
            h_expand (bool): Horizontal Expanding, defaults to false
            v_expand (bool): Vertical Expanding, defaults to false

        Returns:
            QSpacerItem

        """
        h_policy = QSizePolicy.Expanding if h_expand else QSizePolicy.Fixed
        v_policy = QSizePolicy.Expanding if v_expand else QSizePolicy.Fixed
        super(Spacer, self).__init__(w, h, h_policy, v_policy)

class ScrollLayout(QVBoxLayout):
    def __init__(self, parent, layout, *args, **kwargs):
        """Constructor
        
        Args:
            parent: Parent widget
            layout: Layout to add this scroll layout to
            
        Returns:
            QVBoxLayout
            
        """
        super(ScrollLayout, self).__init__(parent)
        self.parent = parent
        self.scroll_area = QScrollArea(parent)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_widget = QWidget(parent)
        self.scroll_area.setWidget(self._scroll_widget)
        layout.addWidget(self.scroll_area)
        self._scroll_widget.setLayout(self)

class VLine(QFrame):
    def __init__(self, parent):
        super(VLine, self).__init__(parent)
        self.setObjectName('line')
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)

# ______________________________________________________________________________________________________________________
