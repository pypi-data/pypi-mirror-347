#!/usr/bin/env python3
"""
This module contains the vini class for viewing MRI files.

To better search for relevant functions note that the class is subdivided
by these sections:
## Section: Loading and Deleting Images ##
## Section: Resampling Methods ##
## Section: Linking Views ##
## Section: Crosshair and Cursor Movements and Connected Functions ##
## Section: Zoom and Pan Views ##
## Section: Updating the Slices ##
## Section: Activating and Deactivating Images ##
## Section: Current Image Selection Update ##
## Section: Extra Windows ##
## Section: imagelist Actions ##
## Section: Functional Image Methods ##
## Section: Color Map Thresholds Settings ##
## Section: Search Extrema ##
## Section: Open Slice Popouts ##
## Section: Slice Focusing ##
## Section: Opening Dialogs and Windows for Image Settings ##
## Section: Tools Related ##
## Section: Settings Management ##
## Section: Closing the Viewer ##
"""

verbose_level = 5
from .QxtSpanSlider import QxtSpanSlider

from .pyqtgraph_vini.Qt import QtCore, QtGui, QtWidgets
from .pyqtgraph_vini.exporters import ImageExporter

import numpy as np
import math
import os
import time
import copy
import sys
import os.path
import threading
# for saving preferences
if sys.version_info[0] == 3:
    from configparser import ConfigParser as ConfigParser
else:
    from ConfigParser import ConfigParser

# makes the program exit from the bash with ctrl+c
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from .pyqtgraph_vini import * 
# for colormap thresholds:


from .ColorMapWidget import *
from .SliceBox import *
from .SliceWidget import *
from .SingleSlice import *
from .Image3D import *
from .Image4D import *
from .loadImage import *
from .ImageItemMod import *
from .SliceWindow import *
from .ValueWindow import *
from .HistogramThresholdWidget import *
from .SettingsDialog import *
from .MosaicDialog import *
from .MosaicView import *
# for functional movie mode:
from .JumpSlider import JumpSlider
# testing input
from .testInputs import testFloat, testInteger
# print infos if necessary
from .Verboseprint import verboseprint
import time
import re
import traceback
import matplotlib
from matplotlib.image import imsave
import pkg_resources

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

def log1(msg):
    if verbose_level <= 1:
        print("log1 {}: {}".format(get_time(),msg))

def log2(msg):
    if verbose_level <= 2:
        print("log2 {}: {}".format(get_time(),msg))

def get_time():
    current_time = time.localtime()
    str_time = time.strftime('%H%M%S', current_time)
    return str_time

def unicode(string):
    try:
        res = unicode(string)
    except:
        res = string
    return res

