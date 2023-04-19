#!/usr/bin/env python
"""
    Name:           config.py
    Description:    Main configuration file for the tool
 
"""
# System Imports
import os
import sys
import logging

# Third-Party Imports

# Local Imports

# ______________________________________________________________________________________________________________________

# Constants
ATTR_ASS_FILE = 'Ass_File_Representation'
ATTR_ASSET_CODE = 'Asset_Code_Representation'

GROUPINGS = {
    'all': 'All under one file',
    'scatterer':  'One file per scatterer',
    'asset': 'One file per asset'
}

SELECTION_TYPES = {
    'no_selection': 'No Selection',
    'inclusive': 'Inclusive Selection',
    'exclusive': 'Exclusive Selection'
}

# Default export values
DEFAULT_GROUPING = 'all'
DEFAULT_SELECTION_TYPE = 'no_selection'


# ______________________________________________________________________________________________________________________
