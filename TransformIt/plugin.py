import math
import os
import pcbnew
import re
import wx


from .dialog import ConfigDialog, Config


class TransformItPlugin(pcbnew.ActionPlugin):
    ORIGIN = pcbnew.VECTOR2I(0, 0)

    def __init__(self):
        super(TransformItPlugin, self).__init__()
        self.name = "Transform It"
        self.category = "Modify PCB"
        self.show_toolbar_button = True
        icon_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(icon_dir, "icon.png")
        self.description = "Scale, mirror, flip, rotate items"

        self.kicad_version = None
        try:
            version = re.search("\\d+\\.\\d+\\.\\d+",
                                pcbnew.Version()).group(0)
            self.kicad_version = list(map(int, version.split('.')))
        except Exception:
            pass

        self.config = Config()

        self.zones_to_refill = pcbnew.ZONES()

    def defaults(self):
        pass

    def _transform_point(self,
                         point: pcbnew.VECTOR2I,
                         center: pcbnew.VECTOR2I) -> pcbnew.VECTOR2I:
        x = point.x - center.x
        y = point.y - center.y

        # scale
        x *= self.config.x_scale
        y *= self.config.y_scale

        # rotate
        angle = self.config.rotation
        x, y = (
            x * math.cos(angle) - y * math.sin(angle),
            x * math.sin(angle) + y * math.cos(angle)
        )

        return pcbnew.VECTOR2I(center.x + int(x), center.y + int(y))

    def _transform_poly_set(self,
                            poly: pcbnew.SHAPE_POLY_SET,
                            center: pcbnew.VECTOR2I):
        for i in range(poly.OutlineCount()):
            outline: pcbnew.SHAPE_LINE_CHAIN = poly.Outline(i)
            for pi in range(outline.PointCount()):
                point = outline.CPoint(pi)
                outline.SetPoint(pi, self._transform_point(point, center))

    def _transform_shape(self,
                         shape: pcbnew.PCB_SHAPE,
                         center: pcbnew.VECTOR2I):
        shape_type = shape.GetShape()

        if shape_type == pcbnew.SHAPE_T_POLY:
            self._transform_poly_set(shape.GetPolyShape(), center)

        elif shape_type == pcbnew.SHAPE_T_ARC:
            shape.SetArcGeometry(
                self._transform_point(shape.GetStart(), center),
                self._transform_point(shape.GetArcMid(), center),
                self._transform_point(shape.GetEnd(), center))

        else:
            shape.SetStart(self._transform_point(shape.GetStart(), center))
            shape.SetEnd(self._transform_point(shape.GetEnd(), center))
            if shape_type == pcbnew.SHAPE_T_BEZIER:
                shape.SetBezierC1(
                    self._transform_point(shape.GetBezierC1(), center))
                shape.SetBezierC2(
                    self._transform_point(shape.GetBezierC2(), center))

        shape.SetWidth(int(shape.GetWidth() * self.config.shape_width))

    def _transform_fp_shape(self, shape: pcbnew.FP_SHAPE):
        shape_type = shape.GetShape()

        if shape_type == pcbnew.SHAPE_T_POLY:
            self._transform_poly_set(shape.GetPolyShape(), self.ORIGIN)

        elif shape_type == pcbnew.SHAPE_T_ARC:
            shape.SetArcGeometry0(
                self._transform_point(shape.GetStart0(), self.ORIGIN),
                self._transform_point(shape.GetArcMid0(), self.ORIGIN),
                self._transform_point(shape.GetEnd0(), self.ORIGIN))

        else:
            shape.SetStart0(
                self._transform_point(shape.GetStart0(), self.ORIGIN))
            shape.SetEnd0(self._transform_point(shape.GetEnd0(), self.ORIGIN))

            if shape_type == pcbnew.SHAPE_T_BEZIER:
                shape.SetBezierC1_0(
                    self._transform_point(shape.GetBezierC1_0(), self.ORIGIN))
                shape.SetBezierC2_0(
                    self._transform_point(shape.GetBezierC2_0(), self.ORIGIN))

        shape.SetWidth(int(shape.GetWidth() * self.config.shape_width))

        shape.SetDrawCoord()

    def _transform_track(
            self, track: pcbnew.PCB_TRACK, center: pcbnew.VECTOR2I):
        track.SetStart(self._transform_point(track.GetStart(), center))
        track.SetEnd(self._transform_point(track.GetEnd(), center))

        if isinstance(track, pcbnew.PCB_ARC):
            track.SetMid(self._transform_point(track.GetMid(), center))

        track.SetWidth(int(track.GetWidth() * self.config.track_width))

    def _transform_text(self, text: pcbnew.PCB_TEXT, center: pcbnew.VECTOR2I):
        text.SetPosition(self._transform_point(text.GetPosition(), center))
        text.SetMirrored(bool(text.IsMirrored()) ^
                         (self.config.x_scale < 0) ^
                         (self.config.y_scale < 0))
        text.Rotate(text.GetPosition(), pcbnew.EDA_ANGLE(
            -self.config.rotation, pcbnew.RADIANS_T))

    def _transform_pad(self, pad: pcbnew.PAD):
        pad.SetPos0(self._transform_point(pad.GetPos0(), self.ORIGIN))
        pad.SetDrawCoord()

        pad.Rotate(
            pad.GetPosition(),
            pcbnew.EDA_ANGLE(-self.config.rotation, pcbnew.RADIANS_T))

    def _transform_drawing(self,
                           drawing: pcbnew.BOARD_ITEM,
                           center: pcbnew.VECTOR2I):
        if isinstance(drawing, pcbnew.FP_SHAPE):
            self._transform_fp_shape(drawing)

        elif isinstance(drawing, pcbnew.PCB_SHAPE):
            self._transform_shape(drawing, center)

        elif isinstance(drawing, pcbnew.PCB_TRACK):
            self._transform_track(drawing, center)

        elif isinstance(drawing, pcbnew.PAD):
            self._transform_pad(drawing)

        elif isinstance(drawing, pcbnew.FOOTPRINT):
            drawing.SetPosition(
                self._transform_point(drawing.GetPosition(), center))
            drawing.Rotate(
                drawing.GetPosition(),
                pcbnew.EDA_ANGLE(-self.config.rotation, pcbnew.RADIANS_T))

        elif (isinstance(drawing, pcbnew.PCB_TEXT) or
              isinstance(drawing, pcbnew.FP_TEXT)):
            self._transform_text(drawing, center)

        elif (isinstance(drawing, pcbnew.ZONE)):
            self._transform_poly_set(drawing.Outline(), center)
            drawing.HatchBorder()

            if drawing.IsFilled():
                drawing.UnFill()
                self.zones_to_refill.push_back(drawing)

    def Run(self):
        selection: pcbnew.DRAWINGS = pcbnew.GetCurrentSelection()

        if len(selection) == 0:
            wx.MessageBox("Select some items first!", "Transform It")
            return

        dialog = ConfigDialog()

        try:
            if dialog.ShowModal() != wx.ID_OK:
                return

            self.config = dialog.GetConfig()

            fp = None
            old_fp = None

            if (len(selection) == 1 and
                    isinstance(selection[0].Cast(), pcbnew.FOOTPRINT)):
                old_fp = selection[0].Cast()
                fp = pcbnew.FOOTPRINT(old_fp)
                selection = list(fp.GraphicalItems())
                selection.extend(fp.Pads())

            bbox = pcbnew.BOX2I()

            for d in selection:
                bbox.Merge(d.GetBoundingBox())

            center = bbox.Centre()

            for drawing in selection:
                self._transform_drawing(drawing, center)

            if fp:
                self._transform_text(fp.Reference(), fp.GetPosition())
                self._transform_text(fp.Value(), fp.GetPosition())
                board: pcbnew.BOARD = pcbnew.GetBoard()
                board.Remove(old_fp)
                board.Add(fp)
                if self.kicad_version > [7, 0, 0]:
                    fp.SetSelected()
                else:
                    fp.ClearSelected()

            if not self.zones_to_refill.empty():
                zf = pcbnew.ZONE_FILLER(pcbnew.GetBoard())
                zf.Fill(self.zones_to_refill)

        finally:
            dialog.Destroy()
            self.zones_to_refill.clear()
