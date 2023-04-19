# ScattererToArnold

Github: https://github.com/mikesided/scatterertoarnold

# Table of contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
    1. [Requirements](#requirements)
    1. [Package](#package)
    1. [Shelf](#shelf)
4. [Screenshots](#screenshots)

## Introduction <a name="introduction"></a>
In order to use clarisse's scatterer system to quickly generate setdresses for an Arnold based project, this tool was developped to simplify the ingest of the setdress back into Maya.

As it stands, the only requirement is that each geometry present in the exported point clouds must have an .ass file exported in advance. The tool will let you select your .ass file for each individual geometry, and build the resulting .ass file using procedurals.

It is possible to integrate this to your own tools using only the core classes.

## Features <a name="features"></a>
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


### Requirements
- Clarisse iFX 5+ (Developped & Tested on 5.0 SP11)
- Python 3


## Installation <a name="installation"></a>

### Requirements <a name="requirements"></a>
You will need packages specified in `requirements.txt` to be present in your clarisse environment. Assuming that clarisse launches on your default python installation, located in your PATH environment variable, you can browse to the cloned repository's location, and install requirements:

`python -m  pip install -r requirements.txt`

### Package <a name="package"></a>
The package `scatterertoarnold` must also be present in your PYTHONPATH environment variables. There are a few ways you can do this:
- Add the package to $CLARISSE_INSTALL_PATH/Clarisse/python3 (Requires admin)
- Add the package to $PYTHON_INSTALL_PATH/lib/site-packages
- Add the package's parent folder's path to your clarisse.env
- Append the package's parent folder's path to your local PYTHONPATH variable

### Shelf <a name="shelf"></a>
To add the shelf icon, you can browse to your local `shelf.cfg` file and add a new slot for the tool.\ 
On Windows, this file is located here: `%appdata%\Isotropix\Clarisse\5.0\shelf.cfg`\
The final result will look like this, for a blank shelf.cfg\
__(Make sure to replace the `script_filename` and `icon_filename` according to your installation)__

shelf {\
&emsp;slot_selected 0\
&emsp;category_selected "General"\
&emsp;show_toolbar yes\
&emsp;style 0\
&emsp;view_mode 0\
&emsp;slot 0 {\
&emsp;&emsp;category "ScattererToArnold" {\
&emsp;&emsp;&emsp;shelf_item {\
&emsp;&emsp;&emsp;&emsp;title "ScattererToArnold"\
&emsp;&emsp;&emsp;&emsp;description "Launch the ScattererToArnold Tool"\
&emsp;&emsp;&emsp;&emsp;script_filename "C:/Users/Michael/Documents/dev/scatterertoarnold/scatterertoarnold/shelf_launcher.py"\
&emsp;&emsp;&emsp;&emsp;icon_filename "C:/Users/Michael/Documents/dev/scatterertoarnold/resources/img/icon.png"\
&emsp;&emsp;&emsp;}\
&emsp;&emsp;}\
&emsp;}\
}


## Screenshots <a name="screenshots"></a>
![Main Tool View](https://github.com/mikesided/scatterertoarnold/blob/main/resources/img/tool_main_view.png)
![Export Process View](https://github.com/mikesided/scatterertoarnold/blob/main/resources/img/tool_export_process.png)

