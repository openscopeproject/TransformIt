import os
import wx


class LinkToggle(wx.BitmapToggleButton):
    def __init__(self, parent):
        link_image = wx.Image(os.path.join(
            os.path.dirname(__file__), "link.png"))
        super().__init__(parent,
                         label=wx.BitmapBundle(link_image),
                         style=wx.BU_EXACTFIT)
        sz: wx.Size = link_image.GetSize()
        wxport = wx.PlatformInformation().PortIdName
        if wxport == "wxMSW":
            sz.IncBy(10, 8)
        else:
            sz.IncBy(20, 8)
        self.SetMinClientSize(sz)
        self.SetValue(True)