class Viff(QtGui.QMainWindow):
    """
    Class to view MRI files
    """

    def __init__(self, parent=None):
        """Initialize vini object"""
        super(Viff, self).__init__(parent)

        # 'img_coord' contains the coordinates of the crosshair/slices within
        # the resampled image data.
        self.img_coord = [0, 0, 0]
        # 'frame' contains the index of the current frame.
        #  By convention the first frame number is 0.
        self.frame = 0
        # 'img_dims' is the dimensions of the resampled image data.
        # This is e.g. necessary to decide whether the crosshair or cursor is
        # within the image.
        self.img_dims = [0, 0, 0]
        # 'time_dim' is the number of frames of the time series data.
        # For images this is 1.
        self.time_dim = 1
        # 'cursor_coord' is a list for the current cursor position.
        self.cursor_coord = [0, 0, 0]
        # 'affine' contains a numpy array for keeping track of what
        # transformation was used for the resampled data.
        self.affine = np.eye(4)

        # 'voxel_coord' contains a boolean value that tells whether the voxel
        # coordinates of the original data are displayed or the coordinates of
        # the coordinates system w.r.t. the given affine.
        self.voxel_coord = False

        # Saves what kind of transform to apply
        # 0 - resamples to coordinate system
        # 1 - resamples to the currently selected image
        # 2 - resamples ignoring the affine and matching the first dimensions
        self.transform_ind = 0

        # 'images' is the list of Image instances (Image3D or Image4D) loaded
        # into the viewer
        self.images = []
        # 'states' saves if image is shown or not in the main window
        self.states = []

        # slice window popouts
        self.slice_popouts = [None] * 3
        # 'popouts_ii contains the imageitems for the slice window popouts
        self.popouts_ii = []

        ## Extra Windows ##
        # 'image_window_list' is the list of lists of lists containing for each
        # image a list of windows-lists containing slice image items (for each
        # plane, sagittal, coronal or transverse)
        # Those image items are displayed in the SliceWidgets.
        self.image_window_list = []
        # 'extra_windows' contains the instances of the windows class themselves
        self.extra_windows = []
        # 'window_ids' manages the ids for all extra windows
        self.window_ids = []
        # 'window_count' counts the number of all extra windows having been
        # openend. It is used to assign ids to the windows.
        self.window_count = 0

        # 'deselected' saves whether the deselect function was used.
        # It toggles off the visibility of all images in the main window but
        # the currently selected image. Calling it again will toggle on the
        # visibility of all images.
        self.deselected = False

        # 'slice_focus' save which plane is currently focused ('c', 's' or 't')
        self.slice_focus = 'c'

        ## Time series image playing variables ##
        # 'func_enables' saves whether the buttons and sliders for the playing
        # functions should be enabled. Should be false if no functional image
        # is loaded.
        self.func_enabled = False
        self.timer = QtCore.QTimer()
        self.playstate = False
        self.slicestate = False
        self.playrate = 3
        # Because the frame index can be changed from multiple locations and
        # has to be updated in the others the 'frame_write_block' tells you if
        # changes in one location have to be propagated to the others.
        self.frame_write_block = False

        # The same for colormap thresholds.
        self.threshold_write_block = False

        # 'prefered_path' saves the path last used to load a file into the
        # viewer, making it more convenient to use the File Dialog.
        self.prefered_path = None
        
        
        #forbidding the display of mm units (whenevre clicked on ignoring affine)
        self.forbid_mm = False

        # preferences: init with default preferences
        self.setDefaultPreferences()
        
        
        
        # then overwrite specific settings that were saved in sessions before...
        self.loadPreferences()
        
        # variables are copied, so changing them doesn't change the preferences
        self.link_mode = self.preferences['link_mode']
        self.voxel_coord = self.preferences['voxel_coord']

        # Initialize the SettingsDialog.
        self.settings = SettingsDialog(self.preferences)
        self.settings.sigSaveSettings.connect(self.savePreferences)
        self.settings.sigWindowSize.connect(self.saveWindowSize)

        # Initializes the ValueWindow and MosaicDialog.
        self.value_window = ValueWindow()
        self.mosaic_dialog = MosaicDialog()
        self.mosaic_dialog.sigEdited.connect(self.setMosaicLines)
        self.mosaic_dialog.sigFinished.connect(self.openMosaicView)
        self.mosaic_dialog.sigClosed.connect(self.mosaicDialogClosed)

        # The MosaicView class is only initialized if needed
        self.mosaic_view = None

        # 'mosaic_lines' contains a list of help lines shown when the
        # MosaicDialog is openend.
        self.mosaic_lines = {}

        # The histogram window is only initialized if needed
        self.hist = None

        # The ipython qtconsole is only initialized if needed.
        self.console = None
        
        self.is_linked = False
        
        self.mosaic_active = False
        self.blockSavingWindowSize = False
        self.setWindowTitle("vini viewer")
        self.setupUI()
        
        
    

    def setupUI(self):
        """
        Sets up all window elements, keyboard shortcuts and signal.
        """
        
        #%%setupUI
        
        full_path = os.path.realpath(__file__)

        # vini is a QMainWindow
        self.setObjectName(_fromUtf8("vini"))
        width = self.preferences['window_width']
        height = self.preferences['window_height']
        posx = self.preferences['window_posx']
        posy = self.preferences['window_posy']
        log1("setupUI: window posx: {}, posy: {}, width: {}, height: {}".format(posx, posy, width, height))
        self.setGeometry(posx, posy, width, height)

        self.setWindowIcon(QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/app_icon.svg')))

        # The size of the slice widget kept changing as did the offset of all
        # other widgets. 'listoffset' was used to make this easier.
        self.listoffset = 36

        # Set central widget
        self.centralwidget = QtGui.QWidget()
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # Layout Initialization: set central widget to window
        self.l = QtGui.QGridLayout()
        # Sets a 0 pixel border around each widget.
        self.l.setSpacing(0)
        # Sets a 2 pixel border at the border of the window
        self.l.setContentsMargins(1,1,1,1)
        self.centralwidget.setLayout(self.l)
        self.setCentralWidget(self.centralwidget)

        # Sets up the menu
        self.setMenu()

        # SliceWidget initializations
        self.c_slice_widget = SliceWidget('c')
        self.s_slice_widget = SliceWidget('s')
        self.t_slice_widget = SliceWidget('t')
        ydim_slicewidget = 12
        self.l.addWidget(self.c_slice_widget, 0, 0, ydim_slicewidget, ydim_slicewidget)
        self.l.addWidget(self.s_slice_widget, 0, 12, ydim_slicewidget, ydim_slicewidget)
        self.l.addWidget(self.t_slice_widget, 0, 24, ydim_slicewidget, ydim_slicewidget)
        self.c_slice_widget.sigSelected.connect(self.sliceFocusC)
        self.s_slice_widget.sigSelected.connect(self.sliceFocusS)
        self.t_slice_widget.sigSelected.connect(self.sliceFocusT)
        self.c_slice_widget.sb.menu.sigPopout.connect(self.openSliceC)
        self.s_slice_widget.sb.menu.sigPopout.connect(self.openSliceS)
        self.t_slice_widget.sb.menu.sigPopout.connect(self.openSliceT)

        self.slice_popouts[0] = SingleSlice('c')
        self.slice_popouts[1] = SingleSlice('s')
        self.slice_popouts[2] = SingleSlice('t')

        spacer = QtWidgets.QSpacerItem(7, ydim_slicewidget, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.l.addItem(spacer, 0, 36, ydim_slicewidget, 1)
        #self.l.addItem(spacer, 0, 50, ydim_slicewidget, ydim_slicewidget)


        imagelist_layout = QtGui.QGridLayout()
        imagelist_layout.setSpacing(0)

        # Imagelist widget (containing the names of all images)
        self.imagelist = QtGui.QListWidget()
        # The 'currentItemChanged'-signal is necessary if someone uses the up
        # and down arrows to change the selected item.
        # one might have to override mouseReleaseEvent() to fix "release over
        # checkbox" bug
        self.imagelist.currentItemChanged.connect(self.selectionChange)
        self.imagelist.itemClicked.connect(self.selectionChange)
        self.imagelist.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        
        ypos = 0
        imagelist_layout.addWidget(self.imagelist, 0, 0, 4, 2)

        # Swap up and down buttons
        self.up_button = QtGui.QToolButton(self)
        self.down_button = QtGui.QToolButton(self)
        self.up_button.clicked.connect(self.swapUp)
        self.down_button.clicked.connect(self.swapDown)
        
        icon_up = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/chevron-up.svg'))
        icon_down = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/chevron-down.svg'))
        self.up_button.setIcon(icon_up)
        self.down_button.setIcon(icon_down)
        self.up_button.setToolTip('move image up')
        self.down_button.setToolTip('move image down')
        imagelist_layout.addWidget(self.up_button, 0, 4, 1, 1)
        imagelist_layout.addWidget(self.down_button, 1, 4, 1, 1)
        
        # add image button
        self.add_button = QtGui.QToolButton(self)
        self.add_button.clicked.connect(self.openNewFile)
        icon_add = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/plus.svg'))
        
        self.add_button.setIcon(icon_add)
        self.add_button.setToolTip("add image")
        imagelist_layout.addWidget(self.add_button, 2, 4, 1, 1)

        # delete image button
        self.del_button = QtGui.QToolButton(self)
        self.del_button.clicked.connect(self.deleteImage)
        icon_dash = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/dash.svg'))
        self.del_button.setIcon(icon_dash)
        self.del_button.setToolTip("remove currently selected image")
        imagelist_layout.addWidget(self.del_button, 3, 4, 1, 1)
        
        imagelist_layout_title = QtWidgets.QLabel("<b>Image List<b>")
        imagelist_layout_title.setStyleSheet("""
            font-family: Arial;
            font-size: 15px;
        """)
        imagelist_layout_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        upper_layout = QtWidgets.QVBoxLayout()
        upper_layout.setContentsMargins(0, 20, 0, 30)
        upper_layout.addWidget(imagelist_layout_title)
        upper_layout.addSpacing(10)
        upper_layout.addLayout(imagelist_layout)

        self.l.addLayout(upper_layout, 0, self.listoffset+2, 1, 1)
        
        
        # Crosshair button toggle
        button_row_crosshair = QtGui.QHBoxLayout()
        button_row_crosshair.setSpacing(0)
        self.cross_button = QtGui.QToolButton(self)
        self.cross_button.setCheckable(True)
        self.cross_button.setChecked(True)
        
        icon_cross = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/cross.svg'))
        self.cross_button.setIcon(icon_cross)
        self.cross_button.setToolTip("toggle crosshair on/off")
        self.cross_button.clicked.connect(self.setCrosshairsVisible)
        button_row_crosshair.addWidget(self.cross_button, 1)


        # Find min/max buttons
        self.min_button = QtGui.QToolButton(self)
        self.max_button = QtGui.QToolButton(self)
        self.min_button.clicked.connect(self.findMin)
        self.max_button.clicked.connect(self.findMax)
        icon_min = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/min.svg'))
        icon_max = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/max.svg'))
        self.min_button.setIcon(icon_min)
        self.max_button.setIcon(icon_max)
        self.min_button.setToolTip("go to local minimum")
        self.max_button.setToolTip("go to local maximum")
        button_row_crosshair.addWidget(self.min_button, 1)
        button_row_crosshair.addWidget(self.max_button, 1)
        
        #reset all button
        self.reset_button = QtGui.QPushButton("reset")
        self.reset_button.clicked.connect(self.resetEverything)
        self.reset_button.setToolTip("reset everything!")
        button_row_crosshair.addWidget(self.reset_button, 2)
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Fixed)
        button_row_crosshair.addWidget(spacer,5)
        
        
        self.alpha_sld_timer = QtCore.QTimer(self)
        self.alpha_sld_timer.setSingleShot(True)
        self.alpha_sld_timer.timeout.connect(self.setAlphaFromSlider)
        # alpha slider
        # ypos = 8
        button_row_alpha = QtGui.QHBoxLayout()
        button_row_alpha.setSpacing(0)
        self.alpha_sld = JumpSlider(QtCore.Qt.Orientation.Horizontal)
        self.alpha_sld.setMinimum(0)
        self.alpha_sld.setMaximum(100)
        self.alpha_sld.setValue(100)
        self.alpha_sld.setToolTip("change opacity of selected image")
        self.alpha_sld.valueChanged.connect(self.startSetAlphaTimer)
        button_row_alpha.addWidget(self.alpha_sld, 2)
        
        self.alpha_label = QtGui.QLabel('100% opacity')
        self.alpha_label.setAlignment( QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        button_row_alpha.addWidget(self.alpha_label, 3)
        

        # coordinate labels
        button_row_coordinates = QtGui.QHBoxLayout()
        self.x_box = QtGui.QLineEdit()
        self.y_box = QtGui.QLineEdit()
        self.z_box = QtGui.QLineEdit()
        
        #not nice... setting px explicitly
        width_q = width/4
        self.txt_box_size = round(width_q/8)
        self.txt_box_size_xl = round(width_q/5.5)
        self.grad_size = round(2*width_q/5)
        
        self.x_box.setFixedWidth(self.txt_box_size)
        self.y_box.setFixedWidth(self.txt_box_size)
        self.z_box.setFixedWidth(self.txt_box_size)
        
        self.x_box.setToolTip("enter x coordinate")
        self.y_box.setToolTip("enter y coordinate")
        self.z_box.setToolTip("enter z coordinate")
        #only allow numbers here...
        self.x_box.setValidator(QtGui.QDoubleValidator())
        self.y_box.setValidator(QtGui.QDoubleValidator())
        self.z_box.setValidator(QtGui.QDoubleValidator())
        
        
        self.x_box.editingFinished.connect(self.setCrosshairBoxCoord)
        self.y_box.editingFinished.connect(self.setCrosshairBoxCoord)
        self.z_box.editingFinished.connect(self.setCrosshairBoxCoord)
        button_row_coordinates.addWidget(self.x_box,1)
        button_row_coordinates.addWidget(self.y_box,1)
        button_row_coordinates.addWidget(self.z_box,1)
        
        self.voxel_button = QtGui.QPushButton("voxel")
        self.voxel_button.clicked.connect(self.switchVoxelCoord)
        self.voxel_button.setToolTip("toggle voxel / millimeter coordinates")
        
        button_row_coordinates.addWidget(self.voxel_button,1)
        
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Minimum)
        button_row_coordinates.addWidget(spacer,5)
        button_row_coordinates.setSpacing(0)

        
        # ypos = 6
        # one frame backward button
        button_row_fmri = QtGui.QHBoxLayout()
        button_row_fmri.setSpacing(0)
        self.backward_button = QtGui.QToolButton(self)
        self.backward_button.pressed.connect(self.prevFrame)
        self.backward_button.released.connect(self.setSliceStateOff)
        icon_backward = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/prev.svg'))
        
        self.backward_button.setIcon(icon_backward)
        self.backward_button.setToolTip("move to previous volume")
        
        button_row_fmri.addWidget(self.backward_button)

        
        # play button
        self.play_button = QtWidgets.QPushButton(self)
        self.play_button.pressed.connect(self.playFuncPressed)
        self.play_button.released.connect(self.playFuncReleased)
        
        self.icon_play = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/triangle-right.svg'))
        self.icon_pause = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/pause.svg'))
        
        self.play_button.setIcon(self.icon_play)
        self.play_button.setToolTip("play as movie")
        button_row_fmri.addWidget(self.play_button)
        
        # forward one frame button
        self.forward_button = QtWidgets.QPushButton(self)#QToolButton(self)
        self.forward_button.pressed.connect(self.nextFrame)
        self.forward_button.released.connect(self.setSliceStateOff)
        icon_forward = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/next.svg'))
        
        
        self.forward_button.setIcon(icon_forward)
        self.forward_button.setToolTip("move to next volume")
        button_row_fmri.addWidget(self.forward_button)
        


        # Lineedit for frame number
        self.frame_box = QtGui.QLineEdit('0')
        self.frame_box.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        self.frame_box.returnPressed.connect(self.setFrameFromBox)
        self.frame_box.editingFinished.connect(self.setFrameFromBox)
        self.frame_box.setToolTip("enter volume")
        self.frame_box.setFixedWidth(self.txt_box_size)
        self.frame_box.setValidator(QtGui.QDoubleValidator())
        
        button_row_fmri.addWidget(self.frame_box)
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Fixed)
        button_row_fmri.addWidget(spacer,5)

        self.frame_sld_timer = QtCore.QTimer(self)
        self.frame_sld_timer.setSingleShot(True)
        self.frame_sld_timer.timeout.connect(self.setFrameFromSlider)
        # frame slider (time)
        button_row_fmrislider = QtGui.QHBoxLayout()
        self.frame_sld = JumpSlider(QtCore.Qt.Orientation.Horizontal)
        self.frame_sld.setMinimum(0)
        self.frame_sld.setMaximum(0)
        self.frame_sld.setValue(0)
        self.frame_sld.sliderPressed.connect(self.setSliceStateOn)
        self.frame_sld.sliderReleased.connect(self.setSliceStateOff)
        self.frame_sld.valueChanged.connect(self.startSetFrameTimer)
        self.frame_sld.setToolTip("select volume")
        
        
        button_row_fmrislider.addWidget(self.frame_sld,3)
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Fixed)
        button_row_fmrislider.addWidget(spacer,1)

        slider_box_title = QtWidgets.QLabel("<b>Sliders<b>")
        slider_box_title.setStyleSheet("""
            font-family: Arial;
            font-size: 15px;
        """)
        slider_box_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        slider_box_layout = QtWidgets.QVBoxLayout()
        slider_box_layout.setSpacing(0)
        slider_box_layout.setContentsMargins(0, 30, 0, 30)
        slider_box_layout.addWidget(slider_box_title)

        box_layout = QtWidgets.QVBoxLayout()

        button_row_alpha_title = QtWidgets.QLabel("<b><Opacity</b>")
        button_row_alpha_title.setStyleSheet("""
            font-family: Arial;
            font-size: 12px;
        """)
        box_layout.addWidget(button_row_alpha_title)
        box_layout.addLayout(button_row_alpha)

        box_layout.addSpacing(10)
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine) 
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        box_layout.addWidget(line)
        box_layout.addSpacing(10)

        button_row_fmri_title = QtWidgets.QLabel("<b>Time series toolbar<b>")
        button_row_fmri_title.setStyleSheet("""
            font-family: Arial;
            font-size: 12px;
        """)
        box_layout.addWidget(button_row_fmri_title)
        box_layout.addLayout(button_row_fmri)
        box_layout.addLayout(button_row_fmrislider)


        slider_box = QtWidgets.QGroupBox()
        slider_box.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 5px; margin-top: 10px; } ")

        slider_box.setLayout(box_layout)
        slider_box_layout.addWidget(slider_box)

        self.l.addLayout(slider_box_layout, 1, self.listoffset+2, 1, 1)
        

        #intensity layout
        intensity_layout = QtGui.QHBoxLayout()

        self.intensity_image_name= QtGui.QLabel('')
        self.intensity_image_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.intensity_image_name.setFixedWidth(120)
        intensity_layout.addWidget(self.intensity_image_name,1)
        intensity_layout.addSpacing(20)

        icon_label =  QtGui.QToolButton(self)
        icon_cross = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/cross.svg'))
        icon_label.setIcon(icon_cross)
        icon_label.setIconSize(QtCore.QSize(20, 20))
        intensity_layout.addWidget(icon_label)
        intensity_layout.addSpacing(10)

        self.intensity_value = QtGui.QLabel("nan")
        self.intensity_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.intensity_value.setFixedWidth(80)
        intensity_layout.addWidget(self.intensity_value)
        intensity_layout.addSpacing(10)

        icon_label =  QtGui.QToolButton(self)
        icon_cursor = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/cursor.svg'))
        icon_label.setIcon(icon_cursor)
        icon_label.setIconSize(QtCore.QSize(20, 20))
        intensity_layout.addWidget(icon_label)
        intensity_layout.addSpacing(10)

        self.intensity_value_mouse = QtGui.QLabel("nan")
        self.intensity_value_mouse.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.intensity_value_mouse.setFixedWidth(80)
        intensity_layout.addWidget(self.intensity_value_mouse)
        intensity_layout.addSpacing(10)

        #self.l.addLayout(intensity_layout, 6, self.listoffset+2, 1, 4)


        crosshair_info_layout_title = QtWidgets.QLabel("<b>Crosshair Toolbar<b>")
        crosshair_info_layout_title.setStyleSheet("""
            font-family: Arial;
            font-size: 15px;
        """)
        crosshair_info_layout_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        crosshair_info_layout = QtWidgets.QVBoxLayout()
        crosshair_info_layout.setSpacing(0)
        crosshair_info_layout.setContentsMargins(0, 30, 0, 60)
        crosshair_info_layout.addWidget(crosshair_info_layout_title)

    
        button_row_coordinates_title = QtWidgets.QLabel("<b>Crosshair position<b>")
        button_row_coordinates_title .setStyleSheet("""
            font-family: Arial;
            font-size: 12px;
        """)

        crosshair_box_layout = QtWidgets.QVBoxLayout()
        crosshair_box_layout.addWidget(button_row_coordinates_title)
        crosshair_box_layout.addLayout(button_row_coordinates)

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Fixed)
        spacer.setFixedHeight(10)

        crosshair_box_layout.addWidget(spacer)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine) 
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        crosshair_box_layout.addWidget(line)
        crosshair_box_layout.addWidget(spacer)


        button_row_crosshair_title = QtWidgets.QLabel("<b>Crosshair actions<b>")
        button_row_crosshair_title.setStyleSheet("""
            font-family: Arial;
            font-size: 12px;
        """)
        crosshair_box_layout.addWidget(button_row_crosshair_title)
        crosshair_box_layout.addLayout(button_row_crosshair)

        crosshair_box_layout.addWidget(spacer)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine) 
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        crosshair_box_layout.addWidget(line)
        crosshair_box_layout.addWidget(spacer)

        intensity_layout_title = QtWidgets.QLabel("<b>Crosshair and cursor intensities<b>")
        intensity_layout_title.setStyleSheet("""
            font-family: Arial;
            font-size: 12px;
        """)
        crosshair_box_layout.addWidget(intensity_layout_title)
        crosshair_box_layout.addLayout(intensity_layout)

        crosshair_box = QtWidgets.QGroupBox()
        crosshair_box.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 5px; margin-top: 10px; } ")
        crosshair_box.setLayout(crosshair_box_layout)
        crosshair_info_layout.addWidget(crosshair_box)

        self.l.addLayout(crosshair_info_layout, 2, self.listoffset+2, 1, 1)

        
        
        # upper threshold slider
        button_row_thresh_pos = QtGui.QHBoxLayout()
        button_row_thresh_neg = QtGui.QHBoxLayout()
        self.slider_color = QtGui.QColor()
        self.slider_color.setRgb(255, 110, 0)
        
        self.slider_color_off = QtGui.QColor()
        self.slider_color_off.setRgb(150, 150, 150)

        self.slider_pos_timer = QtCore.QTimer(self)
        self.slider_pos_timer.setSingleShot(True) 
        self.slider_pos_timer.timeout.connect(self.setPosThresholdFromSliders)

        self.slider_pos = QxtSpanSlider()
        self.slider_pos.setGradientLeftColor(self.slider_color)
        self.slider_pos.setGradientRightColor(self.slider_color)
        self.slider_pos.setRange(0, 1000)
        self.slider_pos.setSpan(0, 1000)
        self.slider_pos.setEnabled(False)
        self.slider_pos.setMinimumWidth(100)
        self.slider_pos.spanChanged.connect(self.startPosSliderTimer)
        self.slider_pos.setToolTip("change positive thresholds")

        self.slider_neg_timer = QtCore.QTimer(self)
        self.slider_neg_timer.setSingleShot(True) 
        self.slider_neg_timer.timeout.connect(self.setNegThresholdFromSliders)
        
        self.slider_neg = QxtSpanSlider()
        self.slider_neg.setGradientLeftColor(self.slider_color)
        self.slider_neg.setGradientRightColor(self.slider_color)
        self.slider_neg.setRange(0, 1000)
        self.slider_neg.setSpan(0, 1000)
        self.disableSliderNeg()
        self.slider_neg.spanChanged.connect(self.startNegSliderTimer)
        self.slider_neg.setToolTip("change negative thresholds")
        # small fix, otherwise layout will be messed up!
        not_resize = self.slider_neg.sizePolicy()
        not_resize.setRetainSizeWhenHidden(True)
        self.slider_neg.setSizePolicy(not_resize)



        # threshold line edits
        self.min_pos = QtGui.QLineEdit()
        self.max_pos = QtGui.QLineEdit()
        self.max_neg = QtGui.QLineEdit()
        self.min_neg = QtGui.QLineEdit()
        
        self.min_pos.setValidator(QtGui.QDoubleValidator())
        self.max_pos.setValidator(QtGui.QDoubleValidator())
        self.max_neg.setValidator(QtGui.QDoubleValidator())
        self.min_neg.setValidator(QtGui.QDoubleValidator())
        
        # small fix, otherwise layout will be messed up!
        not_resize = self.max_neg.sizePolicy()
        not_resize.setRetainSizeWhenHidden(True)
        self.max_neg.setSizePolicy(not_resize)

        
        self.min_pos.setMaxLength(6)
        self.max_pos.setMaxLength(6)
        self.max_neg.setMaxLength(6)
        self.min_neg.setMaxLength(6)
        
        
        self.min_pos.setFixedWidth(self.txt_box_size_xl)
        self.max_pos.setFixedWidth(self.txt_box_size_xl)
        self.max_neg.setFixedWidth(self.txt_box_size_xl)
        self.min_neg.setFixedWidth(self.txt_box_size_xl)
        
        
        self.min_pos.returnPressed.connect(self.setPosThresholdsFromBoxes)
        self.max_pos.returnPressed.connect(self.setPosThresholdsFromBoxes)
        self.max_neg.returnPressed.connect(self.setNegThresholdsFromBoxes)
        self.min_neg.returnPressed.connect(self.setNegThresholdsFromBoxes)
        
        self.min_pos.editingFinished.connect(self.setPosThresholdsFromBoxes)
        self.max_pos.editingFinished.connect(self.setPosThresholdsFromBoxes)
        self.max_neg.editingFinished.connect(self.setNegThresholdsFromBoxes)
        self.min_neg.editingFinished.connect(self.setNegThresholdsFromBoxes)
        
        self.min_neg.setToolTip("change minimum negative threshold")
        self.max_neg.setToolTip("change maximum negative threshold")
        self.min_pos.setToolTip("change minimum positive threshold")
        self.max_pos.setToolTip("change maximum positive threshold")
        
        
        button_row_thresh_pos.addWidget(self.min_pos)
        button_row_thresh_pos.addWidget(self.max_pos)
        
        button_row_thresh_neg.addWidget(self.max_neg)
        button_row_thresh_neg.addWidget(self.min_neg)

        colormaps_title = QtWidgets.QLabel("<b>Colormaps Toolbar<b>")
        colormaps_title .setStyleSheet("""
            font-family: Arial;
            font-size: 15px;
        """)
        colormaps_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.l.addWidget(colormaps_title, 7, self.listoffset+2, 1, 1)
        
        self.l.addWidget(self.slider_pos, 8, self.listoffset+2, 1, 1)
        self.l.addLayout(button_row_thresh_pos, 9, self.listoffset+2, 1, 1)
        self.l.addLayout(button_row_thresh_neg, 10, self.listoffset+2, 1, 1)
        self.l.addWidget(self.slider_neg, 11, self.listoffset+2, 1, 1)
        
        self.crosshair_timer = QtCore.QTimer(self)
        self.crosshair_timer.setSingleShot(True)
        self.crosshair_timer.timeout.connect(self.setCrosshair)
        

        # connect crosshair and cursor move events
        # for crosshair
        self.c_slice_widget.sigCPChanged.connect(self.startCrosshairTimer)
        self.s_slice_widget.sigCPChanged.connect(self.startCrosshairTimer)
        self.t_slice_widget.sigCPChanged.connect(self.startCrosshairTimer)
        self.slice_popouts[0].sw.sigCPChanged.connect(self.startCrosshairTimer)
        self.slice_popouts[1].sw.sigCPChanged.connect(self.startCrosshairTimer)
        self.slice_popouts[2].sw.sigCPChanged.connect(self.startCrosshairTimer)

        # for cursor
        self.c_slice_widget.sigMouseOver.connect(self.MouseMoved)
        self.s_slice_widget.sigMouseOver.connect(self.MouseMoved)
        self.t_slice_widget.sigMouseOver.connect(self.MouseMoved)
        self.slice_popouts[0].sw.sigMouseOver.connect(self.MouseMoved)
        self.slice_popouts[1].sw.sigMouseOver.connect(self.MouseMoved)
        self.slice_popouts[2].sw.sigMouseOver.connect(self.MouseMoved)

        ## keyboard shortcuts ##
        # zooming in
        self.zoom_in = QtGui.QAction('ZoomIn', self)
        self.zoom_in.setShortcut(QtGui.QKeySequence.StandardKey.ZoomIn)
        self.zoom_in.triggered.connect(self.zoomIn)
        self.addAction(self.zoom_in)

        # zooming out
        self.zoom_out = QtGui.QAction('ZoomOut', self)
        self.zoom_out.setShortcut(QtGui.QKeySequence.StandardKey.ZoomOut)
        self.zoom_out.triggered.connect(self.zoomOut)
        self.addAction(self.zoom_out)

        # toggle visibility of currently selected image
        self.visibility = QtGui.QAction('visibility', self)
        self.visibility.setShortcut(QtGui.QKeySequence('v'))
        self.visibility.triggered.connect(self.toggleVisibility)
        # makes the shortcut possible when other window is focused:
        self.visibility.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.visibility)

        # toggling off the visibility of all but the current image
        self.deselect = QtGui.QAction('deselect', self)
        self.deselect.setShortcut(QtGui.QKeySequence('d'))
        self.deselect.triggered.connect(self.toggleDeselect)
        self.deselect.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.deselect)

        # reset view
        self.reset_view = QtGui.QAction('reset view', self)
        self.reset_view.setShortcut(QtGui.QKeySequence('r'))
        self.reset_view.triggered.connect(self.autoRange)
        self.addAction(self.reset_view)

        # toggling the crosshair off/on
        self.crosshair_ac = QtGui.QAction('crosshair toggle', self)
        self.crosshair_ac.setShortcut(QtGui.QKeySequence('x'))
        self.crosshair_ac.triggered.connect(self.toggleCrosshairs)
        self.crosshair_ac.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.crosshair_ac)

        # move image up (in list and z-value)
        self.set_current_higher = QtGui.QAction('set_higher', self)
        self.set_current_higher.setShortcut(QtGui.QKeySequence('w'))
        self.set_current_higher.triggered.connect(self.setCurrentHigher)
        self.set_current_higher.setShortcutContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.set_current_higher)

        # move image down (in list and z-value)
        self.set_current_lower = QtGui.QAction('set_lower', self)
        self.set_current_lower.setShortcut(QtGui.QKeySequence('s'))
        self.set_current_lower.triggered.connect(self.setCurrentLower)
        self.set_current_lower.setShortcutContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.set_current_lower)

        # go to next frame
        self.next_frame = QtGui.QAction('next frame', self)
        self.next_frame.setShortcut(QtGui.QKeySequence('n'))
        self.next_frame.triggered.connect(self.nextFrame)
        self.next_frame.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.next_frame)

        # go to previous frame
        self.prev_frame = QtGui.QAction('previous frame', self)
        self.prev_frame.setShortcut(QtGui.QKeySequence('b'))
        self.prev_frame.triggered.connect(self.prevFrame)
        self.prev_frame.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.prev_frame)

        # play frames
        self.play_func = QtGui.QAction('play functional frames', self)
        self.play_func.setShortcut(QtGui.QKeySequence(' '))
        self.play_func.triggered.connect(self.shortcutPlay)
        self.play_func.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.addAction(self.play_func)

        # disables the functional play buttons and sliders
        self.disableFuncView()

        # links or delinks the slice widgets
        if self.link_mode == 0:
            self.linkSlices(True)
        else:
            self.linkSlices(False)

        # this turn on the visibility of the window
        self.show()


    def setMenu(self):
        """
        Sets up the menu categories and items
        """

        # main menu bar
        self.menubar = QtGui.QMenuBar(self)
        # categories in the menu bar
        self.file_menu = self.menubar.addMenu('&File')
        self.resampling_menu = self.menubar.addMenu('&Resampling')
        self.image_menu = self.menubar.addMenu('&Image')
        self.tools_menu = self.menubar.addMenu('&Tools')
        self.settings_menu = self.menubar.addMenu('&Preferences')

        ## file related menu items ##
        openFile = QtGui.QAction(
            QtGui.QIcon.fromTheme("document-open"), 'Open Image', self)
        openFile.setShortcut(QtGui.QKeySequence("o"))
        openFile.setStatusTip('Open new file')
        openFile.triggered.connect(self.openNewFile)
        self.file_menu.addAction(openFile)

        exit_action = QtGui.QAction(
            QtGui.QIcon.fromTheme("window-close"), '&Exit', self)
        exit_action.setShortcut(QtGui.QKeySequence("Ctrl+C"))
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.closeAndSave)
        self.file_menu.addAction(exit_action)

        ## resampling and view related menu items ##
        res_os_ratio = QtGui.QAction('Set oversampling ratio', self)
        res_os_ratio.triggered.connect(self.setOSRatio)
        self.resampling_menu.addAction(res_os_ratio)

        self.icon_checked  = QtGui.QIcon(pkg_resources.resource_filename(__name__, 'icons/check.svg'))
        

        self.res_affine = QtGui.QAction('Apply affine transformation', self)
        self.res_affine.setShortcut('Ctrl+A')
        self.res_affine.setIcon(self.icon_checked)
        self.res_affine.setStatusTip('Applies affine of the image')
        self.res_affine.triggered.connect(self.resampleToAffineClicked)
        self.resampling_menu.addAction(self.res_affine)

        self.res_current = QtGui.QAction(
            'Resample to currently selected image', self)
        self.res_current.setShortcut('Ctrl+I')
        self.res_current.setStatusTip(
            'Resamples to currently selected image and uses its resolution')
        self.res_current.triggered.connect(self.resampleToCurrentClicked)
        self.resampling_menu.addAction(self.res_current)

        self.res_fit = QtGui.QAction('Ignore affine and pray', self)
        self.res_fit.setShortcut('Ctrl+F')
        self.res_fit.setStatusTip(
            'Use this only for images with missing affine transformations')
        self.res_fit.triggered.connect(self.resampleToFitClicked)
        self.resampling_menu.addAction(self.res_fit)

        ## Image related properties and options ##
        # for opening the image settings
        image_settings = QtGui.QAction('Image settings', self)
        image_settings.setShortcut(QtGui.QKeySequence('i'))
        image_settings.setStatusTip('Set properties of current image')
        image_settings.triggered.connect(self.openImageSettings)
        self.image_menu.addAction(image_settings)

        # for displaying the time series data
        image_time = QtGui.QAction('Image time series', self)
        image_time.setShortcut(QtGui.QKeySequence('t'))
        image_time.setStatusTip('View time series of image voxel')
        image_time.triggered.connect(self.openTimeSeries)
        self.image_menu.addAction(image_time)


        ## Tools menu for helpful tools ##
        # export function
        openExport = QtGui.QAction('Export Images', self)
        openExport.setShortcut(QtGui.QKeySequence('e'))
        openExport.setStatusTip('Open Exporter')
        openExport.triggered.connect(self.export)
        self.tools_menu.addAction(openExport)

        # for opening the histogram threshold widget
        openHistogram = QtGui.QAction('Histogram', self)
        openHistogram.setShortcut(QtGui.QKeySequence('h'))
        openHistogram.setStatusTip('Open Histogram')
        openHistogram.triggered.connect(self.openHistogramWindow)
        self.tools_menu.addAction(openHistogram)

        # copy properties
        copyImageProps = QtGui.QAction('Copy image properties', self)
        copyImageProps.setShortcut('c')
        copyImageProps.setStatusTip('Copy image properties to other images')
        copyImageProps.triggered.connect(self.copyImagePropsFunc)
        self.tools_menu.addAction(copyImageProps)

        # for opening the mosaic view
        openMosaic = QtGui.QAction('Open mosaic dialog', self)
        openMosaic.setShortcut('m')
        openMosaic.setStatusTip('Opens mosaic dialog')
        openMosaic.triggered.connect(self.openMosaic)
        self.tools_menu.addAction(openMosaic)

        ## Preferences ##
        # for editing the search width
        searchPreferences = QtGui.QAction('Search min/max width', self)
        searchPreferences.setStatusTip('Change search width')
        searchPreferences.triggered.connect(self.changeSearchRadius)
        self.settings_menu.addAction(searchPreferences)

        # editing preferences
        openPreferences = QtGui.QAction('Settings', self)
        openPreferences.setShortcut('p')
        openPreferences.setStatusTip('Open Settings')
        openPreferences.triggered.connect(self.openSettings)
        self.settings_menu.addAction(openPreferences)

        self.setMenuBar(self.menubar)

    ## Section: Loading and Deleting Images ##
    def loadImagesFromFiles(self, filename_list, type_list):
        """
        Takes a list of filenames and types (normal - 0, or z-map = 1) and
        loads them into the viewer.

        This function is supposed to be called only once at the start of the
        viewer. (It is assumed there are no further extra windows.)
        For subsequent images use loadNewImage.
        """
        # Don't do anything for an empty list.
        if len(filename_list) == 0:
            return

        for i in range(len(filename_list)):
            img = loadImageFromFile(
                unicode(filename_list[i]), self.preferences, type_list[i])
            # Saves the first part of the path as 'prefered_path'.
            self.prefered_path = "/".join(filename_list[i].split('/')[:-1])
            # Connects changes in the image dialog with rerendering the image.
            img.dialog.sigImageChanged.connect(self.updateImages)
            img.dialog.sigImageChanged.connect(self.updateSelected)

            if img.type_d() == "4D":
                if img.getTimeDim() > self.time_dim:
                    self.time_dim = img.getTimeDim()
                    self.frame_sld.setMaximum(self.time_dim-1)

            # Images are always inserted at the beginning.
            self.images.insert(0, img)
            # By default the image is visible in the main window.
            # Create ImageItemMods here.
            image_item_list_tmp = [[]]
            for j in range(3):
                image_item_list_tmp[0].append(ImageItemMod())
            self.image_window_list.append(image_item_list_tmp)

            # This creates ImageItemMods for the popout slices.
            image_item_list_tmp_po = []
            for j in range(3):
                image_item_list_tmp_po.append(ImageItemMod())
            self.popouts_ii.append(image_item_list_tmp_po)
            # Set state as True, because it's visible in the main window.
            self.states.insert(0, True)
            # Add image list entry.
            itemname = filename_list[i]
            self.addToList(itemname)
        
        self.checkIf2DAndRemovePanes()

        # Resample all loaded images to one coordinate system.
        # Which coordinate system is used depends on the preference settings.
        if self.preferences['res_method'] == 0:
            verboseprint("resampling to affine")
            self.resampleToAffine()
        if self.preferences['res_method'] == 1:
            verboseprint("resampling to current")
            self.resampleToCurrent()
        if self.preferences['res_method'] == 2:
            verboseprint("resampling to fit")
            self.resampleToFit()

        self.setSliceWidgetsDims()

        # After the resampled data is available the thresholds and colormaps
        # can be set to their default values.
        for img in self.images:
            img.setThresholdsDefault()
            img.setColorMapPos()
            img.setColorMapNeg()

        # This updates the image data in all the ImageItemMods.
        self.updateImageItems()

        for i in range(len(filename_list)):
            # Add ImageItemMods to the SliceWidgets.
            self.addToSliceWidgets(i)
            # Add colormaps to the layout.
            self.addPosNegWidget(self.images[i].pos_gradient, self.images[i].neg_gradient)
            # Connect the color map gradients to update the slices and images.
            self.images[i].pos_gradient.sigGradientChanged.connect(self.updateImages)
            self.images[i].neg_gradient.sigGradientChanged.connect(self.updateImages)
            self.images[i].pos_gradient.sigDiscreteCM.connect(self.setDiscreteCM)
            self.images[i].neg_gradient.sigDiscreteCM.connect(self.setDiscreteCM)

        # Because the images are inserted at 0 the filelist has to be reversed
        # to align correctly with the image list.
        filename_list.reverse()
        # The filenames are passed to the image objects for useful window
        # titles in the dialogs and such.
        for i in range(len(filename_list)):
            itemname = os.path.split(filename_list[i])[-1]
            self.images[i].dialog.setWindowTitle(itemname)
            if self.images[i].type_d() == "4D":
                self.images[i].funcdialog.setWindowTitle(itemname)
                if self.images[i].frame_time == 0: # HERE IS THE QUICK FIX
                    self.images[i].frame_time = 1.0
                    QtGui.QMessageBox.warning(
                            self, "Warning",
                            "Warning: TR not found. Set automatically to 1. TR can \
    			             be changed in the functional image dialog.")

        # If functional image are present the widgets are turned on.
        self.resetFuncView()

        # Reseting the z values will render the images in the correct order.
        self.resetZValues()

        # Select the image on top as the current image.
        self.imagelist.setCurrentRow(0)

        self.setCrosshairPositionCenter()

        # This sets all properties of the current image to the widgets in the
        # viewer.
        self.updateSelected()

        # This will automatically scale and pan the images in the slices.
        self.autoRange()

    def loadNewImageObject(self, fileobj, filename='NiftiObj'):
        """
        Loads a new file.
        """
        # Gets the image instance from 
        img = loadImageFromNifti(fileobj, self.preferences, 0)
        img.dialog.sigImageChanged.connect(self.updateImages)
        img.dialog.sigImageChanged.connect(self.updateSelected)

        if img.type_d() == "4D":
            if img.getTimeDim() > self.time_dim:
                self.time_dim = img.getTimeDim()
                self.frame_sld.setMaximum(self.time_dim-1)
            if img.frame_time == 0:
                QtGui.QMessageBox.warning(
                    self, "Warning",
                    "Warning: TR not found. Set it automatically in the \
                    functional image dialog.")

        # For each extra window add a list of Nones because the image is in
        # none of them.
        image_item_list_tmp = [[]] + [ [None]*3 ] * len(self.extra_windows)
        image_item_list_tmp_po = []
        # The image should be in the main window.
        for j in range(3):
            image_item_list_tmp[0].append(ImageItemMod())
            image_item_list_tmp_po.append(ImageItemMod())
        self.image_window_list.insert(0, image_item_list_tmp)
        self.popouts_ii.insert(0, image_item_list_tmp_po)

        self.images.insert(0, img)
        self.states.insert(0, True)

        itemname = os.path.split(filename)[-1]
        self.addToList(itemname)

        # Resample all images with previous settings
        # This makes sense since the new image might have a higher resolution.
        self.reresample()

        self.addToSliceWidgets(0)

        self.setSliceWidgetsDims()
        self.setCrosshairPositionCenter()

        # Colormaps
        self.addPosNegWidget(self.images[0].pos_gradient, self.images[0].neg_gradient)
        # connect to update slices and imageitems
        self.images[0].pos_gradient.sigGradientChanged.connect(self.updateImages)
        self.images[0].neg_gradient.sigGradientChanged.connect(self.updateImages)
        self.images[0].pos_gradient.sigDiscreteCM.connect(self.setDiscreteCM)
        self.images[0].neg_gradient.sigDiscreteCM.connect(self.setDiscreteCM)

        self.images[0].dialog.setWindowTitle(itemname)

        if self.images[0].type_d() == "4D":
            self.images[0].funcdialog.setWindowTitle(itemname)
            if self.images[0].frame_time == 0:
                QtGui.QMessageBox.warning(
                    self, "Warning",
                    "Warning: TR not found. Set it automatically in the \
                    functional image dialog.")
                
        self.resetFuncView()

        self.resetZValues()

        self.imagelist.setCurrentRow(0)
        self.updateSelected()
        self.autoRange()

    def loadNewImage(self, filename):
        """
        Loads a new file.
        """   
        # Gets the image instance from 
        img = loadImageFromFile(unicode(filename), self.preferences, 0)
        # save path as prefered
        self.prefered_path = "/".join(filename.split('/')[:-1])
        img.dialog.sigImageChanged.connect(self.updateImages)
        img.dialog.sigImageChanged.connect(self.updateSelected)

        if img.type_d() == "4D":
            if img.getTimeDim() > self.time_dim:
                self.time_dim = img.getTimeDim()
                self.frame_sld.setMaximum(self.time_dim-1)
            if img.frame_time == 0:
                QtGui.QMessageBox.warning(
                    self, "Warning",
                    "Warning: TR not found. Set it automatically in the \
                    functional image dialog.")

        # For each extra window add a list of Nones because the image is in
        # none of them.
        image_item_list_tmp = [[]] + [ [None]*3 ] * len(self.extra_windows)
        image_item_list_tmp_po = []
        # The image should be in the main window.
        for j in range(3):
            image_item_list_tmp[0].append(ImageItemMod())
            image_item_list_tmp_po.append(ImageItemMod())
        self.image_window_list.insert(0, image_item_list_tmp)
        self.popouts_ii.insert(0, image_item_list_tmp_po)

        self.images.insert(0, img)
        self.states.insert(0, True)

        itemname = os.path.split(filename)[-1]
        self.addToList(itemname)

        # Resample all images with previous settings
        # This makes sense since the new image might have a higher resolution.
        self.reresample()

        self.addToSliceWidgets(0)

        self.setSliceWidgetsDims()
        self.setCrosshairPositionCenter()

        # Colormaps
        self.addPosNegWidget(self.images[0].pos_gradient, self.images[0].neg_gradient)
        # connect to update slices and imageitems
        self.images[0].pos_gradient.sigGradientChanged.connect(self.updateImages)
        self.images[0].neg_gradient.sigGradientChanged.connect(self.updateImages)
        self.images[0].pos_gradient.sigDiscreteCM.connect(self.setDiscreteCM)
        self.images[0].neg_gradient.sigDiscreteCM.connect(self.setDiscreteCM)

        self.images[0].dialog.setWindowTitle(itemname)

        if self.images[0].type_d() == "4D":
            self.images[0].funcdialog.setWindowTitle(itemname)
            if self.images[0].frame_time == 0:
                QtGui.QMessageBox.warning(
                    self, "Warning",
                    "Warning: TR not found. Set it automatically in the \
                    functional image dialog.")

        self.resetFuncView()

        self.resetZValues()

        self.imagelist.setCurrentRow(0)
        self.updateSelected()
        self.autoRange()
        
    def loadImagesFromNumpy(self, array, itemname):
        """
        Loads an image provided as numpy array
        """

        img = loadImageFromNumpy(array, self.preferences, 0)
        # save path as prefered
        img.dialog.sigImageChanged.connect(self.updateImages)
        img.dialog.sigImageChanged.connect(self.updateSelected)

        if img.type_d() == "4D":
            if img.getTimeDim() > self.time_dim:
                self.time_dim = img.getTimeDim()
                self.frame_sld.setMaximum(self.time_dim-1)
            if img.frame_time == 0:
                img.frame_time = 1

        # For each extra window add a list of Nones because the image is in
        # none of them.
        image_item_list_tmp = [[]] + [ [None]*3 ] * len(self.extra_windows)
        image_item_list_tmp_po = []
        # The image should be in the main window.
        for j in range(3):
            image_item_list_tmp[0].append(ImageItemMod())
            image_item_list_tmp_po.append(ImageItemMod())
        self.image_window_list.insert(0, image_item_list_tmp)
        self.popouts_ii.insert(0, image_item_list_tmp_po)

        self.images.insert(0, img)
        self.states.insert(0, True)

        img.filename = itemname
        self.addToList(itemname)
        

        # Resample all images with previous settings
        # This makes sense since the new image might have a higher resolution.
        self.reresample()

        self.addToSliceWidgets(0)

        self.setSliceWidgetsDims()
        self.setCrosshairPositionCenter()

        # Colormaps
        self.addPosNegWidget(self.images[0].pos_gradient, self.images[0].neg_gradient)
        # connect to update slices and imageitems
        self.images[0].pos_gradient.sigGradientChanged.connect(self.updateImages)
        self.images[0].neg_gradient.sigGradientChanged.connect(self.updateImages)
        self.images[0].pos_gradient.sigDiscreteCM.connect(self.setDiscreteCM)
        self.images[0].neg_gradient.sigDiscreteCM.connect(self.setDiscreteCM)

        self.images[0].dialog.setWindowTitle(itemname)

        if self.images[0].type_d() == "4D":
            self.images[0].funcdialog.setWindowTitle(itemname)
            if self.images[0].frame_time == 0:
                self.images[0].frame_time = 1

        self.resetFuncView()

        self.resetZValues()

        self.imagelist.setCurrentRow(0)
        self.updateSelected()
        self.autoRange()
        
        
        #%% checkIf2DAndRemovePanes
    def checkIf2DAndRemovePanes(self):
        
        max_c = -1
        max_s = -1
        max_t = -1
        
        for i in range(len(self.images)):
            sh = np.asanyarray(self.images[i].image.dataobj).shape
            if sh[0] > max_c:
                max_c = sh[0]
            if sh[1] > max_s:
                max_s = sh[1]
            if sh[2] > max_t:
                max_t = sh[2]
                
        log2("max_c: {} max_s: {} max_t: {}".format(max_c, max_s, max_t))
        
        decrease_winsize = False
                
        if max_s == 1:
            self.s_slice_widget.setHidden(True)
            self.t_slice_widget.setHidden(True)
            decrease_winsize = True
        elif max_c == 1:
            self.c_slice_widget.setHidden(True)
            self.t_slice_widget.setHidden(True)
            decrease_winsize = True
        elif max_t == 1:
            self.c_slice_widget.setHidden(True)
            self.s_slice_widget.setHidden(True)
            decrease_winsize = True
            
        if decrease_winsize:
            self.setObjectName(_fromUtf8("vini"))
            width = self.preferences['window_width']
            height = self.preferences['window_height']
            posx = self.preferences['window_posx']
            posy = self.preferences['window_posy']
            log1("setupUI: window posx: {}, posy: {}, width: {}, height: {}".format(posx, posy, width, height))
            self.setGeometry(posx, posy, round(width/2), height)
            self.blockSavingWindowSize = True
        
        
    def addPosNegWidget(self, pos_gradient, neg_gradient):
        """ helper function for refreshing the positive and negative colormap and sliders"""

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Minimum)

        fixed_width = 175

        pos_gradient.setMaxDim(pixels=self.grad_size)
        pos_gradient.setFixedWidth(fixed_width)
        neg_gradient.setMaxDim(pixels=self.grad_size)
        neg_gradient.setFixedWidth(fixed_width)
    
        button_row_thresh_pos = QtGui.QHBoxLayout()
        button_row_thresh_pos.addWidget(self.min_pos, 1)
        button_row_thresh_pos.addWidget(pos_gradient, 1)
        button_row_thresh_pos.addWidget(self.max_pos, 1)
        self.l.addLayout(button_row_thresh_pos, 9, self.listoffset+2, 1, 1)    
        

        button_row_thresh_neg = QtGui.QHBoxLayout()
        button_row_thresh_neg.addWidget(self.max_neg, 1)
        button_row_thresh_neg.addWidget(neg_gradient, 1)
        button_row_thresh_neg.addWidget(self.min_neg, 1)
        self.l.addLayout(button_row_thresh_neg, 10, self.listoffset+2, 1, 1)
        log2("addPosNegWidget called")

    
        

    def openNewFile(self):
        """
        Opens dialog for adding images.
        """
        if self.prefered_path is None:
            fnames = QtGui.QFileDialog.getOpenFileNames(self, 'Open file')
        else:
            fnames = QtGui.QFileDialog.getOpenFileNames(
                self, 'Open file', self.prefered_path)
        # Go through list and add them one by one.
        if fnames != []:
            for filename in fnames:
                if len(filename) > 0:
                    if os.path.isfile(filename[0]):
                        log2("openNewFile: filename {}".format(filename[0]))
                        try:
                            self.loadNewImage(filename[0])
                        except:
                            QtGui.QMessageBox.warning(self, "Warning", "Error: image could not be loaded")
                            
                            
                                

    def deleteImage(self):
        """
        Removes the current image from the viewer.

        This will remove it from all lists.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.removeFromSliceWidgets(index)
            if self.states[index]:
                self.updateImageItem(index)
            self.removeFromList(index)
            self.images[index].neg_gradient.setParent(None)
            self.images[index].pos_gradient.setParent(None)
            del self.image_window_list[index]
            del self.popouts_ii[index]
            del self.images[index]
            del self.states[index]
            # reset everything
            self.resetFuncView()
            self.resetZValues()
            self.updateSelected()

    def addToList(self, name):
        """
        Adds the name to the imagelist.
        """
        log2("addToList: adding {}".format(name))
        item = QtGui.QListWidgetItem(name)

        item.setFlags(item.flags() |
                      QtCore.Qt.ItemFlag.ItemIsUserCheckable |
                      QtCore.Qt.ItemFlag.ItemIsEditable)
        item.setCheckState(QtCore.Qt.CheckState.Checked)
            
        self.imagelist.insertItem(0, item)

    def removeFromList(self, ind):
        """
        Removes the item of index ind from the imagelist.
        """
        self.imagelist.takeItem(ind)
        
    def closeAndSave(self):
        log1("closeAndSave called!")
        self.saveWindowSize()
        self.close()

    def resample_img_to_affine(self, img, img_dims, affine):
        img.resample(shape=img_dims, affine=affine)

    ## Section: Resampling Methods ##
    def resampleToAffine(self):
        """
        Resamples the images using the affine transformations given in their
        file headers.
        """
        # compute voxel size with the oversampling ratio and the smallest voxel
        # resolution
        vsize = 1./self.preferences['os_ratio']*self.getVoxelResolution()
        self.affine = np.multiply(vsize, np.eye(4))
        self.affine[3,3] = 1

        # create bounding box
        bounds = None
        for img in self.images:
            b = img.getBounds()
            if bounds is None:
                bounds = np.zeros((3,2))
                bounds[0,0] = b[0][0]
                bounds[0,1] = b[0][1]
                bounds[1,0] = b[1][0]
                bounds[1,1] = b[1][1]
                bounds[2,0] = b[2][0]
                bounds[2,1] = b[2][1]
            else:
                bounds[0,0] = min(b[0][0],bounds[0,0],bounds[0,1])
                bounds[0,1] = max(b[0][1],bounds[0,1],bounds[0,0])
                bounds[1,0] = min(b[1][0],bounds[1,0],bounds[1,1])
                bounds[1,1] = max(b[1][1],bounds[1,1],bounds[1,0])
                bounds[2,0] = min(b[2][0],bounds[2,0],bounds[2,1])
                bounds[2,1] = max(b[2][1],bounds[2,1],bounds[2,0])

        # set offset and shape with bounds
        self.affine[0:3,3] = bounds[:,0]

        
        self.img_dims = np.ceil(np.dot(np.linalg.inv(self.affine[0:3,0:3]),
                                       np.ceil(bounds[:,1]-bounds[:,0])) + 1)
        # +1 to avoid having a 0 in img_dims

        # resample
        threads = [threading.Thread(target = self.resample_img_to_affine,args = (img, self.img_dims, self.affine)) for img in self.images]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.transform_ind = 0 # save what transformation was applied
        self.res_affine.setIcon(self.icon_checked)
        self.res_current.setIcon(QtGui.QIcon())
        self.res_fit.setIcon(QtGui.QIcon())

    def resampleToCurrent(self):
        """
        Resamples all images to the original voxels of the selected image.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.affine = self.images[index].getAffine()
            self.img_dims = self.images[index].getOriginalDimensions()
            # resample
            for img in self.images:
                img.resample(shape = self.img_dims, affine = self.affine)
        else: # if for whatever reason the index is < 0 take first image.
            if len(self.images) != 0:
                self.affine = self.images[0].getAffine()
                self.img_dims = self.images[0].getOriginalDimensions()
                # resample
                for img in self.images:
                    img.resample(shape = self.img_dims, affine = self.affine)

        self.transform_ind = 1 # save what transformation was applied
        self.res_affine.setIcon(QtGui.QIcon())
        self.res_current.setIcon(self.icon_checked)
        self.res_fit.setIcon(QtGui.QIcon())

    def resampleToFit(self):
        """
        Resamples the images assuming they align in all dimension.

        The images might look anisotropic depending on how all the dimensions
        are resolved in the images.
        """
        # check for the image with the highest first dimension
        index = -1
        high_dim = np.asarray([1,1,1])
        for img in self.images:
            high_dim = np.maximum(high_dim, img.getOriginalDimensions())

        self.img_dims = copy.copy(high_dim).astype(int)

        self.affine = np.eye(4)

        iter_idx = 0
        for img in self.images:
            # Compute scaling and resample.
            scale = np.divide(
                high_dim.astype(float),
                np.asarray(img.getOriginalDimensions()).astype(float))
            t_affine = np.eye(4)
            t_affine[0:3,0:3] = np.diag(scale)
            img.resample_overaffine(
                shape=self.img_dims, t_affine=np.eye(4), over_affine=t_affine)
            iter_idx += 1

        self.transform_ind = 2 # save what transformation was applied
        self.res_affine.setIcon(QtGui.QIcon())
        self.res_current.setIcon(QtGui.QIcon())
        self.res_fit.setIcon(self.icon_checked)

    def resampleToAffineClicked(self):
        self.resampleToAffine()
        self.resamplingAftermath()
        self.forbid_mm = False
        self.voxel_button.setCheckable(True)

    def resampleToCurrentClicked(self):
        self.resampleToCurrent()
        self.resamplingAftermath()
        self.forbid_mm = False
        self.voxel_button.setCheckable(True)

    def resampleToFitClicked(self):
        self.resampleToFit()
        self.resamplingAftermath()
        self.forbid_mm = True
        self.voxel_button.setCheckable(False)

    def reresample(self):
        """
        Reapplies the resampling.

        This is necessary if the interpolation method or the
        oversampling ratio are changed, or a new image is loaded.
        """
        if self.transform_ind == 0:
            self.resampleToAffine()
        if self.transform_ind == 1:
            self.resampleToCurrent()
        if self.transform_ind == 2:
            self.resampleToFit()
        self.resamplingAftermath()

    def resamplingAftermath(self):
        """
        This function takes care of updating everything after resampling.

        This means setting all SliceWidgets to the correct dimensions,
        updating the ImageItemMods, placing the crosshair in the center
        (the old coordinates could be outside the resampled dimensions),
        reseting all image properties displayed in the viewer (thresholds...)
        and reseting the views reasonably.
        """
        self.setSliceWidgetsDims()
        self.updateImageItems()
        self.setCrosshairPositionCenter()
        self.updateSelected()
        self.autoRange()

    def getVoxelResolution(self):
        """
        Returns highest voxel resolution of all images
        """
        eig_val = 1000000 # smallest eigenvalue initialized with large value.
        iter_idx = 0
        if len(self.images) > 0:
            for img in self.images:
                eigenValues, eigenVectors = np.linalg.eig(
                    img.image.affine[:,0:3][0:3])
                eigenValues = np.abs(eigenValues)
                idx = eigenValues.argsort()[::-1]
                new_val = eigenValues[idx[-1]]
                if abs(new_val) < abs(eig_val):
                    eig_val = new_val
            return eig_val
        else:
            QtGui.QMessageBox.warning(self, "Warning", "Error: No images")
            return None

    def getHighestResImageIdx(self):
        """
        Returns index in images belonging to highest resolution Image
        """
        idx = -1 # return index
        det = 10000 # determinant of affine, set to large value.
        iter_idx = 0
        for img in self.images:
            # take determinant
            new_det = np.linalg.det(img.image.affine)
            if abs(new_det) < abs(det):
                det = new_det
                idx = iter_idx
            iter_idx += 1
        return idx

    def setSliceWidgetsDims(self):
        """
        This passes the correct image dimensions to all slice views to ensure
        correct behaviour of the cursor and crosshair.

        Should be executed after each resampling.
        """
        self.c_slice_widget.setImageDimensions(
            [self.img_dims[0], self.img_dims[2], self.img_dims[1]])
        self.s_slice_widget.setImageDimensions(
            [self.img_dims[1], self.img_dims[2], self.img_dims[0]])
        self.t_slice_widget.setImageDimensions(
            [self.img_dims[0], self.img_dims[1], self.img_dims[2]])
        for window in self.extra_windows:
            window.sw_c.setImageDimensions(
                [self.img_dims[0], self.img_dims[2], self.img_dims[1]])
            window.sw_s.setImageDimensions(
                [self.img_dims[1], self.img_dims[2], self.img_dims[0]])
            window.sw_t.setImageDimensions(
                [self.img_dims[0], self.img_dims[1], self.img_dims[2]])
        self.slice_popouts[0].sw.setImageDimensions(
            [self.img_dims[0], self.img_dims[2], self.img_dims[1]])
        self.slice_popouts[1].sw.setImageDimensions(
            [self.img_dims[1], self.img_dims[2], self.img_dims[0]])
        self.slice_popouts[2].sw.setImageDimensions(
            [self.img_dims[0], self.img_dims[1], self.img_dims[2]])

    def applyTransform(self, x, y, z, mapping, inverse=False):
        """
        Applies map to coordinates.
        """
        xyz = np.array([x, y, z, 1])
        if mapping is None:
            mapping = np.eye(4)
        if inverse == False:
            mapped_xyz = np.dot(mapping, xyz)
        else:
            inv_code_map = np.linalg.inv(mapping)
            # apply inverse of affine map
            mapped_xyz = np.dot(inv_code_map, xyz)
        return mapped_xyz

    def setOSRatio(self):
        """
        Opens the dialog to set the oversampling ratio.
        """

        try:
            raise Exception("OSRatio currently cant be set") 

            self.os_setting = QtGui.QDialog()
            self.os_setting.resize(40,40)

            ratio_le = QtGui.QLineEdit()
            ratio_le.setText(str(self.preferences['os_ratio']))

            def save():
                if testFloat(ratio_le.text()):
                    self.preferences['os_ratio'][0]= float(ratio_le.text())
                self.os_setting.close()

            ratio_le.returnPressed.connect(save)
            ratio_le.editingFinished.connect(save)

            resample_button = QtGui.QPushButton("Resample now!", self)
            resample_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            resample_button.clicked.connect(self.reresample)

            form = QtGui.QFormLayout()
            form.addRow("Oversampling ratio:", ratio_le)
            form.addRow("Apply resampling:", resample_button)
            self.os_setting.setLayout(form)

            quit = QtGui.QAction('Quit', self)
            quit.setShortcut(QtGui.QKeySequence.StandardKey.Quit)
            quit.triggered.connect(self.os_setting.close)
            self.os_setting.addAction(quit)

            self.os_setting.show()
        except Exception as e:
            QtGui.QMessageBox.warning(self, "Warning", f"Warning: {e}")
        
    def setDiscreteCM(self):
        log2("setting discrete colormap")
        
        index = self.imagelist.currentRow()
        if index >= 0:
            value_set = np.unique(np.asanyarray(self.images[index].image.dataobj))
            value_set_int = np.round(value_set).astype(int)
            delta_int = np.linalg.norm(value_set_int-value_set) / float(value_set.size)
            if value_set.size >= 256:
                QtGui.QMessageBox.warning(self,"Warning", "Warning: Image has more than 256 different values. Cannot set random lookup table.")
            elif delta_int > 0.0001:
                QtGui.QMessageBox.warning(self,"Warning", "Warning: Image need to be in integer format. Cannot set random lookup table.")
            else:
                self.images[index].useDiscreteCM()
            
        

    ## Section: Linking Views ##
    def linkSlices(self, state):
        """
        Links or unlinks the different views within the main window or extra
        windows.
        """
        if state != True:
            self.link_mode = False
            # this frees all the axis of any linking
            self.c_slice_widget.sb.linkView(ViewBox.XAxis)
            self.c_slice_widget.sb.linkView(ViewBox.YAxis)
            self.s_slice_widget.sb.linkView(ViewBox.XAxis)
            self.s_slice_widget.sb.linkView(ViewBox.YAxis)
            self.t_slice_widget.sb.linkView(ViewBox.XAxis)
            self.t_slice_widget.sb.linkView(ViewBox.YAxis)
            for window in self.extra_windows:
                window.sw_c.sb.linkView(ViewBox.XAxis)
                window.sw_c.sb.linkView(ViewBox.YAxis)
                window.sw_s.sb.linkView(ViewBox.XAxis)
                window.sw_s.sb.linkView(ViewBox.YAxis)
                window.sw_t.sb.linkView(ViewBox.XAxis)
                window.sw_t.sb.linkView(ViewBox.YAxis)
            self.interlinkWindows(False)
            self.autoRange()
        else:
            self.link_mode = True
            # c.x links with t.x and
            # c.y links with s.y
            # s.x links with t.y
            self.c_slice_widget.sb.setXLink(self.t_slice_widget.sb)
            self.s_slice_widget.sb.setYLink(self.c_slice_widget.sb)
            self.s_slice_widget.sb.linkViewXY(self.t_slice_widget.sb,
                                              ViewBox.YAxis,
                                              ViewBox.XAxis)
            for window in self.extra_windows:
                window.sw_c.sb.setXLink(window.sw_t.sb)
                window.sw_s.sb.setYLink(window.sw_c.sb)
                window.sw_s.sb.linkViewXY(window.sw_t.sb,
                                          ViewBox.YAxis, ViewBox.XAxis)
            self.interlinkWindows(True)
            self.autoRange()

    def interlinkWindows(self, state=True):
        """
        Establishes links of the views between the main window and the extra
        windows.
        """
        if state != True:
            self.c_slice_widget.sb.linkView(ViewBox.YAxis)
            self.t_slice_widget.sb.linkView(ViewBox.XAxis)
            self.t_slice_widget.sb.linkView(ViewBox.YAxis)
            for window in self.extra_windows:
                window.sw_c.sb.linkView(ViewBox.YAxis)
                window.sw_t.sb.linkView(ViewBox.XAxis)
                window.sw_t.sb.linkView(ViewBox.YAxis)
        else:
            if len(self.extra_windows) != 0:
                self.c_slice_widget.sb.setYLink(self.extra_windows[0].sw_c.sb)
                self.t_slice_widget.sb.setXLink(self.extra_windows[0].sw_t.sb)
                self.t_slice_widget.sb.setYLink(self.extra_windows[0].sw_t.sb)
            for i in range(1,len(self.extra_windows)):
                self.extra_windows[i-1].sw_c.sb.setYLink(
                    self.extra_windows[i].sw_c.sb)
                self.extra_windows[i-1].sw_t.sb.setXLink(
                    self.extra_windows[i].sw_t.sb)
                self.extra_windows[i-1].sw_t.sb.setYLink(
                    self.extra_windows[i].sw_t.sb)


    ## Section: Crosshair and Cursor Movements and Connected Functions ##
    def setCrosshairBoxCoord(self):
        """
        Sets the crosshair to the box coordinates on enter.
        """
        if ((testFloat(self.x_box.text()) and
                testFloat(self.y_box.text()) and
                testFloat(self.z_box.text()))):
            
            x = int(float(self.x_box.text()))
            y = int(float(self.y_box.text()))
            z = int(float(self.z_box.text()))
            index = self.imagelist.currentRow()
            if self.voxel_coord:
                if index >= 0:
                    m = self.applyTransform(x, y, z, self.images[index].getAffineUsed(), inverse=True)
                    log2("setCrosshairBoxCoord: x {} y {} z {}. Transformed to: m={}".format(x,y,z,m))
                else:
                    QtGui.QMessageBox.warning(self, "Warning",
                        "Error: No image selected to display voxel \
                        coordinates for.")
            else:
                m = self.applyTransform(x, y, z, self.affine, inverse=True)
            self.img_coord = np.asarray(np.round(m), dtype=np.int32)
            # Now that the new coordinates are computed, move the crosshair
            # to that position.
            # But first check whether the coordinates are in the resampled
            # dimensions.
            self.moveCrosshairIntoImage()
            self.setCrosshair()
        else:
            QtGui.QMessageBox.warning(self, "Error: text input cannot be \
                                      interpreted as a number")

    def MouseMoved(self, xyz):
        """
        This function is connected with cursor signals passing the position.

        Because each position of the cursor in a slice is two dimensional
        the remaining dimension is None and is set to the crosshair coordinate.
        """
        self.cursor_coord = [xyz[i] if xyz[i] is not None else
            self.img_coord[i] for i in range(3)]
        self.updateIntensityLabel(self.cursor_coord)


    def updateIntensityLabel(self, cursor_coord= None):
        """
        Updates the intensity labels in the main window and the value window
        for the crosshair.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            # no check for coordinates because the crosshair position should
            # always be within the image
            nmb_images = len(self.images)
            str_intens = ""
            str_image_name = ""
            str_intens_tooltip = ""
            for i in range(nmb_images):
                str_img = str(self.imagelist.item(i).text()).split(".")[0]
                
                if (self.playstate or self.slicestate) and self.images[i].type_d() == "4D":
                    intensity = self.images[i].xhairval
                elif cursor_coord is not None:
                    if all(0 <= int(cursor_coord[j]) < self.images[i].image_res.shape[j] for j in range(3)):
                        intensity = self.images[i].getIntensity(cursor_coord)
                    else: intensity = np.nan
                else:
                    intensity = self.images[i].getIntensity()
                intensity = np.round(intensity, 3)
                
                str_tooltip = "%g \t %s" %(intensity,str_img)
                if i > 0:
                    str_intens += "\n"
                    str_image_name += "\n"
                    str_intens_tooltip += "\n"
                if i<6:
                    str_intens += " %g" %intensity
                    if len(str_img) > 15:
                        str_img = str_img[0:15] + "..."
                    str_image_name += str_img
                str_intens_tooltip += str_tooltip

            if cursor_coord is None:
                self.intensity_value.setText((str_intens))
                self.intensity_image_name.setText((str_image_name))
                self.intensity_value.setToolTip(str_intens_tooltip)
            else:
                self.intensity_value_mouse.setText((str_intens))
                self.intensity_image_name.setText((str_image_name))
            
            log1("updateCrossIntensityLabel was called")
            

            
        self.setAlphaToSlider()
        
    def resetEverything(self):
        self.resetAlpha()
        self.autoRange()
        self.resetPosThresholds()
        self.resetNegThresholds()
        
        self.resetHistogram()
        

    def switchVoxelCoord(self):
        """
        Changes the coordinates used.

        If voxel_coord is True the original voxel coordinates of the images are
        used. For False the coordinate system coordinates are used.
        """
        if self.forbid_mm:
            self.voxel_coord = True
        else:
            self.voxel_coord = not self.voxel_coord
        self.refreshVoxelCoord()
        log2("switchVoxelCoord to state {}".format(self.voxel_coord))

        
    def refreshVoxelCoord(self):
        """
        Refreshes the coordinates used.
        """
        self.updateDisplayCoordinates()
        if self.voxel_coord:
            self.voxel_button.setText("voxel")
        else:
            index = self.imagelist.currentRow()
            sform_code=-2
            if index >= 0:
                m = [np.trunc(x) for x in self.img_coord]
                m = self.images[index]
                sform_code = m.sform_code
            log2("refreshVoxelCoord, sform_code {}".format(sform_code))
            if sform_code == 4:
                self.voxel_button.setText("mni")
            else:
                self.voxel_button.setText("mm")
                
                
        

    def setCrosshairsVisible(self, state):
        """
        Set crosshairs visibility to state.

        Used by the checkable box.
        """
        self.c_slice_widget.setCrosshairVisible(state)
        self.s_slice_widget.setCrosshairVisible(state)
        self.t_slice_widget.setCrosshairVisible(state)
        for window in self.extra_windows:
            window.sw_c.setCrosshairVisible(state)
            window.sw_s.setCrosshairVisible(state)
            window.sw_t.setCrosshairVisible(state)
        self.slice_popouts[0].sw.setCrosshairVisible(state)
        self.slice_popouts[1].sw.setCrosshairVisible(state)
        self.slice_popouts[2].sw.setCrosshairVisible(state)

    def toggleCrosshairs(self):
        """
        Toggles the crosshair on/off.
        """
        state = self.cross_button.isChecked()
        state = not state
        self.cross_button.setChecked(state)
        self.setCrosshairsVisible(state)

    
    def startCrosshairTimer(self, xyz):
        self.img_coord = [xyz[i] if xyz[i] is not None else self.img_coord[i]
            for i in range(3)]
        self.crosshair_timer.start(1)

    def CrosshairMoved(self, xyz):
        """
        This connects to crosshair move signals.

        The signals pass the two dimensional coordinates and a None depending
        on the plane the crosshair was moved in.
        """
        self.img_coord = [xyz[i] if xyz[i] is not None else self.img_coord[i]
            for i in range(3)]
        self.setCrosshair()

    def setCrosshairPositionCenter(self):
        """
        This centers the crosshair.

        Should only be called after the img_coord are correctly updated.
        """
        if len(self.images) > 0:
            shape = self.images[0].image_res.shape
            self.img_coord = np.round(np.multiply(np.asarray(shape),0.5)).astype(int)
            self.setCrosshair()
            
    def setCrosshair(self):
        """
        This function literally moves the crosshair to the desired position.

        It involves updating the slices and ImageItemMods and manually moving
        the lines of the crosshair.
        """
        # Reset img_coord if out of bounds
        self.moveCrosshairIntoImage()
        # Reslice the images
        self.updateSlices()
        self.updateImageItems()
        # Moving the lines:
        self.c_slice_widget.setCrosshairPos(
            [self.img_coord[0], self.img_coord[2], self.img_coord[1]])
        self.s_slice_widget.setCrosshairPos(
            [self.img_coord[1], self.img_coord[2], self.img_coord[0]])
        self.t_slice_widget.setCrosshairPos(
            [self.img_coord[0], self.img_coord[1], self.img_coord[2]])
        for window in self.extra_windows:
            window.sw_c.setCrosshairPos(
                [self.img_coord[0], self.img_coord[2], self.img_coord[1]])
            window.sw_s.setCrosshairPos(
                [self.img_coord[1], self.img_coord[2], self.img_coord[0]])
            window.sw_t.setCrosshairPos(
                [self.img_coord[0], self.img_coord[1], self.img_coord[2]])
        self.slice_popouts[0].sw.setCrosshairPos(
            [self.img_coord[0], self.img_coord[2], self.img_coord[1]])
        self.slice_popouts[1].sw.setCrosshairPos(
            [self.img_coord[1], self.img_coord[2], self.img_coord[0]])
        self.slice_popouts[2].sw.setCrosshairPos(
            [self.img_coord[0], self.img_coord[1], self.img_coord[2]])
        # Update crosshair dependent values.
        self.updateDisplayCoordinates()

    def moveCrosshairIntoImage(self):
        """
        If the img_coord are out of bounds of the img_dims they are moved.
        """
        # Bound from below by 0.
        self.img_coord = [self.img_coord[i] if self.img_coord[i] >= 0 else
            0 for i in range(3)]
        # Bound from above by img_dims.
        self.img_coord = [self.img_coord[i] if
            self.img_coord[i] < self.img_dims[i] else self.img_dims[i]-1 for
            i in range(3)]

    def updateDisplayCoordinates(self):
        """
        Updating the right coordinates in the coordinate boxes (line edits).
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            if self.voxel_coord:
                m = [np.trunc(x) for x in self.img_coord]
                m = self.images[index].getVoxelCoords(m)
                self.x_box.setText(str(int(np.round(m[0]))))
                self.y_box.setText(str(int(np.round(m[1]))))
                self.z_box.setText(str(int(np.round(m[2]))))
            else:
                m = [np.trunc(x) for x in self.img_coord]
                m = self.applyTransform(m[0], m[1], m[2], self.affine)
                self.x_box.setText(str(m[0]))
                self.y_box.setText(str(m[1]))
                self.z_box.setText(str(m[2]))
            # Is this needed?
            self.updateIntensityLabel()


    ## Section: Zoom and Pan Views ##
    def autoRange(self):
        """
        Resets all views to a reasonable region.
        """
        self.setCrosshairPositionCenter()
        self.c_slice_widget.sb.autoRange()
        self.s_slice_widget.sb.autoRange()
        self.t_slice_widget.sb.autoRange()
        
        self.slice_popouts[0].sw.sb.autoRange()
        self.slice_popouts[1].sw.sb.autoRange()
        self.slice_popouts[2].sw.sb.autoRange()
        for window in self.extra_windows:
            window.sw_c.sb.autoRange()
            window.sw_s.sb.autoRange()
            window.sw_t.sb.autoRange()

    def zoomOut(self):
        if self.link_button.isChecked():
            self.c_slice_widget.zoomOut()
        else:
            if self.slice_focus == 'c':
                self.c_slice_widget.zoomOut()
            if self.slice_focus == 's':
                self.s_slice_widget.zoomOut()
            if self.slice_focus == 't':
                self.t_slice_widget.zoomOut()

    def zoomIn(self):
        if self.link_button.isChecked():
            self.c_slice_widget.zoomIn()
        else:
            if self.slice_focus == 'c':
                self.c_slice_widget.zoomIn()
            if self.slice_focus == 's':
                self.s_slice_widget.zoomIn()
            if self.slice_focus == 't':
                self.t_slice_widget.zoomIn()

    ## Section: Updating the Slices ##
    def updateImages(self):
        self.updateSlices()
        self.updateImageItems()

    def updateSlices(self):
        threads = [threading.Thread(target = self.updateSlice,args = (img,)) for img in self.images]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
    def updateSlice(self, img):
        img.slice(np.asarray(self.img_coord).astype(np.int32))

    def updateImageItems(self):
        for index in range(len(self.images)):
            self.updateImageItem(index)

    def updateImageItem(self, index):
        """
        Resets the image arrays of all ImageItemMods.
        """
        # treat original vini separately
        mode = self.images[index].mode
        for window in range(len(self.image_window_list[index])):
            if self.image_window_list[index][window][0] is not None:
                # attention: order of indies change
                self.image_window_list[index][window][0].setImage(
                    self.images[index].getImageArrays()[1])
                self.image_window_list[index][window][1].setImage(
                    self.images[index].getImageArrays()[0])
                self.image_window_list[index][window][2].setImage(
                    self.images[index].getImageArrays()[2])
                for i in range(3):
                    self.image_window_list[index][window][i] \
                        .setCompositionMode(mode)
        if self.popouts_ii[index][0] is not None:
            self.popouts_ii[index][0].setImage(
                self.images[index].getImageArrays()[1])
            self.popouts_ii[index][1].setImage(
                self.images[index].getImageArrays()[0])
            self.popouts_ii[index][2].setImage(
                self.images[index].getImageArrays()[2])
            for i in range(3):
                self.popouts_ii[index][i].setCompositionMode(mode)

    def resetZValues(self):
        """
        Reset the Z Values such that the list order defines the reverse order
        of rendering
        """
        z = 0
        for i in range(len(self.images)):
            for win in self.image_window_list[i]:
                if win[0] is not None:
                    win[0].setZValue(z)
                    win[1].setZValue(z)
                    win[2].setZValue(z)
            if self.popouts_ii[i][0] is not None:
                self.popouts_ii[i][0].setZValue(z)
                self.popouts_ii[i][1].setZValue(z)
                self.popouts_ii[i][2].setZValue(z)
            z -= 1


    ## Section: Activating and Deactivating Images ##
    def toggleVisibility(self):
        """
        Toggles the visibility of the current image.

        Connected to signal keyboard shortcut 'v'.
        """
        item = self.imagelist.currentItem()
        index = self.imagelist.currentRow()
        if index >= 0:
            if self.states[index]:
                self.imagelist.item(index).setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.deactivateImage()
            else:
                self.imagelist.item(index).setCheckState(QtCore.Qt.CheckState.Checked)
                self.activateImage()

    def toggleDeselect(self):
        """
        Toggles all other but the current image off or all images on.

        Connected to signal keyboard shortcut 'd'.
        """
        if self.deselected == False:
            # deselect all but current
            index = self.imagelist.currentRow()
            for i in range(len(self.images)):
                if index != i:
                    self.imagelist.item(i).setCheckState(QtCore.Qt.CheckState.Unchecked)
                    self.deactivateImageIndex(i)
            self.deselected = True
        else:
            # select all
            for i in range(len(self.images)):
                self.imagelist.item(i).setCheckState(QtCore.Qt.CheckState.Checked)
                self.activateImageIndex(i)
            self.deselected = False

    def activateImage(self):
        """
        Activates the current image.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.activateImageIndex(index)

    def activateImageIndex(self, ind):
        """
        Activate image with index 'ind'.
        """
        if self.states[ind] == False:
            self.enableControls()
            self.imagelist.item(ind).setCheckState(QtCore.Qt.CheckState.Checked)
            self.states[ind] = True
            image_item_list_tmp = []
            image_item_list_tmp_po = []
            for j in range(3):
                image_item_list_tmp.append(ImageItemMod())
                image_item_list_tmp_po.append(ImageItemMod())
            self.image_window_list[ind][0] = image_item_list_tmp
            self.popouts_ii[ind] = image_item_list_tmp_po
            self.updateImageItem(ind)
            self.resetZValues()
            self.addToSliceWidget(ind, 0)

    def deactivateImage(self):
        """
        Deactivates the current image.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.deactivateImageIndex(index)

    def deactivateImageIndex(self, ind):
        if self.states[ind]:
            self.disableControls()
            self.imagelist.item(ind).setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.states[ind] = False
            self.removeFromSliceWidget(ind, 0)
            image_item_list_tmp = [None] * 3
            self.image_window_list[ind][0] = image_item_list_tmp
            self.popouts_ii[ind] = image_item_list_tmp

    def addToSliceWidgets(self, index):
        """
        Add the already created ImageItemMods to the SliceWidgets.
        """
        for i in range(len(self.image_window_list[index])):
            self.addToSliceWidget(index, i)

    def addToSliceWidget(self, img_ind, win_ind):
        """
        Add the already created ImageItemMods to a specific SliceWidget.
        """
        if self.image_window_list[img_ind][win_ind][0] is not None:
            if win_ind == 0:
                verboseprint("add to vini")
                self.c_slice_widget.addImageItem(
                    self.image_window_list[img_ind][0][0])
                self.s_slice_widget.addImageItem(
                    self.image_window_list[img_ind][0][1])
                self.t_slice_widget.addImageItem(
                    self.image_window_list[img_ind][0][2])
                # add to popouts
                self.slice_popouts[0].sw.addImageItem(
                    self.popouts_ii[img_ind][0])
                self.slice_popouts[1].sw.addImageItem(
                    self.popouts_ii[img_ind][1])
                self.slice_popouts[2].sw.addImageItem(
                    self.popouts_ii[img_ind][2])
            else:
                self.extra_windows[win_ind-1].sw_c.addImageItem(
                    self.image_window_list[img_ind][win_ind][0])
                self.extra_windows[win_ind-1].sw_s.addImageItem(
                    self.image_window_list[img_ind][win_ind][1])
                self.extra_windows[win_ind-1].sw_t.addImageItem(
                    self.image_window_list[img_ind][win_ind][2])

    def removeFromSliceWidgets(self, index):
        """
        Removing ImageItemMods
        """
        for i in range(len(self.image_window_list[index])):
            self.removeFromSliceWidget(index, i)

    def removeFromSliceWidget(self, img_ind, win_ind):
        if self.image_window_list[img_ind][win_ind][0] is not None:
            if win_ind == 0:
                verboseprint("remove from vini ", img_ind)
                self.c_slice_widget.removeImageItem(
                    self.image_window_list[img_ind][0][0])
                self.s_slice_widget.removeImageItem(
                    self.image_window_list[img_ind][0][1])
                self.t_slice_widget.removeImageItem(
                    self.image_window_list[img_ind][0][2])
                # remove from popouts
                self.slice_popouts[0].sw.removeImageItem(
                    self.popouts_ii[img_ind][0])
                self.slice_popouts[1].sw.removeImageItem(
                    self.popouts_ii[img_ind][1])
                self.slice_popouts[2].sw.removeImageItem(
                    self.popouts_ii[img_ind][2])
            else:
                self.extra_windows[win_ind-1].sw_c.removeImageItem(
                    self.image_window_list[img_ind][win_ind][0])
                self.extra_windows[win_ind-1].sw_s.removeImageItem(
                    self.image_window_list[img_ind][win_ind][1])
                self.extra_windows[win_ind-1].sw_t.removeImageItem(
                    self.image_window_list[img_ind][win_ind][2])


    #%% Section: Current Image Selection Updates ##
    def selectionChange(self, item=None):
        """
        Is called when an item in the image list is selected.

        Has intricacies with the visibility state of an image.
        Calls updateSelected when those problems were dealt with.
        """
        if item is not None:
            self.imagelist.setCurrentItem(item)
        else:
            item = self.imagelist.currentItem()
        if item is not None:
            index = self.imagelist.row(item)
            self.addPosNegWidget(self.images[index].pos_gradient, self.images[index].neg_gradient)
            
            # only the checkbox is checked or unchecked
            if bool(item.checkState().value if hasattr(item.checkState(), "value") else item.checkState()) != self.states[index]:
                if item.checkState() == QtCore.Qt.CheckState.Checked:
                    self.activateImage()
                else:
                    self.deactivateImage()
            else:
                self.updateSelected()
            #change the window highlighting if in linked mode (only for zmaps)
            if self.is_linked:
                for j in range(len(self.window_ids)):
                    if j==index-1:
                        self.setExtraWindowTitle(j, True)
                    else:
                        self.setExtraWindowTitle(j, False)
                        
                #get title of main window
                title_main = "vini viewer: "
                first = True
                for i in range(len(self.images)):
                    if self.image_window_list[i][0][0] is not None:
                        if first is not True:
                            title_main += ", "
                        else:
                            first = False
                        title_main += self.imagelist.item(i).text()
                    
                if index == 0:
                    title_main += " [SELECTED]"
                self.setWindowTitle(title_main)

                
