import os, sys
from importlib import reload
sys.path.append(r'C:\Users\Michael\Documents\dev\clarisse')
import scatterertoarnold
reload(scatterertoarnold)
from scatterertoarnold import pkginfo
from scatterertoarnold.style import stylesheet
from scatterertoarnold.widgets.main import scattererToArnoldWidget, base, panelWidget, exportWindow
from scatterertoarnold.widgets.options import optionsWidget
from scatterertoarnold.widgets.scatterers import scattererWidget, scattererItemWidget
from scatterertoarnold.widgets.geometry import geometryWidget, geometryItemWidget
from scatterertoarnold.widgets.arnoldsettings import arnoldSettingsWidget
from scatterertoarnold.lib import libclarisse
from scatterertoarnold.core import clarisse_exporter, ass_generator, box_parser
from scatterertoarnold.configs import config
from scatterertoarnold.widgets.selection import selectionBoxWidget
reload(scattererToArnoldWidget)
reload(pkginfo)
reload(base)
reload(stylesheet)
reload(optionsWidget)
reload(panelWidget)
reload(scattererWidget)
reload(scattererItemWidget)
reload(geometryWidget)
reload(geometryItemWidget)
reload(libclarisse)
reload(clarisse_exporter)
reload(config)
reload(ass_generator)
reload(exportWindow)
reload(arnoldSettingsWidget)
reload(selectionBoxWidget)
reload(box_parser)
scatterertoarnold.launch()

"""
slot 0 {
    category "new_category" {
      shelf_item {
        title "Execute my item"
        description "my item"
        script_filename "./items/my_item.py"
        icon_filename "./icons/icon.png"
      }
    }
  }
"""