#!/usr/bin/env python
"""
    Name:           box_parser.py
    Description:    Parser functions for selection boxes / cubes
 
"""
# System Imports
import os
import sys
import logging

# Third-Party Imports
import ix
import numpy as np

# Local Imports
from scatterertoarnold.lib import libclarisse

# ______________________________________________________________________________________________________________________

def get_default_box_definition() -> dict:
    """Returns the default box definition dict
    
    Returns:
        dict: Default box definition
        
    """
    box_definition = {
        'geometry': None, # Geometry object
        'bounding_box': ix.api.GMathBbox3d(), # The bounding box of the cube. Used for preliminary searches
        'vector_origin_point': np.array([]), # (x, y, z) Point
        'vectors_from_center': {
            'i': np.array([]), # (x, y, z)
            'j': np.array([]), # (x, y, z)
            'k': np.array([]), # (x, y, z)
        },
        'vectors_from_origin': {
            'i': np.array([]), # (x, y, z)
            'j': np.array([]), # (x, y, z)
            'k': np.array([]), # (x, y, z)
        },
        'center_point': np.array([]), # (x, y, z) Point
    }
    return box_definition

def get_box_definition(box) -> dict:
    """Calculates the geometry's box definition.
    
    Essentially gets the it's center point and an origin point from which three 
    vectors will be generated to define the cube
    
    Args:
        box: Cube Geometry
        
    Returns:
        dict: BOX_DEFINITION with values
        
    """
    # Copy the box to work with
    temp_box = ix.cmds.CopyItemTo(box, box.get_context().get_full_name())
    geo = temp_box.get_module()

    box_def = get_default_box_definition()

    # Get bounding box
    bounding_box = ix.api.GMathBbox3d()
    matrix = geo.get_global_matrix()
    geo.get_bbox().transform_bbox_and_get_bbox(matrix, bounding_box)

    # Get the geometry's rotation. To get the euler angles, we must scale down the geo temporarily to (1, 1, 1)
    _init_scale = ix.api.GMathVec3d()
    rotation = ix.api.GMathVec3d()
    matrix = geo.get_global_matrix()
    matrix.extract_scaling(_init_scale) # Get initial scale
    geo.set_scaling(ix.api.GMathVec3d(1, 1, 1)) # Scale to (1, 1, 1)
    geo.get_global_matrix().compute_euler_angles(rotation) # Extract euler angles
    geo.set_scaling(_init_scale) # Set initial scale back
    x_rot, y_rot, z_rot = map(lambda euler: (euler/180 * np.pi), rotation) # Convert the rotation to radians

    # We can now remove the rotation from the geometry to work with it in the (x, y, z) system.
    # We only need to do this to capture its values, we then set the box back to original values
    geo.set_rotation(ix.api.GMathVec3d()) # Reset rotation to 0, 0, 0
    matrix_norot = geo.get_global_matrix()
    bb_norot = ix.api.GMathBbox3d()
    geo.get_bbox().transform_bbox_and_get_bbox(matrix_norot, bb_norot)
    geo.set_rotation(rotation) # Set rotation back to the original geometry

    x_min, y_min, z_min = bb_norot[0]
    x_max, y_max, z_max = bb_norot[1]
    
    # Set the geometry's center to definition.
    center = np.array([
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        (z_min + z_max) / 2,
    ])

    # We need vectors starting from the center to the X, Y and Z planes. Once rotated with and offset to the geo's center,
    # we will have our exact box's definition, from the center point.
    vectors = {}
    x = (x_max - x_min) / 2
    y = (y_max - y_min) / 2
    z = (z_max - z_min) / 2
    vectors['i'] = np.array([x, 0, 0])
    vectors['j'] = np.array([0, y, 0])
    vectors['k'] = np.array([0, 0, z])

    # Rotate them
    for plane, vector in vectors.items():
        x, y, z = vector
        y, z = (y*np.cos(x_rot)) - (z*np.sin(x_rot)), (y*np.sin(x_rot)) + (z*np.cos(x_rot)) # X Axis Rotation
        x, z = (x*np.cos(y_rot)) + (z*np.sin(y_rot)), (-x*np.sin(y_rot)) + (z*np.cos(y_rot)) # Y Axis Rotation
        x, y = (x*np.cos(z_rot)) - (y*np.sin(z_rot)), (x*np.sin(z_rot)) + (y*np.cos(z_rot)) # Z Axis Rotation
        vectors[plane] = np.array([x, y, z])

    # These vectors are current defining the box from the center. Multiplying them by two will define the box from
    # one of its 8 points, which will be more handy to calculate the point cloud. We will use the (-x, -y, -z) point.
    x_origin = center[0] - vectors['i'][0] - vectors['j'][0] - vectors['k'][0]
    y_origin = center[1] - vectors['i'][1] - vectors['j'][1] - vectors['k'][1]
    z_origin = center[2] - vectors['i'][2] - vectors['j'][2] - vectors['k'][2]
    vector_origin = np.array([x_origin, y_origin, z_origin])
    vectors_from_origin = {
        'i': vectors['i'] * 2,
        'j': vectors['j'] * 2,
        'k': vectors['k'] * 2
    }

    # Set everything to the definition
    box_def['geometry'] = box.get_module()
    box_def['bounding_box'] = bounding_box
    box_def['center_point'] = center
    box_def['vector_origin_point'] = vector_origin
    box_def['vectors_from_origin'] = vectors_from_origin
    box_def['vectors_from_center'] = vectors

    ix.cmds.DeleteItem(temp_box)
    return box_def

