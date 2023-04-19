#!/usr/bin/env python
"""
    Name:           libclarisse.py
    Description:    Library to deal with the clarisse API
 
"""
# System Imports
import os
import sys
import logging

# Third-Party Imports
import ix

# Local Imports

# ______________________________________________________________________________________________________________________
# ATTRIBUTES

def get_attribute_object(item, attr_name):
    """Returns the attribute object

    Args:
        item: Item to read
        attr_name (str): Attribute to get
        
    Returns:
        None|Attribute
        
    """
    attr = None
    if item.attribute_exists(attr_name):
        attr = item.get_attribute(attr_name)

    return attr

def get_str_attribute(item, attr_name):
    """Returns the string value of an attribute. 
    Returns none if attribute not found
    
    Args:
        item: Item to read
        attr_name (str): Attribute to read
        
    Returns:
        None|Attribute Value
        
    """
    value = None
    if item.attribute_exists(attr_name):
        attr = item.get_attribute(attr_name)
        value = attr.get_string()

    return value

def set_str_attribute(attr, value):
    """Sets a string attribute
    
    Args:
        attr: Attribute object
        value (str): String to set
        
    """
    attr.set_string(value)

def create_custom_attribute(item, attr_type, attr_name):
    """Creates a custom attribute to the given object

    Args:
        item: Item to add attr to
        attr_type: ix.api.OfAttr.[TYPE]
        attr_name (str): Name of the attribute
    
    Returns:
        attribute
    """
    attr = item.add_attribute(attr_name, attr_type)
    return attr

def get_scatterer_geometry_attrs(self, scatterer):
    """Returns a list of geometry attributes
    
    Args:
        scatterer (SceneObjectScatterer): Scatter to list

    Returns:
        list: Geometry attributes  
    """
    attrs = []
    geo_attr = scatterer.get_attribute('geometry')
    for i in range(geo_attr.get_value_count()):
        geo_attr = scatterer.get_attribute('geometry')
        attrs.append(geo_attr)

    return attrs

# ______________________________________________________________________________________________________________________
# GEOMETRY

def get_geometries_from_scatterers(scatterers, return_count=False):
    """Returns a list of geometry objects from the given scatterers
    
    Args:
        scatterers (list): List of SceneObjectScatterers
        return_count (bool): If set, also returns the instance count of each geometry
        
    Returns:
        list, list: List of geometries, and optionally list of instance count

    """
    geometries = {}
    for _scatterer in scatterers:
        scatterer = _scatterer.get_module()
        instances_id = scatterer.get_instances()
        for i in range(scatterer.get_instance_count()):
            # Loop each scatter
            instance_id = instances_id.get_item(i)
            instance = scatterer.get_base_objects().get_item(instance_id)
            geometry = ix.get_item(instance.get_object_name())
            
            # Add the geo to the cache, keep count
            if geometry in geometries:
                geometries[geometry] = geometries[geometry] + 1
            else:
                geometries[geometry] = 1

    geometry_list = list(geometries.keys())
    instance_count = list(geometries.values())

    if return_count:
        return geometry_list, instance_count
    else:
        return geometry_list
    
def get_selection_box_definition(selection_box):
    """Gets a selection box's definition vectors and points
    
    Args:
        selection_box: Box Geometry
        
    Returns:
        dict: Selection box definition
        
    """
    
# ______________________________________________________________________________________________________________________
# MISC

def get_default_file_name():
    """Returns the default file name to be used if none is specified"""
    project_path = ix.application.get_current_project_filename()
    default_file_name = os.path.splitext(os.path.basename(project_path))[0] + '.ass'
    return default_file_name

def get_default_dir_path():
    """Returns the default file name to be used if none is specified"""
    project_path = ix.application.get_current_project_filename()
    default_dir_path = os.path.join(os.path.dirname(project_path), 'arnold_ass_export')
    default_dir_path = os.path.normpath(default_dir_path)
    return default_dir_path

def get_selected_objects():
    """Returns the selected objects"""
    return ix.selection

# ______________________________________________________________________________________________________________________
