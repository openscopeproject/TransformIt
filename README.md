# Transform It plugin for KiCad

Batch resize, scale, mirror graphics, tracks, zones, footprints and
other items in the PCB editor.

Inspired by free transform tool in graphics editors.

Important notes:
* Mirror does not change layers, it transforms in place
* When a singular footprint is selected it's items are scaled so the footprint itself will
  become larger/smaller
* When more than one item is selected footprints are not changed or rescaled, only repositioned/rotated
* Pads are not rescaled, only repositioned/rotated
* Rotation center is geometrical center of combined bounding box of all selected items

# License

Plugin is distributed under MIT (Expat) license, see `LICENSE` for details.
