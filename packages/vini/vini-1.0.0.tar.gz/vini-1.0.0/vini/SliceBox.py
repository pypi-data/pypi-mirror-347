from .pyqtgraph_vini.Qt import QtCore, QtGui
import numpy as np
from .pyqtgraph_vini import *
import sys

from .pyqtgraph_vini import functions as fn
from .pyqtgraph_vini import Point
import weakref
from .pyqtgraph_vini import ItemGroup

""" Change some pyqtgraph 0.9.1 classes to do what we need. """

class WeakList(object):

    def __init__(self):
        self._items = []

    def append(self, obj):
        #Add backwards to iterate backwards (to make iterating more efficient on removal).
        self._items.insert(0, weakref.ref(obj))

    def __iter__(self):
        i = len(self._items)-1
        while i >= 0:
            ref = self._items[i]
            d = ref()
            if d is None:
                del self._items[i]
            else:
                yield d
            i -= 1

class ChildGroup(ItemGroup):

    def __init__(self, parent):
        ItemGroup.__init__(self, parent)

        # Used as callback to inform ViewBox when items are added/removed from
        # the group.
        # Note 1: We would prefer to override itemChange directly on the
        #         ViewBox, but this causes crashes on PySide.
        # Note 2: We might also like to use a signal rather than this callback
        #         mechanism, but this causes a different PySide crash.
        self.itemsChangedListeners = WeakList()

        # excempt from telling view when transform changes
        self._GraphicsObject__inform_view_on_change = False

    def itemChange(self, change, value):
        ret = ItemGroup.itemChange(self, change, value)
        if change == self.ItemChildAddedChange or change == self.ItemChildRemovedChange:
            try:
                itemsChangedListeners = self.itemsChangedListeners
            except AttributeError:
                # It's possible that the attribute was already collected when the itemChange happened
                # (if it was triggered during the gc of the object).
                pass
            else:
                for listener in itemsChangedListeners:
                    listener.itemsChanged()
        return ret

