# -*- coding: utf-8 -*-
from .pyqtgraph_vini.Qt import QtCore, QtGui
from .pyqtgraph_vini import GraphicsView
from .ColorMapItem import *
import weakref
import numpy as np

__all__ = ['ColorMapWidgetObj']


class ColorMapWidgetObj(GraphicsView):
    """
    Widget displaying an editable color gradient. The user may add, move, recolor,
    or remove colors from the gradient. Additionally, a context menu allows the
    user to select from pre-defined gradients.
    """
    sigGradientChanged = QtCore.Signal(object)
    sigGradientChangeFinished = QtCore.Signal(object)
    

    def __init__(self, parent=None, orientation='bottom',  *args, **kargs):
        """
        The *orientation* argument may be 'bottom', 'top', 'left', or 'right'
        indicating whether the gradient is displayed horizontally (top, bottom)
        or vertically (left, right) and on what side of the gradient the editable
        ticks will appear.

        All other arguments are passed to
        :func:`GradientEditorItem.__init__ <pyqtgraph.GradientEditorItem.__init__>`.

        Note: For convenience, this class wraps methods from
        :class:`GradientEditorItem <pyqtgraph.GradientEditorItem>`.
        """
        
        GraphicsView.__init__(self, parent, useOpenGL=False, background=None)
        self.maxDim = 20
        kargs['tickPen'] = 'k'
        self.item = ColorMapItem(*args, **kargs)
        self.item.sigGradientChanged.connect(self.sigGradientChanged)
        self.item.sigGradientChangeFinished.connect(self.sigGradientChangeFinished)
        self.setCentralItem(self.item)
        self.setOrientation(orientation)
        self.setCacheMode(self.CacheModeFlag.CacheNone)
        self.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing)
        self.setFrameStyle(QtGui.QFrame.Shape.NoFrame | QtGui.QFrame.Shadow.Plain)


    def setOrientation(self, ort):
        """Set the orientation of the widget. May be one of 'bottom', 'top',
        'left', or 'right'."""
        self.item.setOrientation(ort)
        self.orientation = ort
        self.setMaxDim()

    def setMaxDim(self, mx=None, pixels=None):
        if mx is None:
            mx = self.maxDim
        else:
            self.maxDim = mx
            
        if pixels==None:
            pixels = 100

        if self.orientation in ['bottom', 'top']:
            self.setFixedHeight(mx)
            self.setMaximumWidth(pixels)
        else:
            self.setFixedWidth(mx)
            self.setMaximumHeight(16777215)

    def __getattr__(self, attr):
        ### wrap methods from ColorMapItem
        return getattr(self.item, attr)
