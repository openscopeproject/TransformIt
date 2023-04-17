import wx

from dataclasses import dataclass
from math import pi

from .dialog_base import ConfigDialogBase


@dataclass
class Config:
    x_scale: float = 1.0
    y_scale: float = 1.0
    rotation: float = 0.0
    shape_width: float = 1.0
    track_width: float = 1.0
    debug_log: bool = False


class ConfigDialog(ConfigDialogBase):
    def __init__(self):
        ConfigDialogBase.__init__(self, None)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnLinkToggle, self.m_linkButton)
        self.Bind(wx.EVT_SPINCTRLDOUBLE,
                  self.OnHorizontalScaleChange, self.m_horizontalScale)
        self.Bind(wx.EVT_CHECKBOX, self.OnHorizontalMirrorChange,
                  self.m_horizontalMirror)

    def GetConfig(self) -> Config:
        return Config(
            # x_scale
            self.m_horizontalScale.Value *
            (-0.01 if self.m_horizontalMirror.Value else 0.01),
            # y_scale
            self.m_verticalScale.Value *
            (-0.01 if self.m_verticalMirror.Value else 0.01),
            # rotation
            self.m_rotation.Value * pi / 180,
            # shape_width
            self.m_shapeWidth.Value * 0.01,
            # track_width
            self.m_trackWidth.Value * 0.01,
            # enable logging
            debug_log=self.m_debugLog.IsChecked()
        )

    def OnLinkToggle(self, event: wx.CommandEvent):
        if event.GetEventObject().GetValue():
            self.m_verticalScale.Enable(False)
            self.m_verticalScale.SetValue(self.m_horizontalScale.Value)
            self.m_verticalMirror.Enable(False)
            self.m_verticalMirror.SetValue(self.m_horizontalMirror.Value)
        else:
            self.m_verticalScale.Enable()
            self.m_verticalMirror.Enable()

    def OnHorizontalScaleChange(self, event: wx.CommandEvent):
        if self.m_linkButton.Value:
            self.m_verticalScale.SetValue(self.m_horizontalScale.Value)

    def OnHorizontalMirrorChange(self, event: wx.CommandEvent):
        if self.m_linkButton.Value:
            self.m_verticalMirror.SetValue(self.m_horizontalMirror.Value)
