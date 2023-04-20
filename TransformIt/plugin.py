import math
import os
import pcbnew
import re
import wx
import logging


from .dialog import ConfigDialog, Config


class TransformItPlugin(pcbnew.ActionPlugin):
    ORIGIN = pcbnew.VECTOR2I(0, 0)
    logger = logging.getLogger(__name__)
    log_handler = None

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

    def _setup_logging(self, board_file: str):
        self.logger.propagate = False

        if self.log_handler is not None:
            self.log_handler.close()
            self.logger.removeHandler(self.log_handler)
            self.log_handler = None
            return

        if self.config.debug_log:
            fn = os.path.join(os.path.dirname(board_file), "transformit.log")
            self.log_handler = logging.FileHandler(fn, "w")
            self.log_handler.setLevel(logging.DEBUG)
            self.log_handler.setFormatter(
                logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
            self.logger.addHandler(self.log_handler)
            self.logger.setLevel(logging.DEBUG)
            self.logger.info("Log handlers: %s", self.logger.handlers)

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
        self.logger.debug("Polygon shape has %d outlines", poly.OutlineCount())

        for i in range(poly.OutlineCount()):
            outline: pcbnew.SHAPE_LINE_CHAIN = poly.Outline(i)
            self.logger.debug("Outline has %d vertices", outline.PointCount())

            for pi in range(outline.PointCount()):
                point = outline.CPoint(pi)
                outline.SetPoint(pi, self._transform_point(point, center))

    def _transform_shape(self,
                         shape: pcbnew.PCB_SHAPE,
                         center: pcbnew.VECTOR2I):
        shape_type = shape.GetShape()
        self.logger.debug("Transforminig shape type %s", shape.ShowShape())

        if shape_type == pcbnew.SHAPE_T_POLY:
            self._transform_poly_set(shape.GetPolyShape(), center)

        elif shape_type == pcbnew.SHAPE_T_ARC:
            self.logger.debug("Setting arc geometry")
            shape.SetArcGeometry(
                self._transform_point(shape.GetStart(), center),
                self._transform_point(shape.GetArcMid(), center),
                self._transform_point(shape.GetEnd(), center))

        else:
            self.logger.debug("Segment/bezier shape")
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
        self.logger.debug("Transforminig footprint shape type %d", shape_type)

        if shape_type == pcbnew.SHAPE_T_POLY:
            self._transform_poly_set(shape.GetPolyShape(), self.ORIGIN)

        elif shape_type == pcbnew.SHAPE_T_ARC:
            self.logger.debug("Setting arc geometry")
            shape.SetArcGeometry0(
                self._transform_point(shape.GetStart0(), self.ORIGIN),
                self._transform_point(shape.GetArcMid0(), self.ORIGIN),
                self._transform_point(shape.GetEnd0(), self.ORIGIN))

        else:
            self.logger.debug("Segment/bezier shape")
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
        self.logger.debug("Transforming track")

        track.SetStart(self._transform_point(track.GetStart(), center))
        track.SetEnd(self._transform_point(track.GetEnd(), center))

        if isinstance(track, pcbnew.PCB_ARC):
            self.logger.debug("which is an arc")
            track.SetMid(self._transform_point(track.GetMid(), center))

        track.SetWidth(int(track.GetWidth() * self.config.track_width))

    def _transform_text(self, text: pcbnew.PCB_TEXT, center: pcbnew.VECTOR2I):
        self.logger.debug("Transforming text '%s'", text.GetShownText())

        text.SetPosition(self._transform_point(text.GetPosition(), center))
        text.SetMirrored(bool(text.IsMirrored()) ^
                         (self.config.x_scale < 0) ^
                         (self.config.y_scale < 0))
        text.Rotate(text.GetPosition(), pcbnew.EDA_ANGLE(
            -self.config.rotation, pcbnew.RADIANS_T))

    def _transform_pad(self, pad: pcbnew.PAD):
        self.logger.debug("Transforming pad '%s'", pad.GetPadName())

        pad.SetPos0(self._transform_point(pad.GetPos0(), self.ORIGIN))
        pad.SetDrawCoord()

        pad.Rotate(
            pad.GetPosition(),
            pcbnew.EDA_ANGLE(-self.config.rotation, pcbnew.RADIANS_T))

    def _transform_drawing(self,
                           drawing: pcbnew.BOARD_ITEM,
                           center: pcbnew.VECTOR2I):
        self.logger.debug(
            "Transforming drawing type %s (%s) at %s",
            drawing.Type(), drawing.GetTypeDesc(), drawing.GetPosition())

        if isinstance(drawing, pcbnew.FP_SHAPE):
            self.logger.debug("Drawing is FP_SHAPE")
            self._transform_fp_shape(drawing)

        elif isinstance(drawing, pcbnew.PCB_SHAPE):
            self.logger.debug("Drawing is PCB_SHAPE")
            self._transform_shape(drawing, center)

        elif isinstance(drawing, pcbnew.PCB_TRACK):
            self.logger.debug("Drawing is PCB_TRACK")
            self._transform_track(drawing, center)

        elif isinstance(drawing, pcbnew.PAD):
            self.logger.debug("Drawing is PAD")
            self._transform_pad(drawing)

        elif isinstance(drawing, pcbnew.FOOTPRINT):
            self.logger.debug("Moving footprint '%s'", drawing.GetReference())
            drawing.SetPosition(
                self._transform_point(drawing.GetPosition(), center))
            drawing.Rotate(
                drawing.GetPosition(),
                pcbnew.EDA_ANGLE(-self.config.rotation, pcbnew.RADIANS_T))

        elif (isinstance(drawing, pcbnew.PCB_TEXT) or
              isinstance(drawing, pcbnew.FP_TEXT)):
            self.logger.debug("Drawing is FP/PCB_TEXT")
            self._transform_text(drawing, center)

        elif (isinstance(drawing, pcbnew.ZONE)):
            self.logger.debug("Drawing is ZONE")
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

            board: pcbnew.BOARD = pcbnew.GetBoard()
            self.config = dialog.GetConfig()
            self._setup_logging(board.GetFileName())
            self.logger.debug(
                "Running transform on %d selected items", len(selection))

            fp = None
            old_fp = None

            if (len(selection) == 1 and
                    isinstance(selection[0].Cast(), pcbnew.FOOTPRINT)):
                self.logger.debug("Selected item is a footprint")

                old_fp = selection[0].Cast()
                fp = pcbnew.FOOTPRINT(old_fp)
                selection = list(fp.GraphicalItems())
                selection.extend(fp.Pads())

            bbox = pcbnew.BOX2I()

            for d in selection:
                bbox.Merge(d.GetBoundingBox())

            center: pcbnew.VECTOR2I = bbox.Centre()
            self.logger.debug("Calculated transform center: %s", center)

            for drawing in selection:
                self._transform_drawing(drawing, center)

            if fp:
                self._transform_text(fp.Reference(), fp.GetPosition())
                self._transform_text(fp.Value(), fp.GetPosition())
                self.logger.debug(
                    "Replacing footprint on board with transformed version")
                board.Remove(old_fp)
                board.Add(fp)
                if self.kicad_version > [7, 0, 0]:
                    fp.SetSelected()
                else:
                    self.logger.debug(
                        "Old kicad detected, clearing selection flag")
                    fp.ClearSelected()

            if not self.zones_to_refill.empty():
                self.logger.debug("Refilling zones")
                zf = pcbnew.ZONE_FILLER(pcbnew.GetBoard())
                zf.Fill(self.zones_to_refill)

            self.logger.debug("Done")
        finally:
            dialog.Destroy()
            self.zones_to_refill.clear()
