from .pyqtgraph_vini.Qt import QtCore, QtGui
import numpy as np
import math
import os
import copy
import sys, os.path

from .pyqtgraph_vini import *

from .ColorMapWidget import *
from .SliceWidget import *
from .SliceBox import *
from .ImageItemMod import *


class SliceWindow(QtGui.QWidget):
    """
    Class to display an extra window.
    """

    sigClose = QtCore.Signal(int)

    def __init__(self, window_number):
        super(SliceWindow, self).__init__()

        self.resize(960,320)
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        size = self.geometry()
        self.id = window_number
        # Place it in the center of the screen.
        self.move(int((screen.width()-size.width())/2), int((screen.height()-size.height())/2))

        self.l = QtGui.QGridLayout()
        self.setLayout(self.l)
        self.l.setContentsMargins(2,2,2,2)
        self.l.setSpacing(0)

        self.sw_c = SliceWidget('c')
        self.sw_s = SliceWidget('s')
        self.sw_t = SliceWidget('t')
        self.sw_c.useMenu(1)
        self.sw_s.useMenu(1)
        self.sw_t.useMenu(1)
        self.l.addWidget(self.sw_c)
        self.l.addWidget(self.sw_c, 0, 0, 12, 12)
        self.l.addWidget(self.sw_s)
        self.l.addWidget(self.sw_s, 0, 12, 12, 12)
        self.l.addWidget(self.sw_t)
        self.l.addWidget(self.sw_t, 0, 24, 12, 12)

        self.close_view = QtGui.QAction('close view', self)
        self.close_view.setShortcut(QtGui.QKeySequence.StandardKey.Quit)
        self.close_view.triggered.connect(self.close)
        self.addAction(self.close_view)


        self.setWindowTitle("Window " + str(window_number))

        self.show()

    def closeEvent(self, ev):
        self.sigClose.emit(self.id)
        self.hide()
