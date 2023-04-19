#!/usr/bin/env python
"""
    Name:           shelf_launcher.py
    Description:    Entry point from clarisse's shelf
 
"""
# System Imports
import os
import sys
import logging
import inspect

# Local Imports

# Third-Party Imports

# ______________________________________________________________________________________________________________________
      
def run_tool():
    """Runs the tool"""
    import scatterertoarnold
    scatterertoarnold.launch()

if __name__ == '__main__':
    run_tool()
        
# ______________________________________________________________________________________________________________________
