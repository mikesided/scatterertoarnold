# ScattererToArnold

Github: https://github.com/mikesided/scatterertoarnold

In order to use clarisse's scatterer system to quickly generate setdresses for an Arnold based project, this tool was developped to simplify the ingest of the setdress back into Maya.

As it stands, the only requirement is that each geometry present in the exported point clouds must have an .ass file exported in advance. The tool will let you select your .ass file for each individual geometry, and build the resulting .ass file using procedurals.

It is possible to integrate this to your own tools using only the core classes.

## Features
- Granularly select scatterers to export
- Granularly select geometries to export (fetched from selected scatterer's pointclouds)
- Set an .ass file representation of each geometry (saved to the geo's attributes)
- Select n number of cube geometries to act as a "point cloud" selection.
	- Use these "selection boxes" as an "Inclusive" selection, or "Exclusive" selection
- Override any default .ass file parameter values
- Multiple export formats:
	- Export all under one file
	- Export one .ass file per scatterer
	- Export one .ass file per geometry


## Requirements
- Clarisse iFX 5+ (Developped & Tested on 5.0 SP11)
- Python 3


## Installation
You will need packages specified in `requirements.txt` to be present in your clarisse environment. Assuming that clarisse launches on your default python installation, located in your PATH environment variable, you can browse to the cloned repository's location, and install requirements:

`python -m  pip install -r requirements.txt`

The package `scatterertoarnold` must also be present in your PYTHONPATH environment variables. There are a few ways you can do this:
- Add the package to $CLARISSE_INSTALL_PATH/Clarisse/python3 (Requires admin)
- Add the package to $PYTHON_INSTALL_PATH/lib/site-packages
- Add the package's parent folder's path to your clarisse.env
- Append the package's parent folder's path to your local PYTHONPATH variable

## Main Tool View
![Main Tool View](https://github.com/mikesided/scatterertoarnold/blob/main/resources/img/tool_main_view.png)
![Export Process View](https://github.com/mikesided/scatterertoarnold/blob/main/resources/img/tool_export_process.png)