#% updateSelected: updating boxes sliders labels
    def updateSelected(self):
        """
        Updates the boxes, sliders, labels, when the selected image is changed.
        """
        # hide all other colormap gradients
        for img in self.images:
            img.hide_gradients()

        self.threshold_write_block = True
        index = self.imagelist.currentRow()
        if index >= 0:
            # enable controls
            self.enableControls()
            # actions for all images
            self.images[index].pos_gradient.show()
            self.slider_pos.setEnabled(True)

            if self.images[index].type() == "one":
                self.slider_neg.setSpan(0,1000)
                self.disableSliderNeg()
                self.min_neg.setHidden(True)
                self.max_neg.setHidden(True)
                self.slider_neg.setHidden(True)
                self.slider_pos.setSpan(
                    self.images[index].getPosSldValueLow(),
                    self.images[index].getPosSldValueHigh())
                
                
            if self.images[index].type() == "two":
                self.enableSliderNeg()
                self.min_neg.setHidden(False)
                self.max_neg.setHidden(False)
                self.slider_neg.setHidden(False)
                self.slider_neg.setSpan(
                    self.images[index].getNegSldValueHigh(),
                    self.images[index].getNegSldValueLow())
                self.images[index].neg_gradient.show()
                self.slider_pos.setSpan(
                    self.images[index].getPosSldValueLow(),
                    self.images[index].getPosSldValueHigh())

            self.updateIntensityLabel()
            self.updateDisplayCoordinates()
            self.setThresholdsToBoxes()
            # If there is a histogram window, update that, too.
            if self.hist is not None:
                self.resetHistogram()
            # if image is inactive: disable all controls
            if self.states[index] is not True:
                self.disableControls()
            # image is functional and active enable functional widgets
            if self.states[index] is True and self.images[index].type_d() == "4D":
                self.enableFuncView()
        
            #should func view (aka time controls) be enabled or disabled?
            if self.images[index].type_d() == "4D":
                self.enableFuncView()
            else:
                self.disableFuncView()
                
            
        self.threshold_write_block = False
        
        
        
        #also save current window sizes....
        self.saveWindowSize()

    def disableControls(self):
        return

    def enableControls(self):
        index = self.imagelist.currentRow()
        if self.images[index].type() == "two":
            self.min_neg.setEnabled(True)
            self.max_neg.setEnabled(True)
            self.slider_neg.setEnabled(True)
            self.slider_neg.setGradientLeftColor(self.slider_color)
            self.slider_neg.setGradientRightColor(self.slider_color)
        self.min_pos.setEnabled(True)
        self.max_pos.setEnabled(True)
        self.slider_pos.setEnabled(True)
        self.slider_pos.setGradientLeftColor(self.slider_color)
        self.slider_pos.setGradientRightColor(self.slider_color)
        self.min_button.setEnabled(True)
        self.max_button.setEnabled(True)
        if self.images[index].type_d() == "4D":
            self.enableFuncView()

    def disableSliderNeg(self):
        self.slider_neg.setEnabled(False)
        self.slider_neg.setGradientLeftColor(self.slider_color_off)
        self.slider_neg.setGradientRightColor(self.slider_color_off)

    def enableSliderNeg(self):
        self.slider_neg.setEnabled(True)
        self.slider_neg.setGradientLeftColor(self.slider_color)
        self.slider_neg.setGradientRightColor(self.slider_color)



    def newWindow(self):
        """
        Creates a new extra window with the current image in it.
        """
        index = self.imagelist.currentRow()
        self.newWindowInd(index)
        # Remove Image from main window if it's still in there.
        index = self.imagelist.currentRow()
        if index >= 0:
            if self.states[index]:
                self.imagelist.item(index).setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.deactivateImage()

    def newWindowInd(self, index):
        """
        Creates a new extra window with image indexed by index.
        """
        # For all images create a new list of ImageItemMods for that
        # particular window initialized with Nones.
        for i in self.image_window_list:
            i.append([None] * 3)
        # For index fill that list with ImageItemMods.
        image_item_list_tmp = []
        for j in range(3):
            image_item_list_tmp.append(ImageItemMod())
        self.image_window_list[index][-1] = image_item_list_tmp
        # Create a new id for that window.
        self.window_count += 1
        self.window_ids.append(self.window_count)
        # initialize the window itself.
        window = SliceWindow(self.window_count)
        self.extra_windows.append(window)
        window.sigClose.connect(self.delWindowClose)
        
        # Set the crosshair
        window.sw_c.setCrosshairPos(
            [self.img_coord[0], self.img_coord[2], self.img_coord[1]])
        window.sw_s.setCrosshairPos(
            [self.img_coord[1], self.img_coord[2], self.img_coord[0]])
        window.sw_t.setCrosshairPos(
            [self.img_coord[0], self.img_coord[1], self.img_coord[2]])
        # connect slice focus
        window.sw_c.sigSelected.connect(self.sliceFocusC)
        window.sw_s.sigSelected.connect(self.sliceFocusS)
        window.sw_t.sigSelected.connect(self.sliceFocusT)
        # connect crosshair movements
        window.sw_c.sigCPChanged.connect(self.startCrosshairTimer)
        window.sw_s.sigCPChanged.connect(self.startCrosshairTimer)
        window.sw_t.sigCPChanged.connect(self.startCrosshairTimer)
        # connect cursor movements
        window.sw_c.sigMouseOver.connect(self.MouseMoved)
        window.sw_s.sigMouseOver.connect(self.MouseMoved)
        window.sw_t.sigMouseOver.connect(self.MouseMoved)

        self.updateImageItem(index)
        window_number = len(self.extra_windows)
        self.addToSliceWidget(index, window_number)

        if self.link_mode:
            window.sw_c.sb.setXLink(window.sw_t.sb)
            window.sw_s.sb.setYLink(window.sw_c.sb)
            window.sw_s.sb.linkViewXY(
                window.sw_t.sb, ViewBox.YAxis, ViewBox.XAxis)
        self.interlinkWindows(self.link_mode)

        window.sw_c.sb.autoRange()
        window.sw_s.sb.autoRange()
        window.sw_t.sb.autoRange()

        self.setExtraWindowTitle(window_number-1) # index instead of length

    def addToWindow(self, window):
        """
        Adds the current image to the window with index window.
        """
        index = self.imagelist.currentRow()
        self.addToWindowId(index, window)

    def addToWindowId(self, index, window):
        """
        Adds image with index index to window with index window.
        """
        image_item_list_tmp = []
        for j in range(3):
            image_item_list_tmp.append(ImageItemMod())
        self.image_window_list[index][window+1] = image_item_list_tmp
        self.updateImageItem(index)
        self.addToSliceWidget(index, window+1)
        self.resetZValues()
        # update the window title including the image name
        self.setExtraWindowTitle(window)

    def removeFromWindow(self, window):
        """
        Remove current image from window with index window.
        """
        index = self.imagelist.currentRow()
        self.removeFromWindowInd(index, window)

    def removeFromWindowInd(self, index, window):
        """
        Remove image with index index from window with index window.
        """
        verboseprint("Remove " + str(index) + " from window " +
            str(self.window_ids[window]))
        self.removeFromSliceWidget(index, window+1)
        image_item_list_tmp = [None] * 3
        self.image_window_list[index][window+1] = image_item_list_tmp
        # See if window contains images.
        # Only do this if window is not the vini itself.
        no_images = True
        for i in range(len(self.image_window_list)):
            if self.image_window_list[i][window+1][0] is not None:
                no_images = False
        if no_images:
            self.delWindow(window)
        else:
            self.setExtraWindowTitle(window)

    def setExtraWindowTitle(self, window, selected=False):
        """
        Refreshes the window title of window with index window.
        """
        title = "Linked Window " + str(self.window_ids[window]) + ": "
        first = True
        for i in range(len(self.images)):
            if self.image_window_list[i][window+1][0] is not None:
                if first is not True:
                    title += ", "
                else:
                    first = False
                title += self.imagelist.item(i).text()
                
        if selected:
            title += " [SELECTED]"
        
        self.extra_windows[window].setWindowTitle(title)

    def delWindowClose(self, window_id):
        """
        Is called from the window on a closeEvent to let the viewer know it.
        """
        try:
            window = self.window_ids.index(window_id)
        except ValueError:
            window = None
        if window is not None:
            self.delWindow(window)

    def delWindow(self, window):
        """
        Keep lists and SliceWidgets up to date after deleting a window.
        """
        for i in range(len(self.images)):
            self.removeFromSliceWidget(i, window+1)
        for i in range(len(self.image_window_list)):
            del self.image_window_list[i][window+1]
        del self.window_ids[window]
        self.extra_windows[window].close()
        del self.extra_windows[window]
        self.interlinkWindows(self.link_mode)

    def printImageWindowList(self):
        """
        Helper function to debug code that deals with extra windows.
        Prints out the current image window assignments.
        """
        for i in range(len(self.image_window_list)):
            verboseprint("image: " + str(i+1))
            for j in range(len(self.image_window_list[i])):
                verboseprint("window: " + str(j+1))
                if self.image_window_list[i][j][0] is None:
                    verboseprint("no")
                else:
                    verboseprint("yes")

    ## Section: imagelist Actions ##
    def setCurrentHigher(self):
        """
        Select the image one higher in the imagelist.
        """
        index = self.imagelist.currentRow()
        # check if selecting higher image is possible
        if index > 0:
            index -= 1
            self.imagelist.setCurrentRow(index)
            
        self.refreshVoxelCoord()

    def setCurrentLower(self):
        """
        Select the image one lower in the imagelist.
        """
        index = self.imagelist.currentRow()
        # check if selecting higher image is possible
        if index < len(self.imagelist)-1:
            index += 1
            self.imagelist.setCurrentRow(index)
        self.refreshVoxelCoord()

    def setCurrent(self, index):
        """
        Select image with index index.
        """
        if index < len(self.imagelist):
            self.imagelist.setCurrentRow(index)

    def swapDown(self):
        """
        Swap current image down in the imagelist.
        """
        if self.is_linked:
            return
        index = self.imagelist.currentRow()
        # check if swapDown is possible
        if index < len(self.images)-1:
            self.swapItems(index+1)
            index += 1
            self.imagelist.setCurrentRow(index)
            self.resetZValues()
        self.updateIntensityLabel()

    def swapUp(self):
        """
        Swap current image down in the imagelist.
        """
        if self.is_linked:
            return
        index = self.imagelist.currentRow()
        # check if swapUp is possible
        if index > 0 and len(self.images) > 1:
            self.swapItems(index)
            index -= 1
            self.imagelist.setCurrentRow(index)
            self.resetZValues()
        self.updateIntensityLabel()

    def swapItems(self, ind):
        """
        Swaps index ind and ind-1.
        """
        self.images[ind], self.images[ind-1] = \
            self.images[ind-1], self.images[ind]
        self.states[ind], self.states[ind-1] = \
            self.states[ind-1], self.states[ind]
        self.image_window_list[ind], self.image_window_list[ind-1] = \
            self.image_window_list[ind-1], self.image_window_list[ind]
        self.popouts_ii[ind], self.popouts_ii[ind-1] = \
            self.popouts_ii[ind-1], self.popouts_ii[ind]
        item = self.imagelist.takeItem(ind)
        self.imagelist.insertItem(ind-1, item)

    ## Section: Functional Image Methods ##
    def resetFuncView(self):
        """
        Dis- or enables all functional widgets and resets properties.
        """
        self.funcview = False
        for img in self.images:
            if img.type_d() == "4D":
                self.funcview = True
                if self.time_dim < img.time_dim:
                    self.time_dim = img.time_dim
        if self.funcview:
            self.enableFuncView()
        else:
            self.disableFuncView()
            self.frame = 0
            self.time_dim = 1
            self.setFrameToBox()
            self.setFrameToSlider()

    def enableFuncView(self, state=True):
        """
        Dis- or enables all functional image widgets.
        """
        self.func_enabled = state
        self.frame_sld.setEnabled(state)
        self.frame_box.setEnabled(state)
        self.backward_button.setEnabled(state)
        self.forward_button.setEnabled(state)
        self.play_button.setEnabled(state)

    def disableFuncView(self):
        self.enableFuncView(False)

    def firstFrame(self):
        """
        Goes to the first frame.
        """
        self.frame = 0
        self.setSliceStateOn()
        self.setFrame()
        self.setFrameToBox()
        self.setFrameToSlider()

    def lastFrame(self):
        """
        Goes to the last frame.
        """
        self.frame = self.time_dim - 1
        self.setSliceStateOn()
        self.setFrame()
        self.setFrameToBox()
        self.setFrameToSlider()

    def nextFrame(self):
        """
        Goes to the next frame.
        """
        self.frame = self.frame+1
        if self.frame >= self.time_dim:
            self.frame = self.time_dim - 1
            
        else:
            self.setSliceStateOn()
            self.setFrame()
            self.setFrameToBox()
            self.setFrameToSlider()
            self.setSliceStateOff()
            
            

    def prevFrame(self):
        """
        Goes to the previous frame.
        """
        self.frame = self.frame-1
        if self.frame < 0:
            self.frame = 0
        else:
            self.setSliceStateOn()
            self.setFrame()
            self.setFrameToBox()
            self.setFrameToSlider()
            self.setSliceStateOff()

    def setPlayState(self, play):
        """
        Sets the playstate.

        If playstate is True then the time series is played.
        """
        self.playstate = play

    def setSliceState(self, play):
        """
        Sets the slicestate.

        If slicestate is True, only the displayed slices are resampled.
        """
        self.slicestate = play

    def setSliceStateOn(self):
        self.slicestate = True

    def setSliceStateOff(self):
        """
        Setting the slicestate to False.

        Must resample the whole image afterwards.
        """
        self.slicestate = False
        self.setFrame()
        
        

    def playFuncPressed(self):
        """
        Is called when play button is pressed and initializes the play mode
        or pauses it.
        """
        if self.func_enabled:
            if self.playstate == True:
                self.play_button.setIcon(self.icon_play)
                self.playstate = False
                self.setSliceState(True)
                # This might not be needed anymore.
                for i in range(len(self.images)):
                    if self.images[i].type_d() == "4D":
                        self.images[i].setPlaying(False)
                self.setFrame()
            else:
                self.playstate = True
                # This might not be needed anymore.
                for i in range(len(self.images)):
                    if self.images[i].type_d() == "4D":
                        self.images[i].setPlaying(True)
                self.play_button.setIcon(self.icon_pause)
                self.playingFunc()

    def playFuncReleased(self):
        if self.func_enabled:
            if self.playstate == False:
                self.setSliceStateOff()

    def shortcutPlay(self):
        self.playFuncPressed()
        self.playFuncReleased()

    def playingFunc(self):
        """
        This is repeatedly called in play mode and goes to the next frame.
        """
        if self.playstate == True:
            try:
                if self.frame == self.time_dim-1:
                    self.frame = -1
                self.nextFrame()
            finally:
                self.timer.singleShot(self.playrate, self.playingFunc)

    def setFrameToBox(self):
        """
        Sets the correct current frame to the line edit.
        """
        self.frame_write_block = True
        self.frame_box.setText(str(self.frame))
        self.frame_write_block = False

    def setFrameFromBox(self):
        """
        After manually changing the frame in the line edit the displayed frame
        is updated and the slider moved.
        """
        if self.frame_write_block == False:
            if testInteger(self.frame_box.text()):
                self.frame = int(self.frame_box.text())
                self.setFrame()
                self.setFrameToBox()
                self.setFrameToSlider()

    def setFrame(self):
        """
        Updates all functional image items to display the correct frame.

        This includes resampling the images, updating the ImageItemMods, all
        labels, the histogram and frame line edit and frame slider.
        """
        # Index for histogram update.
        index = self.imagelist.currentRow()
        # Move the frame number within the possible range.
        if self.frame >= self.time_dim:
            self.frame = self.time_dim - 1
        if self.frame < 0:
            self.frame = 0
        for i in range(len(self.images)):
            if self.images[i].type_d() == "4D":
                self.images[i].setFrame(self.frame) # only set the variable
                if self.playstate or self.slicestate:
                    # resample only slices
                    self.images[i].resample_slice(shape=self.img_dims, affine=self.affine)
                    self.updateImageItem(i)
                else:
                    # resample whole frame and slice
                    self.images[i].resample_frame()
                    # if the image is selected update the histogram if open.
                    if i == index and self.hist is not None:
                        if self.hist.isVisible():
                            self.resetHistogram()
                    self.images[i].slice()
                    self.updateImageItem(i)
        self.setFrameToBox()
        self.setFrameToSlider()
        self.updateIntensityLabel()
        self.refreshMosaicView()
        log1("setFrame called (self.frame {})".format(self.frame))
        
    def startSetAlphaTimer(self):
        self.alpha_sld_timer.start(5)

    def setAlphaFromSlider(self):
        """
        Sets the alpha value of the current image
        """

        alpha = self.alpha_sld.value()
        alpha_fract = float(alpha)/100
        self.alpha_label.setText("{}% opacity".format(alpha))
        
        index = self.imagelist.currentRow()
        if index >= 0:
            self.images[index].alpha = alpha_fract
            self.images[index].setColorMapPos()
            self.images[index].setColorMapNeg()
            self.updateSlices()
            self.updateImageItems()
        log2("setAlphaFromSlider called (alpha_fract {})".format(alpha_fract))


    def setAlphaToSlider(self):
        """
        Takes the alpha value of the current image and sets that the slider.
        """
        
        index = self.imagelist.currentRow()
        alpha=100
        if index >= 0:
            alpha_fract = self.images[index].alpha
            alpha = np.round(alpha_fract*100)

        self.alpha_sld.setValue(int(alpha))
        
        log1("setAlphaFromSlider called (alpha {})".format(alpha))
        
        

    def resetAlpha(self):
        """
        Takes the alpha value of the current image and sets that the slider.
        """
        
        alpha_fract = 1.0
        alpha = 100
        for i in range(len(self.images)):
            self.images[i].alpha = alpha_fract

        self.alpha_sld.setValue(alpha)
        
        log1("resetAlpha called")
        
        
    def startSetFrameTimer(self):
        if self.frame_write_block != True:
            self.frame_sld_timer.start(1)   


    def setFrameFromSlider(self):
        """
        Takes the slider frame value and resets the current frame.
        """
        # Use a frame_write_block to prevent cycles.
        if self.frame_write_block == False:
            self.setSliceStateOn()
            self.frame = self.frame_sld.value()
            self.setFrame()
        log1("setFrameFromSlider called (self.frame {})".format(self.frame))

    def setFrameToSlider(self):
        """
        Takes the frame line edit value and reset the current frame.
        """
        # Use a frame_write_block to prevent cycles.
        self.frame_write_block = True
        self.frame_sld.setValue(self.frame)
        self.frame_write_block = False
        log1("setFrameToSlider called (self.frame {})".format(self.frame))

    ## Section: Color Map Thresholds Settings ##
    def setThresholdsFromHistogram(self):
        """
        Resets all thresholds if the line regions in the histogram are moved.
        """
        # It's not necessary to check whether self.hist is None.
        index = self.imagelist.currentRow()
        if index >= 0 and self.threshold_write_block != True:
            thresholds = self.hist.getThresholdsPos()
            self.images[index].setPosThresholds(thresholds)
            if self.images[index].two_cm:
                thresholds = self.hist.getThresholdsNeg()
                self.images[index].setNegThresholds(thresholds)
            self.threshold_write_block = True
            self.setThresholdsToBoxes()
            self.setThresholdsToSliders()
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()

    def startPosSliderTimer(self):
        if self.threshold_write_block != True:
            self.slider_pos_timer.start(1) 

    def setPosThresholdFromSliders(self):
        """
        Resets all thresholds when the sliders are moved.
        """
        index = self.imagelist.currentRow()
        if index >= 0 and self.threshold_write_block != True:
            self.images[index].setPosThresholdsFromSlider(self.slider_pos.lowerValue, self.slider_pos.upperValue)
            self.threshold_write_block = True
            self.setThresholdsToBoxes()
            self.setThresholdsToHistogram()
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()

    def startNegSliderTimer(self):
        self.slider_neg_timer.start(1)  
        
    def setNegThresholdFromSliders(self):
        """
        Resets all thresholds when the sliders are moved.
        """
        index = self.imagelist.currentRow()
        if index >= 0 and self.threshold_write_block != True:
            self.images[index].setNegThresholdsFromSlider(
                self.slider_neg.lowerValue, self.slider_neg.upperValue)
            self.threshold_write_block = True
            self.setThresholdsToBoxes()
            self.setThresholdsToHistogram()
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()

    def setPosThresholdsFromBoxes(self):
        """
        Resets all thresholds when positive thresholds in the line edits are
        edited.
        """
        index = self.imagelist.currentRow()
        if index >= 0 and self.threshold_write_block != True:
            self.threshold_write_block = True
            if (testFloat(self.min_pos.text()) and
                    testFloat(self.max_pos.text())):
                pos_levels = [float(self.min_pos.text()),
                              float(self.max_pos.text())]
                self.images[index].setPosThresholds(pos_levels)
                self.setThresholdsToSliders()
                self.setThresholdsToHistogram()
            else:
                QtGui.QMessageBox.warning(
                    self, "Warning",
                    "Error: text input cannot be interpreted as a number")
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()

    def setNegThresholdsFromBoxes(self):
        """
        Resets all thresholds when negative thresholds in the line edits are
        edited.
        """
        index = self.imagelist.currentRow()
        if index >= 0 and self.threshold_write_block != True:
            self.threshold_write_block = True
            if (testFloat(self.min_neg.text()) and
                    testFloat(self.max_neg.text())):
                neg_levels = [float(self.min_neg.text()),
                              float(self.max_neg.text())]
                self.images[index].setNegThresholds(neg_levels)
                self.setThresholdsToSliders()
                self.setThresholdsToHistogram()
            else:
                QtGui.QMessageBox.warning(
                    self, "Warning",
                    "Error: text input cannot be interpreted as a number")
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()

    def setThresholdsToHistogram(self):
        """
        If thresholds were changed elsewhere, update them in the histogram.
        """  
        index = self.imagelist.currentRow()
        if index >= 0 and self.hist is not None:
            min_level = self.images[index].threshold_pos[0]
            max_level = self.images[index].threshold_pos[1]
            self.hist.setPosRegion(min_level,max_level)
            if self.images[index].two_cm:
                min_level = self.images[index].threshold_neg[0]
                max_level = self.images[index].threshold_neg[1]
                self.hist.setNegRegion(min_level,max_level)

    def setThresholdsToSliders(self):
        """
        If thresholds were changed elsewhere, update them in the sliders.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            lower_value = self.images[index].getPosSldValueLow()
            upper_value = self.images[index].getPosSldValueHigh()
            self.slider_pos.setSpan(lower_value, upper_value)
            if self.images[index].two_cm:
                lower_value = self.images[index].getNegSldValueLow()
                upper_value = self.images[index].getNegSldValueHigh()
                self.slider_neg.setSpan(upper_value, lower_value)

    def setThresholdsToBoxes(self):
        """
        If thresholds were changed elsewhere, update them in the line edits.
        """
        index = self.imagelist.currentRow()
        if index >= 0: 
            self.setPosThresholdsToBoxes()
            self.setNegThresholdsToBoxes()

    def setPosThresholdsToBoxes(self, level=0):
        index = self.imagelist.currentRow()
        if index >= 0:
            min_level = self.images[index].threshold_pos[0]
            max_level = self.images[index].threshold_pos[1]
            self.min_pos.setText(str(np.round(min_level,3)))
            self.max_pos.setText(str(np.round(max_level,3)))

    def setNegThresholdsToBoxes(self, level=0):
        index = self.imagelist.currentRow()
        if index >= 0:
            min_level = self.images[index].threshold_neg[0]
            max_level = self.images[index].threshold_neg[1]
            self.min_neg.setText(str(np.round(min_level,3)))
            self.max_neg.setText(str(np.round(max_level,3)))

    def resetPosThresholds(self):
        """
        Reset current image's positive thresholds to the default values.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.images[index].setPosThresholdsDefault()
            self.threshold_write_block = True
            self.setPosThresholdsToBoxes()
            self.setThresholdsToSliders()
            self.setThresholdsToHistogram()
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()

    def resetNegThresholds(self):
        """
        Reset current image's negative thresholds to the default values.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.images[index].setNegThresholdsDefault()
            self.threshold_write_block = True
            self.setNegThresholdsToBoxes()
            self.setThresholdsToSliders()
            self.setThresholdsToHistogram()
            self.threshold_write_block = False
        # Make changes visible.
        self.updateSlices()
        self.updateImageItems()


    ## Section: Search Extrema ##
    def findMin(self):
        """
        Finds minimum in the current image within a cube of given width.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.img_coord = self.images[index].getMinCoord(
                self.preferences['search_radius'])
            self.setCrosshair()

    def findMax(self):
        """
        Finds maximum in the current image within a cube of given width.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.img_coord = self.images[index].getMaxCoord(
                self.preferences['search_radius'])
            self.setCrosshair()


    ## Section: Open Slice Popouts ##
    def openSliceC(self):
        self.slice_popouts[0].show()

    def openSliceS(self):
        self.slice_popouts[1].show()

    def openSliceT(self):
        self.slice_popouts[2].show()


    ## Section: Slice Focusing ##
    def sliceFocusC(self):
        self.slice_focus = 'c'

    def sliceFocusS(self):
        self.slice_focus = 's'

    def sliceFocusT(self):
        self.slice_focus = 't'


    ## Section: Opening Dialogs and Windows for Image Settings ##
    def openImageSettings(self):
        """
        Open current image's image dialog.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            self.images[index].openDialog()

    def openFuncSettings(self):
        """
        Open current image's functional image dialog.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            if self.images[index].type_d() == "4D":
                self.images[index].openFuncDialog()
            else:
                QtGui.QMessageBox.warning(
                    self, "Warning", "Error: 3D image has no time data!")

    def openTimeSeries(self):
        """
        Opens window to display the time series of the crosshair voxel.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            if self.images[index].type_d() == "4D":
                pos = (self.preferences['ts_posx'], self.preferences['ts_posy'], self.preferences['ts_width'], self.preferences['ts_height'])
                self.images[index].showTimeSeries(pos)
            else:
                QtGui.QMessageBox.warning(self, "Warning",
                    "Error: 3D image has no time data!")

    def openFuncConds(self):
        """
        Open functional conditional trial averages.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            if self.images[index].type_d() == "4D":
                self.images[index].openTrialAverages()
            else:
                QtGui.QMessageBox.warning(
                    self, "Warning", "Error: 3D image has no time data!")


    ## Section: Tools Related ##
    def openQtConsoleWindow(self):
        from qtconsole.jupyter_widget import JupyterWidget
        """
        Opens the ipython qtconsole window.
        """
        if self.console is None:
            self.console = JupyterWidget(viewer=self, images=self.images)
            self.console.kernel.shell.run_cell('%pylab qt')
        self.console.show()

    def openHistogramWindow(self):
        """
        Opens the histogram window.
        """
        #set title
        index = self.imagelist.currentRow()
        filename = ""
        if index >= 0:
            filename = self.images[index].filename
            
        pos = (self.preferences['hist_posx'], self.preferences['hist_posy'], self.preferences['hist_width'], self.preferences['hist_height'])
            
        self.hist = HistogramThresholdWidget(pos=pos, title=filename)
        log2("openHistogramWindow: filename {}".format(filename))
            
        self.resetHistogram()
        self.hist.show()

    def resetHistogram(self):
        """
        Resets the histogram window when changing the current image or the
        frame.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            #set title
            index = self.imagelist.currentRow()
            filename = ""
            if index >= 0:
                filename = self.images[index].filename
            
                if len(self.images[index].image.shape) == 4:
                    filename += " (vol {})".format(self.frame)
                
            if self.hist is None:
                return
            self.hist.reset()
            
            self.hist.setTitle(filename)
            # set Histogram
            [x, y] = self.images[index].getHistogram()
            self.hist.setPlot(x,y)
            # set line regions
            thresholds = self.images[index].threshold_pos
            self.hist.LineRegionPos(thresholds[0], thresholds[1])
            if self.images[index].two_cm:
                thresholds = self.images[index].threshold_neg
                self.hist.LineRegionNeg(thresholds[0], thresholds[1])

    def copyImagePropsFunc(self):
        """
        Copies thresholds and colormaps from the current image to all others.
        """
        index = self.imagelist.currentRow()
        if index >= 0:
            # copy values
            thres_pos = self.images[index].threshold_pos
            thres_neg = self.images[index].threshold_neg
            cm_pos = self.images[index].pos_gradient.name
            cm_neg = self.images[index].neg_gradient.name
            for i in range(len(self.images)):
                self.images[i].setPosThresholds(thres_pos)
                self.images[i].setNegThresholds(thres_neg)
                self.images[i].pos_gradient.loadPreset(cm_pos)
                self.images[i].neg_gradient.loadPreset(cm_neg)

    def showValueWindow(self):
        """
        Open the value_window.
        """
        self.value_window.show()
        # refresh the text
        self.updateIntensityLabel()

    def openMosaic(self):
        """
        Open the mosaic dialog.
        """
		# if the dimensions changed then the values are reset
        if self.cross_button.isChecked():
            self.toggleCrosshairs()
        self.mosaic_dialog.setDims(self.img_dims)
        self.setMosaicLines()
        self.mosaic_dialog.show()
        self.mosaic_active = True

    def mosaicDialogClosed(self):
        """
        Removes the mosaic help lines when closing the mosaic dialog
        and switches crosshair back on.
        """
        self.removeMosaicLines()
        self.mosaic_active = False
        if not self.cross_button.isChecked():
            self.toggleCrosshairs()

    def setMosaicLines(self):
        """
        Sets the mosaic help lines in the main windows SliceWidgets.
        """
        plane = self.mosaic_dialog.plane
        number = self.mosaic_dialog.rows * self.mosaic_dialog.cols
        start = self.mosaic_dialog.start
        end = self.mosaic_dialog.end
        increment = float(end-start)/float(number-1.0)
        if increment == int(increment):
            label_text = "increment: <b>" + str(increment) + "</b>"
            self.mosaic_dialog.increment_label.setText(label_text)
        else:
            self.mosaic_dialog.increment_label.setText(
                "increment: " + str(increment))
        #to avoid ZeroDivisionError in np.arrange
        if increment == 0:
            increment = 0.001
        # +0.5*increment to avoid rounding problems
        coords = np.arange(start, end+0.5*increment, increment)
        coords = np.round(coords,0).astype(int)
        coords = coords.tolist()
        # Because it's too annoying deleting some of them: start from scratch
        self.removeMosaicLines()
        # Initialize lists.
        if plane == 's':
            self.mosaic_lines['c'] = []
            self.mosaic_lines['t'] = []
        if plane == 'c':
            self.mosaic_lines['s'] = []
            self.mosaic_lines['t'] = []
        if plane == 't':
            self.mosaic_lines['c'] = []
            self.mosaic_lines['s'] = []

        for coord in coords:
            # Add to dictionaries and slices.
            if 'c' in self.mosaic_lines:
                if plane in ['t']:
                    line = InfiniteLine(angle=0, movable=False)
                else:
                    line = InfiniteLine(angle=90, movable=False)
                line.setPen(mkPen({'color': "F55", 'width': 1}))
                line.setPos(coord+0.5)
                line.setZValue(1000)
                self.mosaic_lines['c'].append(line)
                self.c_slice_widget.sb.addItem(line)
            if 's' in self.mosaic_lines:
                if plane in ['t']:
                    line = InfiniteLine(angle=0, movable=False)
                else:
                    line = InfiniteLine(angle=90, movable=False)
                line.setPen(mkPen({'color': "F55", 'width': 1}))
                line.setPos(coord+0.5)
                line.setZValue(1000)
                self.mosaic_lines['s'].append(line)
                self.s_slice_widget.sb.addItem(line)
            if 't' in self.mosaic_lines:
                if plane in ['c']:
                    line = InfiniteLine(angle=0, movable=False)
                else:
                    line = InfiniteLine(angle=90, movable=False)
                line.setPen(mkPen({'color': "F55", 'width': 1}))
                line.setPos(coord+0.5)
                line.setZValue(1000)
                self.mosaic_lines['t'].append(line)
                self.t_slice_widget.sb.addItem(line)

    def removeMosaicLines(self):
        """
        Removes the mosaic help lines from SliceWidgets.
        """
        if 'c' in self.mosaic_lines:
            for line in self.mosaic_lines['c']:
                self.c_slice_widget.sb.removeItem(line)
            del self.mosaic_lines['c']
        if 's' in self.mosaic_lines:
            for line in self.mosaic_lines['s']:
                self.s_slice_widget.sb.removeItem(line)
            del self.mosaic_lines['s']
        if 't' in self.mosaic_lines:
            for line in self.mosaic_lines['t']:
                self.t_slice_widget.sb.removeItem(line)
            del self.mosaic_lines['t']
        self.mosaic_lines = {}

    def openMosaicView(self):
        """
        Opens a mosaic view window with the specified values.
        """
        # Get values from the mosaic dialog.
        rows = self.mosaic_dialog.rows
        cols = self.mosaic_dialog.cols
        plane = self.mosaic_dialog.plane
        number = self.mosaic_dialog.rows * self.mosaic_dialog.cols
        start = self.mosaic_dialog.start
        end = self.mosaic_dialog.end
        increment = float(end-start)/float(number-1.0)
        #to avoid ZeroDivisionError in np.arrange
        if increment == 0:
            increment = 0.001
        # +0.5*increment to avoid rounding problems
        coords = np.arange(start, end+0.5*increment, increment)
        coords = np.round(coords,0).astype(int)
        coords = coords.tolist()
        self.mosaic_view = None
        self.mosaic_view = MosaicView(rows, cols)
        for img_ind in range(len(self.images)):
            # check if image is seen in main window
            if self.image_window_list[img_ind][0][0] is not None:
                # iterate over viewboxes
                for coord_ind in range(len(coords)):
                    rgba_slice = self.images[img_ind].mosaicSlice(
                        plane, coords[coord_ind])
                    img = ImageItemMod()
                    img.setImage(rgba_slice)
                    img.setZValue(-img_ind)
                    # Use composition mode?
                    img.setCompositionMode(self.images[img_ind].mode)
                    self.mosaic_view.viewboxes[coord_ind].addItem(img)
        self.mosaic_view.show()

    def refreshMosaicView(self):
        """
        Refreshes mosaic view window with the specified values.
        """
        if not self.mosaic_active:
            return
        # Get values from the mosaic dialog.
        rows = self.mosaic_dialog.rows
        cols = self.mosaic_dialog.cols
        plane = self.mosaic_dialog.plane
        number = self.mosaic_dialog.rows * self.mosaic_dialog.cols
        start = self.mosaic_dialog.start
        end = self.mosaic_dialog.end
        increment = float(end-start)/float(number-1.0)
        #to avoid ZeroDivisionError in np.arrange
        if increment == 0:
            increment = 0.001
        # +0.5*increment to avoid rounding problems
        coords = np.arange(start, end+0.5*increment, increment)
        coords = np.round(coords,0).astype(int)
        coords = coords.tolist()
        for img_ind in range(len(self.images)):
            # check if image is seen in main window
            if self.image_window_list[img_ind][0][0] is not None:
                # iterate over viewboxes
                for coord_ind in range(len(coords)):
                    rgba_slice = self.images[img_ind].mosaicSlice(plane, coords[coord_ind])
                    img = ImageItemMod()
                    img.setImage(rgba_slice)
                    img.setZValue(-img_ind)
                    # Use composition mode?
                    img.setCompositionMode(self.images[img_ind].mode)
                    self.mosaic_view.viewboxes[coord_ind].addItem(img)
        self.mosaic_view.show()

    #%% export    
    def export(self):
        """
        exports the current view and colorbar
        """
        
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Export Images')[0]
        if not filename:
            return
        dp_write = os.path.split(filename)[0]
        fn_base = os.path.split(filename)[1].split(".")[0]
        fp_base = os.path.join(dp_write, fn_base+".png")
        
        self.setCrosshairsVisible(False)
        
        #concatenate all images and save
        list_slices = [self.c_slice_widget.sb, self.s_slice_widget.sb, self.t_slice_widget.sb]
        ydim = 1000
        imgs = []
        for i,l in enumerate(list_slices):
            x = ImageExporter(l)
            x.parameters()['width'] = ydim 
            x.parameters()['height'] = ydim 
            img = x.export(toBytes=True)
            ptr = img.bits()
            ptr.setsize(img.sizeInBytes())
            arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)
            arr_swapped = np.copy(arr)
            arr_swapped[:,:,0] = arr[:,:,2]
            arr_swapped[:,:,2] = arr[:,:,0]
            if i==0:
                imgs = arr_swapped
            else:
                imgs = np.append(imgs, arr_swapped, axis=1)
        
        imsave(fp_base, imgs)
        
        index = self.imagelist.currentRow()
        
        #save positive cmap
        ar = np.outer(np.ones(110),np.arange(0,1,0.001))
        br = mymakeARGB(ar, lut=self.images[index].cmap_pos,levels=[0, 1],useRGBA=True)[0]
        
        from matplotlib import pyplot
        
        fig, ax = pyplot.subplots()
        pyplot.imshow(br)
        pyplot.xticks([0,1000],["%g" %self.images[index].threshold_pos[0], "%g" %self.images[index].threshold_pos[1]])
        pyplot.yticks([])
        fp_figure_pos = os.path.join(dp_write, fn_base+"_cmap_pos.png")
        pyplot.savefig(fp_figure_pos, dpi=100)
        
        #save negative cmap
        if self.images[index].two_cm:
            ar = np.outer(np.ones(110),np.arange(1,0,-0.001))
            br = mymakeARGB(ar, lut=self.images[index].cmap_neg,levels=[0, 1],useRGBA=True)[0]
            fig, ax = pyplot.subplots()
            pyplot.imshow(br)
            pyplot.xticks([0,1000],["%g" %self.images[index].threshold_neg[1],"%g" %self.images[index].threshold_neg[0]])
            pyplot.yticks([])
            fp_figure_pos = os.path.join(dp_write, fn_base+"_cmap_neg.png")
            pyplot.savefig(fp_figure_pos, dpi=100)
        
      
        self.setCrosshairsVisible(True)

    

    ## Section: Settings Management ##
    def changeSearchRadius(self):
        """
        Change the search width.
        """
        self.sr_setting = QtGui.QDialog()
        self.sr_setting.resize(40,40)

        search_le = QtGui.QLineEdit()
        search_le.setText(str(self.preferences['search_radius']))

        def save():
            if testInteger(search_le.text()):
                self.preferences['search_radius'] = int(search_le.text())
            self.savePreferences()
            self.sr_setting.close()

        search_le.returnPressed.connect(save)

        form = QtGui.QFormLayout()
        form.addRow("Search radius in Voxels", search_le)
        self.sr_setting.setLayout(form)

        quit = QtGui.QAction('Quit', self)
        quit.setShortcut(QtGui.QKeySequence.StandardKey.Quit)
        quit.triggered.connect(self.sr_setting.close)
        self.sr_setting.addAction(quit)

        self.sr_setting.show()

    def openSettings(self):
        """
        Loads the settings from the config file and opens the settings window.
        """
        self.loadPreferences()
        self.settings.exec()

   
    def setDefaultPreferences(self):
        self.preferences = {
            # viewing
            'voxel_coord': True,
            'link_mode': 0, # linked == 0, link zoom == 1, unlinked == 2
            'window_width': 1000,
            'window_height': 300,
            'window_posx': 0,
            'window_posy': 0,
            
            'hist_width': 900,
            'hist_height': 600,
            'hist_posx': 150,
            'hist_posy': 150,
            
            'ts_width': 900,
            'ts_height': 600,
            'ts_posx': 150,
            'ts_posy': 150,
            
            

            # colormaps
            'cm_under': 'grey',
            'cm_pos': 'red_vlv',
            'cm_neg': 'blue_vlv',
            'clip_under_high': False,
            'clip_under_low': True,
            'clip_pos_high': False,
            'clip_pos_low': True,
            'clip_neg_high': True,
            'clip_neg_low': False,

            # resampling
            'res_method': 0, # (0 - affine, 1 - image, 2 - fit)
            'interpolation': 1,
            'os_ratio': 1.0,

            # search
            'search_radius': 5
        }
        

    
    def loadPreferences(self):
        settings = QtCore.QSettings()
        list_bools = ['voxel_coord', 'clip_under_high', 'clip_under_low', 'clip_pos_high', 'clip_pos_low', 'clip_neg_high', 'clip_neg_low']
        list_ints = ['link_mode', 'window_width', 'window_height', 'window_posx', 'window_posy', 'hist_width', 'hist_height', 'hist_posx', 'hist_posy', 
                     'ts_width', 'ts_height', 'ts_posx', 'ts_posy','interpolation', 'res_method', 'search_radius']
        list_floats = ['os_ratio']
        list_strings = ['cm_under', 'cm_pos', 'cm_neg']
        
        for xs in settings.allKeys():
            if xs[0:5] != "vini/":
                continue
            val = settings.value(xs) 
            if val is not None:
                key = xs[5:]
                #evil qt saves everything as string sooner or later... de-string it here.
                if key in list_bools:
                    if val == "true":
                        val = True
                    elif val == "false":
                        val = False
                elif key in list_ints:
                    val =  int(val)
                elif key in list_floats:
                    val = float(val)
                elif key in list_strings:
                    pass
                else:
                    continue
                    
                
                self.preferences[key] = val
                log1("loadPreferences: loading key: {} value: {}".format(key, val))
                
                
            
        
        

    def savePreferences(self):
        settings = QtCore.QSettings()
        for key in self.preferences.keys():
            savekey = "vini/{}".format(key)
            settings.setValue(savekey, self.preferences[key])
            log1("savePreferences: writing key: {} value: {}".format(key, self.preferences[key]))
      
 

    def saveWindowSize(self):
        if self.blockSavingWindowSize:
            return
        self.preferences['window_width'] = self.geometry().width()
        self.preferences['window_height'] = self.geometry().height()
        self.preferences['window_posx'] = self.geometry().x()
        self.preferences['window_posy'] = self.geometry().y()
        
        if self.hist is not None:
            self.preferences['hist_width'] = self.hist.geometry().width()
            self.preferences['hist_height'] = self.hist.geometry().height()
            self.preferences['hist_posx'] = self.hist.geometry().x()
            self.preferences['hist_posy'] = self.hist.geometry().y()
            
        for i in range(len(self.images)):
            if hasattr(self.images[i], "timeseries") and self.images[i].timeseries is not None:
                self.preferences['ts_width'] = self.images[i].timeseries.geometry().width()
                self.preferences['ts_height'] = self.images[i].timeseries.geometry().height()
                self.preferences['ts_posx'] = self.images[i].timeseries.geometry().x()
                self.preferences['ts_posy'] = self.images[i].timeseries.geometry().y()
                
            
        
        
        
        
        self.savePreferences()

    ## Section: Closing the Viewer ##
    def closeEvent(self, event):
        """
        Closes all other windows.
        """
        for img in self.images:
            if img.type_d() == "4D":
                if img.timeseries is not None:
                    img.timeseries.hide()
                if img.time_averages is not None:
                    img.time_averages.hide()
                if img.funcdialog is not None:
                    img.funcdialog.hide()
        self.settings.hide()
        self.value_window.hide()
        self.mosaic_dialog.hide()
        self.slice_popouts[0].hide()
        self.slice_popouts[1].hide()
        self.slice_popouts[2].hide()
        for window in self.extra_windows:
            window.hide()
        if hasattr(self, 'os_setting'):
            self.os_setting.hide()
        if hasattr(self, 'sr_setting'):
            self.sr_setting.hide()
        if self.hist is not None:
            self.hist.hide()
        if self.mosaic_view is not None:
            self.mosaic_view.hide()


