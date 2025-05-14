from .pyqtgraph_vini.Qt import QtCore, QtGui
import numpy as np
import math
import os
import time
import copy
import sys, os.path

from .pyqtgraph_vini import *

from .ColorMapWidget import *
from .testInputs import testFloat, testInteger


class SettingsDialog(QtGui.QDialog):
    """
    Settings dialog window
    """

    sigSaveSettings = QtCore.Signal()
    sigWindowSize = QtCore.Signal()

    def __init__(self, pref):
        super(SettingsDialog, self).__init__()

        self.preferences = pref

        self.layout = QtGui.QGridLayout()

        self.qtab = QtGui.QTabWidget()
        self.tab_view = QtGui.QWidget()
        self.tab_color = QtGui.QWidget()
        self.tab_resample = QtGui.QWidget()
        self.tab_search = QtGui.QWidget()

        # View Options
        self.l_view = QtGui.QFormLayout()
        self.tab_view.setLayout(self.l_view)
        self.voxel_cb = QtGui.QCheckBox()
        self.l_view.addRow("Use voxel coordinates by default:", self.voxel_cb)
        self.link_menu = QtGui.QComboBox()
        self.link_menu.addItem("link zoom and panning")
        self.link_menu.addItem("unlinked views")
        self.l_view.addRow("Use as default link mode:", self.link_menu)
        self.savesize_button = QtGui.QPushButton("Start with current window size")
        self.savesize_button.clicked.connect(self.saveWindowSize)
        self.l_view.addRow("Save window size:", self.savesize_button)

        # Color maps
        self.l_color = QtGui.QFormLayout()
        self.tab_color.setLayout(self.l_color)
        self.gradient_underlay = ColorMapWidgetObj()
        self.l_color.addRow("Color map underlays:", self.gradient_underlay)
        self.gradient_overlay_pos = ColorMapWidgetObj()
        self.l_color.addRow(
            'Default positive color map for overlays:',
            self.gradient_overlay_pos)
        self.gradient_overlay_neg = ColorMapWidgetObj()
        self.l_color.addRow(
            'Default negative color map for overlays:',
            self.gradient_overlay_neg)
        self.clip_cb_under_high = QtGui.QCheckBox()
        self.clip_cb_under_low = QtGui.QCheckBox()
        self.clip_cb_over_high_pos = QtGui.QCheckBox()
        self.clip_cb_over_low_pos = QtGui.QCheckBox()
        self.clip_cb_over_high_neg = QtGui.QCheckBox()
        self.clip_cb_over_low_neg = QtGui.QCheckBox()
        self.l_color.addRow(
            "Clip underlay higher threshold:", self.clip_cb_under_high)
        self.l_color.addRow(
            "Clip underlay lower threshold:", self.clip_cb_under_low)
        self.l_color.addRow(
            "Clip overlay higher pos. threshold:", self.clip_cb_over_high_pos)
        self.l_color.addRow(
            "Clip overlay lower pos. threshold:", self.clip_cb_over_low_pos)
        self.l_color.addRow(
            "Clip overlay higher neg. threshold:", self.clip_cb_over_high_neg)
        self.l_color.addRow(
            "Clip overlay lower neg. threshold:", self.clip_cb_over_low_neg)

        # Resampling defaults
        self.l_resample = QtGui.QFormLayout()
        self.tab_resample.setLayout(self.l_resample)
        self.interp_menu = QtGui.QComboBox()
        self.interp_menu.addItem("nearest neighbor")
        self.interp_menu.addItem("linear")
        self.l_resample.addRow("Interpolation:", self.interp_menu)
        self.method_box = QtGui.QComboBox()
        self.method_box.addItem("use affine information")
        self.method_box.addItem("resample to last loaded")
        self.method_box.addItem("resample to fit")
        self.l_resample.addRow("Resampling method:", self.method_box)

        self.qtab.addTab(self.tab_view, "Viewing options")
        self.qtab.addTab(self.tab_color, "Color maps")
        self.qtab.addTab(self.tab_resample, "Resampling")

        # cancel button
        self.cancel_button = QtGui.QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setShortcut(QtGui.QKeySequence.StandardKey.Quit)

        # save button
        self.save_button = QtGui.QPushButton('Save', self)
        self.save_button.clicked.connect(self.savePreferences)

        self.layout.addWidget(self.qtab, 0, 0, 10, 10)
        self.layout.addWidget(self.save_button, 10, 0, 1, 5)
        self.layout.addWidget(self.cancel_button, 10, 5, 1, 5)

        self.setPreferences()

        self.setLayout(self.layout)

    def setPreferences(self):
        """
        Set the tools to the correct values.
        """
        # View
        self.voxel_cb.setChecked(self.preferences['voxel_coord'])
        self.link_menu.setCurrentIndex(self.preferences['link_mode'])
        # window size...

        # Color
        self.gradient_underlay.item.loadPreset(self.preferences['cm_under'])
        self.gradient_overlay_pos.item.loadPreset(self.preferences['cm_pos'])
        self.gradient_overlay_neg.item.loadPreset(self.preferences['cm_neg'])
        self.clip_cb_under_high.setChecked(
            self.preferences['clip_under_high'])
        self.clip_cb_under_low.setChecked(self.preferences['clip_under_low'])
        self.clip_cb_over_high_pos.setChecked(
            self.preferences['clip_pos_high'])
        self.clip_cb_over_low_pos.setChecked(
            self.preferences['clip_pos_low'])
        self.clip_cb_over_high_neg.setChecked(
            self.preferences['clip_neg_high'])
        self.clip_cb_over_low_neg.setChecked(
            self.preferences['clip_neg_low'])

        # Resampling
        self.interp_menu.setCurrentIndex(self.preferences['interpolation'])
        self.method_box.setCurrentIndex(self.preferences['res_method'])

    def savePreferences(self):
        """
        Get the values form the tools and change preferences.
        """
        # View
        self.preferences['voxel_coord'] = self.voxel_cb.isChecked()
        self.preferences['link_mode'] = self.link_menu.currentIndex()
        # window size has signal and is saved directly.

        # Color
        self.preferences['cm_under'] = self.gradient_underlay.item.name
        self.preferences['cm_pos'] = self.gradient_overlay_pos.item.name
        self.preferences['cm_neg'] = self.gradient_overlay_neg.item.name
        self.preferences['clip_under_high'] = self.clip_cb_under_high.isChecked()
        self.preferences['clip_under_low'] =  self.clip_cb_under_low.isChecked()
        self.preferences['clip_pos_high'] = self.clip_cb_over_high_pos.isChecked()
        self.preferences['clip_pos_low'] = self.clip_cb_over_low_pos.isChecked()
        self.preferences['clip_neg_high'] = self.clip_cb_over_high_neg.isChecked()
        self.preferences['clip_neg_low'] = self.clip_cb_over_low_neg.isChecked()

        # Resampling
        self.preferences['interpolation'] = self.interp_menu.currentIndex()
        self.preferences['res_method'] = self.method_box.currentIndex()

        self.sigSaveSettings.emit()
        self.close()

    def saveWindowSize(self):
        self.sigWindowSize.emit()
