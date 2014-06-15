"""
***************************************************************************
 LatLonGridLayer - manages and draws an overlay grid.
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


import math

from qgis.core import *
import qgis.utils

from PyQt4.QtGui import QProgressBar
from PyQt4 import QtCore, QtGui, QtXml
from qgis.core import QGis
#from util import *

from PyQt4.QtGui import *
from qgis import core, gui
from PyQt4.QtCore import *

from qgis.gui import QgsMessageBar


from latlongriddialog import LatLonGridDialog


def convertDMS(dms,hemis, type, digits):
  
    if dms > 0:
        hemi=hemis[0]
    else:
        hemi=hemis[1]
        dms=-dms
        
    if type == 0:
        return '{0:.{dec}F}\xb0{1}'.format(dms, hemi, dec=digits)
          
    d = int(dms)
    ms = (dms-d) * 60.0
    
    if type == 1:
        return '{0:d}\xb0{1:.{dec}F}\'{2}'.format(d, ms, hemi, dec=digits)
    
    m = int(ms)
    s = (ms - m) * 60.0
    return '{0:d}\xb0{1}\'{2:.{dec}F}\"{3}'.format(d, m, s, hemi, dec=digits)



class LatLonGridLayer (core.QgsPluginLayer):
    LAYER_TYPE = 'LatLonGrid'

    _featuremap = {
        0: core.QgsField('angle', QtCore.QVariant.Double, 'double', 8, 4),
        1: core.QgsField('ordinate', QtCore.QVariant.String, 'string', 32),
        2: core.QgsField('alignment', QtCore.QVariant.String, 'string', 8),
        3: core.QgsField('offset_x', QtCore.QVariant.Double, 'double', 8, 4),
        4: core.QgsField('offset_y', QtCore.QVariant.Double, 'double', 8, 4)
        }

    def __init__(self):
        core.QgsPluginLayer.__init__(self, LatLonGridLayer.LAYER_TYPE,
                                     'Lat/Lon grid overlay')
        self.setValid(True)
               
        self.parent_layer_name = ""
        self.parent_layer_id   = ""
        
        #dialog
        self.dlg = LatLonGridDialog(self)
        
        # connect slot for parent removal
        QgsMapLayerRegistry.instance().layerRemoved.connect(self.RemovingParentSlot)
        
        # use dialog boxes or status
        self.use_dialogs = False
                
        # grid itlesf
        self.ll_grid = []
        
        # step size in decimal degrees
        self.step = 0.01
        
        #labels positions
        
        self.labels_S = []
        self.labels_N = []      
        self.labels_W = []
        self.labels_E = []
        
        # label to draw
        #fields = QgsFields()
        #self.label = core.QgsLabel(fields)
        #self.label = core.QgsLabel(LatLonGridLayer._featuremap)
        
        
        #eature.setAttribute(core.QgsLabel.Text, "sasasas")
        
        
        self.fields = QgsFields()    
        self.label = QgsLabel(self.fields)                  
 
        #self.label.labelAttributes().setText('test label')
        
        self.label_features = []
        
        #self.label.labelAttributes().setOffset(-8.66774, 37.08391, 0)
 
        #self.feat.setAttribute(0,'Test Text')
        #self.feat.setAttribute('8', -8.66774)
        #self.feat.setAttribute('9', 37.08391)
                
    def showDialog(self):
        
        # test if layers are available
        nLayers = 0

        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == QgsMapLayer.PluginLayer :
                continue
            nLayers += 1
        
        if nLayers == 0 :   
            text = "No layers avalaible to create Lat/Lon grid.\nOnly vector and raster layers can be used.\n\n Please add layers to QGIS project!"
            if self.use_dialogs :
                QtGui.QMessageBox.information(None,'Warning', text,  QMessageBox.Ok)
            else :
                qgis.utils.iface.messageBar().pushMessage("Warning", text, QgsMessageBar.WARNING, 5)
                
            self.setValid(False)
            return 
        
        # see if on the fly projection is enabled

        is_defined = QgsProject.instance().readEntry("SpatialRefSys", "/ProjectionsEnabled")[1]
        
        if not is_defined or int(QgsProject.instance().readEntry("SpatialRefSys", "/ProjectionsEnabled")[0]) == 0:
            if self.use_dialogs :
                QtGui.QMessageBox.information(None,'Cannot add lat/lon grid', """Lat/Lon grid alsways uses geograhical coordinates.\n\nPlease enable projection 'on the fly' CRS transformation in project settings!""",  QMessageBox.Ok)
            else :
                qgis.utils.iface.messageBar().pushMessage("Cannot add lat/lon grid", """Lat/Lon grid alsways uses geograhical coordinates.\n\nPlease enable projection 'on the fly' CRS transformation in project settings!""", QgsMessageBar.WARNING, 5)
              
            self.setValid(False)
            return           
        
        self.get_layer_name_by_id()
        
        self.dlg.show()
        result = self.dlg.exec_()
     
        if result == 1:
            self.get_layer_id_by_name()
            #self.generateGrid()
            self.setValid(True)
            self.setLatLonGridCrsAndExtent()
            self.generateLatLonGrid()
            self.setCacheImage(None)
            self.emit(QtCore.SIGNAL('repaintRequested()'))
        else:
            self.setValid(False)  

    def draw(self, renderContext):
        
        
        if self.CheckLayerExtent() == False :
            self.setLatLonGridCrsAndExtent()
            self.generateLatLonGrid()
        
        mapToPixel = renderContext.mapToPixel()

        proj = core.QgsProject.instance()
        # Default CRS: 3452 == EPSG:4326
        srid = proj.readNumEntry('SpatialRefSys', '/ProjectCRSID', 3452)[0]
        crs = core.QgsCoordinateReferenceSystem(srid, core.QgsCoordinateReferenceSystem.InternalCrsId)

        xform = core.QgsCoordinateTransform(self.crs(), crs)

        self.dlg.symbol.startRender(renderContext)

        for line in self.ll_grid:
            
            polyline = QtGui.QPolygonF()

            for vertex in line:
                end = mapToPixel.transform(xform.transform(vertex))
                polyline.append(QtCore.QPointF(end.x(), end.y()))

                if QGis.QGIS_VERSION_INT < 10800:
                    self.dlg.symbol.renderPolyline(polyline, renderContext)
                else:
                    self.dlg.symbol.renderPolyline(polyline, None, renderContext)

        if QGis.QGIS_VERSION_INT > 20200 :
            self.drawLabels(renderContext)
        
        self.dlg.symbol.stopRender(renderContext)

        return True

    def drawLabels(self, renderContext):
        
        self.label.setLabelField(QgsLabel.Text,QgsLabel.Text)
        self.label.setLabelField(QgsLabel.Angle,QgsLabel.Angle)
        self.label.setLabelField(QgsLabel.Alignment,QgsLabel.Alignment)
        self.label.setLabelField(QgsLabel.XOffset,QgsLabel.XOffset)
        self.label.setLabelField(QgsLabel.YOffset,QgsLabel.YOffset)
        
        for feat in self.label_features :
            self.label.renderLabel(renderContext, feat, False)
        return
        
    def writeXml(self, node, doc):
        element = node.toElement()
        element.setAttribute('type', 'plugin')
        element.setAttribute('name', LatLonGridLayer.LAYER_TYPE);
        
        # custom properties
        gridElement = doc.createElement('latlongrid')
               
        gridElement.setAttribute('parent_layer', str(self.parent_layer_id))
        
        gridElement.setAttribute('label_format', str(self.dlg.ui.labels_format.currentIndex()))
    
        gridElement.setAttribute('long_spacing', str(self.dlg.ui.long_spacing.value()))
        gridElement.setAttribute('lat_spacing',  str(self.dlg.ui.lat_spacing.value()))
        
        gridElement.setAttribute('label_north', str(self.dlg.ui.label_north.isChecked())) 
        gridElement.setAttribute('label_south', str(self.dlg.ui.label_south.isChecked())) 
        gridElement.setAttribute('label_west',  str(self.dlg.ui.label_west.isChecked()))
        gridElement.setAttribute('label_east',  str(self.dlg.ui.label_east.isChecked()))
        
        gridElement.setAttribute('label_orientation', str(self.dlg.ui.label_orientation.currentIndex()))
        
        node.appendChild(gridElement)
        
        # write font
        
        gridElement = doc.createElement('latlongrid_font')
        gridElement.setAttribute('farmily',    str(self.dlg.label_attributes.family()))
        gridElement.setAttribute('bold',       str(self.dlg.label_attributes.bold()))
        gridElement.setAttribute('italic',     str(self.dlg.label_attributes.italic()))
        gridElement.setAttribute('underline',  str(self.dlg.label_attributes.underline()))
        gridElement.setAttribute('strikeOut',  str(self.dlg.label_attributes.strikeOut()))
        gridElement.setAttribute('size',       str(self.dlg.label_attributes.size()))
        gridElement.setAttribute('color',      str(self.dlg.label_attributes.color().rgba()))
                 
        node.appendChild(gridElement)
  
        self.writeSymbology(node, doc)
    
        # write extend
        
        gridElement = doc.createElement('latlongrid_extend')
        gridElement.setAttribute('xmin',    str(core.QgsPluginLayer.extent(self).xMinimum()))
        gridElement.setAttribute('xmax',    str(core.QgsPluginLayer.extent(self).xMaximum()))
        gridElement.setAttribute('ymin',    str(core.QgsPluginLayer.extent(self).yMinimum()))
        gridElement.setAttribute('ymax',    str(core.QgsPluginLayer.extent(self).yMaximum()))       
        node.appendChild(gridElement)
 
        return True
 

    def writeSymbology(self, node, doc):
        symbolElement = core.QgsSymbolLayerV2Utils.saveSymbol('grid_lines', self.dlg.symbol, doc)
        node.appendChild(symbolElement)
        return True


        
    def readXml(self, node):
        
        element = node.toElement()
        
        gridElement = node.firstChildElement('latlongrid')
        
        if gridElement is not None:
            
            
            self.parent_layer_id = str(gridElement.attribute('parent_layer'))
            self.dlg.ui.labels_format.setCurrentIndex(int(gridElement.attribute('label_format')))
            
            self.dlg.ui.long_spacing.setValue(float(gridElement.attribute('long_spacing')))
            self.dlg.ui.lat_spacing.setValue(float(gridElement.attribute('lat_spacing')))
            
            self.dlg.ui.label_north.setChecked('True'== gridElement.attribute('label_north', 'False'))
            self.dlg.ui.label_south.setChecked('True'== gridElement.attribute('label_south', 'False')) 
            self.dlg.ui.label_west.setChecked('True'==  gridElement.attribute('label_west', 'False'))
            self.dlg.ui.label_east.setChecked('True'==  gridElement.attribute('label_east', 'False'))
        
            self.dlg.ui.label_orientation.setCurrentIndex(int(gridElement.attribute('label_orientation')))
          
         
         
        gridElement = node.firstChildElement('latlongrid_font')
        
        if gridElement is not None: 
            self.dlg.label_attributes.setFamily(str(gridElement.attribute('farmily')))
            self.dlg.label_attributes.setBold('True'== gridElement.attribute('bold', 'False'))
            self.dlg.label_attributes.setItalic('True'== gridElement.attribute('italic', 'False'))
            self.dlg.label_attributes.setUnderline('True'== gridElement.attribute('underline', 'False'))
            self.dlg.label_attributes.setStrikeOut('True'== gridElement.attribute('strikeOut', 'False'))
            self.dlg.label_attributes.setSize(float(gridElement.attribute('size')), core.QgsLabelAttributes.PointUnits)
            self.dlg.label_attributes.setColor(QtGui.QColor.fromRgba(int(gridElement.attribute('color'))))         
           
        self.readSymbology(node)
                
        gridElement = node.firstChildElement('latlongrid_extend')
        
        if gridElement is not None:             
            rect = QgsRectangle();
            rect.setXMinimum(float(gridElement.attribute('xmin')))
            rect.setXMaximum(float(gridElement.attribute('xmax')))
            rect.setYMinimum(float(gridElement.attribute('ymin')))
            rect.setYMaximum(float(gridElement.attribute('ymax')))
            self.setExtent(rect);
            self.generateLatLonGrid()     
  
                
                
        return True
        
        
        
    def readSymbology(self, node):
        symbolElement = node.firstChildElement('symbol')

        if symbolElement is not None and symbolElement.attribute('name') == 'grid_lines':
            self.dlg.symbol = core.QgsSymbolLayerV2Utils.loadSymbol(symbolElement)
            self.setCacheImage(None)
            self.emit(QtCore.SIGNAL('repaintRequested()'))
            return True
        else:
            return False
            

    def get_layer_id_by_name(self) :

        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == QgsMapLayer.PluginLayer and layer.pluginLayerType() == LatLonGridLayer.LAYER_TYPE :
                continue
            if layer.name() == self.parent_layer_name :
                self.parent_layer_id = layer.id()
                break
                
                
    def get_layer_name_by_id(self) :

        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == QgsMapLayer.PluginLayer and layer.pluginLayerType() == LatLonGridLayer.LAYER_TYPE :
                continue
            if layer.id() == self.parent_layer_id :
                self.parent_layer_name = layer.name()
                break               
                
                
    def RemovingParentSlot(self, parent_id) :
        
        try: 
            if parent_id == self.parent_layer_id:
             text = "Lat/Lon grid layer '" + self.name() + "'\nwas removed because its parent has been removed!"
             
             if self.use_dialogs :
                QtGui.QMessageBox.information(None,'Warning', text,  QMessageBox.Ok)
             else :
               qgis.utils.iface.messageBar().pushMessage("Warning", text, QgsMessageBar.WARNING, 5)
 
             QgsMapLayerRegistry.instance().removeMapLayer(self.id())
             
        except:     
            print "No layer exists..."
            
            
    def get_parent_layer(self, parent_layer):
        
        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == QgsMapLayer.PluginLayer and layer.pluginLayerType() == LatLonGridLayer.LAYER_TYPE :
                continue
            if layer.id() == self.parent_layer_id :
                parent_layer = layer
                return True
                
        return False        
        
        
    def setLatLonGridCrsAndExtent(self) :
        
        layer = QgsMapLayerRegistry.instance().mapLayer(self.parent_layer_id)
        
        # for vector layers
        if layer.type() == QgsMapLayer.VectorLayer :
            layer.updateExtents()
        
        if layer == None :
            text = "Cannot get parent layer for Lat/Lon grid !\nLat/Lon CRS not set!"
            QtGui.QMessageBox.information(None,'Warning', text,  QMessageBox.Ok)
            return
            
        if layer.crs().geographicFlag() == False:  # deal with projected CRS
            proj_str = "+proj=longlat +datum=" + layer.crs().ellipsoidAcronym() + " +no_defs"
            geo_system = QgsCoordinateReferenceSystem()
            geo_system.createFromProj4(proj_str)
            core.QgsPluginLayer.setCrs(self, geo_system)
            
            transform  = QgsCoordinateTransform(layer.crs(), geo_system)
            core.QgsPluginLayer.setExtent(self, transform.transform(layer.extent()))
            return
            
        # if parent layer is lat/lon CRS, use it
        
        core.QgsPluginLayer.setCrs(self, layer.crs())   
        core.QgsPluginLayer.setExtent(self, layer.extent())
 
    def CheckLayerExtent(self) :
        
        layer = QgsMapLayerRegistry.instance().mapLayer(self.parent_layer_id)
        
        # for vector layers
        if layer.type() == QgsMapLayer.VectorLayer :
            layer.updateExtents()
            
        if layer.extent().xMinimum() == core.QgsPluginLayer.extent(self).xMinimum() and \
           layer.extent().xMaximum() == core.QgsPluginLayer.extent(self).xMaximum() and \
           layer.extent().yMinimum() == core.QgsPluginLayer.extent(self).yMinimum() and \
           layer.extent().yMaximum() == core.QgsPluginLayer.extent(self).yMaximum() :
               return True
       
        return False
    
    
    def generateLatLonGrid(self) :
        
        self.ll_grid = []
        
        dx = self.dlg.ui.long_spacing.value()
        dy = self.dlg.ui.lat_spacing.value()
        
        x1 = core.QgsPluginLayer.extent(self).xMinimum()/dx
        y1 = core.QgsPluginLayer.extent(self).yMinimum()/dy
        x2 = core.QgsPluginLayer.extent(self).xMaximum()/dx
        y2 = core.QgsPluginLayer.extent(self).yMaximum()/dy
  
        #progressMessageBar = self.iface.messageBar().createMessage("Generating Lat/Lon grid...")
        #progress = QProgressBar()
        #progress.setMaximum(100)
        #progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        #progressMessageBar.layout().addWidget(progress)
        #self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
        
        #i_progress = 0;
                
        scale = 1.
        
        # x1, y1 x2, y2 in lat / lon, transate in selected units
        
        if self.dlg.ui.labels_format.currentIndex() == 1 : # minutes
            x1   *= 60.
            y1   *= 60.
            x2   *= 60.
            y2   *= 60.
            scale = 60.
        elif self.dlg.ui.labels_format.currentIndex() == 2: # seconds
            x1   *= 3600.
            y1   *= 3600.
            x2   *= 3600.
            y2   *= 3600.
            scale = 3600.
            
 
        x1 = round(x1)
        y1 = round(y1)
        x2 = round(x2)
        y2 = round(y2)
  
        if x2 - x1 > 1000 or y2 - y1 > 1000 :
            
            text = "Too many Lat/Lon lines! Cannot update view!"
            if self.use_dialogs :
                QtGui.QMessageBox.information(None,'Warning', text,  QMessageBox.Ok)
            else :
                qgis.utils.iface.messageBar().pushMessage("Warning", text, QgsMessageBar.WARNING, 10)
                
            return
            

        self.labels_S = []
        self.labels_N = []      
        self.labels_W = []
        self.labels_E = []
        
        # horizontal lines
        
        if y1 < scale*core.QgsPluginLayer.extent(self).yMinimum()/dy : y1 += 1
        if y2 > scale*core.QgsPluginLayer.extent(self).yMaximum()/dy : y2 -= 1
        
        
        yt = y1
        
        while yt <= y2 :
            line = []
            xt1 = core.QgsPluginLayer.extent(self).xMinimum()
            i = 1
            bContinue = True
            line.append(core.QgsPoint(xt1, dy*yt/scale));
            
            self.labels_W.append([xt1, (dy*yt/scale)])
            
            while bContinue:   
               xt2 =  xt1 + self.step * i
               if xt2 > core.QgsPluginLayer.extent(self).xMaximum() :
                   xt2 = core.QgsPluginLayer.extent(self).xMaximum()
                   bContinue = False
                   self.labels_E.append([xt2, (dy*yt/scale)])
                   
               line.append(core.QgsPoint(xt2, dy*yt/scale));    
               i += 1
            self.ll_grid.append(line)
            
            yt += 1
            
            #i_progress += 1
            #progress.setValue(i_progress)
            
        # vertical lines
    
        if x1 < scale*core.QgsPluginLayer.extent(self).xMinimum()/dx : x1 += 1
        if x2 > scale*core.QgsPluginLayer.extent(self).xMaximum()/dx : x2 -= 1
    
        xt = x1
        
        while xt <= x2:
            line = []
            yt1 = core.QgsPluginLayer.extent(self).yMinimum()
            i = 1
            bContinue = True
            line.append(core.QgsPoint(dx*xt/scale, yt1));
            
            self.labels_S.append([(dx*xt/scale), yt1])
                        
            while bContinue:   
               yt2 =  yt1 + self.step * i
               if yt2 > core.QgsPluginLayer.extent(self).yMaximum() :
                   yt2 = core.QgsPluginLayer.extent(self).yMaximum()
                   bContinue = False
                   self.labels_N.append([(dx*xt/scale), yt2])
            
               line.append(core.QgsPoint(dx*xt/scale, yt2));    
               i += 1
            self.ll_grid.append(line)
            xt += 1
        
        #self.iface.messageBar().clearWidgets()
        self.generateLabels()
        
        
    def generateLabels(self) :
        
        self.label.labelAttributes().setFamily(self.dlg.label_attributes.family())
        self.label.labelAttributes().setBold(self.dlg.label_attributes.bold())
        self.label.labelAttributes().setItalic(self.dlg.label_attributes.italic())
        self.label.labelAttributes().setUnderline(self.dlg.label_attributes.underline())
        self.label.labelAttributes().setStrikeOut(self.dlg.label_attributes.strikeOut())
        self.label.labelAttributes().setSize(self.dlg.label_attributes.size(), core.QgsLabelAttributes.PointUnits)
        self.label.labelAttributes().setColor(QtGui.QColor.fromRgba(self.dlg.label_attributes.color().rgba()))
    
        self.label_features = []
    
        x_digits = 0;
        a = math.log(float(self.dlg.ui.long_spacing.value()))/math.log(10.)
        if a < 0 :
            x_digits = int(round(math.fabs(a)))
        
        y_digits = 0;
        a = math.log(float(self.dlg.ui.lat_spacing.value()))/math.log(10.)
        if a < 0 :
            y_digits = int(round(math.fabs(a)))
            
    
        if self.dlg.ui.label_south.isChecked() :
            for pos in self.labels_S :
                
                fields = QgsFields()
                feat =  QgsFeature(fields)
                feat.initAttributes(QgsLabel.LabelFieldCount)
                
                feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(pos[0], pos[1])))        
        
                if self.dlg.ui.label_orientation.currentIndex() == 0 :
                    feat.setAttribute(QgsLabel.Angle,90.)
                    feat.setAttribute(QgsLabel.Alignment, 'right')
                    feat.setAttribute(QgsLabel.XOffset, -2)
                else :
                    feat.setAttribute(QgsLabel.Angle,0.)
                    feat.setAttribute(QgsLabel.Alignment, 'center|top')
                
                feat.setAttribute(QgsLabel.Text, convertDMS(pos[0], "EW", self.dlg.ui.labels_format.currentIndex(), x_digits))
                
                self.label_features.append(feat)
                
        if self.dlg.ui.label_north.isChecked() :
            for pos in self.labels_N :
                
                fields = QgsFields()
                feat =  QgsFeature(fields)
                feat.initAttributes(QgsLabel.LabelFieldCount)
                
                feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(pos[0], pos[1])))        
        
                if self.dlg.ui.label_orientation.currentIndex() == 0 :
                    feat.setAttribute(QgsLabel.Angle,90.)
                    feat.setAttribute(QgsLabel.Alignment, 'left')
                    feat.setAttribute(QgsLabel.XOffset, 2)
                else :
                    feat.setAttribute(QgsLabel.Angle,0.)
                    feat.setAttribute(QgsLabel.Alignment, 'center|bottom')
                    feat.setAttribute(QgsLabel.YOffset, 2)
                
                feat.setAttribute(QgsLabel.Text, convertDMS(pos[0], "EW", self.dlg.ui.labels_format.currentIndex(), x_digits))
                
                self.label_features.append(feat) 
   
        if self.dlg.ui.label_west.isChecked() :
            for pos in self.labels_W :
                
                fields = QgsFields()
                feat =  QgsFeature(fields)
                feat.initAttributes(QgsLabel.LabelFieldCount)
                
                feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(pos[0], pos[1])))        
        
                if self.dlg.ui.label_orientation.currentIndex() == 0 :
                    feat.setAttribute(QgsLabel.Angle,0.)
                    feat.setAttribute(QgsLabel.Alignment, 'right')
                    feat.setAttribute(QgsLabel.XOffset, -2)
                else :
                    feat.setAttribute(QgsLabel.Angle,90.)
                    feat.setAttribute(QgsLabel.Alignment, 'center|bottom')
                    feat.setAttribute(QgsLabel.YOffset, 2)
                
                feat.setAttribute(QgsLabel.Text, convertDMS(pos[1], "NS", self.dlg.ui.labels_format.currentIndex(), y_digits))
                
                self.label_features.append(feat)  
               
              
        if self.dlg.ui.label_east.isChecked() :
            for pos in self.labels_E :
                
                fields = QgsFields()
                feat =  QgsFeature(fields)
                feat.initAttributes(QgsLabel.LabelFieldCount)
                
                feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(pos[0], pos[1])))        
        
                if self.dlg.ui.label_orientation.currentIndex() == 0 :
                    feat.setAttribute(QgsLabel.Angle,0.)
                    feat.setAttribute(QgsLabel.Alignment, 'left')
                    feat.setAttribute(QgsLabel.XOffset, 2)
                else :
                    feat.setAttribute(QgsLabel.Angle,90.)
                    feat.setAttribute(QgsLabel.Alignment, 'center|top')
                
                feat.setAttribute(QgsLabel.Text, convertDMS(pos[1], "NS", self.dlg.ui.labels_format.currentIndex(),y_digits))
                
                self.label_features.append(feat)                
 
  
    
