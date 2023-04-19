#!/usr/bin/env python
"""
    Name:           clarisse_exporter.py
    Description:    Core functions to export data from clarisse
 
"""
# System Imports
import os
import sys
import logging
import threading
import time
import hashlib

# Third-Party Imports
import ix
from PySide2.QtCore import QObject, Signal

# Local Imports
from scatterertoarnold.lib import libclarisse
from scatterertoarnold.core import ass_generator, box_parser
from scatterertoarnold.configs import config

# ______________________________________________________________________________________________________________________

class ScattererToAss(QObject):
    """Main class to export scatterers to an Arnold .ass file"""

    export_started = Signal()
    pre_validation_started = Signal()
    pre_validation_finished = Signal(list, list)
    export_progress = Signal(int, int)
    export_finished = Signal(bool)
    def __init__(self, 
                 scatterers: list=[],
                 geometries: list=[],
                 grouping: str=config.DEFAULT_GROUPING,
                 selection_type: str=config.DEFAULT_SELECTION_TYPE,
                 selection_boxes: list=[],
                 export_dir: str='',
                 export_file_name: str='',
                 request_user_input_on_warning: bool=False
                 ):
        """Constructor.
        Each parameter is also settable via attributes.
        
        Args:
            scatterers (list): List of SceneObjectScatterers to export
            geometries (list): List of geometries to export
            grouping (str): Grouping method. See grouping attribute
            selection_type (str): Selection method. See selection_type attribute
            selection_boxes (list): List of objects to represent the selected points
            export_dir (str): Path to the export directory
            export_file_name (str): Base name for the exports

            request_user_input_on_warning (bool): If running in GUI mode, user will be questioned with export warnings

        """
        super(ScattererToAss, self).__init__()
        self.scatterers = scatterers
        self.geometries = geometries
        self.grouping = grouping
        self.selection_type = selection_type
        self.selection_boxes = selection_boxes
        self.export_dir = export_dir
        self.export_file_name = export_file_name

        self.box_definitions = [] # Used by the exporter

        self.ASS_NODE_TYPES = {}

        self.request_user_input_on_warning = request_user_input_on_warning

        self._export_thread = None
        self._cancel_event = None
        self._warning_event = None

    # __________________________________________________________________________________________________________________
    # PROPERTIES

    @property
    def scatterers(self) -> list:
        """Returns the current scatterers"""
        return self._scatterers

    @scatterers.setter
    def scatterers(self, scatterers: list):
        """Set the scatterers
        
        Args:
            scatterers (list): List of SceneObjectScatterer
            
        """
        self._scatterers = scatterers

    @property
    def geometries(self) -> list:
        """Returns the current geometries"""
        return self._geometries

    @geometries.setter
    def geometries(self, geometries: dict):
        """Set the geometries.
        
        Args:
            geometries (list): List of geometry objects (usually GeometryPolybox)
            
        """
        self._geometries = geometries

    @property
    def grouping(self) -> str:
        """Returns the current grouping method"""
        return self._grouping

    @grouping.setter
    def grouping(self, grouping: str):
        """Set the grouping method. It will group points in different .ass files depending on the method chosen.

        See config.py for values

        Args:
            grouping (str): Grouping method
            
        """
        valid_methods = list(config.GROUPINGS.keys())
        if not grouping in valid_methods:
            raise ValueError('Invalid grouping method. Provided: {}. Valid: {}'.format(grouping, str(valid_methods)))
        self._grouping = grouping

    @property
    def selection_type(self) -> str:
        """Returns the current selection method"""
        return self._selection_type

    @selection_type.setter
    def selection_type(self, selection_type: str):
        """Set the selection method. The selection needs ``selection_boxes`` to be set. 
        It will define how to actually interpret these boxes.

        See config.py for values

        Args:
            selection_type (str): Selection type.
            
        """
        valid_methods = list(config.SELECTION_TYPES.keys())
        if not selection_type in valid_methods:
            raise ValueError('Invalid selection method. Provided: {}. Valid: {}'.format(selection_type, str(valid_methods)))
        self._selection_type = selection_type

    @property
    def selection_boxes(self) -> list:
        """Returns the current selection boxes"""
        return self._selection_boxes

    @selection_boxes.setter
    def selection_boxes(self, selection_boxes: list):
        """Set the selection boxes. These will get interpreted by the ``selection_type``.

        Args:
            selection_boxes (list): List of cube objects (Ideally GeometryPolybox)
            
        """
        self._selection_boxes = selection_boxes

    @property
    def export_dir(self) -> str:
        """Returns the current export directory"""
        return self._export_dir or libclarisse.get_default_dir_path()

    @export_dir.setter
    def export_dir(self, export_dir: str):
        """Set the export directory
        
        Args:
            export_dir (str): Path to the base folder for the export
            
        """
        export_dir = os.path.normpath(export_dir)
        self._export_dir = export_dir

    @property
    def export_file_name(self) -> str:
        """Returns the current export file name"""
        return self._export_file_name or libclarisse.get_default_file_name()

    @export_file_name.setter
    def export_file_name(self, export_file_name: str):
        """Set the export file name
        
        Args:
            export_file_name (str): Base name for the exported files
            
        """
        if not export_file_name[-4:] == '.ass':
            export_file_name += '.ass'
        self._export_file_name = export_file_name

    # __________________________________________________________________________________________________________________
    # CONVENIENCE METHODS

    def get_geometries_from_scatterers(self):
        """Returns a list of geometry objects from the scatterers"""
        return libclarisse.get_geometries_from_scatterers(self.scatterers)
    
    def get_export_file_names(self):
        """Returns a list of export filenames based on the chosen grouping"""
        if not self.export_file_name:
            logging.warning('export_file_name not set')
            return []
        
        file_names = []
        if self.grouping == 'all':
            # Simply return the configured export file name
            file_names.append(self.export_file_name)

        elif self.grouping == 'asset':
            # Add the asset_code token to each file. This token is set to the geometry as a custom attribute by the tool.
            # If you are not using the GUI, you must set the attribute ``Asset_Code_Representation`` as a string.
            for geometry in self.geometries:
                token = geometry.get_name()
                _file_name = self.get_file_name_with_token(token=token)
                file_names.append(_file_name)

        elif self.grouping == 'scatterer':
            # Add the scatterer's name to each file.
            for scatterer in self.scatterers:
                _file_name = self.get_file_name_with_token(token=scatterer.get_name())
                file_names.append(_file_name)

        return file_names
    
    def get_file_name_with_token(self, token):
        """Returns a file name with the given token.
        The token can represent either a scatterer, an asset, or any string.
        
        Args:
            token (str): token to add
            
        Returns:
            str: file name
        
        """
        if not self.export_file_name:
            logging.warning('export_file_name not set')
            return ''
        
        base_name, ext = os.path.splitext(self.export_file_name)
        file_name = '{base_name}_{token}{ext}'.format(base_name=base_name, token=token, ext=ext)
        return file_name
    
    def get_export_file(self, export_files, geometry_name, scatterer_name):
        """Returns the export file based on the current context
        
        Args:
            export_files (list): List of export_files
            geometry_name (str): Geometry name
            scatterer_name (str): Scatterer name
            
        Returns:
            AssFileGenerator: Export file

        """
        if self.grouping == 'all':
            return export_files[0]

        elif self.grouping == 'asset':
            file_name = self.get_file_name_with_token(token=geometry_name)

        elif self.grouping == 'scatterer':
            file_name = self.get_file_name_with_token(token=scatterer_name)

        export_file = [file for file in export_files if os.path.basename(file.file_path) == file_name][0]
        return export_file

    # __________________________________________________________________________________________________________________
    # VALIDATION

    def _run_pre_validation(self):
        """Runs the validation pre-export
        
        Returns:
            list: Error strings
            list: Warning strings
            
        """
        _errors = []
        _warnings = []

        if not self._validate_selection():
            _errors.append('An {} selection_type requires at least one selection_box'.format(self.selection_type))

        if not self._validate_export_dir():
            _warnings.append('Export directory does not exist, it will be created')
        if self._validate_export_files():
            _warnings.append('Export files already exists, they will be overwritten')
        if not self._validate_selection_boxes():
            _warnings.append('Chosen selection_type does not require any selection boxes, they will be ignored')
        if not self._validate_ass_file_attr():
            _errors.append('Some geometries do not have the {} attribute set.'.format(config.ATTR_ASS_FILE))

        return _errors, _warnings

    def _validate_selection(self):
        """Returns if the chosen selection has the required selection boxes set"""
        valid = True
        if self.selection_type in ['inclusive', 'exclusive']:
            if len(self.selection_boxes) == 0:
                valid = False

        return valid
    
    def _validate_selection_boxes(self):
        """Returns False if there's selectionboxes but no selection_type for them"""
        return not (self.selection_type == 'no_selection' and len(self.selection_boxes) > 1)
    
    def _validate_export_dir(self):
        """Returns if the destination directory exists"""
        return os.path.exists(self.export_dir)

    def _validate_export_files(self):
        """Returns if any export file already exists"""
        exists = False
        file_names = self.get_export_file_names()
        for file_name in file_names:
            file_path = os.path.join(self.export_dir, file_name)
            if os.path.exists(file_path):
                exists = True

        return exists
    
    def _validate_ass_file_attr(self):
        """Returns if each geometries have the ass file attribute set"""
        for geometry in self.geometries:
            attr = libclarisse.get_str_attribute(item=geometry, attr_name=config.ATTR_ASS_FILE)
            if not attr:
                return False

        return True

    def _validate_asset_code_attr(self):
        """
        NOTE: DEPRECATED
        
        Returns if each geometries have the asset code attribute set
        """        
        for geometry in self.geometries:
            attr = libclarisse.get_str_attribute(item=geometry, attr_name=config.ATTR_ASSET_CODE)
            if not attr:
                return False

        return True
    
    # __________________________________________________________________________________________________________________
    # EXPORT

    def export(self):
        """Starts the export process in a seperate thread"""
        logging.info('Starting export')
        self._cancel_event = threading.Event()
        self._warning_event = threading.Event()

        # Accept warning event if user is not expected to accept it
        if not self.request_user_input_on_warning:
            self._warning_event.set()

        # Parse selection boxes
        self.box_definitions = []
        for box in self.selection_boxes:
            box_definition = box_parser.get_box_definition(box)
            self.box_definitions.append(box_definition)

        # Start process
        self._export_thread = threading.Thread(target=self._export, args=(self._cancel_event, self._warning_event, ))
        self._export_thread.start()

    def abort_export(self):
        """Stops the export process"""
        if self._cancel_event:
            self._cancel_event.set()

    def accept_warnings(self):
        """Accepts the warning logs"""
        if self._warning_event:
            self._warning_event.set()

    def _export(self, cancel_event, warning_event):
        """Runs the export"""
        success = True
        self.export_started.emit()
        logging.info('Export Started')

        self.pre_validation_started.emit()
        errors, warnings = self._run_pre_validation()
        self.pre_validation_finished.emit(errors, warnings)

        if errors:
            # Cancel the export
            cancel_event.set()

        elif warnings:
            # Wait for user input
            while not warning_event.is_set():
                if cancel_event.is_set():
                    break
                time.sleep(0.1)

        if not cancel_event.is_set():
            # Start exporting
            self._export_scatterers(cancel_event=cancel_event)

        if cancel_event.is_set():
            success = False

        # Finished/cancelled
        self.export_finished.emit(success)
        logging.info('Export completed')
        self._cancel_event = None
        self._warning_event = None

    def _export_scatterers(self, cancel_event):
        """Exports the scatterers based on the configured attributes"""
        # Let us declare some values
        tr_vector3D = ix.api.GMathVec3d()
        scale_vector3D = ix.api.GMathVec3d()
        rot_vector3D = ix.api.GMathVec3d()
        shear_vector3D  = ix.api.GMathVec3d()
        rot_matrix4X4 = ix.api.GMathMatrix4x4d()

        # First get the amount of points to parse based on the scatterers selected for the signals
        total_points = 0
        for _scatterer in self.scatterers:
            scatterer = _scatterer.get_module()
            instances_id = scatterer.get_instances()
            total_points += scatterer.get_instance_count()

        # Get Files
        ass_files = []
        file_names = self.get_export_file_names()
        for file_name in file_names:
            file_path = os.path.join(self.export_dir, file_name)
            ass_file = ass_generator.AssFileGenerator(file_path=file_path)
            ass_file.ASS_NODE_TYPES.update(self.ASS_NODE_TYPES)
            ass_files.append(ass_file)
            
        # Now parse points
        current_point = 0
        for _scatterer in self.scatterers:
            scatterer = _scatterer.get_module()
            scatterer_name = scatterer.get_object_name().split('/')[-1]
            instances_id = scatterer.get_instances()
            for i in range(scatterer.get_instance_count()):
                # Loop each scatter
                current_point += 1
                self.export_progress.emit(current_point, total_points)
                instance_id = instances_id.get_item(i)
                instance = scatterer.get_base_objects().get_item(instance_id)
                geometry = ix.get_item(instance.get_object_name())
                geometry_name = geometry.get_name()
                module = geometry.get_module()

                # Validate that is geometry is selected to export
                if geometry not in self.geometries:
                    continue

                # Get the instance's matrix
                matrix = scatterer.get_instance_matrix(i)
                ix.api.GMathMatrix4x4d.extract_translation(matrix, tr_vector3D)
                ix.api.GMathMatrix4x4d.compute_euler_angles(matrix, rot_vector3D)
                ix.api.GMathMatrix4x4d.extract_scaling(matrix, scale_vector3D)
                ix.api.GMathMatrix4x4d.extract_shearing(matrix, shear_vector3D)
                ix.api.GMathMatrix4x4d.extract_rotation(matrix, rot_matrix4X4)
                matrix.transpose()

                # See if the point is selected by the user
                if self.selection_type == 'inclusive':
                    if not box_parser.is_point_in_any_box(point=tr_vector3D, boxes=self.box_definitions):
                        continue
                elif self.selection_type == 'exclusive':
                    if box_parser.is_point_in_any_box(point=tr_vector3D, boxes=self.box_definitions):
                        continue

                # Find a unique ID for this instance. 
                # We will has the location of the point to define its ID, appended with the geometry name
                loc_hash = hashlib.md5(str(matrix).split('\n')[3].encode('utf-8'))
                loc_hash = loc_hash.hexdigest()
                unique_id = f'id_{loc_hash}_{geometry_name}'

                # We must multiple the scale of the geometry, if any
                geo_scale_vector3D = self._get_geo_scale_vector3D(module)

                rescaled_vector3D = ix.api.GMathVec3d(
                    geo_scale_vector3D[0] * scale_vector3D[0], 
                    geo_scale_vector3D[1] * scale_vector3D[1], 
                    geo_scale_vector3D[2] * scale_vector3D[2]
                    )
                
                # Define a new matrix and compose it with the new scale
                scaled_matrix = ix.api.GMathMatrix4x4d()
                scaled_matrix.compose(tr_vector3D, rot_matrix4X4, shear_vector3D, rescaled_vector3D)
                scaled_matrix.transpose()

                # Prepare the matrix to be printed out to the .ass file
                matrix_str = self._format_matrix_to_ass_string(scaled_matrix)        

                # FIND FILE
                ass_file = self.get_export_file(ass_files, geometry_name=geometry_name, scatterer_name=scatterer_name)

                # Get procedural dict from the default
                procedural_dict = ass_file.ASS_NODE_TYPES['procedural'].copy()
                dcc_name = f'{unique_id}Shape'
                procedural_dict.update({
                    'name': f'/scatterers/{scatterer_name}/{geometry_name}/{unique_id}',
                    'matrix': matrix_str,
                    'filename': '"{}"'.format(libclarisse.get_str_attribute(item=geometry, attr_name=config.ATTR_ASS_FILE)),
                    'dcc_name': f'"{dcc_name}"',
                })

                # Verify if we've aborted, else add our new dict to the .ass file
                if cancel_event.is_set():  
                    return False
                else:
                    ass_file.add_node(node_type='procedural', value=procedural_dict)

        # Complete the export
        for ass_file in ass_files:
            ass_file.on_export_complete()

        return True
    
    def _get_geo_scale_vector3D(self, module):
        """Gets the scale vector3D from a ModuleSceneObjectTree
        
        Returns:
            tuple: (x, y, z)
        
        """
        # Get scale matrix from a combiner and return a simple dict
        matrix = module.get_global_matrix()
        matrix = str(matrix).split('\n')
        vector3D = (
            float(matrix[0].split(' ')[0]), 
            float(matrix[1].split(' ')[1]), 
            float(matrix[2].split(' ')[2])
            )
        return vector3D

    def _format_matrix_to_ass_string(self, matrix):
        """Formats the given matrix to an .ass file string"""
        matrix_str = str()
        for line in str(matrix).split('\n'):
            if line.strip() == '': 
                continue

            # Add value to the string
            matrix_str += '\n ' 
            for value in line.strip().split():
                normalized = '{:f}'.format(float(value))
                matrix_str += f'{normalized} '

        return matrix_str

# ______________________________________________________________________________________________________________________
