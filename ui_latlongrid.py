# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_latlongrid.ui'
#
# Created: Mon Oct 14 15:58:58 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LatLonGrid(object):
    def setupUi(self, LatLonGrid):
        LatLonGrid.setObjectName(_fromUtf8("LatLonGrid"))
        LatLonGrid.setWindowModality(QtCore.Qt.ApplicationModal)
        LatLonGrid.resize(372, 307)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LatLonGrid.sizePolicy().hasHeightForWidth())
        LatLonGrid.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/latlongrid/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LatLonGrid.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(LatLonGrid)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(LatLonGrid)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.selected_layer = QtGui.QComboBox(LatLonGrid)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selected_layer.sizePolicy().hasHeightForWidth())
        self.selected_layer.setSizePolicy(sizePolicy)
        self.selected_layer.setObjectName(_fromUtf8("selected_layer"))
        self.horizontalLayout.addWidget(self.selected_layer)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(LatLonGrid)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.labels_format = QtGui.QComboBox(LatLonGrid)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labels_format.sizePolicy().hasHeightForWidth())
        self.labels_format.setSizePolicy(sizePolicy)
        self.labels_format.setObjectName(_fromUtf8("labels_format"))
        self.labels_format.addItem(_fromUtf8(""))
        self.labels_format.addItem(_fromUtf8(""))
        self.labels_format.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.labels_format)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.long_spacing_label = QtGui.QLabel(LatLonGrid)
        self.long_spacing_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.long_spacing_label.setObjectName(_fromUtf8("long_spacing_label"))
        self.horizontalLayout_3.addWidget(self.long_spacing_label)
        self.long_spacing = QtGui.QDoubleSpinBox(LatLonGrid)
        self.long_spacing.setDecimals(7)
        self.long_spacing.setSingleStep(0.01)
        self.long_spacing.setProperty(_fromUtf8("value"), 1.0)
        self.long_spacing.setObjectName(_fromUtf8("long_spacing"))
        self.horizontalLayout_3.addWidget(self.long_spacing)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.lat_spacing_label = QtGui.QLabel(LatLonGrid)
        self.lat_spacing_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lat_spacing_label.setObjectName(_fromUtf8("lat_spacing_label"))
        self.horizontalLayout_6.addWidget(self.lat_spacing_label)
        self.lat_spacing = QtGui.QDoubleSpinBox(LatLonGrid)
        self.lat_spacing.setDecimals(7)
        self.lat_spacing.setSingleStep(0.01)
        self.lat_spacing.setProperty(_fromUtf8("value"), 1.0)
        self.lat_spacing.setObjectName(_fromUtf8("lat_spacing"))
        self.horizontalLayout_6.addWidget(self.lat_spacing)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(LatLonGrid)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_9.addWidget(self.label_3)
        self.label_north = QtGui.QCheckBox(LatLonGrid)
        self.label_north.setChecked(True)
        self.label_north.setObjectName(_fromUtf8("label_north"))
        self.horizontalLayout_9.addWidget(self.label_north)
        self.label_south = QtGui.QCheckBox(LatLonGrid)
        self.label_south.setChecked(True)
        self.label_south.setObjectName(_fromUtf8("label_south"))
        self.horizontalLayout_9.addWidget(self.label_south)
        self.label_west = QtGui.QCheckBox(LatLonGrid)
        self.label_west.setChecked(True)
        self.label_west.setObjectName(_fromUtf8("label_west"))
        self.horizontalLayout_9.addWidget(self.label_west)
        self.label_east = QtGui.QCheckBox(LatLonGrid)
        self.label_east.setChecked(True)
        self.label_east.setObjectName(_fromUtf8("label_east"))
        self.horizontalLayout_9.addWidget(self.label_east)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_4 = QtGui.QLabel(LatLonGrid)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_8.addWidget(self.label_4)
        self.label_orientation = QtGui.QComboBox(LatLonGrid)
        self.label_orientation.setObjectName(_fromUtf8("label_orientation"))
        self.label_orientation.addItem(_fromUtf8(""))
        self.label_orientation.addItem(_fromUtf8(""))
        self.horizontalLayout_8.addWidget(self.label_orientation)
        self.font_button = QtGui.QPushButton(LatLonGrid)
        self.font_button.setObjectName(_fromUtf8("font_button"))
        self.horizontalLayout_8.addWidget(self.font_button)
        self.color_button = QtGui.QPushButton(LatLonGrid)
        self.color_button.setObjectName(_fromUtf8("color_button"))
        self.horizontalLayout_8.addWidget(self.color_button)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.grid_style_button = QtGui.QPushButton(LatLonGrid)
        self.grid_style_button.setObjectName(_fromUtf8("grid_style_button"))
        self.horizontalLayout_10.addWidget(self.grid_style_button)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.buttonBox = QtGui.QDialogButtonBox(LatLonGrid)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LatLonGrid)
        self.labels_format.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LatLonGrid.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LatLonGrid.reject)
        QtCore.QObject.connect(self.font_button, QtCore.SIGNAL(_fromUtf8("clicked()")), LatLonGrid.chooseFont)
        QtCore.QObject.connect(self.color_button, QtCore.SIGNAL(_fromUtf8("clicked()")), LatLonGrid.chooseColour)
        QtCore.QObject.connect(self.grid_style_button, QtCore.SIGNAL(_fromUtf8("clicked()")), LatLonGrid.chooseStyle)
        QtCore.QObject.connect(self.selected_layer, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), LatLonGrid.changeLayer)
        QtCore.QObject.connect(self.labels_format, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), LatLonGrid.changeFormat)
        QtCore.QMetaObject.connectSlotsByName(LatLonGrid)

    def retranslateUi(self, LatLonGrid):
        LatLonGrid.setWindowTitle(QtGui.QApplication.translate("LatLonGrid", "Latitude / Longitude grid lines", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LatLonGrid", "Select existing layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_layer.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Select layer to use for extend of lat/lon grid", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LatLonGrid", "Grid labels format:", None, QtGui.QApplication.UnicodeUTF8))
        self.labels_format.setToolTip(QtGui.QApplication.translate("LatLonGrid", "<html><head/><body><p>Select label format. Grid interval specified below is based on this selection</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labels_format.setItemText(0, QtGui.QApplication.translate("LatLonGrid", "Decimal degrees", None, QtGui.QApplication.UnicodeUTF8))
        self.labels_format.setItemText(1, QtGui.QApplication.translate("LatLonGrid", "Decimal degress and minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.labels_format.setItemText(2, QtGui.QApplication.translate("LatLonGrid", "Decimal degress, minutes and seconds", None, QtGui.QApplication.UnicodeUTF8))
        self.long_spacing_label.setText(QtGui.QApplication.translate("LatLonGrid", "Longitude spacing, deg:", None, QtGui.QApplication.UnicodeUTF8))
        self.long_spacing.setToolTip(QtGui.QApplication.translate("LatLonGrid", "<html><head/><body><p>Longitude grid step in dec. degrees, minutes or second based on format</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lat_spacing_label.setText(QtGui.QApplication.translate("LatLonGrid", "Latitude spacing, deg:", None, QtGui.QApplication.UnicodeUTF8))
        self.lat_spacing.setToolTip(QtGui.QApplication.translate("LatLonGrid", "<html><head/><body><p>Latitude grid step in dec. degrees, minutes or second based on format</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LatLonGrid", "Labels:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_north.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Check this box to display north labels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_north.setText(QtGui.QApplication.translate("LatLonGrid", "North", None, QtGui.QApplication.UnicodeUTF8))
        self.label_south.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Check this box to display south  labels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_south.setText(QtGui.QApplication.translate("LatLonGrid", "South", None, QtGui.QApplication.UnicodeUTF8))
        self.label_west.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Check this box to display west labels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_west.setText(QtGui.QApplication.translate("LatLonGrid", "West", None, QtGui.QApplication.UnicodeUTF8))
        self.label_east.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Check this box to display east labels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_east.setText(QtGui.QApplication.translate("LatLonGrid", "East", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("LatLonGrid", "Label orientation:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_orientation.setToolTip(QtGui.QApplication.translate("LatLonGrid", "<html><head/><body><p>Label orientation relatively to the frame</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_orientation.setItemText(0, QtGui.QApplication.translate("LatLonGrid", "Perpendicular", None, QtGui.QApplication.UnicodeUTF8))
        self.label_orientation.setItemText(1, QtGui.QApplication.translate("LatLonGrid", "Parallel", None, QtGui.QApplication.UnicodeUTF8))
        self.font_button.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Select label font", None, QtGui.QApplication.UnicodeUTF8))
        self.font_button.setText(QtGui.QApplication.translate("LatLonGrid", "Font...", None, QtGui.QApplication.UnicodeUTF8))
        self.color_button.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Select label color", None, QtGui.QApplication.UnicodeUTF8))
        self.color_button.setText(QtGui.QApplication.translate("LatLonGrid", "Color...", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_style_button.setToolTip(QtGui.QApplication.translate("LatLonGrid", "Set grid lines style", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_style_button.setText(QtGui.QApplication.translate("LatLonGrid", "Set grid style...", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
