#!/usr/bin/env python

from gimpfu import *

def create_multiple_layers(image, drawable, num_layers, layer_type, fill_color, layer_increment, layer_increment_by):
    pdb.gimp_image_undo_group_start(image)
    
    for i in range(num_layers):
        # Create layer
        layer_name = "Layer_%d" % (i * layer_increment_by + 1) if layer_increment else "Layer"
        layer = gimp.Layer(image, layer_name, image.width, image.height, RGBA_IMAGE, 100, NORMAL_MODE)
        
        pdb.gimp_image_insert_layer(image, layer, None, 0)
        
        # Fill layer based on type and color
        if layer_type == 0:  # Transparent
            pdb.gimp_drawable_fill(layer, TRANSPARENT_FILL)
        elif layer_type == 1:  # Foreground
            pdb.gimp_drawable_fill(layer, FOREGROUND_FILL)
        elif layer_type == 2:  # Background
            pdb.gimp_drawable_fill(layer, BACKGROUND_FILL)
    
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

register(
    "python_fu_create_multiple_layers",
    "Create multiple layers",
    "Creates multiple layers with optional fill and incremented names",
    "Jordan B",
    "J",
    "2024",
    "<Image>/Layer/Create Multiple Layers...",
    "*",
    [
        (PF_INT, "num_layers", "Number of layers", 1),
        (PF_OPTION, "layer_type", "Layer Type", 0, ["Transparent", "Foreground", "Background"]),
        (PF_COLOR, "fill_color", "Fill Color", (255, 255, 255)),
        (PF_TOGGLE, "layer_increment", "Increment Layer Names", FALSE),
        (PF_INT, "layer_increment_by", "Layer Increment By", 1),
    ],
    [],
    create_multiple_layers
)

main()
