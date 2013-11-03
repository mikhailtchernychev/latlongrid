# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LatLonGrid
                                 A QGIS plugin
 Create Lat/lon grid based on layer extend
                             -------------------
        begin                : 2013-09-27
        copyright            : (C) 2013 by Mikhail Tchernychev
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "LatLonGrid"


def description():
    return "Create Lat/lon grid based on layer extend"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Mikhail Tchernychev"

def email():
    return "mikhail_tchernychev@yahoo.com"

def classFactory(iface):
    # load LatLonGrid class from file LatLonGrid
    from latlongrid import LatLonGrid
    return LatLonGrid(iface)