class SliceBox(ViewBox):
    """
    **Bases:** :class:`GraphicsWidget <pyqtgraph.GraphicsWidget>`

    Box that allows internal scaling/panning of children by mouse drag.
    This class is usually created automatically as part of a :class:`PlotItem <pyqtgraph.PlotItem>` or :class:`Canvas <pyqtgraph.canvas.Canvas>` or with :func:`GraphicsLayout.addViewBox() <pyqtgraph.GraphicsLayout.addViewBox>`.

    Features:

    * Scaling contents by mouse or auto-scale when contents change
    * View linking--multiple views display the same data ranges
    * Configurable by context menu
    * Item coordinate mapping methods

    """

    sigYRangeChanged = QtCore.Signal(object, object)
    sigXRangeChanged = QtCore.Signal(object, object)
    sigRangeChangedManually = QtCore.Signal(object)
    sigRangeChanged = QtCore.Signal(object, object)
    #sigActionPositionChanged = QtCore.Signal(object)
    sigStateChanged = QtCore.Signal(object)
    sigTransformChanged = QtCore.Signal(object)
    sigResized = QtCore.Signal(object)

    center = [0, 0] # coordinates to zoom into.

    ## mouse modes
    PanMode = 3
    RectMode = 1

    ## axes
    XAxis = 0
    YAxis = 1
    XYAxes = 2

    ## for linking views together
    NamedViews = weakref.WeakValueDictionary()   # name: ViewBox
    AllViews = weakref.WeakKeyDictionary()       # ViewBox: None

    def __init__(self, parent=None, border=None, lockAspect=False, enableMouse=True, invertY=False, enableMenu=True, name=None, invertX=False):
        """
        ==============  =============================================================
        **Arguments:**
        *parent*        (QGraphicsWidget) Optional parent widget
        *border*        (QPen) Do draw a border around the view, give any
                        single argument accepted by :func:`mkPen <pyqtgraph.mkPen>`
        *lockAspect*    (False or float) The aspect ratio to lock the view
                        coorinates to. (or False to allow the ratio to change)
        *enableMouse*   (bool) Whether mouse can be used to scale/pan the view
        *invertY*       (bool) See :func:`invertY <pyqtgraph.ViewBox.invertY>`
        *invertX*       (bool) See :func:`invertX <pyqtgraph.ViewBox.invertX>`
        *enableMenu*    (bool) Whether to display a context menu when
                        right-clicking on the ViewBox background.
        *name*          (str) Used to register this ViewBox so that it appears
                        in the "Link axis" dropdown inside other ViewBox
                        context menus. This allows the user to manually link
                        the axes of any other view to this one.
        ==============  =============================================================
        """
        super(SliceBox, self).__init__(parent=None, border=border, lockAspect=True, enableMouse=True, invertY=False, enableMenu=True, name=None, invertX=False)
        self.zoomCenter = [0, 0]
        self.state['wheelScaleFactor'] = -0.025
        self.useMyMenu()

        """ linkedAxis saves to which axis of the linked view the axis is linked to """
        self.state['linkedAxis']= [None, None]

    # def switchMenu(self):
    #

    def mouseDragEvent(self, ev, axis=None):
        ## if axis is specified, event will only affect that axis.
        ev.accept()  ## we accept all buttons
        pos = ev.pos()

        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1

        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.state['mouseEnabled'], dtype=float)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1-axis] = 0.0

        ## Scale or translate based on mouse button
        if ev.button() & (QtCore.Qt.MouseButton.RightButton | QtCore.Qt.MouseButton.MiddleButton):

            if self.state['mouseMode'] == SliceBox.RectMode:
                if ev.isFinish():  ## This is the final move in the drag; change the view scale now
                    #print "finish"
                    self.rbScaleBox.hide()
                    #ax = QtCore.QRectF(Point(self.pressPos), Point(self.mousePos))
                    ax = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                    ax = self.childGroup.mapRectFromParent(ax)
                    self.showAxRect(ax)
                    self.axHistoryPointer += 1
                    self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                else:
                    ## update shape of scale box
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())

            else:
                tr = dif*mask
                tr = self.mapToView(tr) - self.mapToView(Point(0,0))
                x = tr.x() if mask[0] == 1 else None
                y = tr.y() if mask[1] == 1 else None

                self._resetTarget()
                if x is not None or y is not None:
                    self.translateBy(x=x, y=y)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        """
        if ev.button() & QtCore.Qt.MouseButton.RightButton:
            #print "vb.rightDrag"
            if self.state['aspectLocked'] is not False:
                mask[0] = 0

            dif = ev.screenPos() - ev.lastScreenPos()
            dif = np.array([dif.x(), dif.y()])
            dif[0] *= -1
            s = ((mask * 0.02) + 1) ** dif

            tr = self.childGroup.transform()
            tr = fn.invertQTransform(tr)

            x = s[0] if mouseEnabled[0] == 1 else None
            y = s[1] if mouseEnabled[1] == 1 else None

            center = Point(tr.map(ev.buttonDownPos(QtCore.Qt.MouseButton.RightButton)))
            self._resetTarget()
            self.scaleBy(x=x, y=y, center=center)
            self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        """
    def setZoomCenter(self, pos):
        # pos : [crosshair_x, crosshair_y]
        self.zoomCenter = Point(pos)
        #print(self.zoomCenter)

    def zoom(self, scale):
        center = self.childGroup.mapToParent(self.zoomCenter)
        center = self.childGroup.mapToView(center)
        center = fn.invertQTransform(self.childGroup.transform()).map(center)
        self._resetTarget()
        self.scaleBy(scale, center)

    # def keyPressEvent(self, event):
    #     if type(event) == QtGui.QKeyEvent:
    #         # print event.key()
    #         print event.key()
    #         if event.key() == 49: # 1
    #             s = 0.9
    #             center = self.childGroup.mapToParent(self.zoomCenter)
    #             center = self.childGroup.mapToView(center)
    #             center = fn.invertQTransform(self.childGroup.transform()).map(center)
    #             self._resetTarget()
    #             self.scaleBy(s, center)
    #
    #         if event.key() == 50: # 2
    #             s = 1.1
    #             center = self.childGroup.mapToParent(self.zoomCenter)
    #             center = self.childGroup.mapToView(center)
    #             center = fn.invertQTransform(self.childGroup.transform()).map(center)
    #             self._resetTarget()
    #             self.scaleBy(s, center)
    #         event.accept()
    #     else:
    #         event.ignore()

    def wheelEvent(self, ev, axis=None):
        mask = np.array(self.state['mouseEnabled'], dtype=float)
        if axis is not None and axis >= 0 and axis < len(mask):
            mv = mask[axis]
            mask[:] = 0
            mask[axis] = mv
        s = ((mask * 0.02) + 1) ** (ev.delta() * self.state['wheelScaleFactor']) # actual scaling factor

        #center = Point(fn.invertQTransform(self.childGroup.transform()).map(ev.pos()))
        # map scene point to viewpoint
        #print "center: " + str(self.zoomCenter)
        center = self.childGroup.mapToParent(self.zoomCenter)
        center = self.childGroup.mapToView(center)
        center = fn.invertQTransform(self.childGroup.transform()).map(center)

        self._resetTarget()
        self.scaleBy(s, center)
        self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        ev.accept()

    def linkView(self, axis, view=None):
        """
        Link X or Y axes of two views and unlink any previously connected axes. *axis* must be ViewBox.XAxis or ViewBox.YAxis.
        If view is None, the axis is left unlinked.
        """
        if isinstance(view, str):
            if view == '':
                view = None
            else:
                view = ViewBox.NamedViews.get(view, view)  ## convert view name to ViewBox if possible

        if hasattr(view, 'implements') and view.implements('ViewBoxWrapper'):
            view = view.getViewBox()

        ## used to connect/disconnect signals between a pair of views
        if axis == ViewBox.XAxis:
            signal = 'sigXRangeChanged'
            slot = self.linkedXChanged
        else:
            signal = 'sigYRangeChanged'
            slot = self.linkedYChanged

        oldLink = self.linkedView(axis)
        if oldLink is not None:
            try:
                getattr(oldLink, signal).disconnect(slot)
                oldLink.sigResized.disconnect(slot)
            except (TypeError, RuntimeError):
                ## This can occur if the view has been deleted already
                pass


        if view is None or isinstance(view, str):
            self.state['linkedViews'][axis] = view
        else:
            self.state['linkedViews'][axis] = weakref.ref(view)
            getattr(view, signal).connect(slot)
            view.sigResized.connect(slot)
            if view.autoRangeEnabled()[axis] is not False:
                self.enableAutoRange(axis, False)
                slot()
            else:
                if self.autoRangeEnabled()[axis] is False:
                    slot()

        self.sigStateChanged.emit(self)

    def setXLink(self, view):
        """Link this view's X axis to another view. (see LinkView)"""
        self.state['linkedAxis'][ViewBox.XAxis] = ViewBox.XAxis
        self.linkView(self.XAxis, view)

    def setYLink(self, view):
        """Link this view's Y axis to another view. (see LinkView)"""
        self.state['linkedAxis'][ViewBox.YAxis] = ViewBox.YAxis
        self.linkView(self.YAxis, view)

    def linkViewXY(self, view, axis, own_axis):
        """
        Link X or Y axes of two views and unlink any previously connected axes. *axis* must be ViewBox.XAxis or ViewBox.YAxis.
        If view is None, the axis is left unlinked.
        """
        if isinstance(view, str):
            if view == '':
                view = None
            else:
                view = ViewBox.NamedViews.get(view, view)  ## convert view name to ViewBox if possible

        if hasattr(view, 'implements') and view.implements('ViewBoxWrapper'):
            view = view.getViewBox()

        ## used to connect/disconnect signals between a pair of view
        if axis == ViewBox.XAxis:
            signal = 'sigXRangeChanged'
        else:
            signal = 'sigYRangeChanged'

        if own_axis == ViewBox.XAxis:
            slot = self.linkedXChanged
        else:
            slot = self.linkedYChanged

        oldLink = self.linkedView(own_axis)
        if oldLink is not None:
            try:
                getattr(oldLink, signal).disconnect(slot)
                oldLink.sigResized.disconnect(slot)
            except (TypeError, RuntimeError):
                ## This can occur if the view has been deleted already
                pass

        if view is None or isinstance(view, str):
            self.state['linkedViews'][own_axis] = view
        else:
            self.state['linkedViews'][own_axis] = weakref.ref(view)
            self.state['linkedAxis'][own_axis] = axis
            getattr(view, signal).connect(slot)
            view.sigResized.connect(slot)
            if view.autoRangeEnabled()[axis] is not False:
                self.enableAutoRange(own_axis, False)
                slot()
            else:
                if self.autoRangeEnabled()[own_axis] is False:
                    slot()

        self.sigStateChanged.emit(self)

    def blockLink(self, b):
        self.linksBlocked = b  ## prevents recursive plot-change propagation

    def linkedXChanged(self):
        ## called when x range of linked view has changed
        linkedAxis = self.state['linkedAxis'][ViewBox.XAxis]
        view = self.linkedView(0)
        self.linkedViewXYChanged(view, linkedAxis, ViewBox.XAxis)

    def linkedYChanged(self):
        ## called when y range of linked view has changed
        linkedAxis = self.state['linkedAxis'][ViewBox.YAxis]
        view = self.linkedView(1)
        self.linkedViewXYChanged(view, linkedAxis, ViewBox.YAxis)

    def linkedView(self, ax):
        ## Return the linked view for axis *ax*.
        ## this method _always_ returns either a ViewBox or None.
        v = self.state['linkedViews'][ax]
        if v is None or isinstance(v, str):
            return None
        else:
            return v()  ## dereference weakref pointer. If the reference is dead, this returns None

    def linkedViewXYChanged(self, view, axis, own_axis):
        if self.linksBlocked or view is None:
            return

        #print self.name, "ViewBox.linkedViewChanged", axis, view.viewRange()[axis]
        vr = view.viewRect()
        vg = view.screenGeometry()
        sr = self.viewRect()
        sg = self.screenGeometry()
        if vg is None or sg is None:
            return

        view.blockLink(True)
        try:
            # distinguish four cases of axis linkage
            # if axis == ViewBox.XAxis and own_axis == ViewBox.XAxis:
            #     diff_ratio = float(sg.width()) / float(vg.width())
            #     diff = vr.right() - vr.left()
            #     diff *= (diff_ratio - 1.)
            #     part1 = diff * (self.zoomCenter[0] - sr.left())/float(sr.right() - sr.left())
            #     part2 = diff * (sr.right() - self.zoomCenter[0])/float(sr.right() - sr.left())
            #     print "xx"
            #     print diff
            #     print part1
            #     print part2
            #     x1 = vr.left() - part1 #diff/2.
            #     x2 = vr.right() + part2 #diff/2.
            #     # x1 = vr.left() - diff/2.
            #     # x2 = vr.right() + diff/2.
            #     self.enableAutoRange(ViewBox.XAxis, False)
            #     self.setXRange(x1, x2, padding=0)
            # if axis == ViewBox.XAxis and own_axis == ViewBox.YAxis:
            #     diff_ratio = float(sg.height()) / float(vg.width())
            #     diff = vr.right() - vr.left()
            #     diff *= (diff_ratio - 1.)
            #     part1 = diff * (self.zoomCenter[1] - sr.top())/float(sr.bottom() - sr.top())
            #     part2 = diff * (sr.bottom() - self.zoomCenter[1])/float(sr.bottom() - sr.top())
            #     print "xy"
            #     print diff
            #     print part1
            #     print part2
            #     y1 = vr.left() - part1
            #     y2 = vr.right() + part2
            #     self.enableAutoRange(ViewBox.YAxis, False)
            #     self.setYRange(y1, y2, padding=0)
            # if axis == ViewBox.YAxis and own_axis == ViewBox.YAxis:
            #     diff_ratio = sg.height() / float(vg.height())
            #     diff = vr.bottom() - vr.top()
            #     diff *= (diff_ratio - 1)
            #     part1 = diff * (self.zoomCenter[1] - sr.top())/float(sr.bottom() - sr.top())
            #     part2 = diff * (sr.bottom() - self.zoomCenter[1])/float(sr.bottom() - sr.top())
            #     print "yy"
            #     print diff
            #     print part1
            #     print part2
            #     y1 = vr.top() - part1
            #     y2 = vr.bottom() + part2
            #     self.enableAutoRange(ViewBox.YAxis, False)
            #     self.setYRange(y1, y2, padding=0)
            # if axis == ViewBox.YAxis and own_axis == ViewBox.XAxis:
            #     diff_ratio = sg.width() / float(vg.height())
            #     diff = vr.bottom() - vr.top()
            #     diff *= (diff_ratio - 1)
            #     part1 = diff * (self.zoomCenter[0] - sr.left())/float(sr.right() - sr.left())
            #     part2 = diff * (sr.right() - self.zoomCenter[0])/float(sr.right() - sr.left())
            #     print "yx"
            #     print diff
            #     print part1
            #     print part2
            #     x1 = vr.top() - part1
            #     x2 = vr.bottom() + part2
            #     self.enableAutoRange(ViewBox.XAxis, False)
            #     self.setXRange(x1, x2, padding=0)
            if axis == ViewBox.XAxis and own_axis == ViewBox.XAxis:
                diff_ratio = float(sg.width()) / float(vg.width())
                diff = vr.right() - vr.left()
                diff *= (diff_ratio - 1.)
                x1 = vr.left() - diff/2.
                x2 = vr.right() + diff/2.
                self.enableAutoRange(ViewBox.XAxis, False)
                self.setXRange(x1, x2, padding=0)
            if axis == ViewBox.XAxis and own_axis == ViewBox.YAxis:
                diff_ratio = float(sg.height()) / float(vg.width())
                diff = vr.right() - vr.left()
                diff *= (diff_ratio - 1.)
                y1 = vr.left() - diff/2.
                y2 = vr.right() + diff/2.
                self.enableAutoRange(ViewBox.YAxis, False)
                self.setYRange(y1, y2, padding=0)
            if axis == ViewBox.YAxis and own_axis == ViewBox.YAxis:
                diff_ratio = sg.height() / float(vg.height())
                diff = vr.bottom() - vr.top()
                diff *= (diff_ratio - 1)
                y1 = vr.top() - diff/2.
                y2 = vr.bottom() + diff/2.
                self.enableAutoRange(ViewBox.YAxis, False)
                self.setYRange(y1, y2, padding=0)
            if axis == ViewBox.YAxis and own_axis == ViewBox.XAxis:
                diff_ratio = sg.width() / float(vg.height())
                diff = vr.bottom() - vr.top()
                diff *= (diff_ratio - 1)
                y1 = vr.top() - diff/2.
                y2 = vr.bottom() + diff/2.
                self.enableAutoRange(ViewBox.XAxis, False)
                self.setXRange(y1, y2, padding=0)
        finally:
            view.blockLink(False)


    def getState(self, copy=True):
        """Return the current state of the ViewBox.
        Linked views are always converted to view names in the returned state."""
        state = self.state.copy()
        views = []
        for v in state['linkedViews']:
            if isinstance(v, weakref.ref):
                v = v()
            if v is None or isinstance(v, str):
                views.append(v)
            else:
                views.append(v.name)
        state['linkedViews'] = views
        if copy:
            return deepcopy(state)
        else:
            return state

    def setState(self, state):
        """Restore the state of this ViewBox.
        (see also getState)"""
        state = state.copy()
        print("The action you have performed requires a reimplementation of the linkage of the slice viewers")
        self.setXLink(state['linkedViews'][0])
        self.setYLink(state['linkedViews'][1])
        del state['linkedViews']

        self.state.update(state)
        #self.updateMatrix()
        self.updateViewRange()
        self.sigStateChanged.emit(self)


    def updateViewRange(self, forceX=True, forceY=True):
        ## Update viewRange to match targetRange as closely as possible, given
        ## aspect ratio constraints. The *force* arguments are used to indicate
        ## which axis (if any) should be unchanged when applying constraints.
        viewRange = [self.state['targetRange'][0][:], self.state['targetRange'][1][:]]
        changed = [False, False]

        #-------- Make correction for aspect ratio constraint ----------

        # aspect is (widget w/h) / (view range w/h)
        aspect = self.state['aspectLocked']  # size ratio / view ratio
        tr = self.targetRect()
        bounds = self.rect()
        if aspect is not False and 0 not in [aspect, tr.height(), bounds.height(), bounds.width()]:

            ## This is the view range aspect ratio we have requested
            targetRatio = tr.width() / tr.height() if tr.height() != 0 else 1
            ## This is the view range aspect ratio we need to obey aspect constraint
            viewRatio = (bounds.width() / bounds.height() if bounds.height() != 0 else 1) / aspect
            viewRatio = 1 if viewRatio == 0 else viewRatio

            # Decide which range to keep unchanged
            #print self.name, "aspect:", aspect, "changed:", changed, "auto:", self.state['autoRange']
            if forceX:
                ax = 0
            elif forceY:
                ax = 1
            else:
                # if we are not required to keep a particular axis unchanged,
                # then make the entire target range visible
                ax = 0 if targetRatio > viewRatio else 1

            if ax == 0:
                ## view range needs to be taller than target
                dy = 0.5 * (tr.width() / viewRatio - tr.height())
                if dy != 0:
                    changed[1] = True
                viewRange[1] = [self.state['targetRange'][1][0] - dy, self.state['targetRange'][1][1] + dy]
            else:
                ## view range needs to be wider than target
                dx = 0.5 * (tr.height() * viewRatio - tr.width())
                if dx != 0:
                    changed[0] = True
                viewRange[0] = [self.state['targetRange'][0][0] - dx, self.state['targetRange'][0][1] + dx]


        # ----------- Make corrections for view limits -----------

        limits = (self.state['limits']['xLimits'], self.state['limits']['yLimits'])
        minRng = [self.state['limits']['xRange'][0], self.state['limits']['yRange'][0]]
        maxRng = [self.state['limits']['xRange'][1], self.state['limits']['yRange'][1]]

        for axis in [0, 1]:
            if limits[axis][0] is None and limits[axis][1] is None and minRng[axis] is None and maxRng[axis] is None:
                continue

            # max range cannot be larger than bounds, if they are given
            if limits[axis][0] is not None and limits[axis][1] is not None:
                if maxRng[axis] is not None:
                    maxRng[axis] = min(maxRng[axis], limits[axis][1]-limits[axis][0])
                else:
                    maxRng[axis] = limits[axis][1]-limits[axis][0]

            #print "\nLimits for axis %d: range=%s min=%s max=%s" % (axis, limits[axis], minRng[axis], maxRng[axis])
            #print "Starting range:", viewRange[axis]

            # Apply xRange, yRange
            diff = viewRange[axis][1] - viewRange[axis][0]
            if maxRng[axis] is not None and diff > maxRng[axis]:
                delta = maxRng[axis] - diff
                changed[axis] = True
            elif minRng[axis] is not None and diff < minRng[axis]:
                delta = minRng[axis] - diff
                changed[axis] = True
            else:
                delta = 0

            viewRange[axis][0] -= delta/2.
            viewRange[axis][1] += delta/2.

            #print "after applying min/max:", viewRange[axis]

            # Apply xLimits, yLimits
            mn, mx = limits[axis]
            if mn is not None and viewRange[axis][0] < mn:
                delta = mn - viewRange[axis][0]
                viewRange[axis][0] += delta
                viewRange[axis][1] += delta
                changed[axis] = True
            elif mx is not None and viewRange[axis][1] > mx:
                delta = mx - viewRange[axis][1]
                viewRange[axis][0] += delta
                viewRange[axis][1] += delta
                changed[axis] = True

            #print "after applying edge limits:", viewRange[axis]

        changed = [(viewRange[i][0] != self.state['viewRange'][i][0]) or (viewRange[i][1] != self.state['viewRange'][i][1]) for i in (0,1)]
        self.state['viewRange'] = viewRange

        # emit range change signals
        if changed[0]:
            self.sigXRangeChanged.emit(self, tuple(self.state['viewRange'][0]))
        if changed[1]:
            self.sigYRangeChanged.emit(self, tuple(self.state['viewRange'][1]))

        if any(changed):
            self.sigRangeChanged.emit(self, self.state['viewRange'])
            self.update()
            self._matrixNeedsUpdate = True

            # Inform linked views that the range has changed
            for ax in [0, 1]:
                if not changed[ax]:
                    continue
                link = self.linkedView(ax)
                if link is not None:
                    linkedAxis = self.state['linkedAxis'][ax]
                    link.linkedViewXYChanged(self, ax, linkedAxis)
