from .pyqtgraph_vini import *

from .Image import Image
from .ColorMapWidget import *
# try:
#     from pyvista import pyvista
# except ImportError:
#     pass


class Image3D(Image):
    """
    Class derived from Image to handle 3D images.
    """

    def __init__(self, **kwargs): # filename=None

        super(Image3D, self).__init__() #filename=None

        self.pos_gradient.item.loadPreset('grey')

        if 'filename' in kwargs:
            self.loadImageFromFile(kwargs['filename'])
        if 'image' in kwargs:
            self.loadImageFromObject(kwargs['image'], kwargs['color'])

    def type(self):
        """
        Returns a string to say whether it has one or two color maps
        """
        if self.two_cm:
            return "two"
        else:
            return "one"

    def type_d(self):
        return "3D"

    def loadImageFromObject(self, img, color=False):

        self.image = img

        self.image_res = np.asanyarray(img.dataobj)

        self.extremum[0] = np.asanyarray(img.dataobj).min()
        self.extremum[1] = np.asanyarray(img.dataobj).max()

        self.two_cm = color
        self.dialog.setPreferences(
            two_cm=self.two_cm, clippings_pos=self.clippings_pos,
            clippings_neg=self.clippings_neg)

        self.setPosThresholdsDefault()
        self.setNegThresholdsDefault()
        self.slice()
