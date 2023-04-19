#!/usr/bin/env python
"""
    Name:           ass_generator.py
    Description:    Core functions to generate .ass files

    Doc:
        https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_for_maya_rendering_am_Arnold_Scene_Source_html
        https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_for_maya_system_am_Search_Path_html
        https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_user_guide_ac_shapes_ac_arnold_procedural_html
 
"""
# System Imports
import os
import sys
import logging
from datetime import datetime
from collections import OrderedDict
import time

# Third-Party Imports
import ix

# Local Imports
from scatterertoarnold import pkginfo
from scatterertoarnold.configs import config

# ______________________________________________________________________________________________________________________
# ATTRIBUTES

NODE_BUFFER_MAX_LENGTH = 2500

HEADER = OrderedDict({
    'exported': datetime.now().strftime('%a %b %d %H:%M:%S %Y'),
    'from': f'{pkginfo.pretty_print_name} ({pkginfo.name} v{pkginfo.version}) - {pkginfo.url}',
    'host app': f'{ix.application.get_application_header()} ({ix.application.get_version()})',
    'bounds': '-10 -10 -10 10 10 10',
    'user': os.getlogin(),
    'render_layer': 'defaultRenderLayer',
})

ASS_NODE_TYPES = OrderedDict({
    'options': {
        'AA_samples': '3',
        'xres': '960',
        'yres': '540',
        'texture_per_file_stats': 'on',
        'texture_searchpath': '',
        'texture_automip': 'off',
        'color_manager': 'defaultColorMgtGlobals',
        'frame': '1',
        'procedural_searchpath': '',
        'GI_diffuse_depth': '1',
        'GI_specular_depth': '1',
        'GI_transmission_depth': '8',
        'declare': 'render_layer constant STRING',
        'render_layer': 'defaultRenderLayer'
        },
    'gaussian_filter': {
        'name': 'defaultArnoldFilter/gaussian_filter'
        },
    'driver_exr': {
        'name': 'defaultArnoldDriver/driver_exr',
        'color_space': ''
        },
    'color_manager_syncolor': {
        'name': 'defaultColorMgtGlobals',
        'native_catalog_path': 'C:/Program Files/Autodesk/Maya2023/synColor',
        'custom_catalog_path': '',
        'rendering_color_space': 'scene-linear Rec 709/sRGB'
        },
    'procedural': {
        'name': '', #  $``path``/``$id``Shape
        'visibility': '255',
        'matrix': '',
        'override_nodes': 'off',
        'filename': '', # Path to the .ass file
        'auto_instancing': 'on',
        'declare': 'dcc_name constant STRING',
        'dcc_name': 'aiStandInShape' # ``$id``Shape
        },
})

# ______________________________________________________________________________________________________________________
# Generator

class AssFileGenerator():
    """Class to generate an .ass file"""

    def __init__(self, file_path, *args, **kwargs):
        """Constructor.
        One instance of this class will represent one ass file.
        We will store a copy of the ASS_NODE_TYPES in the class, and allow updating it with default values.
        
        Args:
            file_path (str): File path to save
            **kwargs: key: ASS_NODE_TYPES keys, value: new default value

        """
        super(AssFileGenerator, self).__init__()
        self.file_path = file_path
        
        self.ASS_NODE_TYPES = ASS_NODE_TYPES.copy()
        self._update_default_node_values(**kwargs)
        
        self._node_buffer = []
        self.init_file()
        self.save_headers_to_file()
        self.save_options_to_file()

    def _update_default_node_values(self, **kwargs):
        """
        Update the default ASS_NODE_TYPES values found in the instance.
        
        Args:
            **kwargs: key: ASS_NODE_TYPES keys, value: new default value
            
        """
        for key, value in kwargs.items():
            if key in self.ASS_NODE_TYPES:
                self.ASS_NODE_TYPES[key].update(kwargs.get(key))

    def init_file(self):
        """Simply create the file on disk"""
        # Create the directory if needed
        dir_path = os.path.dirname(self.file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # Create the file
        open(self.file_path, 'w')

    def save_headers_to_file(self):
        """Saves the headers to the file"""
        with open(self.file_path, 'a') as f:
            for key, value in HEADER.items():
                f.write(f'### {key}: {value}\n')

            f.write('\n\n\n')

        time.sleep(0.1)

    def save_options_to_file(self):
        """Saves the options to the file"""
        with open(self.file_path, 'a') as f:
            for node in ['options', 'gaussian_filter', 'driver_exr', 'color_manager_syncolor']:
                f.write(f'{node}\n')
                f.write('{\n')
                for key, value in self.ASS_NODE_TYPES.get(node).items():
                    # Add Quotes to empty values and to any values with spaces
                    if value == '':
                        value = '""'
                    if ' ' in value:
                        value = f'"{value}"'

                    f.write(f' {key} {value}\n')
                f.write('}\n\n')

        time.sleep(0.1)

    def add_node(self, node_type, value):
        """Adds a node to the node_buffer to be written to file
        
        Args:
            node_type (str): Node type to add (from ASS_NODE_TYPES)
            value (dict): Value to update the defaults with, to be written to file
            
        """
        node_str = str(node_type) + '\n'
        node_str += '{\n'

        node_dict = self.ASS_NODE_TYPES.get(node_type).copy()
        node_dict.update(value)
        for k, v in node_dict.items():
            node_str += f' {k} {v}\n'

        node_str += '}\n\n'
        self._node_buffer.append(node_str)

        if len(self._node_buffer) >= NODE_BUFFER_MAX_LENGTH:
            self.save_buffer_to_file()

    def save_buffer_to_file(self):
        """
        Saves the buffer to file, and empties it. 
        We need a buffer because some .ass files can be larger than memory
        """
        with open(self.file_path, 'a') as f:
            for node in self._node_buffer:
                f.write(node)

        self._node_buffer = []

    def on_export_complete(self):
        """Called when the export has completed"""
        self.save_buffer_to_file()

# ______________________________________________________________________________________________________________________
