from ..Qt import QtGui, QtCore, QtWidgets, USE_PYQT4, USE_PYSIDE
if USE_PYQT4:
    import sip
from .GraphicsItem import GraphicsItem

__all__ = ['GraphicsObject']
class GraphicsObject(GraphicsItem, QtWidgets.QGraphicsObject):
    """
    **Bases:** :class:`GraphicsItem <pyqtgraph.graphicsItems.GraphicsItem>`, :class:`QtWidgets.QGraphicsObject`

    Extension of QGraphicsObject with some useful methods (provided by :class:`GraphicsItem <pyqtgraph.graphicsItems.GraphicsItem>`)
    """
    _qtBaseClass = QtWidgets.QGraphicsObject
    def __init__(self, *args):
        self.__inform_view_on_changes = True
        QtWidgets.QGraphicsObject.__init__(self, *args)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)
        GraphicsItem.__init__(self)
        
    def itemChange(self, change, value):
        ret = QtWidgets.QGraphicsObject.itemChange(self, change, value)
        if change in [self.GraphicsItemChange.ItemParentHasChanged, self.GraphicsItemChange.ItemSceneHasChanged]:
            self.parentChanged()
        try:
            inform_view_on_change = self.__inform_view_on_changes
        except AttributeError:
            # It's possible that the attribute was already collected when the itemChange happened
            # (if it was triggered during the gc of the object).
            pass
        else:
            if inform_view_on_change and change in [self.GraphicsItemChange.ItemPositionHasChanged, self.GraphicsItemChange.ItemTransformHasChanged]:
                self.informViewBoundsChanged()
            
        ## workaround for pyqt bug:
        ## http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if USE_PYQT4 and change == self.GraphicsItemChange.ItemParentChange and isinstance(ret, QtGui.QGraphicsItem):
            ret = sip.cast(ret, QtGui.QGraphicsItem)

        return ret