def main():
    #historic reasons!
    import argparse

    parser = argparse.ArgumentParser(
        prog = "MR viewer",
        description = """ Visualize MR functional images with python """
    )
    parser.add_argument("-i", "-in", "--input", metavar='N', nargs='+',
                        help = "specify input image to display",
                        type=str)
    parser.add_argument("-z", "--zmap", metavar='N', nargs='+',
                        help = "specify an overlay where two adjustable \
                        colorbars would liked to be displayed, e.g. zmap",
                        type=str)
    parser.add_argument("-f", "--func", "--functional", metavar='N', nargs='+',
                        help = "specify a functional image", type=str)
    parser.add_argument('-l', action='store_true', default=False,
                        dest='linked', help='Set linked views to true')

    
    args = parser.parse_args()
    
    
    filenames = args.input
    #override if no "-in " is being used...
    if filenames is None:
        filenames = args.files
        
    z_filenames = args.zmap
    func_filenames = args.func
    is_linked = args.linked

    if filenames is None:
        filenames = []
    if z_filenames is None:
        z_filenames = []
    if func_filenames is None:
        func_filenames = []

    # Initialize QT app GUI and setup the layout.
    app = QtWidgets.QApplication([])
    viewer = Viff()

    # change order of the images being loaded to be more intuitive
    filenames.reverse()
    z_filenames.reverse()
    func_filenames.reverse()

    if is_linked:
        viewer.is_linked = True
        file_list = []
        type_list = []
        if filenames is not None:
            for i in range(0, len(filenames)):
                verboseprint("Loading file: " + filenames[i])
                if os.path.isfile(filenames[i]):
                    file_list.append(filenames[i])
                    type_list.append(0)
                else:
                    print("Error: File doesn't exist")
        if z_filenames is not None:
            for i in range(0, len(z_filenames)):
                verboseprint("Loading file: " + z_filenames[i])
                if os.path.isfile(z_filenames[i]):
                    file_list.append(z_filenames[i])
                    type_list.append(1)
                else:
                    print("Error: File doesn't exist")
        if func_filenames is not None:
            for i in range(0, len(func_filenames)):
                verboseprint("Loading file: " + func_filenames[i])
                if os.path.isfile(func_filenames[i]):
                    file_list.append(func_filenames[i])
                    type_list.append(2)
                else:
                    print("Error: File doesn't exist")
        if file_list is not None:
            viewer.loadImagesFromFiles(file_list, type_list)
        viewer.checkIf2DAndRemovePanes()
        len_files = len(filenames)
        len_funcs = len(func_filenames)
        len_zmaps = len(z_filenames)

        # now open new windows and move the z-maps and functional images there
        for i in range(1, len_zmaps + len_funcs):
            verboseprint("move image to new window")
            viewer.newWindowInd(i) # adds to new window
            viewer.deactivateImageIndex(i) # remove from main window

        for i in range(len_zmaps + len_funcs, len_files + len_zmaps +
                len_funcs):
            for j in range(1, len(z_filenames + func_filenames)):
                verboseprint("move underlay to new window")
                viewer.addToWindowId(i,j-1)

    else:
        file_list = []
        type_list = []
        if filenames is not None:
            for i in range(0, len(filenames)):
                verboseprint("Loading file: " + filenames[i])
                if os.path.isfile(filenames[i]):
                    file_list.append(filenames[i])
                    type_list.append(0)
                else:
                    print("Error: File doesn't exist: {}".format(filenames[i]))
        if z_filenames is not None:
            for i in range(0, len(z_filenames)):
                verboseprint("Loading file: " + z_filenames[i])
                if os.path.isfile(z_filenames[i]):
                    file_list.append(z_filenames[i])
                    type_list.append(1)
                else:
                    print("Error: File doesn't exist: {}".format(filenames[i]))
        if func_filenames is not None:
            for i in range(0, len(func_filenames)):
                verboseprint("Loading file: " + func_filenames[i])
                if os.path.isfile(func_filenames[i]):
                    file_list.append(func_filenames[i])
                    type_list.append(2)
                else:
                    print("Error: File doesn't exist: {}".format(filenames[i]))
        if file_list is not None:
            viewer.loadImagesFromFiles(file_list, type_list)

        

    sys.exit(app.exec())


def show(*argv):
    """ 
    use this function to visualize numpy arrays. can handle multiple arguments, e.g.
    vini.show(a,b,c)
    where a,b,c are numpy arrays.
    Args:
        *argv (numpy.ndarray): One or more NumPy arrays to be visualized.

    Returns:
        None

    Example:
    --------
    import vini
    import numpy as np
    a = np.random.rand(40, 40, 40)
    b = np.random.rand(30, 30, 30)
    vini.show(a, b)
    """
    app = QtWidgets.QApplication([])
    viewer = Viff()
    
    #attempt to get array name...
    try:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]
        itemname = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
        if len(itemname) == 1:
            itemname = [itemname]
        else:
            itemname = itemname.split(",")
    except:
        itemname = ["array {}".format(i) for i in range(len(argv))]
    
    for i,arg in enumerate(argv):
        viewer.loadImagesFromNumpy(arg, itemname[i])
    viewer.checkIf2DAndRemovePanes()
    
    app.exec()
    
    
    
    

if __name__ == '__main__':
    main()

