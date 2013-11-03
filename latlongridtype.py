"""
***************************************************************************
 LatLonGridType - registers itself to Quantum as a Plugin Layer
                                 A QGIS plugin
 Overlays a user-definable grid on the map.
                             -------------------
        begin                : 10/01/2013
        copyright            : (C) 2013 Mikhail Tchernychev
        email                : mikhail_tchernychev@yahoo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis import core
from latlongridlayer  import LatLonGridLayer


class LatLonGridType(core.QgsPluginLayerType):
    def __init__(self):
        core.QgsPluginLayerType.__init__(self, LatLonGridLayer.LAYER_TYPE)
    
    def createLayer(self):
        return LatLonGridLayer()

    def showLayerProperties(self, layer):
        layer.showDialog()
        return True
