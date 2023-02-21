import os
import wx


class LinkToggle(wx.BitmapToggleButton):
    def __init__(self, parent):
        link_image = wx.Image(os.path.join(
            os.path.dirname(__file__), "link.png"))
        super().__init__(parent,
                         label=wx.BitmapBundle(link_image),
                         style=wx.BU_EXACTFIT)
        self.SetSizeHints(self.Size)
        self.SetValue(True)
