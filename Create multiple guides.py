#!/usr/bin/env python

from gimpfu import *

def create_multiple_guides(image, drawable, direction, start_position, increment, stop_position, add_borders):
    width = image.width
    height = image.height
    
    if direction == 0 or direction == 2:  # Vertical or Both
        end_position = stop_position if stop_position > 0 else width
        for x in range(start_position, end_position, increment):
            if x >= width:
                break
            pdb.gimp_image_add_vguide(image, x)
        if add_borders:
            pdb.gimp_image_add_vguide(image, 0)
            pdb.gimp_image_add_vguide(image, width)
    
    if direction == 1 or direction == 2:  # Horizontal or Both
        end_position = stop_position if stop_position > 0 else height
        for y in range(start_position, end_position, increment):
            if y >= height:
                break
            pdb.gimp_image_add_hguide(image, y)
        if add_borders:
            pdb.gimp_image_add_hguide(image, 0)
            pdb.gimp_image_add_hguide(image, height)
    
    gimp.displays_flush()

def python_fu_create_multiple_guides(image, drawable, direction, start_position, increment, stop_position, add_borders):
    create_multiple_guides(image, drawable, direction, start_position, increment, stop_position, add_borders)

register(
    "python_fu_create_multiple_guides",
    "Create multiple guides",
    "Creates multiple vertical and/or horizontal guides at specified locations with an optional stopping point",
    "Jordan B",
    "2024",
    "<Image>/Image/Guides/Create Multiple Guides...",
    "*",
    [
        (PF_OPTION, "direction", "Direction", 0, ["Vertical", "Horizontal", "Both"]),
        (PF_INT, "start_position", "Starting position", 0),
        (PF_INT, "increment", "Increment", 10),
        (PF_INT, "stop_position", "Stop position (0 for the layer's end)", 0),
        (PF_BOOL, "add_borders", "Add guides at borders", True),
    ],
    [],
    python_fu_create_multiple_guides
)

main()
