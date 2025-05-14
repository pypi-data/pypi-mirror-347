from .pyqtgraph_vini.Qt import QtCore, QtGui
from .pyqtgraph_vini import *
import numpy as np
import math
import os
import time
import copy
import sys, os.path

from .testInputs import testFloat, testInteger


class ImageDialog(QtGui.QDialog):
    """
    Image properties dialog
    """

    sigPreferencesSave = QtCore.Signal()
    sigImageChanged = QtCore.Signal()
    sigInterpolationChanged = QtCore.Signal()
    sigDiscreteCM = QtCore.Signal()

    def __init__(self):
        super(ImageDialog, self).__init__()

        self.alpha = 0
        self.comp_mode = QtGui.QPainter.CompositionMode.CompositionMode_SourceOver
        self.interpolation = 0
        self.two_colormaps = False
        self.clips_pos = [False, False]
        self.clips_neg = [False, False]

        self.layout = QtGui.QGridLayout()
        self.resize(240,320)

        self.form = QtGui.QFormLayout()

        # Alpha setting
        self.alpha_le = QtGui.QLineEdit()
        self.alpha_le.setMaxLength(5)
        self.alpha_le.returnPressed.connect(self.savePreferences)
        self.alpha_le.editingFinished.connect(self.savePreferences)
        # self.form.addRow("Set alpha:", self.alpha_le)

        # Composition mode
        self.comp_menu = QtGui.QComboBox()
        self.comp_menu.addItem("on top of each other")
        self.comp_menu.addItem("additive")
        self.comp_menu.currentIndexChanged.connect(self.savePreferences)
        self.form.addRow("Overlay mode:", self.comp_menu)

        # Interpolation type
        self.interp_menu = QtGui.QComboBox()
        self.interp_menu.addItem("nearest neighbor")
        self.interp_menu.addItem("linear")
        self.interp_menu.currentIndexChanged.connect(self.savePreferences)
        self.form.addRow("Interpolation type:", self.interp_menu)

        # Colormaps
        self.color_menu = QtGui.QComboBox()
        self.color_menu.addItem("one color map")
        self.color_menu.addItem("two color maps")
        self.color_menu.currentIndexChanged.connect(self.savePreferences)
        self.form.addRow("Color maps:", self.color_menu)

        # Generate a discrete colormap
        self.discrete_cm = QtGui.QPushButton("Discrete CM")
        self.discrete_cm.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.discrete_cm.clicked.connect(self.setDiscreteCM)
        self.form.addRow("Use a discrete color map:", self.discrete_cm)

        # Clippings
        self.clip_cb_high_pos = QtGui.QCheckBox()
        self.clip_cb_high_pos.stateChanged.connect(self.savePreferences)
        self.clip_cb_low_pos = QtGui.QCheckBox()
        self.clip_cb_low_pos.stateChanged.connect(self.savePreferences)
        self.clip_cb_high_neg = QtGui.QCheckBox()
        self.clip_cb_high_neg.stateChanged.connect(self.savePreferences)
        self.clip_cb_low_neg = QtGui.QCheckBox()
        self.clip_cb_low_neg.stateChanged.connect(self.savePreferences)

        self.form.addRow("Clip upper pos. threshold:", self.clip_cb_high_pos)
        self.form.addRow("Clip lower pos. threshold:", self.clip_cb_low_pos)
        self.form.addRow("Clip upper neg. threshold:", self.clip_cb_high_neg)
        self.form.addRow("Clip lower neg. threshold:", self.clip_cb_low_neg)

        self.quit = QtGui.QAction('Quit', self)
        self.quit.setShortcut(QtGui.QKeySequence.StandardKey.Quit)
        self.quit.triggered.connect(self.closeDialog)
        self.addAction(self.quit)

        self.layout.addLayout(self.form, 0, 0, 6, 6)

        self.setLayout(self.layout)

    def setPreferences(self, **kwargs):
        """
        Reset the preferences from the given arguments.
        """
        if 'alpha' in kwargs:
            self.alpha = kwargs['alpha']
            self.alpha_le.setText(str(self.alpha))
        if 'interp' in kwargs:
            self.interpolation = kwargs['interp']
            self.interp_menu.setCurrentIndex(self.interpolation)
        if 'two_cm' in kwargs:
            self.two_colormaps = kwargs['two_cm']
            if self.two_colormaps:
                self.color_menu.setCurrentIndex(1)
            else:
                self.color_menu.setCurrentIndex(0)
        if 'clippings_pos' in kwargs:
            self.clips_pos = kwargs['clippings_pos']
            self.clip_cb_high_pos.setChecked(self.clips_pos[1])
            self.clip_cb_low_pos.setChecked(self.clips_pos[0])
        if 'clippings_neg' in kwargs:
            self.clips_neg = kwargs['clippings_neg']
            self.clip_cb_high_neg.setChecked(self.clips_neg[1])
            self.clip_cb_low_neg.setChecked(self.clips_neg[0])

    def savePreferences(self):
        """
        Write the inputs to the local variables.
        """
        if testFloat(self.alpha_le.text()):
            self.alpha = float(self.alpha_le.text())
        if self.comp_menu.currentIndex() == 0:
            self.comp_mode = QtGui.QPainter.CompositionMode.CompositionMode_SourceOver
        else:
            self.comp_mode = QtGui.QPainter.CompositionMode.CompositionMode_Plus
        self.interpolation = self.interp_menu.currentIndex()
        self.two_colormaps = self.color_menu.currentIndex() != 0
        self.clips_pos = [self.clip_cb_low_pos.isChecked(),
                          self.clip_cb_high_pos.isChecked()]
        self.clips_neg = [self.clip_cb_low_neg.isChecked(),
                          self.clip_cb_high_neg.isChecked()]
        # signal to save the preferences
        self.sigPreferencesSave.emit()
        # signal to apply the changes to the image item
        self.sigImageChanged.emit()

    def setDiscreteCM(self):
        self.sigDiscreteCM.emit()

    def getAlpha(self):
        return self.alpha

    def getInterpolation(self):
        return self.interpolation

    def getColormapNo(self):
        return self.two_colormaps

    def getClipsPos(self):
        return self.clips_pos

    def getClipsNeg(self):
        return self.clips_neg

    def closeDialog(self):
        self.close()
