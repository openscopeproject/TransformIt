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


class ConfigDialog(ConfigDialogBase):
    def __init__(self):
        ConfigDialogBase.__init__(self, None)

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
            self.m_trackWidth.Value * 0.01
        )