def is_point_in_any_box(point, boxes) -> bool:
    """
    Checks if the given point is in any of the given boxes
    
    Args:
        point (tuple): (x, y, z) Point to test
        boxes (list): List of box_definition dicts
        
    Returns:
        bool: Is in any box?
        
    """
    for box in boxes:
        if _is_point_in_bounding_box(point, box):
            if _is_point_in_box(point, box):
                return True
            
    return False

def _is_point_in_bounding_box(point, box) -> bool:
    """
    Checks if the given point is in the given bounding box

    Args:
        point (tuple): (x, y, z) Point to test
        box (dict): Box Definition
        
    Returns:
        bool: Is in bounding box?

    """
    bb = box.get('bounding_box')
    x, y, z = point

    if not bb[0][0] < x < bb[1][0]:
        return False
    
    if not bb[0][1] < y < bb[1][1]:
        return False
    
    if not bb[0][2] < z < bb[1][2]:
        return False
    
    return True
        

def _is_point_in_box(point, box) -> bool:
    """
    Checks if the given point is in the given box    
    
    As seen here:
    https://math.stackexchange.com/a/1552579

        Let:
            p1: Origin point
            pv: Point to test
            i: p2−p1
            j: p4−p1
            k: p5−p1
            v: pv−p1
        If:
            0<v⋅i<i⋅i
            0<v⋅j<j⋅j
            0<v⋅k<k⋅k
        Then:
            Point inside cuboid

    Args:
        point (tuple): (x, y, z) Point to test
        box (dict): Box Definition
        
    Returns:
        bool: Is in box?

    """

    # Offset the point to the box's coord system
    origin = box.get('vector_origin_point')
    offset_point = (point[0] - origin[0], point[1] - origin[1], point[2] - origin[2])

    i = box.get('vectors_from_origin').get('i')
    j = box.get('vectors_from_origin').get('j')
    k = box.get('vectors_from_origin').get('k')

    if not 0 < np.dot(offset_point, i) < np.dot(i, i):
        return False

    if not 0 < np.dot(offset_point, j) < np.dot(j, j):
        return False

    if not 0 < np.dot(offset_point, k) < np.dot(k, k):
        return False

    return True

# ______________________________________________________________________________________________________________________
